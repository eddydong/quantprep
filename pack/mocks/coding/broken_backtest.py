"""Deliberately broken backtest — find at least five bugs.

Used as the prompt for Problem 4. Do not call this from production code.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def broken_backtest(df: pd.DataFrame) -> dict[str, float]:
    """BUGS (for the interviewer; strip this list before sitting the mock):

    1. Signal uses the *same-bar* return (look-ahead).
    2. Position is applied to the same-bar return (executes at stale/future px).
    3. No spread / fee.
    4. Sharpe uses the full-sample standard deviation including the future
       (and sqrt(n) instead of a time convention) — a leakage-ish statistic.
    5. `shift(-1)` on close to 'align labels' pulls tomorrow into today.
    6. Drops NaNs with bfill, which fills *backward* from the future.
    7. Sorts by return (survivorship / peeking) before computing the mean.
    """
    close = df["close"].copy()
    close = close.bfill()
    tomorrow = close.shift(-1)
    ret = tomorrow / close - 1.0  # look-ahead label used as if it were a feature
    signal = np.sign(ret)
    pnl = (signal * ret).sort_values(ascending=False)
    mu = float(pnl.mean())
    sd = float(pnl.std())
    return {
        "n_bars": float(len(df)),
        "pnl_mean": mu,
        "sharpe": float(mu / sd * np.sqrt(len(df))) if sd else 0.0,
    }
