"""Locks the answer key. If this file fails, the mock itself is wrong."""

from __future__ import annotations

import numpy as np
import pandas as pd

import solutions as S
from broken_backtest import broken_backtest


def test_ewma_identity_and_causality():
    x = np.array([1.0, 2.0, 3.0])
    np.testing.assert_allclose(S.ewma(x, 1.0), x)
    x2 = x.copy()
    x2[-1] = 99
    np.testing.assert_allclose(S.ewma(x, 0.4)[:-1], S.ewma(x2, 0.4)[:-1])


def test_ewma_step():
    x = np.array([1.0, 2.0, 3.0])
    y = S.ewma(x, 0.5)
    assert abs(y[1] - 1.5) < 1e-12
    assert abs(y[2] - (0.5 * 3 + 0.5 * 1.5)) < 1e-12


def test_ofi_cont_example_shape():
    bid_px = np.array([1.0, 1.0, 1.1])
    ask_px = np.array([1.1, 1.1, 1.1])
    bid_sz = np.array([5.0, 6.0, 4.0])
    ask_sz = np.array([5.0, 4.0, 4.0])
    ofi = S.order_flow_imbalance(bid_sz, ask_sz, bid_px, ask_px)
    assert ofi.shape == (3,)
    assert ofi[0] == 0.0
    # t=1: bid px eq, bid sz +1; ask px eq, ask sz -1 → ofi = 1 - (-1) wait:
    # ask increment on equal: 4-5 = -1; ofi = 1 - (-1) = 2
    assert abs(ofi[1] - 2.0) < 1e-12


def test_microprice_mid_when_balanced():
    mp = S.microprice(
        np.array([100.0]), np.array([102.0]), np.array([1.0]), np.array([1.0])
    )
    np.testing.assert_allclose(mp, [101.0])


def test_purged_first_fold_empty_train():
    t = np.arange(20, dtype=float)
    splits = S.purged_walk_forward_splits(t, horizon=2, n_folds=4, embargo=1)
    assert len(splits) == 4
    assert splits[0][0].size == 0
    for train_idx, test_idx in splits[1:]:
        assert train_idx.max() < test_idx.min()
        left = t[test_idx].min() - 1
        right = t[test_idx].max() + 2 + 1
        if train_idx.size:
            overlap = ((t[train_idx]) <= right) & ((t[train_idx] + 2) >= left)
            assert not np.any(overlap)


def test_gamma_zero_spread_limit():
    mid = np.array([10.0])
    inv = np.array([0.0])
    out = S.reservation_quote(
        mid, inv, q_max=1, gamma=0.0, sigma=0.2, horizon=1.0, kappa=2.0, fee=0.05
    )
    np.testing.assert_allclose(out["half_spread"], [0.5 + 0.05])
    assert out["bid"][0] <= out["ask"][0]


def test_broken_is_leaky_and_fixed_is_not():
    rng = np.random.default_rng(2)
    n = 300
    close = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, size=n)))
    df = pd.DataFrame({"close": close, "spread": np.full(n, 0.0002)})
    leaky = broken_backtest(df)
    fixed = S.fixed_backtest(df)
    # Look-ahead + sorting makes the broken Sharpe absurdly large.
    assert leaky["sharpe"] > 5
    assert abs(fixed["sharpe"]) < 5
    if fixed["turnover"] > 0:
        assert fixed["net_pnl_mean"] <= fixed["gross_pnl_mean"] + 1e-12
