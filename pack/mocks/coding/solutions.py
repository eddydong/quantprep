"""Answer key for the coding mock."""

from __future__ import annotations

import numpy as np
import pandas as pd


def purged_walk_forward_splits(
    t: np.ndarray,
    horizon: float,
    n_folds: int,
    embargo: float,
) -> list[tuple[np.ndarray, np.ndarray]]:
    t = np.asarray(t, dtype=np.float64)
    n = t.size
    if n_folds < 1:
        raise ValueError("n_folds must be >= 1")
    if n < n_folds:
        raise ValueError("need at least one sample per fold")

    # Contiguous test blocks covering the series from earliest to latest.
    bounds = np.linspace(0, n, n_folds + 1, dtype=int)
    splits: list[tuple[np.ndarray, np.ndarray]] = []
    for k in range(n_folds):
        test_lo, test_hi = int(bounds[k]), int(bounds[k + 1])
        test_idx = np.arange(test_lo, test_hi, dtype=np.int64)
        if test_idx.size == 0:
            continue
        test_t_min = float(t[test_idx].min())
        test_t_max = float(t[test_idx].max())
        left = test_t_min - embargo
        right = test_t_max + horizon + embargo
        # Train is only *earlier* than the test block (walk-forward), then purged.
        train_mask = np.arange(n) < test_lo
        info_lo = t
        info_hi = t + horizon
        overlap = (info_lo <= right) & (info_hi >= left)
        train_idx = np.flatnonzero(train_mask & ~overlap).astype(np.int64)
        splits.append((train_idx, test_idx))
    return splits


def ewma(x: np.ndarray, alpha: float) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    if not (0 < alpha <= 1):
        raise ValueError("alpha must be in (0, 1]")
    y = np.empty_like(x, dtype=np.float64)
    if x.size == 0:
        return y
    y[0] = x[0]
    one_minus = 1.0 - alpha
    for i in range(1, x.size):
        y[i] = alpha * x[i] + one_minus * y[i - 1]
    return y


def order_flow_imbalance(
    bid_sz: np.ndarray,
    ask_sz: np.ndarray,
    bid_px: np.ndarray,
    ask_px: np.ndarray,
) -> np.ndarray:
    bid_sz = np.asarray(bid_sz, dtype=np.float64)
    ask_sz = np.asarray(ask_sz, dtype=np.float64)
    bid_px = np.asarray(bid_px, dtype=np.float64)
    ask_px = np.asarray(ask_px, dtype=np.float64)
    n = bid_sz.size
    ofi = np.zeros(n, dtype=np.float64)
    if n == 0:
        return ofi

    db = np.zeros(n, dtype=np.float64)
    da = np.zeros(n, dtype=np.float64)

    bid_up = bid_px[1:] > bid_px[:-1]
    bid_dn = bid_px[1:] < bid_px[:-1]
    bid_eq = ~bid_up & ~bid_dn
    db[1:] = np.where(bid_up, bid_sz[1:], 0.0)
    db[1:] = np.where(bid_eq, bid_sz[1:] - bid_sz[:-1], db[1:])
    db[1:] = np.where(bid_dn, -bid_sz[:-1], db[1:])

    ask_dn = ask_px[1:] < ask_px[:-1]
    ask_up = ask_px[1:] > ask_px[:-1]
    ask_eq = ~ask_dn & ~ask_up
    da[1:] = np.where(ask_dn, ask_sz[1:], 0.0)
    da[1:] = np.where(ask_eq, ask_sz[1:] - ask_sz[:-1], da[1:])
    da[1:] = np.where(ask_up, -ask_sz[:-1], da[1:])

    ofi[1:] = db[1:] - da[1:]
    return ofi


def microprice(
    bid_px: np.ndarray,
    ask_px: np.ndarray,
    bid_sz: np.ndarray,
    ask_sz: np.ndarray,
) -> np.ndarray:
    bid_px = np.asarray(bid_px, dtype=np.float64)
    ask_px = np.asarray(ask_px, dtype=np.float64)
    bid_sz = np.asarray(bid_sz, dtype=np.float64)
    ask_sz = np.asarray(ask_sz, dtype=np.float64)
    den = bid_sz + ask_sz
    den = np.where(den == 0, np.nan, den)
    return (ask_px * bid_sz + bid_px * ask_sz) / den


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
    mid = np.asarray(mid, dtype=np.float64)
    inventory = np.clip(np.asarray(inventory, dtype=np.float64), -q_max, q_max)
    if kappa <= 0:
        raise ValueError("kappa must be > 0")
    var_term = 0.5 * gamma * sigma**2 * horizon
    if abs(gamma) < 1e-12:
        d = (1.0 / kappa) + fee
    else:
        d = (1.0 / gamma) * np.log(1.0 + gamma / kappa) + var_term + fee
    r = mid - inventory * gamma * sigma**2 * horizon
    bid = r - d
    ask = r + d
    crossed = bid > ask
    bid = np.where(crossed, mid, bid)
    ask = np.where(crossed, mid, ask)
    d_out = np.full_like(mid, d, dtype=np.float64)
    return {
        "reservation": r,
        "bid": bid,
        "ask": ask,
        "half_spread": d_out,
    }


def fixed_backtest(df: pd.DataFrame) -> dict[str, float]:
    """Information set: at close of bar t we know ret[t].

    Position held *during* bar t is sign(ret[t-1]), so PnL on bar t is
    sign(ret[t-1]) * ret[t]. Spread is paid on position change.
    Sharpe uses only realised net returns on tradable bars, annualised
    with sqrt(252) and no future information in the denominator beyond
    those same realised bars.
    """
    px = df["close"].to_numpy(dtype=np.float64)
    n = px.size
    if n < 3:
        return {
            "n_bars": float(n),
            "gross_pnl_mean": 0.0,
            "net_pnl_mean": 0.0,
            "sharpe": 0.0,
            "turnover": 0.0,
        }

    ret = np.zeros(n, dtype=np.float64)
    ret[1:] = px[1:] / px[:-1] - 1.0
    pos = np.zeros(n, dtype=np.float64)
    pos[2:] = np.sign(ret[1:-1])
    gross = pos * ret

    spread = float(df["spread"].to_numpy(dtype=np.float64)[0]) if "spread" in df.columns else 0.0
    dpos = np.diff(pos, prepend=0.0)
    cost = np.abs(dpos) * (spread / 2.0)
    net = gross - cost

    tradable = slice(2, None)
    mu = float(np.mean(net[tradable]))
    sd = float(np.std(net[tradable], ddof=1)) if net[tradable].size > 2 else 0.0
    sharpe = float(mu / sd * np.sqrt(252.0)) if sd > 0 else 0.0
    turnover = float(np.mean(np.abs(dpos[tradable])))
    return {
        "n_bars": float(n),
        "gross_pnl_mean": float(np.mean(gross[tradable])),
        "net_pnl_mean": mu,
        "sharpe": sharpe,
        "turnover": turnover,
    }


# Interviewer notes for Problem 4 — not in broken_backtest.py on purpose.
BROKEN_BACKTEST_BUGS = """
1. Signal uses the same-bar return (look-ahead).
2. Position is applied to the same-bar return (executes at stale/future px).
3. No spread / fee.
4. Sharpe uses the full-sample standard deviation including the future
   (and sqrt(n) instead of a time convention).
5. shift(-1) on close to 'align labels' pulls tomorrow into today.
6. Drops NaNs with bfill, which fills backward from the future.
7. Sorts by return (survivorship / peeking) before computing the mean.
"""

