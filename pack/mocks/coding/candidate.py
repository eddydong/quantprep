"""Director coding mock — implement these APIs.

Run tests from this directory:

    pytest -q

Do not import solutions.py from this module.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def purged_walk_forward_splits(
    t: np.ndarray,
    horizon: float,
    n_folds: int,
    embargo: float,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Walk-forward splits with purge + embargo.

    Sample i's label uses (t[i], t[i] + horizon]. Train must not contain
    samples whose information interval overlaps the embargo-expanded test
    window. See mocks/03-coding.md.
    """
    raise NotImplementedError


def ewma(x: np.ndarray, alpha: float) -> np.ndarray:
    """Causal EWMA with y[0] = x[0]."""
    raise NotImplementedError


def order_flow_imbalance(
    bid_sz: np.ndarray,
    ask_sz: np.ndarray,
    bid_px: np.ndarray,
    ask_px: np.ndarray,
) -> np.ndarray:
    """Causal level-1 OFI. Index 0 is 0."""
    raise NotImplementedError


def microprice(
    bid_px: np.ndarray,
    ask_px: np.ndarray,
    bid_sz: np.ndarray,
    ask_sz: np.ndarray,
) -> np.ndarray:
    raise NotImplementedError


def reservation_quote(
    mid: np.ndarray,
    inventory: np.ndarray,
    q_max: float,
    gamma: float,
    sigma: float,
    horizon: float,
    kappa: float,
    fee: float,
) -> dict[str, np.ndarray]:
    """Simplified Avellaneda–Stoikov reservation quotes."""
    raise NotImplementedError


def fixed_backtest(df: pd.DataFrame) -> dict[str, float]:
    """Leakage-free next-bar backtest. See broken_backtest.py for the bugs.

    Required keys: n_bars, gross_pnl_mean, net_pnl_mean, sharpe, turnover.
    """
    raise NotImplementedError
