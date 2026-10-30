# Report — Algo NDS, one year of a node-based trading engine

**Scope:** 854 messages from the public group *Nodal Math Trading*, posted 2025‑09‑25 → 2026‑10‑29.
**Extracted:** 202 photos → 175 timestamped posts (some posts carry a before/after pair) · 15 machine-readable signals.
**Purpose:** document what the engine is, what it produced, and what can and cannot be concluded from the record.

---

## 1. Executive summary

The archive documents a single trader building and then operating an NDS‑based engine over roughly thirteen months. Three phases are clearly separated in the posts:

1. **Construction (Sep–Nov 2025)** — fractal pressure, symmetry code, sequence framing, a first version of the pattern.
2. **Automation (Nov–Dec 2025)** — the engine starts emitting structured signals with entry, TP, SL, R:R and a reason string.
3. **Operation (Dec 2025 – Oct 2026)** — live chart posts across crypto, indices, gold and FX, with the engine's panel overlaid.

The numbers that can be stated without interpretation:

- **15** fully structured signals exist in the export, all between **2025‑12‑15** and **2025‑12‑22**.
- Their average design **R:R is 3.54** (range 2.67 – 6.86), across **8 symbols**.
- The stop is volatility‑based (GARCH) and the target is the next structural node — so R:R is an output of the setup, not a fixed input.
- The outcome of none of those 15 signals is recorded in the export. **No win rate and no PnL is claimed anywhere in this repository.**

---

## 2. Data and method

| Item | Detail |
| --- | --- |
| Source | Telegram Desktop JSON export of the group, `result.json` |
| Messages | 854 (202 photos, 2 videos, 1 voice note, 42 service messages) |
| Period | 2025‑09‑25 → 2026‑10‑29 |
| Extraction | Photos grouped per post (same‑minute photos = one post); captions kept verbatim |
| Signals | Parsed from the `NDS SIGNAL` text block the engine posts |
| Excluded | Video, voice, and discussion that isn't a chart or a signal |

Nothing was inferred. `data/screenshots.json` carries the timestamp, the verbatim caption and the file paths; where the export had no value (pair, timeframe, outcome) the field is `null` rather than filled in.

---

## 3. The system

### 3.1 What NDS is

Nodal Displacement Sequence: price is read as a sequence of displacements between **nodes** (swing points), not as a pattern of candles. The method's claim is that once the sequence is framed correctly, the *next* node is computable — and therefore so is a target.

The author's own framing, from a post on 2026‑01‑01, is explicit about where the difficulty lies: most people find nodes with generic peak/trough libraries, while the approach used here is to compute derivatives — and specifically the **second derivative** — then frame a **node sequence**, then compute symmetry and geometry on it.

### 3.2 The engine's components

| Component | Appears as | Role |
| --- | --- | --- |
| Node detection | the sequence lines on the chart | Finds swing structure via derivatives |
| Sequence framing | numbered legs / channels | Establishes which displacement is in play |
| Prediction | `PREDICTION` in the panel | Next‑node projection = the target |
| Fractal pressure | `FRACTAL` in the panel | Cross‑timeframe pressure, one number |
| Hooks | `HOOK+` / `HOOK−` markers | Sequence flip / invalidation points |
| Symmetry & geometry | symmetry rectangles, expansion factor | Where the next leg should land |
| Entry / TP / SL | labelled levels on the chart | Execution levels |
| Reason string | `Zone 0.8‑0.92 | Ret: 90.1%` | The retracement zone and depth that triggered the signal |

### 3.3 Two design decisions that matter

**Target = next node.** Stated on 2025‑12‑21: the TPs are calculated from the next node in the sequence. That is why targets sit at structurally meaningful prices instead of at a multiple of risk.

**Stop = volatility, not preference.** Same post: stops are computed from a GARCH‑based volatility estimate. A quiet market therefore gets a tighter stop and a wider R:R, and the same setup in a violent market gets a wider stop — which is why the 15 signals range from 2.67 to 6.86 R without the trader touching anything.

This combination is the actual claim of the method: *structure decides where you exit with profit, volatility decides how much room the trade needs.* It is falsifiable, which is more than most chart‑reading frameworks can say.

---

## 4. Timeline

| Date | Milestone |
| --- | --- |
| 2025‑09‑28 | First post: fractal pressure across all timeframes, collapsed into one histogram |
| 2025‑10‑07 | `alpha version — symmetry code` |
| 2025‑10‑08 | First live charts with the overlay (`EURUSD/4H`, flagged `HighRisk`) |
| 2025‑11‑29 | First version of the pattern — described as several years of work, being tuned on crypto |
| 2025‑11‑30 | `نمونه سیگنال های بات` — first bot signal output shown |
| 2025‑12‑15 | First structured `NDS SIGNAL` block (symbol, side, entry, TP, SL, R:R, reason) |
| 2025‑12‑21 | Method statement: TP from the next node, SL from GARCH volatility |
| 2026‑02‑20 | `NMT Algo Visual` — visual layer of the engine |
| 2026‑02‑28 | `NDS TITAN V36` — richer format: TP1 (S2) / TP2 (90%α), Pmid, lot & risk, wave length, NSI, ATR+kσ stop floor |
| 2026‑06‑29 → 07‑05 | Live‑market sharing of the algorithm and its trades, framed explicitly as research, not signal selling |
| 2026‑10‑29 | Last post in the export |

---

## 5. Coverage

### 5.1 Posts over time

| Month | Posts |
| --- | --- |
| 2025‑09 | 1 |
| 2025‑10 | 51 |
| 2025‑11 | 21 |
| 2025‑12 | 13 |
| 2026‑01 | 3 |
| 2026‑02 | 29 |
| 2026‑03 → 05 | 0 |
| 2026‑06 | 20 |
| 2026‑07 | 10 |
| 2026‑08 | 0 |
| 2026‑09 | 8 |
| 2026‑10 | 19 |

The gaps are real and are left in: this is one person's working record, not a marketing feed. Any serious reading of the archive has to account for the fact that activity stops for months at a time.

### 5.2 Markets covered

Crypto majors and alts (BTC, ETH, SOL, XRP, DOGE, LTC, INJ, NEAR), indices (US30 / Dow), metals (XAU, silver), FX (EURUSD, GBPUSD), and equities (TSLA). The mix shifts over time: crypto‑heavy in the automation phase, indices and gold during the 2026 live sessions.

---

## 6. The signal set (2025‑12‑15 → 2025‑12‑22)

| Metric | Value |
| --- | --- |
| Signals | 15 |
| Symbols | XRP (3), DOGE (3), LTC (2), SOL (2), ETH (2), BTC, INJ, NEAR |
| Direction | 9 short / 6 long |
| Average R:R | 3.54 |
| R:R range | 2.67 – 6.86 |
| Total designed R | 53.06 |
| Trigger | retracement zone `0.8–0.92`, retention depth recorded per signal |

The full table is in [`SIGNALS.md`](SIGNALS.md) and the raw log in [`data/signals.json`](data/signals.json).

---

## 7. What the screenshots actually show

Four recurring frame types, all present in `archive/`:

1. **Engine panel over a chart** — PRICE / PREDICTION / FRACTAL with TP, ENTRY and SL levels drawn. This is the signal in its native form.
2. **Annotated structure** — channels, symmetry rectangles, numbered legs: the reasoning that produced the levels.
3. **Before / after pairs** — a setup, then the same chart later with the move resolved.
4. **Tool output** — fractal pressure histograms, pattern detection, visual layer builds.

A reader who wants to audit a specific signal should open `SIGNALS.md`, take the timestamp, and find the folder at `archive/YYYY-MM/<date>_<time>/` — the chart and its caption sit right there.

---

## 8. Limitations — read this before quoting any number

- **No outcomes are recorded.** The export contains no field stating whether a signal hit TP or SL. The 3.54 average R:R is a *design* metric (target distance ÷ stop distance), not a realised result.
- **Return is not PnL.** A high average R:R with a low hit rate can lose money; without outcomes, the archive cannot distinguish the two.
- **Hindsight.** Charts were annotated in live time, but they are still selected posts. Setups that failed quietly are less likely to be posted than ones that worked.
- **One channel, one trader, self-reported.** No broker statements, no third-party verification, no forward test.
- **Coverage gaps.** Four months of the period have no posts at all.

These are not caveats to bury; they are the honest boundary of what the record supports.

---

## 9. What would turn this into a verifiable track record

1. **An outcome ledger** — one row per signal: `signal_id, posted_at, entry, tp, sl, closed_at, exit_price, outcome (tp/sl/manual), R realised`. Even 50 rows would make the win rate computable instead of asserted.
2. **Timestamped entries before the move** — signals posted and archived with the message timestamp intact, which the current format already supports.
3. **A forward test on unseen data** — run the engine on a fixed date range, publish every signal including the ugly ones, and let the ledger accumulate without editing.
4. **Broker/API export** — for any live period, the account statement is the only artifact that cannot be curated.

The archive in this repo is the raw material for (1) — the timestamps and the reason strings are already there.

---

## 10. Reproducing this report

```bash
python3 scripts/build_archive.py "/path/to/DataExport_YYYY-MM-DD"
```

Regenerates `archive/`, `data/screenshots.json`, `data/signals.json`, `INDEX.md`, `SIGNALS.md`. The report itself is written from those files, so any new export can be folded in without re-doing the work by hand.

---

*Educational material. Not financial advice. Not a signal service. Trade your own risk.*
