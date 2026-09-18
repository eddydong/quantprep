# Round 3 — Coding (Director mock)

**7 of 8** in the pack. Previous: [02-dl.md](02-dl.md). Next: [04-project.md](04-project.md).

**Time:** 90–120 minutes  
**Language:** Python (numpy/pandas). The lab on this page is the mock.  
**Bar:** they are **not looking for software engineers**. You need to be **competent** at coding: correct information sets, no leakage, code a desk would trust. You do **not** need kdb, Java, or a 50µs résumé. Style still matters: type hints, no `iterrows`.

If you are new to Python, finish [Python](#warmup) first (20 short sessions in the page).

Scroll to the **lab** below. Implement `candidate.py`, then **Run tests**. Stubs skip until you replace `raise NotImplementedError`. Your work stays in this browser. The answer key is a separate tab — do not open it first.

`broken_backtest.py` is in the lab too (read-only). First test run downloads a Python runtime into the browser (cached after that).

If they give you a **HackerRank-style** screen, still practise these: they are closer to a **GM AI Director** loop (leakage, microstructure, inventory) than reversing a linked list. Still warm up with **one** medium array/hash problem the night before so you are not rusty.

---

## Problem 1 — Purged walk-forward (25 min)

Implement `purged_walk_forward_splits(t, horizon, n_folds, embargo)`.

- `t` is a 1-D sorted array of decision timestamps (int64 ns or int seconds — treat as comparable numbers).
- Each sample `i` has a **label that uses data in (t[i], t[i] + horizon]**.
- Folds are contiguous in time (walk-forward: fold k’s test is a later block than fold k’s train).
- **Purge:** drop from **train** any index whose interval `[t, t+horizon]` overlaps the test interval expanded by `embargo` on both sides.
- Return a list of `(train_idx, test_idx)` numpy int64 arrays. All indices unique within a split; test blocks cover the series as evenly as possible without shuffling.

This is Lopez de Prado, not sklearn `TimeSeriesSplit`.

**Follow-up they will ask:** why embargo ≥ horizon; what if labels are triple-barrier and hitting time < horizon; how CPCV differs.

## Problem 2 — EWMA fair value and OFI (25 min)

Implement:

- `ewma(x, alpha)` — causal EWMA, `y[0] = x[0]`, `y[t] = alpha * x[t] + (1-alpha) * y[t-1]`. No look-ahead.
- `order_flow_imbalance(bid_sz, ask_sz, bid_px, ask_px)` — a simple **level-1 OFI**:

  For each t > 0:
  - bid increment: if bid_px up, +bid_sz[t]; if unchanged, bid_sz[t]−bid_sz[t-1]; if down, −bid_sz[t-1]
  - ask increment: if ask_px down, +ask_sz[t]; if unchanged, ask_sz[t]−ask_sz[t-1]; if up, −ask_sz[t-1]
  - OFI = bid_increment − ask_increment  
  Index 0 is 0.

- `microprice(bid_px, ask_px, bid_sz, ask_sz)` = (ask_px * bid_sz + bid_px * ask_sz) / (bid_sz + ask_sz) with safe denominator.

**Follow-up:** why microprice ≠ mid; how you would **standardise** OFI online; what happens at a tick-size change.

## Problem 3 — Inventory-aware quotes (20 min)

Implement `reservation_quote(mid, inventory, q_max, gamma, sigma, horizon, kappa, fee)`.

A simplified Avellaneda–Stoikov style:

- reservation `r = mid - inventory * gamma * sigma**2 * horizon`
- half-spread `d = (1/gamma) * log(1 + gamma/kappa) + 0.5 * gamma * sigma**2 * horizon + fee`  (if gamma≈0, use `1/kappa + fee` as the finite limit)
- bid = r − d, ask = r + d
- Clip inventory effect so quotes do not cross: if bid > ask, set both to mid.

Return dict with keys `reservation`, `bid`, `ask`, `half_spread` (all ndarray).

**Follow-up:** map `gamma` to a desk risk appetite; what you **monitor** live (inventory, realised spread vs model, fill asymmetry).

## Problem 4 — Debug the backtest (20–30 min)

`broken_backtest.py` contains a **deliberately leaky** strategy simulator. Do **not** rewrite from scratch. List the bugs (there are at least five), then implement `fixed_backtest(df)` in `candidate.py` that:

- trades only on information available at bar **close of t** for a position held over **t+1**
- applies spread cost
- reports net PnL mean and a **purged** Sharpe that does not use future vol

Write the bug list in comments above `fixed_backtest`.

---

## What interviewers listen for while you type

- You define **time** before you write a loop.
- You ask whether timestamps are **decision time or event time**.
- You refuse `shift(-1)` “to align the label” without an embargo.
- You vectorise, but you can write the O(n) loop correctly first.
- You mention **tests**: a unit test where leakage would make PnL explode.
- You mention **integer cents / tick size** rather than float fantasy, even if the toy uses floats.

## If they switch to “systems” instead of numpy

Only if **they** go there. The typical seat is not a software-engineer screen. Keep it to 10 minutes:

- You specify the model; Singapore/HK **engineering** owns the hot path.
- Registry, canary, kill switch, information set.
- You do not need to design exactly-once fill streams unless asked.
