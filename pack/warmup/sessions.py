"""Twenty in-page Python warmup sessions. No repo paths in the student-facing text."""

from __future__ import annotations

PREFIX = """
def run(st):
    import numpy as np
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
    def nums(x, msg="return a list or array of numbers"):
        try:
            return np.array(x, dtype=float)
        except Exception:
            raise AssertionError(msg)
"""


def checks(body: str) -> str:
    return PREFIX + body + "\n    return rows\n"


SESSIONS: list[dict[str, str]] = [
    {
        "title": "Numbers and a mid",
        "goal": "Names, arithmetic, a bid/ask.",
        "lesson": """
Python stores a value under a **name**. `qty = 2.0` means: remember `2.0` as `qty`. That is **assignment**. One `=` is not “equals”; it is “put this in that name.”

Arithmetic:

- `+` add, `-` subtract, `*` multiply, `/` divide
- Parentheses `( )` change order: `(a + b) / 2` adds first, then divides
- `#` starts a **comment**. Python ignores the rest of that line.

```
qty = 2.0
px = 7.78
notional = qty * px
half = (qty + 0.0) / 2
```

You do not declare types. `7.78` is already a decimal (a **float**).

A dealer’s quote is two numbers: **bid** (they buy) and **ask** (they sell). The **mid** is the average of those two. The **spread** is how far apart they sit: ask minus bid.

The editor already has `bid` and `ask`. Assign `mid` and `spread`.
""",
        "starter": """# A dealer shows these prices.
bid = 7.7800
ask = 7.7804

# Assign mid and spread.
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
        "goal": "Text, joining, an f-string.",
        "lesson": """
**Strings** are text. Write them in quotes: `"eFX"` or `'eFX'` — both fine, pick one style and stay with it.

`len("eFX")` is 3: `len` counts characters. A **function call** is a name followed by parentheses. `len` is built in; you will write your own functions later.

Join text with `+` (both sides must be strings). A number is not a string until you wrap it with `str(...)`. The other way: `float("7.78")` turns text into a number. `"7.78" + 1` is an error.

An **f-string** is a shorter way to drop a value into text. Put `f` before the quotes, then `{name}` inside:

```
desk = "eFX"
n = 3
msg = f"{desk} has {n} makers"
# same idea with +: desk + " has " + str(n) + " makers"
```

Python replaces `{desk}` with the value of `desk`.

The editor has a currency **pair** and a **mid**. Build `line` so it contains both the pair name and the mid.
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
Some values are not numbers or text. **`True`** and **`False`** are **booleans** — yes or no.

A **comparison** produces a boolean. Read `==` as “is equal to” (two equals). One `=` still means assignment.

```
spread = 0.0004
wide = spread > 0.01      # False — this spread is not wide
tight = spread <= 0.0005  # True
same = spread == 0.0004   # True
```

The other comparisons: `<` less, `>` greater, `<=` less or equal, `>=` greater or equal, `!=` not equal.

Combine booleans:

- `and` — True only if both sides are True
- `or` — True if at least one side is True
- `not` — flips True to False and False to True

A healthy quote has bid **below** ask. A **crossed** quote has bid **above** ask (a bug). Set `healthy` and `crossed` from the bid and ask in the editor.
""",
        "starter": """bid = 7.7800
ask = 7.7804

healthy = False
crossed = False
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
        "goal": "Ordered collections, positions, append.",
        "lesson": """
A **list** holds several values in order, in square brackets, separated by commas:

```
sizes = [2.0, 1.0, 4.0]
```

`len(sizes)` is 3 — `len` counts items, not characters, when the input is a list.

Each item has a **position** (an **index**). Counting starts at **zero**, not one:

```
index:   0     1     2
value:  2.0   1.0   4.0
```

- `sizes[0]` is the first item
- `sizes[1]` is the second
- `sizes[-1]` is the last item (`-1` always means “from the end”)

`[]` is an empty list: no items yet. `.append(value)` adds one item at the end:

```
seen = []
seen.append(2.0)
```

The dot means “use this list’s append.” Later you will see more **methods** — names after a dot that do work on that object.

In markets, the last print is “now”; earlier items are history. The editor has `mids`. Set `n` to how many there are, and `last` to the last mid.
""",
        "starter": """mids = [7.7800, 7.7802, 7.7798, 7.7810]

n = 0
last = 0.0
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
A list is “item 0, item 1, item 2.” A **dict** (dictionary) is “this **name** maps to this **value**.” Curly braces, a colon between key and value, commas between pairs:

```
fill = {"px": 100.0, "sz": 2.0}
```

Keys here are strings. Read one field with square brackets, same idea as a list, but you use the key instead of a position: `fill["px"]` is `100.0`.

Write a field the same way — including a **new** key that was not there at the start:

```
fill["notional"] = fill["px"] * fill["sz"]
```

After that line, `fill["notional"]` exists.

The editor has a `quote` dict with bid and ask. Add a `mid` key: the average of those two fields.
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
        "goal": "for, indent, range, a return path.",
        "lesson": """
A **for** loop repeats a block. The next line must be indented **four spaces**. That indent is syntax: it is how Python knows what belongs in the loop.

Walk every value. Here `x` is a **new name** that takes each item in turn:

```
pxs = [10.0, 10.5, 9.5]
for x in pxs:
    last = x
```

After the loop, `last` is `9.5`. That form does not give you the **position**. When you need yesterday *and* today, you need indices.

**`range`** builds a sequence of integers.

- `range(4)` is 0, 1, 2, 3. It **starts at 0** and **stops before 4**. The number you pass is *not* itself included.
- `range(len(pxs))` is every valid index. Three prices → 0, 1, 2.
- `range(start, stop)` starts at `start` and still **stops before** `stop`. `range(1, 4)` is 1, 2, 3.

Index 0 has no previous bar, so a loop that compares to yesterday starts at 1. `append` (session 4) collects results. Dollar change:

```
deltas = []
for i in range(1, len(pxs)):
    change = pxs[i] - pxs[i - 1]
    deltas.append(change)
# deltas is [0.5, -1.0]
```

A **simple return** is not the dollar change. It is today’s mid **divided by** yesterday’s mid, **minus 1**. Four mids give **three** returns. Fill `rets` for the `mids` in the editor.
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
        "title": "Functions: mid and spread",
        "goal": "def, parameters, return, reuse.",
        "lesson": """
A **function** is a named recipe you can run more than once. You **define** it with `def`, then **call** it with parentheses.

```
def notional(qty, px):
    return qty * px
```

What each piece is:

- `def` starts the definition
- `notional` is the name you will call
- `(qty, px)` are **parameters** — placeholders. They get values when you call the function
- the next lines are indented four spaces: the **body**
- `return` hands a value back to whoever called it. After `return`, the function stops

Call it by passing **arguments** in the same order as the parameters:

```
n = notional(2.0, 7.78)    # qty is 2.0, px is 7.78, n is 15.56
```

If you leave out `return`, the function hands back **`None`**: Python’s “no value.” `None` is not 0 and not False; it is empty.

Write two functions the checks can call with *any* numbers: `mid(bid, ask)` is the average of the two prices; `spread(bid, ask)` is ask minus bid.
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
        "title": "Decisions: inventory",
        "goal": "if / elif / else inside a function.",
        "lesson": """
**if** runs a block only when a boolean is True. **elif** is “else if”: try this only when the previous tests failed. **else** runs when none of them matched. Indent the body four spaces, same rule as `for` and `def`.

Only one branch runs. You can also write two separate `if`s and a final `return`; do not leave a path that returns nothing.

```
def width_label(spread):
    if spread > 0.01:
        return "wide"
    if spread < 0.0001:
        return "tight"
    return "ok"
```

`width_label(0.02)` is `"wide"`. `width_label(0.00005)` is `"tight"`. `width_label(0.0004)` is `"ok"`.

Positive **inventory** is a long — you want to **sell**. Negative is a short — you want to **buy**. Zero is **flat**. Put that decision in `side(inventory)` so the checks can try several inventories. Return `"sell"`, `"buy"`, or `"flat"`.
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
        "title": "Indexing: lookback, not lookahead",
        "goal": "Slices. History is behind you.",
        "lesson": """
`sizes[i]` is one item. A **slice** is several items: `sizes[a:b]`.

Same exclusive-end rule as `range`: it starts at index `a` and **stops before** `b`.

```
sizes = [2.0, 1.0, 4.0, 3.0, 8.0]
sizes[1:3]   # [1.0, 4.0]  — index 1 and 2, not 3
sizes[:2]    # [2.0, 1.0]  — from the start, stop before 2
sizes[2:]    # [4.0, 3.0, 8.0] — from 2 through the end
sizes[-2:]   # [3.0, 8.0]  — the last two
```

At decision time, “now” is the last index. History is **behind** you. You must **not** pull a future bar: there is no `sizes[i+1]` when `i` is now. If `n` equals the length of the list, a “last n” slice is the whole list.

Write `lookback(mids, n)` returning the last `n` mids, **including** the current last print.
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
        "goal": "A list of dicts. Loop and collect.",
        "lesson": """
A real log is a **list of dicts** — one dict per timestamp:

```
fills = [
    {"px": 1.0, "sz": 2.0},
    {"px": 1.1, "sz": 0.5},
]
```

`fills[0]` is the first dict. `fills[0]["sz"]` is that fill’s size. To collect one field from every row, start an empty list and `append` inside a `for` (sessions 4–6):

```
def sizes_of(fills):
    out = []
    for f in fills:
        out.append(f["sz"])
    return out
# sizes_of(fills) is [2.0, 0.5]
```

Each round, `f` is one dict. You may later see this one-liner, which means the same loop: `[f["sz"] for f in fills]`. That is a **list comprehension**. Either form is legal.

The editor wants **asks**, not sizes. Write `asks_of(book)` returning every `ask`, in order.
""",
        "starter": """def asks_of(book):
    return []
""",
        "solution": """def asks_of(book):
    asks = []
    for q in book:
        asks.append(q["ask"])
    return asks
""",
        "tests": checks("""
    fn = need("asks_of")
    book = [{"bid": 1.0, "ask": 1.1}, {"bid": 1.0, "ask": 1.25}]
    check("asks", lambda: fn(book) == [1.1, 1.25] or (_ for _ in ()).throw(AssertionError("return each quote's ask, in order")))
"""),
    },
    {
        "title": "Numpy: prices as arrays",
        "goal": "import, arrays, vectorised returns.",
        "lesson": """
A **library** is code someone else wrote. **`import`** loads it. `as np` is a short nickname so you type `np` instead of `numpy`:

```
import numpy as np
```

This page already has numpy. You still write the import.

**NumPy** stores a grid of numbers of the same type. `np.array([2.0, 1.0, 4.0])` turns a list into a 1-D **array** (a time series). Indexing and slicing work like lists: `a[0]`, `a[-1]`, `a[1:]`, `a[:-1]`.

The gain: arithmetic applies to **every** element at once. No Python `for` required.

```
asks = np.array([1.10, 1.12, 1.09])
bids = np.array([1.00, 1.01, 1.00])
wides = asks - bids
# wides is [0.10, 0.11, 0.09]
```

`a[1:]` is every item except the first. `a[:-1]` is every item except the last. Same length, paired in order.

A 2-D array is a table (rows = time, columns = features). A 3-D array is already the shape of a tiny **tensor** (batch × time × features) that deep nets eat. You do not need those shapes here.

Simple returns are today’s mid over yesterday’s, minus 1 — the session-6 idea, now without a loop. Set `rets` from the `mids` array in the editor. Four mids → three returns.
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
    def _len():
        rets = nums(need("rets"), "rets should be three numbers")
        if len(rets) != 3:
            raise AssertionError("four mids → three returns")
    def _first():
        rets = nums(need("rets"), "rets should be three numbers")
        near(rets[0], 0.01, "first return 101/100 - 1", 1e-12)
    def _last():
        rets = nums(need("rets"), "rets should be three numbers")
        near(rets[-1], 0.03, "last return 103/100 - 1", 1e-12)
    check("len", _len)
    check("first", _first)
    check("last", _last)
"""),
    },
    {
        "title": "Causal EWMA",
        "goal": "Write into an array. Never look ahead.",
        "lesson": """
You can **write** into an array slot: `y[i] = ...`. `np.zeros(n)` is `n` zeros to fill. `np.array(x, dtype=float)` copies `x` as decimals (`dtype=float` means “use floats,” not integers). `len(x)` still works.

A **causal** running total uses only the past and now — never `x[i+1]`. Seed `y[0]`, then loop from 1:

```
def running_sum(x):
    x = np.array(x, dtype=float)
    y = np.zeros(len(x))
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = y[i - 1] + x[i]
    return y
# running_sum([1.0, 2.0, 3.0]) is [1.0, 3.0, 6.0]
```

If you used `x[i+1]` here, you would leak the future — the same crime as a leaky backtest.

An **EWMA** (exponentially weighted moving average) is the same causal shape, but today is a **blend**, not a sum. Today’s smoother is `alpha` times the new tick, plus `(1 - alpha)` times yesterday’s smoother. Seed with `y[0] = x[0]`.

Example by hand: `x = [1.0, 2.0]`, `alpha = 0.5` → `y[0] = 1.0`, `y[1] = 0.5 * 2.0 + 0.5 * 1.0 = 1.5`.

Write `ewma(x, alpha)` returning an array the same length as `x`. Changing the last tick must not change earlier `y`.
""",
        "starter": """import numpy as np

def ewma(x, alpha):
    x = np.array(x, dtype=float)
    y = np.zeros(len(x))
    return y
""",
        "solution": """import numpy as np

def ewma(x, alpha):
    x = np.array(x, dtype=float)
    y = np.zeros(len(x))
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = alpha * x[i] + (1 - alpha) * y[i - 1]
    return y
""",
        "tests": checks("""
    def _y():
        fn = need("ewma")
        return nums(fn(np.array([1.0, 2.0, 3.0]), 0.5), "ewma should return an array the same length as x")
    def _first():
        y = _y()
        near(y[0], 1.0, "y[0] must equal x[0]", 1e-12)
    def _step():
        y = _y()
        near(y[1], 1.5, "y[1] = 0.5*2 + 0.5*1", 1e-12)
    def _causal():
        fn = need("ewma")
        y = nums(fn(np.array([1.0, 2.0, 3.0]), 0.5), "ewma should return an array")
        y2 = nums(fn(np.array([1.0, 2.0, 99.0]), 0.5), "ewma should return an array")
        near(y[1], y2[1], "changing the last tick must not change earlier y", 1e-12)
    check("first", _first)
    check("step", _step)
    check("causal", _causal)
"""),
    },
    {
        "title": "Pandas: a series with time",
        "goal": "Series, .iloc, last close.",
        "lesson": """
**pandas** is another library. Import it the same way as numpy, with a short name `pd`:

```
import pandas as pd
```

A **Series** is one column with labels (often timestamps). A **DataFrame** is several columns — next sessions.

```
sz = pd.Series([2.0, 1.0, 4.0, 3.0])
```

A **method** is a function attached to an object, with a dot, like `list.append`. pandas uses two ways to pick a row:

- `.iloc[i]` — by **position**. `0` is first, `-1` is last. Same idea as `sizes[-1]`
- `.loc[label]` — by the **index label**. Mixing `.loc` and `.iloc` is a classic leak

```
first = sz.iloc[0]    # 2.0
```

The editor has a `close` series. Set `last` to the last close using `.iloc`.
""",
        "starter": """import pandas as pd

close = pd.Series([100.0, 101.5, 99.0, 102.0])
last = 0.0
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
        "goal": "pct_change, shift, NaN, chaining.",
        "lesson": """
`.pct_change()` is pandas for the simple return you wrote by hand: each value over the previous one, minus 1. The first row has no previous bar, so it is **NaN** (“not a number”) — missing, not zero.

`.shift(1)` moves values **forward** in the index: yesterday’s number sits on today’s row. That is a **feature** you were allowed to know at today’s open.

`.shift(-1)` pulls **tomorrow** onto today. That is a **label**, not a feature. Train on it as if it were known and the model is cheating.

A missing cell is **NaN**. `pd.isna(value)` is True when that value is missing.

**Chaining:** `a.b().c()` means do `b`, then `c` on the result. Read left to right.

On closes `[100, 110, 132]`, `.pct_change()` is missing, +10%, +20%. Lagging that series by one bar puts **yesterday’s return** on today’s row, so the last value becomes +10%, not +20%. Early rows stay NaN.

Write `lagged_ret(close)`: the simple return, then lagged one bar — a feature, not a label.
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
    def _out():
        fn = need("lagged_ret")
        close = pd.Series([100.0, 110.0, 132.0])
        return pd.Series(fn(close))
    def _early():
        out = _out()
        if not (bool(pd.isna(out.iloc[0])) or bool(pd.isna(out.iloc[1]))):
            raise AssertionError("early rows should be NaN after pct_change and a lag")
    def _past():
        out = _out()
        near(out.iloc[-1], 0.10, "last feature should be the previous bar's 10% return, not 132/110-1")
    check("nan early", _early)
    check("no future", _past)
"""),
    },
    {
        "title": "A feature table",
        "goal": "DataFrame columns the model will see.",
        "lesson": """
A **DataFrame** is a table. Build one from a dict whose values are columns (lists of the same length):

```
fills = pd.DataFrame({
    "px": [100.0, 101.0, 99.0],
    "sz": [2.0, 1.0, 4.0],
})
```

`fills["px"]` is a Series — one column. Adding a column looks like adding a dict key (session 5):

```
fills["notional"] = fills["px"] * fills["sz"]
```

pandas does that arithmetic **row by row**.

A model wants one row per decision time, columns = features known at that time. Never put the thing you are predicting in those feature columns unless you are building a **label** on purpose, and name it as such.

The editor has `df` with `bid` and `ask`. Add three columns: `mid` (average of bid and ask), `spread` (ask minus bid), and `ret_lag` (the session-14 feature: lagged simple return of `mid`).
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
        "goal": "Boolean arrays. & not and.",
        "lesson": """
Compare an **array** to a number and you get an array of True/False — one per row. That is a **mask**. Use it to keep rows: `spreads[wide]` is only the rows where `wide` is True.

On ordinary booleans you used `and` / `or` / `not` (session 3). Those do **not** work element-by-element on arrays. For arrays:

- `&` is and
- `|` is or
- `~` is not

You need parentheses around each comparison, because `&` binds tighter than `>=`:

```
spreads = np.array([0.0002, 0.02, 0.005])
band = (spreads >= 0.001) & (spreads < 0.01)
# band is [False, False, True]
```

Tokyo morning is hour 0, 1, …, 7. Hour 8 is London, not Tokyo. Write `asia_mask(hour)` returning a boolean array: True when the hour is in that Tokyo window, False otherwise.
""",
        "starter": """import numpy as np

def asia_mask(hour):
    hour = np.array(hour)
    return hour == 0
""",
        "solution": """import numpy as np

def asia_mask(hour):
    hour = np.array(hour)
    return (hour >= 0) & (hour < 8)
""",
        "tests": checks("""
    def _mask():
        fn = need("asia_mask")
        h = np.array([0, 7, 8, 15, 3])
        m = np.array(fn(h))
        if len(m) != len(h):
            raise AssertionError("mask length follows hour")
        return m
    def _tokyo():
        m = _mask()
        if not (bool(m[0]) and bool(m[1]) and bool(m[4])):
            raise AssertionError("0, 7, 3 should be True")
    def _london():
        m = _mask()
        if bool(m[2]) or bool(m[3]):
            raise AssertionError("8 and 15 should be False")
    check("shape", lambda: _mask())
    check("tokyo", _tokyo)
    check("london", _london)
"""),
    },
    {
        "title": "A linear fit in numpy",
        "goal": "2-D arrays, lstsq, @, train then test.",
        "lesson": """
A **linear model** predicts `y ≈ X w`. NumPy solves for `w` with least squares. This is the same idea as a one-layer net without an activation.

A **2-D array** is a list of rows. Each inner list is one row. Column 0 is often an **intercept** (all ones). Column 1 is a feature.

```
X = np.array([
    [1.0, 0.0],
    [1.0, 1.0],
    [1.0, 2.0],
])
y = np.array([1.0, 3.0, 5.0])
w = np.linalg.lstsq(X, y, rcond=None)[0]
fit = X @ w
```

`np.linalg.lstsq` returns several results; `[0]` keeps the weights. `rcond=None` is a setting it expects — copy it. `@` is **matrix multiply**.

That snippet fits and scores the **same** `X` (in-sample). Shipping a model means: fit on **train**, predict on **test**. Returning `y_train` is cheating.

Write `fit_predict(X_train, y_train, X_test)`: learn `w` from train, return `X_test @ w`. The checks use a line `y = 2 * x1` and ask for predictions at new `x1`.
""",
        "starter": """import numpy as np

def fit_predict(X_train, y_train, X_test):
    return y_train
""",
        "solution": """import numpy as np

def fit_predict(X_train, y_train, X_test):
    X_train = np.array(X_train, dtype=float)
    y_train = np.array(y_train, dtype=float)
    X_test = np.array(X_test, dtype=float)
    w = np.linalg.lstsq(X_train, y_train, rcond=None)[0]
    return X_test @ w
""",
        "tests": checks("""
    def _pred():
        fn = need("fit_predict")
        Xtr = np.array([[1.0, 0.0], [1.0, 1.0], [1.0, 2.0]])
        ytr = np.array([0.0, 2.0, 4.0])
        Xte = np.array([[1.0, 3.0], [1.0, 4.0]])
        return nums(fn(Xtr, ytr, Xte), "return predictions for X_test")
    def _len():
        pred = _pred()
        if len(pred) != 2:
            raise AssertionError("predict on X_test (2 rows), not on y_train")
    def _fit():
        pred = _pred()
        near(pred[0], 6.0, "the line is y = 2 * x1; test x1=3 → 6")
        near(pred[1], 8.0, "test x1=4 → 8")
    check("test length", _len)
    check("oot", _fit)
"""),
    },
    {
        "title": "Time split, never shuffle",
        "goal": "int, two return values, np.arange.",
        "lesson": """
In images you shuffle rows. In markets you **do not**. Tomorrow is not allowed in today’s training fold.

`int(...)` drops the decimal toward zero: `int(3.9)` is 3. **`np.arange`** is numpy’s `range`: it returns an **array**. `np.arange(0, 4)` is `0,1,2,3`. Same exclusive-end rule.

A function can **return two values**. Write them with a comma. The caller unpacks with a comma too:

```
def head_tail(n, k):
    head = np.arange(0, k)
    tail = np.arange(k, n)
    return head, tail

a, b = head_tail(10, 4)
# a is 0..3, b is 4..9
```

Walk-forward is this idea with more folds. Purged CV (the coding mock) adds a gap so label windows do not overlap the cut.

Write `time_split(n, train_frac)`: cut at `int(n * train_frac)`, train indices before the cut, test indices from the cut to `n`. Every train index must be `<` every test index.
""",
        "starter": """import numpy as np

def time_split(n, train_frac):
    return np.arange(n), np.arange(n)
""",
        "solution": """import numpy as np

def time_split(n, train_frac):
    cut = int(n * train_frac)
    train = np.arange(0, cut)
    test = np.arange(cut, n)
    return train, test
""",
        "tests": checks("""
    def _split():
        fn = need("time_split")
        tr, te = fn(10, 0.7)
        return nums(tr, "train should be an array of indices"), nums(te, "test should be an array of indices")
    def _cover():
        tr, te = _split()
        if len(tr) + len(te) != 10:
            raise AssertionError("train and test should partition 0..n-1")
    def _order():
        tr, te = _split()
        if len(te) == 0 or len(tr) == 0:
            return
        if max(tr) >= min(te):
            raise AssertionError("every train index must be before test")
    def _frac():
        tr, te = _split()
        if len(tr) != 7 or len(te) != 3:
            raise AssertionError("int(10*0.7) = 7 train, 3 test")
    check("cover", _cover)
    check("order", _order)
    check("frac", _frac)
"""),
    },
    {
        "title": "Metrics that lie",
        "goal": "** power, np.mean, np.sign.",
        "lesson": """
`**` is **power**: `3 ** 2` is 9. `np.mean(a)` is the average of array `a`. `float(...)` turns the result into an ordinary Python number.

```
err = np.array([0.0, 2.0, -2.0])
mean_sq = float(np.mean(err ** 2))   # (0 + 4 + 4) / 3
```

`np.sign(3)` is `1.0`, `np.sign(-2)` is `-1.0`, `np.sign(0)` is `0.0`. Comparing two arrays with `==` is element-wise (session 16). `np.mean` treats True as 1 and False as 0, so the mean of a boolean array is a fraction.

**MSE** is the mean squared gap between a prediction and `y`. **Hit-rate** is how often `sign(pred)` matches `sign(y)`. Both can look great while a trading rule loses money: they ignore size, spread, and fill. A toxicity model with a pretty **AUC** can still bleed markout vs fill.

Write `mse(pred, y)` and `hit_rate(pred, y)`.
""",
        "starter": """import numpy as np

def mse(pred, y):
    return 0.0


def hit_rate(pred, y):
    return 0.0
""",
        "solution": """import numpy as np

def mse(pred, y):
    pred = np.array(pred, dtype=float)
    y = np.array(y, dtype=float)
    return float(np.mean((pred - y) ** 2))


def hit_rate(pred, y):
    pred = np.array(pred, dtype=float)
    y = np.array(y, dtype=float)
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
        "goal": "Glue: features, split, fit, test MSE.",
        "lesson": """
Glue what you already wrote. Do not shuffle time. A neural net is the same skeleton with `pred = f(X, weights)` instead of `X @ w` — leakage rules do not change because the model got deeper.

**Align feature and label.** Five toy returns `[r0, r1, r2, r3, r4]`. At the row whose label is `r3` (the next return), the feature you were allowed to know is `r2` (the previous return). So the feature series is `r1,r2,r3` and the label series is `r2,r3,r4` if you also need a lag at the start — equivalently, drop the first two: labels `ret[2:]`, features `ret[1:-1]`. They must be the same length.

**Intercept.** `np.ones(n)` is `n` ones. `np.column_stack([a, b])` glues columns:

```
a = np.array([1.0, 1.0, 1.0])
b = np.array([0.1, -0.2, 0.0])
X = np.column_stack([a, b])
# 3 rows, 2 columns
```

**Split, fit, score.** Cut at 70% of rows (`int(n * 0.7)`). Fit `w` on the earlier block only. Report **train** MSE and **test** MSE (session 19). Test MSE is the claim; train MSE is debugging.

Write `pipeline(mids)` returning `{"train_mse": ..., "test_mse": ...}`. Use lag-1 return as the one feature, next return as `y`, intercept column, 70% time split, `np.linalg.lstsq`.
""",
        "starter": """import numpy as np

def pipeline(mids):
    return {"train_mse": 0.0, "test_mse": 0.0}
""",
        "solution": """import numpy as np

def pipeline(mids):
    mids = np.array(mids, dtype=float)
    ret = np.zeros(len(mids))
    ret[1:] = mids[1:] / mids[:-1] - 1.0
    y = ret[2:]
    x1 = ret[1:-1]
    X = np.column_stack([np.ones(len(x1)), x1])
    cut = int(len(X) * 0.7)
    X_train, X_test = X[:cut], X[cut:]
    y_train, y_test = y[:cut], y[cut:]
    w = np.linalg.lstsq(X_train, y_train, rcond=None)[0]
    train_mse = float(np.mean((X_train @ w - y_train) ** 2))
    test_mse = float(np.mean((X_test @ w - y_test) ** 2))
    return {"train_mse": train_mse, "test_mse": test_mse}
""",
        "tests": checks("""
    def _pipe():
        fn = need("pipeline")
        mids = np.array([100.0, 101.0, 100.5, 102.0, 101.0, 103.0, 102.5, 104.0] * 10, dtype=float)
        return fn(mids), mids
    def _ref(xs):
        xs = np.array(xs, dtype=float)
        ret = np.zeros(len(xs))
        ret[1:] = xs[1:] / xs[:-1] - 1.0
        y = ret[2:]
        x1 = ret[1:-1]
        X = np.column_stack([np.ones(len(x1)), x1])
        cut = int(len(X) * 0.7)
        w = np.linalg.lstsq(X[:cut], y[:cut], rcond=None)[0]
        def mse(Xa, ya):
            return float(np.mean((Xa @ w - ya) ** 2))
        return mse(X[:cut], y[:cut]), mse(X[cut:], y[cut:])
    def _keys():
        out, _mids = _pipe()
        if not (isinstance(out, dict) and {"train_mse", "test_mse"} <= set(out)):
            raise AssertionError("return a dict with train_mse and test_mse")
    def _train():
        out, mids = _pipe()
        want_tr, _want_te = _ref(mids)
        near(out["train_mse"], want_tr, "train_mse should match lag-1 return + intercept, 70% time split, lstsq", 1e-8)
    def _test():
        out, mids = _pipe()
        _want_tr, want_te = _ref(mids)
        near(out["test_mse"], want_te, "test_mse is scored on the later 30%, not shuffled, not in-sample", 1e-8)
    check("keys", _keys)
    check("train_mse", _train)
    check("test_mse", _test)
"""),
    },
]


assert len(SESSIONS) == 20, len(SESSIONS)

_BANNED = ("asarray", "empty_like", "zeros_like", "ones_like", "full_like")
for _s in SESSIONS:
    _blob = _s["lesson"] + _s["starter"] + _s["solution"] + _s["tests"]
    for _name in _BANNED:
        assert _name not in _blob, f"{_s['title']} still mentions {_name}"
