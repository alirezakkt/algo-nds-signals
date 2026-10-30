#!/usr/bin/env python3
"""Group the archive into sessions — the frames that belong to one day's work.

Why days, not pixels: the charts were re-zoomed, restyled and re-tooled across
the year, so two frames of the same setup do not reliably look alike (measured:
perceptual-hash distance for known same-chart pairs ranges from 8 to 42, which
overlaps completely with pairs that are different markets). What *is* reliable
is the sequence of posts itself: on any given day the trader posted a chart,
then an update, then the outcome.

So a session = the posts of one day, split when two captions name different
tickers (a BTC chart and a Dow chart posted a minute apart are two sessions,
not one). Within a session the frames keep their exact timestamps, which is
what makes a before/after reading possible.

Writes data/threads.json:
  {"threads": [{id, date, posts, frames, start, end, span_minutes, symbols}],
   "by_folder": {folder: session_id}}
"""

import json
import re
from collections import defaultdict
from datetime import datetime

TICKERS = [
    "BTC", "ETH", "XRP", "SOL", "DOGE", "LTC", "INJ", "NEAR", "ADA", "BNB", "AVAX",
    "XAUUSD", "XAU", "XAG", "GOLD", "EURUSD", "GBPUSD", "USDJPY", "DXY",
    "US30", "DOW", "NAS100", "US500", "SPX", "DE40", "TSLA", "NVDA", "AAPL",
]


def ticker(caption):
    text = (caption or "").upper()
    for symbol in TICKERS:
        if re.search(rf"\b{re.escape(symbol)}\b", text):
            return "XAU" if symbol == "XAUUSD" else symbol
    return None


def main():
    shots = json.load(open("data/screenshots.json", encoding="utf-8"))

    by_day = defaultdict(list)
    for shot in shots:
        by_day[shot["date"][:10]].append(shot)

    sessions = []
    by_folder = {}
    for day in sorted(by_day):
        posts = sorted(by_day[day], key=lambda p: p["date"])

        # split the day when captions name different tickers
        clusters, current = [], []
        seen = set()
        for post in posts:
            symbol = ticker(post["caption"])
            if symbol and seen and symbol not in seen:
                clusters.append(current)
                current, seen = [], set()
            if symbol:
                seen.add(symbol)
            current.append(post)
        if current:
            clusters.append(current)

        for cluster in clusters:
            start = datetime.fromisoformat(cluster[0]["date"])
            end = datetime.fromisoformat(cluster[-1]["date"])
            sessions.append({
                "id": len(sessions) + 1,
                "date": day,
                "posts": [p["folder"] for p in cluster],
                "frames": sum(len(p["images"]) for p in cluster),
                "start": cluster[0]["date"],
                "end": cluster[-1]["date"],
                "span_minutes": round((end - start).total_seconds() / 60),
                "symbols": sorted({ticker(p["caption"]) for p in cluster if ticker(p["caption"])}),
            })
            for post in cluster:
                by_folder[post["folder"]] = sessions[-1]["id"]

    json.dump({"threads": sessions, "by_folder": by_folder},
              open("data/threads.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    sizes = [s["frames"] for s in sessions]
    multi = [s for s in sessions if s["frames"] > 1]
    print(f"days: {len(by_day)} | sessions: {len(sessions)} | sessions with >1 frame: {len(multi)}")
    print("frames per session:", {n: sizes.count(n) for n in sorted(set(sizes))})
    for s in sorted(multi, key=lambda s: -s["frames"])[:8]:
        print(f'  #{s["id"]:>3} {s["date"]} · {s["frames"]} frames · '
              f'{s["start"][11:16]} → {s["end"][11:16]} ({s["span_minutes"]}m)')


if __name__ == "__main__":
    main()
