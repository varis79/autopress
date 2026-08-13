"""ingest — lee fuentes RSS/Atom reales y produce ítems crudos normalizados.

Determinista salvo el 'as_of' (fecha de referencia, que se pasa; no se usa
Date.now para no romper reproducibilidad). Requiere `feedparser`.

Cada ítem: {id, title, summary, url, published (YYYY-MM-DD), source_name,
topic_hint, geo_hint}. El `id` es estable (hash de la URL canónica) para que
la deduplicación y la procedencia sean reproducibles.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import ipaddress
import re
import socket
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit

from scripts.lib.text import canonical_url, safe_url

try:
    import feedparser  # type: ignore
except ImportError:  # pragma: no cover
    feedparser = None

# User-Agent genérico e INDEPENDIENTE (no referencia a nadie). El pipeline le pasa el
# dominio del PROPIO operador si lo tiene, para identificarse educadamente con su web.
_UA = "AutopressBot/0.1 (news-curation media outlet)"


def _ip_ok(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_unspecified or ip.is_multicast)


def _is_public_host(host: str) -> bool:
    """Resuelve el host (DNS) y valida TODAS sus IPs: nada de loopback/privado/link-local.
    Resolver normaliza formas raras (IP decimal/octal, nombres que apuntan a interno)."""
    if not host:
        return False
    h = host.lower().strip("[]")
    if h in ("localhost", "0.0.0.0") or h.endswith(".local") or h.endswith(".internal"):
        return False
    try:
        ips = {info[4][0] for info in socket.getaddrinfo(h, None)}
    except Exception:
        return False
    return bool(ips) and all(_ip_ok(ip) for ip in ips)


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    """Revalida el destino de CADA redirección (anti-SSRF por rebote público→privado)."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        p = urlsplit(newurl)
        if p.scheme not in ("http", "https") or not _is_public_host(p.hostname):
            raise urllib.error.HTTPError(newurl, code, "redirección a destino no permitido",
                                         headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_SafeRedirect())


def _fetch(url: str, timeout: int = 15, retries: int = 2,
           max_bytes: int = 5_000_000, user_agent: str = None) -> bytes:
    """Descarga controlada: timeout, User-Agent identificable, límite de tamaño y
    reintentos con backoff. Lanza excepción si agota los intentos (el llamador la
    registra por fuente; una fuente caída no debe pasar por 'vacía')."""
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": user_agent or _UA,
                "Accept": "application/rss+xml, application/atom+xml, application/xml, "
                          "text/xml, */*",
            })
            with _OPENER.open(req, timeout=timeout) as r:  # opener con revalidación de redirecciones
                data = r.read(max_bytes + 1)
            if len(data) > max_bytes:
                raise ValueError(f"feed excede el límite de {max_bytes} bytes")
            return data
        except Exception as e:  # noqa: BLE001 - se propaga tras agotar reintentos
            last = e
            if attempt < retries:
                time.sleep(0.5 * (attempt + 1))
    raise last if last else RuntimeError("fallo de descarga desconocido")


def _read_source(url: str, allow_local: bool = False, user_agent: str = None, **kw) -> bytes:
    """http/https público → descarga robusta. Ruta local SOLO con allow_local (fixtures/
    tests), NUNCA desde `sources` en producción (anti-SSRF: leer /etc/hosts, metadata…)."""
    p = urlsplit(url)
    if p.scheme in ("http", "https"):
        if not _is_public_host(p.hostname):
            raise ValueError(f"host no permitido (privado/loopback/no resuelve): {p.hostname}")
        return _fetch(url, user_agent=user_agent, **kw)
    if allow_local and p.scheme in ("", "file"):
        path = p.path if p.scheme == "file" else url
        with open(path, "rb") as f:
            return f.read()
    raise ValueError(f"esquema de fuente no permitido: {p.scheme or 'local'}")


def _item_id(url: str, title: str) -> str:
    key = canonical_url(url) or (title or "")
    return "s" + hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]


def _strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", s).strip()


def _entry_date(entry) -> str:
    for key in ("published_parsed", "updated_parsed"):
        t = entry.get(key)
        if t:
            return dt.date(t.tm_year, t.tm_mon, t.tm_mday).isoformat()
    return ""


def parse_feed(content, source_name: str = "", topic_hint=None, geo_hint=None,
               max_summary: int = 320) -> list:
    """Parsea el contenido (o URL) de un feed → lista de ítems normalizados."""
    if feedparser is None:
        raise RuntimeError("Falta la dependencia 'feedparser' (pip install feedparser).")
    d = feedparser.parse(content)
    feed_title = (d.feed.get("title", "") if getattr(d, "feed", None) else "")
    items = []
    for e in d.entries:
        url = safe_url(e.get("link", ""))   # descarta javascript:/data:/file: en origen
        summary = _strip_html(e.get("summary", e.get("description", "")))
        if len(summary) > max_summary:
            summary = summary[:max_summary].rsplit(" ", 1)[0] + "…"
        items.append({
            "id": _item_id(url, e.get("title", "")),
            "title": _strip_html(e.get("title", "")),
            "summary": summary,
            "url": url,
            "published": _entry_date(e),
            "source_name": source_name or feed_title,
            "topic_hint": topic_hint,
            "geo_hint": geo_hint,
        })
    return items


def _within_window(published: str, as_of: str, lookback_days: int) -> bool:
    if not published:
        return True  # sin fecha: no descartamos por ventana
    try:
        p = dt.date.fromisoformat(published[:10])
        ref = dt.date.fromisoformat(as_of[:10])
    except Exception:
        return True
    return 0 <= (ref - p).days <= lookback_days


def ingest(sources: list, as_of: str, lookback_days: int = 8,
           max_per_source: int = 20, diagnostics=None, allow_local: bool = False,
           user_agent: str = None) -> list:
    """Lee todas las fuentes, filtra por ventana temporal, cap por fuente y
    deduplica por id. `sources`: [{name, url, topic_hint?, geo_hint?}].

    Si se pasa `diagnostics` (lista), se añade una entrada por fuente con su estado
    (`ok`/`empty`/`error`) y su recuento — así una fuente caída se distingue de una
    vacía y el pipeline puede decidir con esa información.
    """
    all_items, seen = [], set()
    for src in sources:
        name, url = src.get("name", ""), src.get("url", "")
        entry = {"name": name, "url": url, "status": "ok", "count": 0}
        try:
            content = _read_source(url, allow_local=allow_local, user_agent=user_agent)
            parsed = parse_feed(content, source_name=name,
                                topic_hint=src.get("topic_hint"),
                                geo_hint=src.get("geo_hint"))
        except Exception as e:  # noqa: BLE001 - registrado, no silenciado
            entry.update(status="error", error=str(e)[:200])
            if diagnostics is not None:
                diagnostics.append(entry)
            continue  # una fuente caída no rompe el pipeline, pero SÍ se registra
        kept = 0
        for it in parsed:
            if kept >= max_per_source:
                break
            if not _within_window(it["published"], as_of, lookback_days):
                continue
            if it["id"] in seen:
                continue
            seen.add(it["id"])
            all_items.append(it)
            kept += 1
        entry["count"] = kept
        if kept == 0:
            entry["status"] = "empty"
        if diagnostics is not None:
            diagnostics.append(entry)
    return all_items
