# Algo NDS — Signal Archive

One year of an NDS-based trading engine, documented frame by frame.

**202 annotated charts · 175 timestamped posts · 15 fully structured signals · Sep 2025 → Oct 2026.**

This repository is the evidence trail behind a math-first approach to price: instead of drawing trendlines by eye, nodes are computed, a sequence is framed, and the next node becomes the target. The screenshots are the working record — every chart, in the order it was posted, with the original date and time attached.

---

## What's in here

| Path | What it is |
| --- | --- |
| [`REPORT.md`](REPORT.md) | The full report: system, method, coverage, numbers, limitations |
| [`SIGNALS.md`](SIGNALS.md) | The 15 machine-readable signals, exactly as the engine posted them |
| [`INDEX.md`](INDEX.md) | Every screenshot in chronological order |
| [`HIGHLIGHTS.md`](HIGHLIGHTS.md) | A short walk-through of the system end to end |
| `archive/YYYY-MM/<date>_<time>/` | The screenshots themselves, one folder per post, with `meta.json` |
| `data/screenshots.json` | Machine-readable archive index |
| `data/signals.json` | Machine-readable signal log |
| `scripts/build_archive.py` | Rebuilds everything from a Telegram JSON export |

---

## The engine, in one screen

The panel that appears across the archive reads:

| Field | What it means |
| --- | --- |
| **PRICE** | Current price at the moment of the snapshot |
| **PREDICTION** | The projected next-node value — the target the sequence implies |
| **FRACTAL** | Fractal pressure across timeframes, collapsed into one number |
| **ENTRY / TP / SL** | Levels drawn on the chart, with TP set at the next node |
| **HOOK+ / HOOK−** | Directional hooks — where the sequence flips |

Two design choices are visible in the posts and worth calling out, because they are what separates this from discretionary chart markup:

- **TP comes from structure, not from a fixed R.** The target is the next node in the sequence (posted 2025‑12‑21: *"TPs are calculated based on the next node"*).
- **SL comes from volatility, not from a round number.** Stops are sized with a GARCH-based volatility estimate (same post), which is why the R:R varies per signal instead of being pinned to 1:2 or 1:3.

---

## The signals

The engine posted 15 fully structured signals between **2025‑12‑15** and **2025‑12‑22** — symbol, side, entry, TP, SL, R:R and the reason string, all machine-readable in [`SIGNALS.md`](SIGNALS.md).

| Metric | Value |
| --- | --- |
| Signals | 15 |
| Symbols | XRP, DOGE, LTC, SOL, ETH, BTC, INJ, NEAR |
| Long / short | 6 / 9 |
| Average R:R | **3.54** |
| R:R range | 2.67 → 6.86 |

The reason string on each signal names the zone and the retracement depth it fired on (`Zone 0.8‑0.92 | Ret: 90.1%`), which is what makes the set auditable later: you can re-check any of them against the chart without guessing what triggered it.

**What is not claimed:** the export contains no outcome field. There is no win rate, no PnL curve, no "TP hit" flag attached to these 15 entries. The archive shows what the engine produced and when — not that it was profitable. Anyone quoting a win rate from this repo would be inventing it.

---

## Why the archive is timestamped

Selection bias is the quiet killer of every trading track record: you keep the winners, delete the losers, and the screenshots stop meaning anything.

Every folder here carries the original post time, and the archive is complete for the period it covers — the charts that went nowhere are in it too. That is the only reason the numbers above can be trusted as *counts* rather than as *results*.

---

## Rebuilding / extending

```bash
python3 scripts/build_archive.py "/path/to/DataExport_YYYY-MM-DD"
```

The script reads Telegram's `result.json`, groups photos posted in the same minute (a before/after pair is usually one post, two images), and regenerates `archive/`, `data/`, `INDEX.md`, `SIGNALS.md`. Nothing is inferred: pair, timeframe and outcome are left `null` unless the export actually contains them.

---

## Disclaimer

Educational material, not financial advice, not a signal service. All annotations were made on TradingView in real time or shortly after; hindsight is unavoidable in any retrospective chart. Nothing here is a recommendation to buy or sell any asset. Trade your own risk.

© AliReza V. Charts: TradingView.
