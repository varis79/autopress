"""Clasificación determinista por keywords (topic, market, players).

Nada de LLM: reglas puras, auditables y reproducibles.
"""
from __future__ import annotations
from scripts.lib.text import kw_in, count_kw


def classify_item(item: dict, taxonomy: dict) -> dict:
    title = item.get("title", "")
    summary = item.get("summary", "")
    text = f"{title} {summary}"

    # Topic: el de más coincidencias de keyword; empate → orden de declaración.
    best_topic, best_topic_score = None, 0
    for topic, kws in taxonomy["topics"].items():
        s = count_kw(text, kws)
        if s > best_topic_score:
            best_topic, best_topic_score = topic, s

    # Market: coincidencias en título ×2 + en resumen ×1.
    best_market, best_market_score = None, 0
    for market, cfg in taxonomy["markets"].items():
        kws = cfg.get("keywords", [])
        s = 2 * count_kw(title, kws) + count_kw(summary, kws)
        if s > best_market_score:
            best_market, best_market_score = market, s

    players = [name for name, kws in taxonomy.get("players", {}).items()
               if any(kw_in(text, k) for k in kws)]

    out = dict(item)
    out["topic"] = best_topic
    out["market"] = best_market
    out["players"] = players
    return out


def classify(items, taxonomy: dict):
    return [classify_item(it, taxonomy) for it in items]
