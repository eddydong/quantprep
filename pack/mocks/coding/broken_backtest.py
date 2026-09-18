"""Deliberately leaky strategy simulator — find at least five bugs.

Used as the prompt for Problem 4. Do not copy this into production.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def broken_backtest(df: pd.DataFrame) -> dict[str, float]:
    close = df["close"].copy()
    close = close.bfill()
    tomorrow = close.shift(-1)
    ret = tomorrow / close - 1.0
    signal = np.sign(ret)
    pnl = (signal * ret).sort_values(ascending=False)
    mu = float(pnl.mean())
    sd = float(pnl.std())
    return {
        "n_bars": float(len(df)),
        "pnl_mean": mu,
        "sharpe": float(mu / sd * np.sqrt(len(df))) if sd else 0.0,
    }
