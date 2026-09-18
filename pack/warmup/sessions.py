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
        "goal": "Names, arithmetic, a bid/ask.",
        "lesson": """
Python stores a value under a **name**. The line `bid = 7.7800` means: remember `7.7800` as `bid`. That is **assignment**. One `=` is not “equals”; it is “put this in that name.”

A dealer’s quote is two numbers: **bid** (they buy) and **ask** (they sell). The **mid** is the average. The **spread** is ask minus bid.

Arithmetic:

- `+` add, `-` subtract, `*` multiply, `/` divide
- Parentheses `( )` change order: `(bid + ask) / 2` adds first, then divides
- `#` starts a **comment**. Python ignores the rest of that line. Comments are notes for you.

```
mid = (bid + ask) / 2
spread = ask - bid
```

You do not declare types. `7.7800` is already a decimal (a **float**).

The editor already has `bid` and `ask`. Assign `mid` and `spread` underneath.
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
**Strings** are text. Write them in quotes: `"USDCNH"` or `'USDCNH'` — both fine, pick one style and stay with it.

`len("USDCNH")` is 6: `len` counts characters. A **function call** is a name followed by parentheses. `len` is built in; you will write your own functions later.

Join text with `+` (both sides must be strings). A number is not a string until you wrap it:

```
pair = "USDCNH"
mid = 7.7802
line = pair + " mid=" + str(mid)
```

`str(mid)` turns the number into text. The other way: `float("7.78")` turns text into a number. `"7.78" + 1` is an error.

An **f-string** is a shorter way to drop a value into text. Put `f` before the quotes, then `{name}` inside:

```
line = f"{pair} mid={mid}"
```

Python replaces `{pair}` with the value of `pair`, and `{mid}` with the value of `mid`.

Build `line` so it contains the pair name and the mid (an f-string or `+` both pass).
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

A **comparison** produces a boolean:

```
bid < ask       # True if bid is smaller — a healthy market
bid > ask       # True if bid is larger — crossed, a bug
bid == ask      # True if they are exactly equal
```

Read `==` as “is equal to.” Two equals. One `=` still means assignment, and does not compare.

The other comparisons: `<=` less or equal, `>=` greater or equal, `!=` not equal.

Combine booleans:

- `and` — True only if both sides are True
- `or` — True if at least one side is True
- `not` — flips True to False and False to True

```
healthy = bid < ask
crossed = bid > ask
```

Set `healthy` and `crossed` from the quote in the editor.
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
mids = [7.7800, 7.7802, 7.7798]
```

`len(mids)` is 3 — `len` counts items, not characters, when the input is a list.

Each item has a **position** (an **index**). Counting starts at **zero**, not one:

```
index:    0        1        2
value:  7.7800   7.7802   7.7798
```

- `mids[0]` is the first item
- `mids[1]` is the second
- `mids[-1]` is the last item (`-1` always means “from the end”)

`[]` is an empty list: no items yet. `.append(value)` adds one item at the end:

```
rets = []
rets.append(0.01)
```

The dot means “use this list’s append.” Later you will see more **methods** — names after a dot that do work on that object.

In markets, the last print is “now”; earlier items are history.

Set `n` to the length of `mids`, and `last` to the last mid.
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
quote = {"bid": 7.7800, "ask": 7.7804, "bid_sz": 5.0}
```

Keys here are strings. Read one field with square brackets, same idea as a list, but you use the key instead of a position:

```
quote["bid"]
```

Write a field the same way — including a **new** key that was not there at the start:

```
quote["mid"] = (quote["bid"] + quote["ask"]) / 2
```

After that line, `quote["mid"]` exists. This is how one tick looks in Python before you put many ticks in a table.

Add `mid` into `quote`: the average of its bid and ask.
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

Walk every mid, one at a time. Here `x` is a **new name** that takes each value in turn:

```
for x in mids:
    last = x
```

After the loop, `last` is the last mid. That form does not give you the **position**. For a return you need two positions: yesterday and today.

**`range`** builds a sequence of integers.

- `range(4)` is 0, 1, 2, 3. It **starts at 0** and **stops before 4**. The number you pass is the count of values, and is *not* itself included.
- `range(len(mids))` is every valid index of `mids`. If there are 4 mids, that is 0, 1, 2, 3.
- `range(start, stop)` starts at `start` and still **stops before** `stop`. So `range(1, 4)` is 1, 2, 3.

A **simple return** from bar `i-1` to bar `i` is:

```
ret = mids[i] / mids[i - 1] - 1
```

There is no previous bar at index 0, so the loop must start at 1. `append` (session 4) collects each return:

```
rets = []
for i in range(1, len(mids)):
    ret = mids[i] / mids[i - 1] - 1
    rets.append(ret)
```

Read that as: “for each index i from 1 up to, but not including, the length of mids…”

Four mids give **three** returns. Fill `rets` that way.
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
def mid(bid, ask):
    return (bid + ask) / 2
```

What each piece is:

- `def` starts the definition
- `mid` is the name you will call
- `(bid, ask)` are **parameters** — placeholders. They are not the live quote yet. They get values when you call the function
- the next lines are indented four spaces: the **body**
- `return` hands a value back to whoever called it. After `return`, the function stops

Call it by passing **arguments** in the same order as the parameters:

```
m = mid(7.7800, 7.7804)    # bid is 7.7800, ask is 7.7804, m is 7.7802
```

If you leave out `return`, the function hands back **`None`**: Python’s “no value.” `None` is not 0 and not False; it is empty.

Write two functions: `mid(bid, ask)` and `spread(bid, ask)` (`ask - bid`). The checks will call them with numbers of their own — they must work for any bid and ask, not only one quote.
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

```
if inventory > 0:
    action = "sell"
elif inventory < 0:
    action = "buy"
else:
    action = "flat"
```

Only one of those three branches runs. You can also write two separate `if`s and a final `return`; do not leave a path that returns nothing.

Put the decision **inside a function** (the previous session) so the checks can try several inventories:

```
def side(inventory):
    if inventory > 0:
        return "sell"
    if inventory < 0:
        return "buy"
    return "flat"
```

Positive inventory is a long — you want to sell. Negative is a short — you want to buy. Zero is flat.

Write `side(inventory)` returning `"sell"`, `"buy"`, or `"flat"`.
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
`mids[i]` is one item. A **slice** is several items: `mids[a:b]`.

Same exclusive-end rule as `range`: it starts at index `a` and **stops before** `b`. `mids[1:3]` is index 1 and 2, not 3.

You may omit a side:

- `mids[:2]` — from the start, stop before 2
- `mids[2:]` — from 2 through the **end**
- `mids[-3:]` — the last three items (from 3-before-the-end through the end)

At decision time, “now” is the last index. You may use `mids[-n:]` (includes now). You must **not** use a future bar: there is no `mids[i+1]` when `i` is now.

```
def lookback(mids, n):
    return mids[-n:]
```

If `n` equals `len(mids)`, `mids[-n:]` is the whole list.

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
        "goal": "A list of dicts. Loop and collect.",
        "lesson": """
A real log is a **list of dicts** — one dict per timestamp:

```
book = [
    {"bid": 1.0, "ask": 1.1},
    {"bid": 1.0, "ask": 1.2},
]
```

`book[0]` is the first dict. `book[0]["ask"]` is that quote’s ask. To collect every ask, start an empty list and `append` inside a `for` (sessions 4–6):

```
def asks_of(book):
    asks = []
    for q in book:
        asks.append(q["ask"])
    return asks
```

Each round, `q` is one dict. You may later see this one-liner, which means the same loop:

```
asks = [q["ask"] for q in book]
```

That is a **list comprehension**. Either form passes. Write `asks_of(book)` returning every ask, in order.
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

**NumPy** stores a grid of numbers of the same type. `np.array([100.0, 101.0, 100.0])` turns a list into a 1-D **array** (a time series). Indexing and slicing work like lists: `mids[0]`, `mids[-1]`, `mids[1:]`, `mids[:-1]`.

The gain: arithmetic applies to **every** element at once. No Python `for` required.

```
mids = np.array([100.0, 101.0, 100.0])
rets = mids[1:] / mids[:-1] - 1
```

`mids[1:]` is every print except the first. `mids[:-1]` is every print except the last. Same length, paired: today’s mid over yesterday’s mid, minus 1. That is the session-6 return path, vectorised.

A 2-D array is a table (rows = time, columns = features). A 3-D array is already the shape of a tiny **tensor** (batch × time × features) that deep nets eat. You do not need those shapes in this session.

Set `rets` from `mids` that way. Four mids → three returns.
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
        "goal": "Write into an array. Never look ahead.",
        "lesson": """
An **EWMA** (exponentially weighted moving average) is a smoother. Today’s smoother is a blend of the new tick and yesterday’s smoother. `*` multiplies (session 1):

```
y[0] = x[0]
y[t] = alpha * x[t] + (1 - alpha) * y[t - 1]
```

Example: `x = [1.0, 2.0]`, `alpha = 0.5`. Then `y[0] = 1.0` and `y[1] = 0.5 * 2.0 + 0.5 * 1.0 = 1.5`.

**Causal** means `y[t]` uses only `x[0]` … `x[t]`. If you use `x[t+1]`, you leak the future — the same crime as a leaky backtest.

Arrays are writable. `np.zeros(n)` is an array of `n` zeros you then fill. `np.array(x, dtype=float)` copies `x` as decimals (`dtype=float` means “use floats,” not integers). `len(x)` still works.

```
def ewma(x, alpha):
    x = np.array(x, dtype=float)
    y = np.zeros(len(x))
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = alpha * x[i] + (1 - alpha) * y[i - 1]
    return y
```

That is the session-6 `range(1, len(...))` pattern, writing into `y[i]` instead of `append`.

Write `ewma(x, alpha)` returning an array the same length as `x`.
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
        "goal": "Series, .iloc, last close.",
        "lesson": """
**pandas** is another library. Import it the same way as numpy, with a short name `pd`:

```
import pandas as pd
```

A **Series** is one column with labels (often timestamps). A **DataFrame** is several columns — next sessions.

```
close = pd.Series([100.0, 101.5, 99.0, 102.0])
```

A **method** is a function attached to an object, with a dot, like `list.append`. pandas uses two ways to pick a row:

- `.iloc[i]` — by **position**. `0` is first, `-1` is last. Same idea as `mids[-1]`
- `.loc[label]` — by the **index label**. Mixing `.loc` and `.iloc` is a classic leak

```
last = close.iloc[-1]
```

Set `last` to the last close using `.iloc`.
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

**Chaining:** `close.pct_change().shift(1)` means: first take returns, then lag those returns by one bar. Read left to right. Each method returns a Series, so the next method can run on it.

```
def lagged_ret(close):
    return close.pct_change().shift(1)
```

On closes `[100, 110, 132]`: returns are “missing, +10%, +20%.” After `shift(1)` the last value is **+10%** (yesterday’s return), not +20%. Early rows stay NaN.

Write `lagged_ret(close)`: simple return lagged by one bar (a feature).
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
A **DataFrame** is a table. Build one from a dict whose values are columns (lists of the same length):

```
df = pd.DataFrame({
    "bid": [100.0, 100.5, 101.0],
    "ask": [100.2, 100.7, 101.2],
})
```

`df["bid"]` is a Series — one column. Adding a column looks like adding a dict key (session 5):

```
df["mid"] = (df["bid"] + df["ask"]) / 2
df["spread"] = df["ask"] - df["bid"]
df["ret_lag"] = df["mid"].pct_change().shift(1)
```

pandas does that arithmetic **row by row**. `ret_lag` is the session-14 feature: a return you were allowed to know.

A model wants one row per decision time, columns = features known at that time. Never put the thing you are predicting in those feature columns unless you are building a **label** on purpose, and name it as such.

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
        "goal": "Boolean arrays. & not and.",
        "lesson": """
Compare an **array** to a number and you get an array of True/False — one per row. That is a **mask**. Use it to keep a session: `mids[asia]` is only the rows where `asia` is True.

On ordinary booleans you used `and` / `or` / `not` (session 3). Those do **not** work element-by-element on arrays. For arrays:

- `&` is and
- `|` is or
- `~` is not

You need parentheses around each comparison, because `&` binds tighter than `>=`:

```
asia = (hour >= 0) & (hour < 8)
```

`>=` is “greater or equal” (session 3). Hour `8` is London, not Tokyo, so it must be False. Hour `0` and `7` are True.

```
def asia_mask(hour):
    hour = np.array(hour)
    return (hour >= 0) & (hour < 8)
```

Write `asia_mask(hour)` returning a boolean array: True when `0 <= hour < 8`.
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
        "goal": "2-D arrays, lstsq, @, train then test.",
        "lesson": """
A **linear model** predicts `y ≈ X w`. NumPy solves for `w` with least squares. This is the same idea as a one-layer net without an activation.

A **2-D array** is a list of rows. Each inner list is one row:

```
X_train = np.array([
    [1.0, 0.0],
    [1.0, 1.0],
    [1.0, 2.0],
])
```

Here column 0 is an **intercept** (all ones). Column 1 is the feature. `y_train` is one number per row.

`np.linalg.lstsq(X, y, rcond=None)` fits `w`. It returns several results; we need the **first**. `[0]` after a call picks item 0 (session 4):

```
w = np.linalg.lstsq(X_train, y_train, rcond=None)[0]
```

`rcond=None` is a setting lstsq expects — copy it.

`@` is **matrix multiply**: `X_test @ w` is the prediction on new rows. Fit on train, predict on **test**. Returning `y_train` is cheating.

```
def fit_predict(X_train, y_train, X_test):
    X_train = np.array(X_train, dtype=float)
    y_train = np.array(y_train, dtype=float)
    X_test = np.array(X_test, dtype=float)
    w = np.linalg.lstsq(X_train, y_train, rcond=None)[0]
    return X_test @ w
```

Write that function. The checks use a line `y = 2 * x1` and ask you to predict at new `x1`.
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
        "goal": "int, two return values, np.arange.",
        "lesson": """
In images you shuffle rows. In markets you **do not**. Tomorrow is not allowed in today’s training fold.

`int(n * 0.7)` multiplies, then **`int(...)`** drops the decimal toward zero. `int(10 * 0.7)` is `int(7.0)` which is 7. That cut is the first test index: train is `0 .. cut-1`, test is `cut .. n-1`.

`range` built integers we looped over. **`np.arange`** is the numpy version: it returns an **array**. `np.arange(0, 7)` is `0,1,2,3,4,5,6`. `np.arange(7, 10)` is `7,8,9`. Same exclusive-end rule.

A function can **return two values**. Write them with a comma. The caller unpacks with a comma too:

```
def time_split(n, train_frac):
    cut = int(n * train_frac)
    train = np.arange(0, cut)
    test = np.arange(cut, n)
    return train, test

tr, te = time_split(10, 0.7)
```

Walk-forward is this idea with more folds. Purged CV (the coding mock) adds a gap so label windows do not overlap the cut.

Write `time_split(n, train_frac)` returning `(train_idx, test_idx)`. Every train index must be `<` every test index.
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
        "goal": "** power, np.mean, np.sign.",
        "lesson": """
**MSE** (mean squared error) for regression: average of squared gaps. `**` is **power**: `3 ** 2` is 9. So `(pred - y) ** 2` squares each gap.

`np.mean(a)` is the average of array `a`. `float(...)` turns the result into an ordinary Python number (numpy likes its own numeric types).

```
def mse(pred, y):
    pred = np.array(pred, dtype=float)
    y = np.array(y, dtype=float)
    return float(np.mean((pred - y) ** 2))
```

**Hit-rate:** how often the **sign** of the prediction matches the sign of `y`. `np.sign(3)` is `1.0`, `np.sign(-2)` is `-1.0`, `np.sign(0)` is `0.0`. Comparing two arrays with `==` is element-wise (session 16): a boolean array. Then `np.mean` treats True as 1 and False as 0, so the mean is the fraction of hits.

```
def hit_rate(pred, y):
    pred = np.array(pred, dtype=float)
    y = np.array(y, dtype=float)
    return float(np.mean(np.sign(pred) == np.sign(y)))
```

Both numbers can look great while a trading rule loses money: they ignore size, spread, and fill. A toxicity model with a pretty **AUC** can still bleed markout vs fill. Implement both so you can refuse to ship on either alone.

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
This is the skeleton of every later model, including a net. Type it from the recipe — do not shuffle time.

**1. Returns.** Same vectorised path as session 11. `ret[0]` stays 0 because there is no previous mid.

```
mids = np.array(mids, dtype=float)
ret = np.zeros(len(mids))
ret[1:] = mids[1:] / mids[:-1] - 1.0
```

**2. Feature and label.** At time `t` the feature is the **previous** return; the label is the **next** return. Align them by dropping the first two rows:

```
y = ret[2:]       # next return (label)
x1 = ret[1:-1]    # previous return (feature)
```

**3. Intercept.** `np.ones(n)` is `n` ones. `np.column_stack([a, b])` glues columns side by side into a 2-D `X`:

```
X = np.column_stack([np.ones(len(x1)), x1])
```

**4. Time split.** Session 18. `len(X)` is the number of rows (`X.shape[0]` is the same idea: `.shape` is rows then columns).

```
cut = int(len(X) * 0.7)
X_train, X_test = X[:cut], X[cut:]
y_train, y_test = y[:cut], y[cut:]
```

**5. Fit on train only. Score both.** Session 17 and 19:

```
w = np.linalg.lstsq(X_train, y_train, rcond=None)[0]
train_mse = float(np.mean((X_train @ w - y_train) ** 2))
test_mse = float(np.mean((X_test @ w - y_test) ** 2))
return {"train_mse": train_mse, "test_mse": test_mse}
```

A neural net is the same pipeline with `pred = f(X, weights)` instead of `X @ w`. The leakage rules do not change because the model got deeper.

Write `pipeline(mids)` returning that dict. In-sample MSE is for debugging, not for claiming skill.
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
        cut = int(len(X) * 0.7)
        w = np.linalg.lstsq(X[:cut], y[:cut], rcond=None)[0]
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
