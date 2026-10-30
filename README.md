<div align="center">

![Algo NDS — precision entries from nodal structure](docs/hero.png)

**A node-based engine for reading price — 202 charts, 15 structured signals, and the full reasoning behind every one of them.**

![charts](https://img.shields.io/badge/charts-202-22d3ee?style=flat-square)
![signals](https://img.shields.io/badge/structured_signals-15-22d3ee?style=flat-square)
![rr](https://img.shields.io/badge/avg_design_R:R-3.54-f5c518?style=flat-square)
![period](https://img.shields.io/badge/record-2025--09_→_2026--10-8a96a8?style=flat-square)

[**The report**](REPORT.md) · [**The signals**](SIGNALS.md) · [**The archive**](INDEX.md) · [**Highlights**](HIGHLIGHTS.md)

</div>

---

## The idea in thirty seconds

Most chart reading starts with a shape — a triangle, a flag, a head and shoulders — and then argues about it.

This starts with **numbers**. Swing points are located by computing derivatives of price and taking the second derivative for precision, not by eyeballing peaks. Those points become **nodes**. The nodes form a **sequence**. And once the sequence is framed, the next node is no longer a guess: it is a computation, and it becomes the target.

That single shift is the whole method:

> **The target is not where you hope price goes. It is where the structure says the next node sits.**

Everything in this repository is that claim, applied — 202 charts across crypto, indices, gold and FX, with the engine's read printed on the chart at the moment it was made.

---

## How a signal is built

```
1. NODES      find swing points via derivatives (second derivative for precision)
2. SEQUENCE   frame the nodes into a leg structure — which displacement is in play
3. SYMMETRY   project the geometry forward: where the next leg should land
4. TARGET     the next node = TP. Structure decides the exit, not a fixed multiple
5. STOP       GARCH volatility estimate = SL. Volatility decides the room, not preference
6. TRIGGER    fire only inside the retracement zone, with the depth recorded
```

Steps 4 and 5 are what make the output usable. Because the target comes from structure and the stop comes from measured volatility, **R:R is an output of the setup rather than an input you force**. The engine never says "go for 1:2". It reads what the market offers and reports the ratio it actually got.

---

## Why 3.54R changes the game

The 15 documented signals average **3.54R of designed reward per 1R of risk**. That number is not a result — it is the geometry the engine produced. But it has a consequence that most trading systems cannot claim:

**Breakeven is 22%.**

| Hit rate | Expectancy per trade | 100 trades |
| --- | --- | --- |
| 20% | −0.29R | −29R |
| **22%** | **0.00R** | **0R — breakeven** |
| 25% | +0.14R | +14R |
| 30% | +0.36R | +36R |
| 35% | +0.59R | +59R |
| 40% | +0.82R | +82R |
| 45% | +1.04R | +104R |

*Expectancy = p × 3.54 − (1 − p) × 1, computed from the average R:R in [`data/signals.json`](data/signals.json).*

A method that needs to be right **4 times out of 5** is a method that will break the first time the market changes character. A method that breaks even at **2 out of 9** has room to be wrong — which, over a few hundred trades, is the only thing that matters.

That is the actual claim of this work: not that it wins every time, but that **the structure of the payoff survives being wrong most of the time.**

---

## The evidence

<div align="center">

<img src="docs/rr.svg" width="88%" alt="Designed R:R per signal">

<img src="docs/timeline.svg" width="88%" alt="Posts per month">

</div>

| What the record shows | |
| --- | --- |
| Annotated charts archived | **202** |
| Timestamped posts | **175** (Sep 2025 → Oct 2026) |
| Machine-readable signals | **15** (13–22 Dec 2025) |
| Symbols | XRP · DOGE · LTC · SOL · ETH · BTC · INJ · NEAR |
| Direction split | 6 long / 9 short |
| Average designed R:R | **3.54** (range 2.67 – 6.86) |
| Markets covered over the year | crypto, indices (US30/Dow), gold, FX, equities |

Every one of the 15 signals carries the reason it fired, in the same format:

```
🎯 NDS SIGNAL
💎 XRP/USDT
🔴 Side: SELL
🚪 Entry: 1.9183     🎯 TP: 1.9056
🛑 SL: 1.9229        ⚖️ R:R: 2.77
🧠 Reason: Zone 0.8-0.92 | Ret: 90.1%
```

Read the full table in [`SIGNALS.md`](SIGNALS.md).

---

## The archive is timestamped on purpose

Anyone can post their winners. The reason this record is worth reading is that it is **complete for the period it covers** — every chart the engine produced, in the order it produced them, including the ones that went nowhere.

Each folder carries the original post time:

```
archive/2025-12/2025-12-21_1454/
├── 01.jpg      ← the chart as posted, 21 Dec 2025 at 14:54
└── meta.json   ← timestamp, message id, verbatim caption
```

That is what makes the 15 signals auditable: pick one from [`SIGNALS.md`](SIGNALS.md), take its timestamp, open the matching folder, and check the chart the engine was looking at when it fired. No "trust me" required — the receipts are in the repository.

---

## Inside the repository

| Path | What it is |
| --- | --- |
| [`REPORT.md`](REPORT.md) | Full report: method, timeline, coverage, numbers, limitations |
| [`SIGNALS.md`](SIGNALS.md) | All 15 signals, exactly as posted |
| [`INDEX.md`](INDEX.md) | Every screenshot, chronologically, with links |
| [`HIGHLIGHTS.md`](HIGHLIGHTS.md) | A short walk-through of the system |
| `archive/` | 175 timestamped folders, 202 charts, with `meta.json` each |
| `data/` | `signals.json` · `screenshots.json` — machine readable |
| `scripts/` | `build_archive.py` (ingest an export) · `make_visuals.py` (rebuild these graphics) |
| `docs/` | The graphics in this README |

---

## What this repository does **not** claim

Being explicit here is what separates a track record from marketing:

- **No win rate.** The source export contains no outcome field. Not one of the 15 signals has a recorded exit. The 3.54R is *designed* reward-to-risk, not realised profit.
- **No PnL, no equity curve, no "verified" badge** — because nobody has verified it, including me.
- **Hindsight is present.** Charts were annotated live, but they are still selected posts from a public channel.
- **Coverage has gaps.** Four months of the period have no posts at all.

What is claimed is narrower and stronger: **the method is documented, the numbers are traceable, and the reasoning is reproducible.** If a result set is ever attached to it, the structure to check it is already here.

---

## What would turn this into a verified track record

1. **An outcome ledger** — `signal_id, posted_at, entry, tp, sl, closed_at, exit, outcome, R` for every trade, including the losers.
2. **Forward test** — run the engine on unseen data for a fixed period, publish everything, edit nothing.
3. **Broker statement** — for any live period, the only artifact that cannot be curated.

The archive is the raw material for (1): timestamps and trigger reasons are already recorded.

---

## Reproduce it

```bash
python3 scripts/build_archive.py "/path/to/DataExport_YYYY-MM-DD"   # rebuild archive + data
python3 scripts/make_visuals.py                                     # rebuild docs/ graphics
```

Both scripts are pure Python + Pillow, no external services.

---

<div align="center">

**Educational research. Not financial advice. Not a signal service.**

*Charts: TradingView · Annotations and engine: AliReza V.*

</div>
