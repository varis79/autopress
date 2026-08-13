"""Selección editorial determinista: blacklist → scoring → cuotas → modo.

(Antes se llamaba select.py; renombrado para no sombrear el módulo `select`
del stdlib.)
"""
from __future__ import annotations
import datetime as dt
from scripts.lib.text import kw_in


def _days_since(as_of: str, published: str) -> int:
    # Fecha ausente/ inválida → se trata como MUY antigua (recencia ~0), no como "de hoy".
    try:
        d1 = dt.date.fromisoformat(as_of)
        d2 = dt.date.fromisoformat((published or "")[:10])
    except Exception:
        return 3650
    return max(0, (d1 - d2).days)


def _neg_ordinal(published: str) -> int:
    try:
        return -dt.date.fromisoformat((published or "")[:10]).toordinal()
    except Exception:
        return 0


def _tier(market, taxonomy: dict) -> str:
    if not market:
        return "other"
    return taxonomy["markets"].get(market, {}).get("tier", "other")


def _blacklisted(item: dict, terms) -> bool:
    text = f"{item.get('title', '')} {item.get('summary', '')}"
    return any(kw_in(text, t) for t in terms)


def score_item(item: dict, scoring: dict, taxonomy: dict, as_of: str) -> float:
    score = 0.0
    topic = item.get("topic")
    if topic:
        score += scoring["topic_match"]
        if topic in taxonomy.get("priority_topics", []):
            score += scoring["topic_priority_boost"]

    tier = _tier(item.get("market"), taxonomy)
    score += scoring.get("market_" + tier, scoring.get("market_other", 0.0))

    players = item.get("players", [])
    if players:
        extra = min(len(players) - 1, scoring["players_max_extra"])
        score += scoring["players_base"] + scoring["players_extra"] * max(0, extra)

    days = _days_since(as_of, item.get("published"))
    recency = scoring["recency_max_bonus"] - scoring["recency_decay_per_day"] * days
    score += max(0.0, recency)

    return round(score, 4)


def select(items, config: dict) -> dict:
    taxonomy = config["taxonomy"]
    sel = config["selection"]
    as_of = config["as_of"]
    modes = config["modes"]

    # 1. Filtro de competidores (antes del scoring).
    pool = [it for it in items if not _blacklisted(it, sel.get("competitor_blacklist", []))]

    # 2. Scoring.
    scored = [(score_item(it, sel["scoring"], taxonomy, as_of), it) for it in pool]

    # 3. Orden: score desc, luego más reciente, luego id (estable/reproducible).
    scored.sort(key=lambda x: (-x[0], _neg_ordinal(x[1].get("published")), x[1].get("id", "")))

    # 4. Cuotas geográficas y por topic; corta al alcanzar el objetivo.
    geo = sel.get("geo_quotas", {})
    topic_q = sel.get("topic_quotas", {})
    tier_count, topic_count = {}, {}
    target = modes["target_normal"]
    chosen = []
    for s, it in scored:
        if len(chosen) >= target:
            break
        tier = _tier(it.get("market"), taxonomy)
        if tier_count.get(tier, 0) >= geo.get(tier, [0, 999])[1]:
            continue
        tp = it.get("topic")
        if tp in topic_q and topic_count.get(tp, 0) >= topic_q[tp]:
            continue
        chosen.append({
            "id": it.get("id"),
            "topic": it.get("topic"),
            "market": it.get("market"),
            "players": it.get("players", []),
            "score": s,
        })
        tier_count[tier] = tier_count.get(tier, 0) + 1
        if tp:
            topic_count[tp] = topic_count.get(tp, 0) + 1

    n = len(chosen)
    mode = "normal" if n >= modes["min_normal"] else "short" if n >= modes["min_short"] else "pause"
    return {"mode": mode, "count": n, "stories": chosen}
