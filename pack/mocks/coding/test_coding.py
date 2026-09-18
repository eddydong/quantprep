"""Tests for the coding lab. Stubs skip until you implement each function."""

from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

import candidate as C
import solutions as S


class TestCandidate(unittest.TestCase):
    def _call(self, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except NotImplementedError:
            self.skipTest("not implemented yet")

    def test_ewma_matches_reference(self):
        rng = np.random.default_rng(0)
        x = rng.normal(size=200)
        got = self._call(C.ewma, x, 0.2)
        np.testing.assert_allclose(got, S.ewma(x, 0.2), rtol=1e-10, atol=1e-12)
        y1 = C.ewma(x, 0.3)
        x2 = x.copy()
        x2[-1] = 1e9
        y2 = C.ewma(x2, 0.3)
        np.testing.assert_allclose(y1[:-1], y2[:-1])

    def test_microprice_and_ofi_causal(self):
        bid_px = np.array([1.0, 1.0, 1.1, 1.1, 1.0])
        ask_px = np.array([1.1, 1.1, 1.2, 1.1, 1.1])
        bid_sz = np.array([5.0, 6.0, 4.0, 4.0, 7.0])
        ask_sz = np.array([5.0, 4.0, 4.0, 8.0, 3.0])
        mp = self._call(C.microprice, bid_px, ask_px, bid_sz, ask_sz)
        np.testing.assert_allclose(mp, S.microprice(bid_px, ask_px, bid_sz, ask_sz))
        ofi = self._call(C.order_flow_imbalance, bid_sz, ask_sz, bid_px, ask_px)
        np.testing.assert_allclose(ofi, S.order_flow_imbalance(bid_sz, ask_sz, bid_px, ask_px))
        self.assertEqual(ofi[0], 0.0)

    def test_purged_splits_no_overlap(self):
        t = np.arange(0, 100, dtype=float)
        horizon, embargo, n_folds = 5.0, 3.0, 5
        splits = self._call(C.purged_walk_forward_splits, t, horizon, n_folds, embargo)
        self.assertEqual(len(splits), n_folds)
        for train_idx, test_idx in splits:
            if train_idx.size == 0:
                continue
            test_lo = t[test_idx].min() - embargo
            test_hi = t[test_idx].max() + horizon + embargo
            train_lo = t[train_idx]
            train_hi = t[train_idx] + horizon
            overlap = (train_lo <= test_hi) & (train_hi >= test_lo)
            self.assertFalse(np.any(overlap), "train information interval overlaps embargoed test")
            self.assertLess(train_idx.max(), test_idx.min())

    def test_reservation_quote_inventory_skew(self):
        mid = np.array([100.0, 100.0, 100.0])
        inv = np.array([-5.0, 0.0, 5.0])
        kwargs = dict(q_max=10, gamma=0.1, sigma=0.2, horizon=1.0, kappa=1.5, fee=0.01)
        out = self._call(C.reservation_quote, mid, inv, **kwargs)
        exp = S.reservation_quote(mid, inv, **kwargs)
        for k in exp:
            np.testing.assert_allclose(out[k], exp[k], rtol=1e-10, atol=1e-12)
        self.assertLess(out["reservation"][2], out["reservation"][1])
        self.assertLess(out["reservation"][1], out["reservation"][0])
        self.assertTrue(np.all(out["ask"] >= out["bid"]))

    def test_fixed_backtest_not_leaky(self):
        rng = np.random.default_rng(1)
        n = 500
        close = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, size=n)))
        df = pd.DataFrame({"close": close, "spread": np.full(n, 0.0002)})
        a = self._call(C.fixed_backtest, df)
        self.assertGreaterEqual(a.keys(), {"n_bars", "gross_pnl_mean", "net_pnl_mean", "sharpe", "turnover"})
        if a["turnover"] > 0:
            self.assertLessEqual(a["net_pnl_mean"], a["gross_pnl_mean"] + 1e-12)
        ref = S.fixed_backtest(df)
        np.testing.assert_allclose(a["gross_pnl_mean"], ref["gross_pnl_mean"], rtol=1e-8, atol=1e-10)
        np.testing.assert_allclose(a["net_pnl_mean"], ref["net_pnl_mean"], rtol=1e-8, atol=1e-10)
        df2 = df.copy()
        df2.loc[df.index[-1], "close"] = close[-1] * 3.0
        b = C.fixed_backtest(df2)
        self.assertEqual(a["n_bars"], b["n_bars"])


if __name__ == "__main__":
    unittest.main()
