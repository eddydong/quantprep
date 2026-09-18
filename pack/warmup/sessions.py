"""Twenty in-page Python warmup sessions. No repo paths in the student-facing text."""

from __future__ import annotations

PREFIX = """
def run(st):
    rows = []
    def check(name, fn):
        try:
            fn()
            rows.append({"name": name, "ok": "pass"})
        except Exception as e:
            rows.append({"name": name, "ok": "fail", "msg": str(e)})
    def need(name):
        if not hasattr(st, name):
            raise AssertionError("Define " + name)
        return getattr(st, name)
    def near(a, b, msg, eps=1e-9):
        if a is None:
            raise AssertionError(msg)
        if abs(float(a) - float(b)) >= eps:
            raise AssertionError(msg)
"""


def checks(body: str) -> str:
    return PREFIX + body + "\n    return rows\n"


SESSIONS: list[dict[str, str]] = [
    {
        "title": "Numbers and a mid",
        "goal": "Variables, arithmetic, a bid/ask.",
        "lesson": """
Python stores values in **names** (variables). A dealer’s quote is two numbers: **bid** (they buy) and **ask** (they sell). The **mid** is the average. The **spread** is ask minus bid.

```
mid = (bid + ask) / 2
spread = ask - bid
```

`#` starts a comment. `=` assigns. `/` divides. You do not declare types.

Assign `mid` and `spread` from the bid and ask already in the editor.
""",
        "starter": """# A dealer shows these prices.
bid = 7.7800
ask = 7.7804

mid = None
spread = None
""",
        "solution": """bid = 7.7800
ask = 7.7804
mid = (bid + ask) / 2
spread = ask - bid
""",
        "tests": checks("""
    check("mid", lambda: abs(need("mid") - 7.7802) < 1e-9 or (_ for _ in ()).throw(AssertionError("mid should be (bid + ask) / 2")))
    check("spread", lambda: abs(need("spread") - 0.0004) < 1e-9 or (_ for _ in ()).throw(AssertionError("spread should be ask - bid")))
"""),
    },
    {
        "title": "Strings and a pair",
        "goal": "Text, f-strings, a currency pair.",
        "lesson": """
Text lives in **strings**: `"USDCNH"` or `'USDCNH'`. An **f-string** inserts a value:

```
pair = "USDCNH"
line = f"{pair} mid={mid}"
```

`len(pair)` is 6. Strings do not do arithmetic: `"7.78" + 1` is an error. Convert with `float("7.78")` when a number arrived as text.

Build `line` so it contains the pair name and the mid.
""",
        "starter": """pair = "USDCNH"
bid = 7.7800
ask = 7.7804
mid = (bid + ask) / 2

line = ""
""",
        "solution": """pair = "USDCNH"
bid = 7.7800
ask = 7.7804
mid = (bid + ask) / 2
line = f"{pair} mid={mid}"
""",
        "tests": checks("""
    line = str(need("line"))
    check("has pair", lambda: "USDCNH" in line or (_ for _ in ()).throw(AssertionError("line should mention USDCNH")))
    check("has mid", lambda: "7.7802" in line or (_ for _ in ()).throw(AssertionError("line should include the mid 7.7802")))
"""),
    },
    {
        "title": "True, false, crossed quotes",
        "goal": "Comparisons and booleans.",
        "lesson": """
`True` and `False` are **booleans**. Comparisons produce them:

```
bid < ask      # a healthy market
bid > ask      # crossed — a bug
spread > 0.01  # wide
```

Combine with `and`, `or`, `not`. Equality is `==` (two equals). `=` only assigns.

Set `healthy` and `crossed` from the quote in the editor.
""",
        "starter": """bid = 7.7800
ask = 7.7804

healthy = None
crossed = None
""",
        "solution": """bid = 7.7800
ask = 7.7804
healthy = bid < ask
crossed = bid > ask
""",
        "tests": checks("""
    check("healthy", lambda: need("healthy") is True or (_ for _ in ()).throw(AssertionError("healthy should be True when bid < ask")))
    check("crossed", lambda: need("crossed") is False or (_ for _ in ()).throw(AssertionError("crossed should be False for this quote")))
"""),
    },
    {
        "title": "Lists of mids",
        "goal": "Ordered collections, len, last print.",
        "lesson": """
A **list** is an ordered sequence in square brackets:

```
mids = [7.7800, 7.7802, 7.7798]
```

`len(mids)` is 3. Index from zero: `mids[0]` is the first print, `mids[-1]` is the **last** (now). `mids.append(7.78)` adds at the end.

Lists can grow. In markets, the last element is “now”; earlier elements are history.

Set `n` and `last`.
""",
        "starter": """mids = [7.7800, 7.7802, 7.7798, 7.7810]

n = None
last = None
""",
        "solution": """mids = [7.7800, 7.7802, 7.7798, 7.7810]
n = len(mids)
last = mids[-1]
""",
        "tests": checks("""
    check("n", lambda: need("n") == 4 or (_ for _ in ()).throw(AssertionError("n should be len(mids)")))
    check("last", lambda: abs(need("last") - 7.7810) < 1e-12 or (_ for _ in ()).throw(AssertionError("last should be mids[-1]")))
"""),
    },
    {
        "title": "A quote as a dict",
        "goal": "Named fields, one snapshot.",
        "lesson": """
A **dict** maps keys to values — one quote, named:

```
quote = {"bid": 7.78, "ask": 7.7804, "bid_sz": 5.0, "ask_sz": 4.0}
quote["bid"]
```

Keys are usually strings. This is how a tick looks in Python before you put it in a table.

Add `mid` **into** the dict: average of bid and ask.
""",
        "starter": """quote = {
    "bid": 7.7800,
    "ask": 7.7804,
    "bid_sz": 5.0,
    "ask_sz": 4.0,
}
""",
        "solution": """quote = {
    "bid": 7.7800,
    "ask": 7.7804,
    "bid_sz": 5.0,
    "ask_sz": 4.0,
}
quote["mid"] = (quote["bid"] + quote["ask"]) / 2
""",
        "tests": checks("""
    q = need("quote")
    check("dict", lambda: isinstance(q, dict) or (_ for _ in ()).throw(AssertionError("quote should stay a dict")))
    check("mid key", lambda: abs(q.get("mid", 0) - 7.7802) < 1e-9 or (_ for _ in ()).throw(AssertionError("set quote['mid'] to (bid+ask)/2")))
"""),
    },
    {
        "title": "Loops and simple returns",
        "goal": "for-loops over a price path.",
        "lesson": """
A **for** loop walks a sequence:

```
for x in mids:
    print(x)
```

`range(n)` is 0, 1, …, n-1. Simple return from bar `i-1` to `i`:

```
ret = mids[i] / mids[i-1] - 1
```

You cannot compute a return at index 0 (no previous bar). Start the loop at 1.

Fill `rets` with the three returns of `mids`.
""",
        "starter": """mids = [100.0, 101.0, 100.0, 102.0]
rets = []
""",
        "solution": """mids = [100.0, 101.0, 100.0, 102.0]
rets = []
for i in range(1, len(mids)):
    rets.append(mids[i] / mids[i - 1] - 1)
""",
        "tests": checks("""
    rets = need("rets")
    check("length", lambda: len(rets) == 3 or (_ for _ in ()).throw(AssertionError("three returns from four mids")))
    check("first ret", lambda: abs(rets[0] - 0.01) < 1e-12 or (_ for _ in ()).throw(AssertionError("first return is 101/100 - 1")))
    check("last ret", lambda: abs(rets[2] - 0.02) < 1e-12 or (_ for _ in ()).throw(AssertionError("last return is 102/100 - 1")))
"""),
    },
    {
        "title": "Decisions: inventory",
        "goal": "if / elif / else.",
        "lesson": """
Branch with **if**:

```
if inventory > 0:
    action = "sell"   # dump the long
elif inventory < 0:
    action = "buy"
else:
    action = "flat"
```

Indentation (spaces) is syntax, not decoration. Four spaces is the convention.

Write a function `side(inventory)` that returns `"sell"`, `"buy"`, or `"flat"`.
""",
        "starter": """def side(inventory):
    return "todo"
""",
        "solution": """def side(inventory):
    if inventory > 0:
        return "sell"
    if inventory < 0:
        return "buy"
    return "flat"
""",
        "tests": checks("""
    fn = need("side")
    check("long", lambda: fn(3) == "sell" or (_ for _ in ()).throw(AssertionError("positive inventory → sell")))
    check("short", lambda: fn(-1) == "buy" or (_ for _ in ()).throw(AssertionError("negative inventory → buy")))
    check("flat", lambda: fn(0) == "flat" or (_ for _ in ()).throw(AssertionError("zero inventory → flat")))
"""),
    },
    {
        "title": "Functions: mid and spread",
        "goal": "def, return, reuse.",
        "lesson": """
A **function** names a recipe:

```
def mid(bid, ask):
    return (bid + ask) / 2
```

Call it: `mid(7.78, 7.7804)`. `return` sends a value back. Without `return`, the function yields `None`.

Write `mid(bid, ask)` and `spread(bid, ask)`. These are the atoms of every later feature.
""",
        "starter": """def mid(bid, ask):
    return None


def spread(bid, ask):
    return None
""",
        "solution": """def mid(bid, ask):
    return (bid + ask) / 2


def spread(bid, ask):
    return ask - bid
""",
        "tests": checks("""
    m = need("mid")
    s = need("spread")
    check("mid", lambda: abs(m(1.0, 1.0004) - 1.0002) < 1e-12 or (_ for _ in ()).throw(AssertionError("mid(bid, ask) = (bid+ask)/2")))
    check("spread", lambda: abs(s(1.0, 1.0004) - 0.0004) < 1e-12 or (_ for _ in ()).throw(AssertionError("spread = ask - bid")))
"""),
    },
    {
        "title": "Indexing: lookback, not lookahead",
        "goal": "Slices. History is behind you.",
        "lesson": """
`mids[a:b]` is a **slice**: from index `a` up to **but not including** `b`. `mids[-3:]` is the last three prints.

At decision time *now* = last index, you may use `mids[-n:]` (includes now) or `mids[-n-1:-1]` (strictly past). You must **not** pull a future bar: there is no `mids[i+1]` at time `i` when `i` is now.

Write `lookback(mids, n)` returning the last `n` mids, including the current last print.
""",
        "starter": """def lookback(mids, n):
    return []
""",
        "solution": """def lookback(mids, n):
    return mids[-n:]
""",
        "tests": checks("""
    fn = need("lookback")
    xs = [10, 11, 12, 13, 14]
    check("last three", lambda: fn(xs, 3) == [12, 13, 14] or (_ for _ in ()).throw(AssertionError("lookback should be mids[-n:]")))
    check("all", lambda: fn(xs, 5) == xs or (_ for _ in ()).throw(AssertionError("n = len should return the whole list")))
"""),
    },
    {
        "title": "A book of quotes",
        "goal": "Lists of dicts.",
        "lesson": """
Real logs are a **list of dicts** — one dict per timestamp:

```
book = [
    {"bid": 1.0, "ask": 1.1},
    {"bid": 1.0, "ask": 1.2},
]
```

Loop and collect a field:

```
asks = [q["ask"] for q in book]
```

That last line is a **list comprehension**: a loop that builds a list.

Write `asks_of(book)` returning every ask, in order.
""",
        "starter": """def asks_of(book):
    return []
""",
        "solution": """def asks_of(book):
    return [q["ask"] for q in book]
""",
        "tests": checks("""
    fn = need("asks_of")
    book = [{"bid": 1.0, "ask": 1.1}, {"bid": 1.0, "ask": 1.25}]
    check("asks", lambda: fn(book) == [1.1, 1.25] or (_ for _ in ()).throw(AssertionError("return each quote's ask, in order")))
"""),
    },
    {
        "title": "Numpy: prices as arrays",
        "goal": "Vectorised returns. The ML workhorse.",
        "lesson": """
**NumPy** stores a homogeneous grid of numbers. Almost every ML feature starts here. A 1-D array is a time series; a 2-D array is a table (rows = time, columns = features). A 3-D array is already the shape of a tiny **tensor** (batch × time × features) that deep nets eat.

```
import numpy as np
mids = np.array([100.0, 101.0, 100.0])
rets = mids[1:] / mids[:-1] - 1
```

`mids[1:]` is every print except the first; `mids[:-1]` is every print except the last. Pair them and you get returns **without** a Python for-loop.

Set `rets` that way. Length should be 3.
""",
        "starter": """import numpy as np

mids = np.array([100.0, 101.0, 100.0, 103.0])
rets = None
""",
        "solution": """import numpy as np

mids = np.array([100.0, 101.0, 100.0, 103.0])
rets = mids[1:] / mids[:-1] - 1
""",
        "tests": checks("""
    import numpy as np
    rets = np.asarray(need("rets"), dtype=float)
    check("len", lambda: rets.size == 3 or (_ for _ in ()).throw(AssertionError("four mids → three returns")))
    check("first", lambda: abs(rets[0] - 0.01) < 1e-12 or (_ for _ in ()).throw(AssertionError("first return 101/100 - 1")))
    check("last", lambda: abs(rets[-1] - 0.03) < 1e-12 or (_ for _ in ()).throw(AssertionError("last return 103/100 - 1")))
"""),
    },
    {
        "title": "Causal EWMA",
        "goal": "A loop that never looks ahead.",
        "lesson": """
An **EWMA** (exponentially weighted moving average) is a smoother: today’s value is a blend of the new tick and yesterday’s smoother.

```
y[0] = x[0]
y[t] = alpha * x[t] + (1 - alpha) * y[t-1]
```

**Causal** means `y[t]` uses only `x[0]…x[t]`. If you accidentally use `x[t+1]`, you leak the future — the same crime as a leaky backtest.

Write `ewma(x, alpha)` returning a numpy array the same length as `x`.
""",
        "starter": """import numpy as np

def ewma(x, alpha):
    x = np.asarray(x, dtype=float)
    y = np.empty_like(x)
    return y
""",
        "solution": """import numpy as np

def ewma(x, alpha):
    x = np.asarray(x, dtype=float)
    y = np.empty_like(x)
    if x.size == 0:
        return y
    y[0] = x[0]
    one_minus = 1.0 - alpha
    for i in range(1, x.size):
        y[i] = alpha * x[i] + one_minus * y[i - 1]
    return y
""",
        "tests": checks("""
    import numpy as np
    fn = need("ewma")
    x = np.array([1.0, 2.0, 3.0])
    y = np.asarray(fn(x, 0.5), dtype=float)
    check("first", lambda: abs(y[0] - 1.0) < 1e-12 or (_ for _ in ()).throw(AssertionError("y[0] must equal x[0]")))
    check("step", lambda: abs(y[1] - 1.5) < 1e-12 or (_ for _ in ()).throw(AssertionError("y[1] = 0.5*2 + 0.5*1")))
    x2 = x.copy(); x2[-1] = 99
    y2 = np.asarray(fn(x2, 0.5), dtype=float)
    check("causal", lambda: abs(y[1] - y2[1]) < 1e-12 or (_ for _ in ()).throw(AssertionError("changing the last tick must not change earlier y")))
"""),
    },
    {
        "title": "Pandas: a series with time",
        "goal": "The table you will actually live in.",
        "lesson": """
**pandas** wraps arrays with labels. A **Series** is one column with an index (often timestamps). A **DataFrame** is several columns.

```
import pandas as pd
s = pd.Series([100.0, 101.0, 99.0], index=[0, 1, 2])
s.iloc[-1]   # last by position
s.loc[1]     # by label
```

`.iloc` is position; `.loc` is label. Mixing them up is a classic leak.

Set `last` to the last close using `.iloc`.
""",
        "starter": """import pandas as pd

close = pd.Series([100.0, 101.5, 99.0, 102.0])
last = None
""",
        "solution": """import pandas as pd

close = pd.Series([100.0, 101.5, 99.0, 102.0])
last = close.iloc[-1]
""",
        "tests": checks("""
    check("last", lambda: abs(float(need("last")) - 102.0) < 1e-12 or (_ for _ in ()).throw(AssertionError("last should be close.iloc[-1]")))
"""),
    },
    {
        "title": "Shift: labels vs features",
        "goal": "The one pandas footgun that costs real money.",
        "lesson": """
`.shift(1)` moves values **forward** in the index: yesterday’s value sits on today’s row. That is a **feature** you were allowed to know at today’s open.

`.shift(-1)` pulls **tomorrow** onto today. That is a **label**, not a feature. If you train on it as if it were known, the model is cheating.

```
ret = close.pct_change()
y = ret.shift(-1)    # next-bar return = label
x = ret.shift(1)     # previous return = feature
```

Write `lagged_ret(close)` returning the simple return **lagged by one bar** (a feature). The first value may be NaN.
""",
        "starter": """import pandas as pd

def lagged_ret(close):
    return close
""",
        "solution": """import pandas as pd

def lagged_ret(close):
    return close.pct_change().shift(1)
""",
        "tests": checks("""
    import pandas as pd
    import numpy as np
    fn = need("lagged_ret")
    close = pd.Series([100.0, 110.0, 132.0])
    out = pd.Series(fn(close)).astype(float)
    def _early():
        if not (bool(np.isnan(out.iloc[0])) or bool(np.isnan(out.iloc[1]))):
            raise AssertionError("early rows should be NaN after pct_change and a lag")
    def _past():
        near(out.iloc[-1], 0.10, "last feature should be the previous bar's 10% return, not 132/110-1")
    check("nan early", _early)
    check("no future", _past)
"""),
    },
    {
        "title": "A feature table",
        "goal": "DataFrame columns the model will see.",
        "lesson": """
A model wants a **table**: one row per decision time, columns = features known at that time.

```
df["mid"] = (df["bid"] + df["ask"]) / 2
df["spread"] = df["ask"] - df["bid"]
df["ret_lag"] = df["mid"].pct_change().shift(1)
```

Never put the thing you are predicting in the same-row features unless you are building the **label** column on purpose, named as such.

Add `mid`, `spread`, and `ret_lag` to `df`.
""",
        "starter": """import pandas as pd

df = pd.DataFrame({
    "bid": [100.0, 100.5, 101.0, 100.0],
    "ask": [100.2, 100.7, 101.2, 100.3],
})
""",
        "solution": """import pandas as pd

df = pd.DataFrame({
    "bid": [100.0, 100.5, 101.0, 100.0],
    "ask": [100.2, 100.7, 101.2, 100.3],
})
df["mid"] = (df["bid"] + df["ask"]) / 2
df["spread"] = df["ask"] - df["bid"]
df["ret_lag"] = df["mid"].pct_change().shift(1)
""",
        "tests": checks("""
    df = need("df")
    check("mid col", lambda: "mid" in df.columns or (_ for _ in ()).throw(AssertionError("add a mid column")))
    check("spread col", lambda: "spread" in df.columns or (_ for _ in ()).throw(AssertionError("add a spread column")))
    check("ret_lag col", lambda: "ret_lag" in df.columns or (_ for _ in ()).throw(AssertionError("add ret_lag from lagged mid returns")))
    check("mid value", lambda: abs(float(df["mid"].iloc[0]) - 100.1) < 1e-9 or (_ for _ in ()).throw(AssertionError("first mid is (100+100.2)/2")))
"""),
    },
    {
        "title": "Masks: Asia hours",
        "goal": "Boolean filters. Sessions.",
        "lesson": """
A **mask** is an array of True/False, one per row. Use it to keep a session:

```
asia = (hour >= 0) & (hour < 8)
asia_mids = mids[asia]
```

`&` is and, `|` is or, `~` is not — and you need parentheses. This is how you restrict a model to Tokyo morning without a for-loop.

Write `asia_mask(hour)` returning a numpy boolean array: True when `0 <= hour < 8`.
""",
        "starter": """import numpy as np

def asia_mask(hour):
    hour = np.asarray(hour)
    return hour == 0
""",
        "solution": """import numpy as np

def asia_mask(hour):
    hour = np.asarray(hour)
    return (hour >= 0) & (hour < 8)
""",
        "tests": checks("""
    import numpy as np
    fn = need("asia_mask")
    h = np.array([0, 7, 8, 15, 3])
    m = np.asarray(fn(h))
    check("shape", lambda: m.shape == h.shape or (_ for _ in ()).throw(AssertionError("mask length follows hour")))
    check("tokyo", lambda: bool(m[0] and m[1] and m[4]) or (_ for _ in ()).throw(AssertionError("0, 7, 3 should be True")))
    check("london", lambda: bool((not m[2]) and (not m[3])) or (_ for _ in ()).throw(AssertionError("8 and 15 should be False")))
"""),
    },
    {
        "title": "A linear fit in numpy",
        "goal": "The smallest ML model: least squares.",
        "lesson": """
A **linear model** predicts `y ≈ X w`. NumPy solves it with least squares. This is the same idea as a one-layer net without an activation.

```
import numpy as np
w, *_ = np.linalg.lstsq(X_train, y_train, rcond=None)
pred = X_test @ w
```

`@` is matrix multiply. Always include a **column of ones** in `X` if you want an intercept.

Write `fit_predict(X_train, y_train, X_test)` — fit on train, **score on test**. Returning `y_train` is cheating and will fail.
""",
        "starter": """import numpy as np

def fit_predict(X_train, y_train, X_test):
    return y_train
""",
        "solution": """import numpy as np

def fit_predict(X_train, y_train, X_test):
    X_train = np.asarray(X_train, dtype=float)
    y_train = np.asarray(y_train, dtype=float)
    X_test = np.asarray(X_test, dtype=float)
    w, *_ = np.linalg.lstsq(X_train, y_train, rcond=None)
    return X_test @ w
""",
        "tests": checks("""
    import numpy as np
    fn = need("fit_predict")
    Xtr = np.array([[1.0, 0.0], [1.0, 1.0], [1.0, 2.0]])
    ytr = np.array([0.0, 2.0, 4.0])
    Xte = np.array([[1.0, 3.0], [1.0, 4.0]])
    pred = np.asarray(fn(Xtr, ytr, Xte), dtype=float)
    def _len():
        if pred.shape[0] != 2:
            raise AssertionError("predict on X_test (2 rows), not on y_train")
    def _fit():
        near(pred[0], 6.0, "the line is y = 2 * x1; test x1=3 → 6")
        near(pred[1], 8.0, "test x1=4 → 8")
    check("test length", _len)
    check("oot", _fit)
"""),
    },
    {
        "title": "Time split, never shuffle",
        "goal": "Train is earlier. Test is later.",
        "lesson": """
In images you shuffle. In markets you **do not**. Tomorrow is not allowed in today’s training fold.

```
cut = int(n * 0.7)
train = np.arange(0, cut)
test = np.arange(cut, n)
```

Walk-forward is this idea with more folds. Purged CV (the coding mock) adds a gap so label windows do not overlap the cut.

Write `time_split(n, train_frac)` returning `(train_idx, test_idx)` as numpy integer arrays. Train indices must all be `<` every test index.
""",
        "starter": """import numpy as np

def time_split(n, train_frac):
    return np.arange(n), np.arange(n)
""",
        "solution": """import numpy as np

def time_split(n, train_frac):
    cut = int(n * train_frac)
    train = np.arange(0, cut, dtype=np.int64)
    test = np.arange(cut, n, dtype=np.int64)
    return train, test
""",
        "tests": checks("""
    import numpy as np
    fn = need("time_split")
    tr, te = fn(10, 0.7)
    tr = np.asarray(tr); te = np.asarray(te)
    check("cover", lambda: tr.size + te.size == 10 or (_ for _ in ()).throw(AssertionError("train and test should partition 0..n-1")))
    check("order", lambda: (te.size == 0 or tr.size == 0 or tr.max() < te.min()) or (_ for _ in ()).throw(AssertionError("every train index must be before test")))
    check("frac", lambda: tr.size == 7 and te.size == 3 or (_ for _ in ()).throw(AssertionError("int(10*0.7) = 7 train, 3 test")))
"""),
    },
    {
        "title": "Metrics that lie",
        "goal": "MSE vs hit-rate. Why AUC is not PnL.",
        "lesson": """
**MSE** (mean squared error) is a number for regression. **Hit-rate** is how often `sign(pred)` matches `sign(y)`. Both can look great while a trading rule loses money: they ignore size, spread, and fill.

A toxicity model with a pretty **AUC** can still bleed markout vs fill. You will meet that in the ML mock. For now, implement both numbers so you can refuse to ship on either alone.

```
mse = mean((pred - y)**2)
hit = mean(sign(pred) == sign(y))   # careful at zeros
```

Write `mse(pred, y)` and `hit_rate(pred, y)` using numpy. Treat `sign(0)` as a miss unless both are 0.
""",
        "starter": """import numpy as np

def mse(pred, y):
    return 0.0


def hit_rate(pred, y):
    return 0.0
""",
        "solution": """import numpy as np

def mse(pred, y):
    pred = np.asarray(pred, dtype=float)
    y = np.asarray(y, dtype=float)
    return float(np.mean((pred - y) ** 2))


def hit_rate(pred, y):
    pred = np.asarray(pred, dtype=float)
    y = np.asarray(y, dtype=float)
    return float(np.mean(np.sign(pred) == np.sign(y)))
""",
        "tests": checks("""
    import numpy as np
    m = need("mse")
    h = need("hit_rate")
    pred = np.array([1.0, -1.0, 0.5])
    y = np.array([1.0, 1.0, 0.5])
    check("mse", lambda: abs(m(pred, y) - np.mean((pred - y)**2)) < 1e-12 or (_ for _ in ()).throw(AssertionError("mse is mean((pred-y)**2)")))
    check("hit", lambda: abs(h(pred, y) - (2 / 3)) < 1e-12 or (_ for _ in ()).throw(AssertionError("two of three signs match")))
"""),
    },
    {
        "title": "A tiny pipeline",
        "goal": "Features, time split, fit, score. No shuffle.",
        "lesson": """
This is the skeleton of every later model, including a net:

1. Build a feature known at `t` (lagged return).
2. Build a label at `t` (next return) — used only as `y`, never as a feature.
3. **Time-split**. Fit on train. Score **test**.
4. Report test MSE. In-sample MSE is for debugging, not for claiming skill.

A neural net is the same pipeline with `pred = f(X, weights)` instead of `X @ w`. The leakage rules do not change because the model got deeper.

Write `pipeline(mids)` returning a dict with keys `train_mse` and `test_mse`. Use lag-1 return as the single feature plus an intercept, next return as `y`, 70% time split, `np.linalg.lstsq`. Drop rows with NaN.
""",
        "starter": """import numpy as np

def pipeline(mids):
    return {"train_mse": 0.0, "test_mse": 0.0}
""",
        "solution": """import numpy as np

def pipeline(mids):
    mids = np.asarray(mids, dtype=float)
    ret = np.zeros_like(mids)
    ret[1:] = mids[1:] / mids[:-1] - 1.0
    y = ret[2:]
    x1 = ret[1:-1]
    X = np.column_stack([np.ones(x1.size), x1])
    n = X.shape[0]
    cut = int(n * 0.7)
    Xtr, Xte = X[:cut], X[cut:]
    ytr, yte = y[:cut], y[cut:]
    w, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)
    def mse(Xa, ya):
        pred = Xa @ w
        return float(np.mean((pred - ya) ** 2))
    return {"train_mse": mse(Xtr, ytr), "test_mse": mse(Xte, yte)}
""",
        "tests": checks("""
    import numpy as np
    fn = need("pipeline")
    mids = np.array([100.0, 101.0, 100.5, 102.0, 101.0, 103.0, 102.5, 104.0] * 10, dtype=float)
    out = fn(mids)
    def ref(xs):
        xs = np.asarray(xs, dtype=float)
        ret = np.zeros_like(xs)
        ret[1:] = xs[1:] / xs[:-1] - 1.0
        y = ret[2:]
        x1 = ret[1:-1]
        X = np.column_stack([np.ones(x1.size), x1])
        cut = int(X.shape[0] * 0.7)
        w, *_ = np.linalg.lstsq(X[:cut], y[:cut], rcond=None)
        def mse(Xa, ya):
            return float(np.mean((Xa @ w - ya) ** 2))
        return mse(X[:cut], y[:cut]), mse(X[cut:], y[cut:])
    want_tr, want_te = ref(mids)
    def _keys():
        if not (isinstance(out, dict) and {"train_mse", "test_mse"} <= set(out)):
            raise AssertionError("return a dict with train_mse and test_mse")
    def _train():
        near(out["train_mse"], want_tr, "train_mse should match lag-1 return + intercept, 70% time split, lstsq", 1e-8)
    def _test():
        near(out["test_mse"], want_te, "test_mse is scored on the later 30%, not shuffled, not in-sample", 1e-8)
    check("keys", _keys)
    check("train_mse", _train)
    check("test_mse", _test)
"""),
    },
]


assert len(SESSIONS) == 20, len(SESSIONS)
