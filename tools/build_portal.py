#!/usr/bin/env python3
"""Build a single self-contained portal.html from the public pack."""

from __future__ import annotations

import html
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack"
OUT = ROOT / "index.html"
KEY_CANDIDATE = "quantprep-candidate"
KEY_WARMUP = "quantprep-warmup"
KEY_SANDBOX = "quantprep-sandbox"

SECTIONS = [
    ("home", "Start", None, "Desk blotter"),
    ("jargon", "1 · Words", PACK / "jargon.md", "Learn the dialect"),
    ("seat", "2 · The seat", PACK / "seat.md", "What the job is"),
    ("briefing", "3 · Briefing", PACK / "briefing.md", "Industry, desks, rails"),
    ("landing", "90 days", PACK / "landing.md", "How you'd start — not a mock"),
    ("plan", "4 · Study plan", PACK / "study-plan.md", "14 days"),
    ("drills", "Drills", None, "Closed-book 5+5, then walk-in"),
    ("warmup", "Python", None, "20 sessions from zero"),
    ("sandbox", "Sandbox", None, "Type, run, see output"),
    ("ml", "5 · ML mock", PACK / "mocks" / "01-ml.md", "90 minutes"),
    ("dl", "6 · DL mock", PACK / "mocks" / "02-dl.md", "90 minutes"),
    ("coding", "7 · Coding", PACK / "mocks" / "03-coding.md", "In-page lab"),
    ("project", "8 · Project", PACK / "mocks" / "04-project.md", "Scenario, 90 min"),
    ("morning", "Morning of", PACK / "one-pager.md", "Interview day only"),
]


CODING_LAB = """
<div class="lab" id="coding-lab">
  <p class="kicker">In this browser</p>
  <h2>Lab</h2>
  <p class="lede">Type in <code>candidate.py</code>, then run the same tests the mock uses. First run downloads a Python runtime (numpy + pandas) into this tab; after that it is cached. Work is saved locally in the browser, not on a server.</p>
  <div class="lab-tabs">
    <button type="button" data-lab-tab="candidate" class="on">candidate.py</button>
    <button type="button" data-lab-tab="broken">broken_backtest.py</button>
    <button type="button" data-lab-tab="solutions">answer key</button>
  </div>
  <textarea class="lab-ed" id="lab-ed" spellcheck="false" autocomplete="off" autocapitalize="off" autocorrect="off" aria-label="candidate.py"></textarea>
  <div class="lab-bar">
    <button type="button" id="lab-run">Run tests</button>
    <button type="button" id="lab-reset">Reset stub</button>
    <span id="lab-status"></span>
  </div>
  <pre class="lab-out" id="lab-out" hidden></pre>
</div>
"""

WARMUP_HTML = """
<div class="warmup" id="warmup-lab">
  <p class="kicker">Twenty sessions · in this browser</p>
  <h1>Python warmup</h1>
  <p class="lede">From zero, aimed at people who will later sit a markets coding mock. Each session is a short lesson, a stub, and checks that run in the same Python as the lab. Work stays in this browser. Finish this before <a href="#coding" data-go="coding">7 · Coding</a> if you are new to the language. Scratch pad: <a href="#sandbox" data-go="sandbox">Sandbox</a>.</p>
  <ol class="wu-track" id="wu-track"></ol>
  <p class="wu-progress" id="wu-progress"></p>
  <p class="kicker" id="wu-kicker"></p>
  <h2 id="wu-title"></h2>
  <p class="lede" id="wu-goal"></p>
  <div class="wu-lesson" id="wu-lesson"></div>
  <textarea class="lab-ed" id="wu-ed" spellcheck="false" autocomplete="off" autocapitalize="off" autocorrect="off" aria-label="session editor"></textarea>
  <div class="lab-bar">
    <button type="button" id="wu-run">Run checks</button>
    <button type="button" id="wu-hint">Show answer</button>
    <button type="button" id="wu-reset">Reset stub</button>
    <button type="button" id="wu-next">Next session</button>
    <span id="wu-status"></span>
  </div>
  <pre class="lab-out" id="wu-out" hidden></pre>
</div>
"""

SANDBOX_HTML = """
<div class="sandbox" id="sandbox-lab">
  <p class="kicker">Scratch pad · in this browser</p>
  <h1>Sandbox</h1>
  <p class="lede">A blank Python file. Same runtime as the warmup and the lab — it runs in this tab, not on a server. First run may download a few megabytes; after that it is cached. Work stays in this browser.</p>
  <h2>How to see output</h2>
  <ol class="sb-guide">
    <li>Type in the editor. Click <strong>Run</strong>, or press Ctrl+Enter (Cmd+Enter on a Mac).</li>
    <li>The whole file runs from the top each time. Names do not carry over from the previous click unless they are still in the editor.</li>
    <li>To send text to the <strong>console</strong> below, call <code>print</code>. Quotes make a string: <code>print("hello")</code>. You can print several things, separated by commas: <code>print("mid", 7.78)</code>.</li>
    <li>A last line that is <em>just a value</em> (for example <code>1 + 1</code>) is also shown. A line that only assigns, like <code>x = 1</code>, stays silent — print <code>x</code> if you want to see it.</li>
    <li>If Python cannot run the file, the error appears in the same console. Change the editor and Run again.</li>
    <li><code>import numpy as np</code> and <code>import pandas as pd</code> work; both libraries are already in this page.</li>
  </ol>
  <textarea class="lab-ed" id="sb-ed" spellcheck="false" autocomplete="off" autocapitalize="off" autocorrect="off" aria-label="sandbox editor"></textarea>
  <div class="lab-bar">
    <button type="button" id="sb-run">Run</button>
    <button type="button" id="sb-reset">Reset starter</button>
    <button type="button" id="sb-clear">Clear console</button>
    <span id="sb-status"></span>
  </div>
  <p class="kicker">Console</p>
  <pre class="lab-out" id="sb-out">Output from print() will show here.</pre>
</div>
"""


def coding_files() -> dict[str, str]:
    folder = PACK / "mocks" / "coding"
    return {
        "candidate": (folder / "candidate.py").read_text(encoding="utf-8"),
        "solutions": (folder / "solutions.py").read_text(encoding="utf-8"),
        "broken": (folder / "broken_backtest.py").read_text(encoding="utf-8"),
        "tests": (folder / "test_coding.py").read_text(encoding="utf-8"),
    }


def inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def md_to_html(src: str) -> str:
    lines = src.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    in_ul = False
    in_ol = False
    in_p: list[str] = []

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def flush_p():
        if in_p:
            out.append("<p>" + inline(" ".join(in_p)) + "</p>")
            in_p.clear()

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        if stripped.startswith("```"):
            flush_p()
            close_lists()
            fence = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                fence.append(lines[i])
                i += 1
            out.append("<pre><code>" + html.escape("\n".join(fence)) + "</code></pre>")
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*-+", lines[i + 1]):
            flush_p()
            close_lists()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(cells)
                i += 1
            if len(rows) >= 2:
                header = rows[0]
                sep = rows[1]
                is_sep = all(re.sub(r"[\s:-]", "", c) == "" and "-" in c for c in sep)
                body = rows[2:] if is_sep else rows[1:]
                thead = "".join(f"<th>{inline(c)}</th>" for c in header)
                body_html = "".join(
                    "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body
                )
                out.append(f"<div class='table-wrap'><table><thead><tr>{thead}</tr></thead><tbody>{body_html}</tbody></table></div>")
            continue

        if stripped == "---":
            flush_p()
            close_lists()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("### "):
            flush_p()
            close_lists()
            out.append(f"<h3>{inline(stripped[4:])}</h3>")
            i += 1
            continue
        if stripped.startswith("## "):
            flush_p()
            close_lists()
            out.append(f"<h2>{inline(stripped[3:])}</h2>")
            i += 1
            continue
        if stripped.startswith("# "):
            flush_p()
            close_lists()
            out.append(f"<h1>{inline(stripped[2:])}</h1>")
            i += 1
            continue

        if stripped.startswith("> "):
            flush_p()
            close_lists()
            quote = [stripped[2:]]
            i += 1
            while i < len(lines) and lines[i].strip().startswith(">"):
                q = lines[i].strip()
                quote.append(q[2:] if q.startswith("> ") else q[1:].lstrip())
                i += 1
            out.append("<blockquote><p>" + "<br>".join(inline(q) for q in quote) + "</p></blockquote>")
            continue

        m_ul = re.match(r"^[-*] (.+)$", stripped)
        if m_ul:
            flush_p()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(m_ul.group(1))}</li>")
            i += 1
            continue

        m_ol = re.match(r"^(\d+)[.)] (.+)$", stripped)
        if m_ol:
            flush_p()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{inline(m_ol.group(2))}</li>")
            i += 1
            continue

        if stripped == "":
            flush_p()
            close_lists()
            i += 1
            continue

        in_p.append(stripped)
        i += 1

    flush_p()
    close_lists()
    return "\n".join(out)


HOME = """
<p class="kicker">Director · Global Markets AI · APAC</p>
<h1>AI for Quant. One page.</h1>
<p class="lede">A bank-agnostic prep blotter for Markets Quant AI/ML interviews. Work the tickets on the left, in order. Tick a ticket when you finish it. Dotted words are live jargon — hover for the meaning.</p>
<blockquote>
<p>I will be the senior AI/ML authority for APAC Markets Quant: hands-on on the first models, competent in coding and modern GenAI, working with engineering — not as a software-engineering hire, and not as a latency specialist unless the desk needs one later.</p>
</blockquote>
<div class="facts">
  <div><span>4–6</span> hybrid team</div>
  <div><span>FX PoC</span> then scale</div>
  <div><span>Not an SE</span> hire · HFT optional</div>
  <div><span>Two rails</span> modelling + agentic</div>
</div>
<h2>How to use this page</h2>
<ol>
<li>Open <strong>1 · Words</strong> if you are not from markets. Read the opening trade story, then search terms as you go.</li>
<li>Read <strong>2 · The seat</strong> then <strong>3 · Briefing</strong>. Say the two-minute opening out loud. <strong>90 days</strong> is how you would start the job — not a technical mock.</li>
<li>Follow <strong>4 · Study plan</strong>. Sit <strong>Drills</strong> closed, then mocks 5–8 timed. Mock 8 is a live desk <em>scenario</em>. Do not peek at model answers first.</li>
<li>If you are new to Python, sit <a href="#warmup" data-go="warmup"><strong>Python</strong></a> first — twenty short sessions in this page, from a bid/ask to a leak-safe pipeline. <a href="#sandbox" data-go="sandbox"><strong>Sandbox</strong></a> is a blank file: type, Run, read the console.</li>
<li>Coding is the lab on <strong>7 · Coding</strong> — implement <code>candidate.py</code> and run tests in the page. Do not open the answer key first.</li>
<li><strong>Morning of</strong> is for interview day only.</li>
</ol>
<p>They are not looking for software engineers. Competent coding plus fundamentals of modern GenAI is the bar.</p>
"""


DRILLS = """
<p class="kicker">Same facts as the long mocks · shorter form</p>
<h1>Drills</h1>
<p class="lede">Ten closed-book questions. Pick in your head, then open the row. The long written mocks still come after this on the blotter.</p>
<h2>ML · five closed-book</h2>
<details>
<summary>1. Purged CV is required in markets labelling mainly because…</summary>
<ol class="choices">
<li>Classes are imbalanced</li>
<li><strong>Label windows overlap train and test</strong></li>
<li>Trees overfit splits</li>
<li>GPU memory is limited</li>
</ol>
<p class="why">If the label uses (t, t+h], a random or even a naive time split still leaks overlapping paths. Purge + embargo by h.</p>
</details>
<details>
<summary>2. A toxicity model with AUC 0.71 can still lose money on the e-trading platform because…</summary>
<ol class="choices">
<li><strong>AUC is not a proper scoring rule for P(toxic) used in widen/last-look, and it ignores size, inventory, and markouts</strong></li>
<li>AUC cannot be computed on FX</li>
<li>AUC requires Gaussian returns</li>
<li>AUC is illegal under SS1/23</li>
</ol>
<p class="why">Policies need calibrated probabilities and a costed threshold. Report 1s/10s markout and fill ratio, not just AUC.</p>
</details>
<details>
<summary>3. Best first model class for tabular eFX (OFI, spread, inventory, tod) is usually…</summary>
<ol class="choices">
<li>A 12-layer Transformer on raw mids</li>
<li>PPO against the live pricing engine</li>
<li><strong>GBDT or penalised linear, then distil for the hot path</strong></li>
<li>An unconstrained LLM mid</li>
</ol>
<p class="why">Tabular + non-stationary + latency. DL when the object is a tensor (LOB, surface, language) or a friction-aware policy.</p>
</details>
<details>
<summary>4. A next-best-product ranker for eSales is not a CTR model because…</summary>
<ol class="choices">
<li>There is no click data</li>
<li><strong>You must trade off client utility, desk inventory/risk, and conduct — multi-stakeholder</strong></li>
<li>Rankers cannot use embeddings</li>
<li>The desk assistant already solved it</li>
</ol>
<p class="why">Multi-stakeholder. Max CTR dumps risk into the book and can systematically disadvantage a client class.</p>
</details>
<details>
<summary>5. What is allowed as an <em>intraday</em> update under typical bank MRM, vs a new model?</summary>
<ol class="choices">
<li>Full LightGBM retrain every hour</li>
<li>Change of feature set at lunch</li>
<li><strong>Slow intercept / temperature / EWMA residual on a frozen approved model, with a kill switch</strong></li>
<li>Swap in a new architecture if loss improves</li>
</ol>
<p class="why">Agree with MRM what is a parameter vs a model change. Architecture and features are a new model.</p>
</details>
<h2>DL / GenAI · five closed-book</h2>
<details>
<summary>1. Batch-norm on a live eFX tick net is dangerous because…</summary>
<ol class="choices">
<li>It is slower than ReLU</li>
<li><strong>Batch statistics do not exist the same way online and mix incompatible sessions</strong></li>
<li>PRA banned it</li>
<li>It prevents residual connections</li>
</ol>
<p class="why">Use frozen PIT moments, LayerNorm/RMSNorm, or a controlled EMA. Do not silently update population stats live.</p>
</details>
<details>
<summary>2. Deep hedging, in one sentence, is…</summary>
<ol class="choices">
<li>Fitting implied vol with a CNN</li>
<li><strong>Training a hedging policy to a risk measure of terminal P&amp;L under frictions, not matching BS delta</strong></li>
<li>Using GPT to write hedges</li>
<li>PCA on the vol surface</li>
</ol>
<p class="why">CVaR / utility + spreads + discrete time. Risk still wants Greeks and limits because the simulator is itself a model.</p>
</details>
<details>
<summary>3. A desk assistant should obtain a USDCNH mid by…</summary>
<ol class="choices">
<li>Asking the LLM to recall the last price it saw in training</li>
<li>RAG over all APAC chat including other clients</li>
<li><strong>A tool call into the approved pricer; the LLM only phrases and never invents the number</strong></li>
<li>Fine-tuning on last week’s tickets with prices in the completion</li>
</ol>
<p class="why">Different model tier: workflow vs pricing. HKMA HITL while customer-facing. No cross-client RAG.</p>
</details>
<details>
<summary>4. A LOB CNN that dies after a matching-engine upgrade most likely…</summary>
<ol class="choices">
<li>Needed more dropout</li>
<li><strong>Overfit venue artefacts / leaked the event in the snapshot</strong></li>
<li>Needed AdamW</li>
<li>Needed a larger batch size</li>
</ol>
<p class="why">Venue-change tests belong in CI. 90-day HKEX work should start classical, not an image net on the router.</p>
</details>
<details>
<summary>5. Offline RL (CQL/IQL) for KRW NDF child orders is blocked first by…</summary>
<ol class="choices">
<li>Lack of GPUs in HK</li>
<li><strong>Missing logged policies/propensities and a huge sim-to-real gap on a thin name</strong></li>
<li>HKMA banning RL</li>
<li>The need for BERT</li>
</ol>
<p class="why">Ship a Hawkes + inventory policy; keep RL in simulator until logging exists. Do not PPO live.</p>
</details>
<h2>Walk-in ticks (project scenario)</h2>
<p>Coverage checks for the live toxicity case — not the 90-day landing page.</p>
<label class="walk"><input type="checkbox" data-tick="w1"> Named the decision (last-look / widen) and both metrics in conflict (markout vs fill)</label>
<label class="walk"><input type="checkbox" data-tick="w2"> Diagnosed random-split AUC, fill-only labels, and nightly retrain as a feedback loop</label>
<label class="walk"><input type="checkbox" data-tick="w3"> Information set: decision time vs label window; purge / embargo</label>
<label class="walk"><input type="checkbox" data-tick="w4"> Costed threshold; corporate CNH overlap as a franchise segment</label>
<label class="walk"><input type="checkbox" data-tick="w5"> SageMaker trains; engine budget is ~80µs — distil or rules, not cloud GBDT live</label>
<label class="walk"><input type="checkbox" data-tick="w6"> Last-look conduct / client-class reject rates</label>
<label class="walk"><input type="checkbox" data-tick="w7"> Desk assistant: tools + reason-code; never invents a mid; different model tier</label>
<label class="walk"><input type="checkbox" data-tick="w8"> Kill: fallback quote, dual-run, signed off-criteria, CNH residency if required</label>
"""


CSS = r"""
:root {
  --blotter: #10231c;
  --blotter-ink: #d7e3d4;
  --mute: #8aa090;
  --ticket: #f4efe4;
  --rule: #d8d0bf;
  --ink: #1b1712;
  --soft: #5c564c;
  --stamp: #8f2d3c;
  --gold: #a67c2d;
  --focus: #2f6f5e;
}
* { box-sizing: border-box; }
html, body { margin: 0; height: 100%; }
body {
  font-family: "IBM Plex Sans", "Source Sans 3", sans-serif;
  color: var(--ink);
  background: var(--ticket);
  display: grid;
  grid-template-columns: 272px 1fr;
  min-height: 100%;
}
.blotter {
  background: var(--blotter);
  color: var(--blotter-ink);
  padding: 28px 18px 40px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: auto;
  border-right: 1px solid #0a1612;
}
.blotter h1 {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin: 0 0 6px;
  color: var(--gold);
}
.blotter p { margin: 0 0 22px; font-size: 12px; color: var(--mute); line-height: 1.45; }
.blotter nav { display: flex; flex-direction: column; gap: 2px; }
.ticket {
  display: grid;
  grid-template-columns: 18px 1fr;
  gap: 8px;
  align-items: start;
  padding: 6px 8px;
  border-left: 2px solid transparent;
}
.ticket:hover, .ticket.on { border-left-color: var(--gold); background: rgba(255,255,255,0.04); }
.blotter a {
  color: inherit;
  text-decoration: none;
  font-size: 13.5px;
  line-height: 1.3;
}
.blotter a small { display: block; color: var(--mute); font-size: 11px; margin-top: 2px; }
.blotter input[type="checkbox"] {
  appearance: none;
  width: 12px;
  height: 12px;
  margin: 4px 0 0;
  border: 1px solid var(--mute);
  background: transparent;
  cursor: pointer;
}
.blotter input[type="checkbox"]:checked {
  background: var(--gold);
  border-color: var(--gold);
}
.search {
  width: 100%;
  margin: 0 0 16px;
  padding: 8px 10px;
  background: #0c1a16;
  border: 1px solid #2a4036;
  color: var(--blotter-ink);
  font: inherit;
  font-size: 13px;
}
.search:focus { outline: 1px solid var(--gold); }
main { overflow: auto; height: 100vh; }
article {
  max-width: 820px;
  padding: 40px 40px 80px;
}
.panel { display: none; }
.panel.on { display: block; }
.kicker {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--stamp);
  margin: 0 0 10px;
}
h1, h2, h3 { font-family: "IBM Plex Sans", sans-serif; font-weight: 600; }
article > h1, .panel h1 { font-size: 2.1rem; letter-spacing: -0.03em; margin: 0 0 12px; }
h2 { font-size: 1.25rem; margin: 2rem 0 0.7rem; }
h3 { font-size: 1.05rem; margin: 1.4rem 0 0.5rem; }
p, li { line-height: 1.6; font-size: 16px; }
.lede { font-size: 1.15rem; color: var(--soft); }
a { color: var(--focus); }
hr { border: 0; border-top: 1px solid var(--rule); margin: 1.6rem 0; }
blockquote {
  margin: 1.2rem 0;
  padding: 12px 16px;
  background: #ebe4d4;
  border-left: 3px solid var(--stamp);
}
blockquote p { margin: 0; }
code, pre { font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 0.86em; }
code { background: #ebe6da; padding: 0.1em 0.35em; }
pre {
  background: var(--blotter);
  color: var(--blotter-ink);
  padding: 14px 16px;
  overflow: auto;
}
pre code { background: none; color: inherit; }
.table-wrap { overflow: auto; margin: 1rem 0 1.4rem; }
table { border-collapse: collapse; width: 100%; font-size: 14px; }
th, td { border-bottom: 1px solid var(--rule); text-align: left; padding: 8px 10px; vertical-align: top; }
th { font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--soft); font-weight: 600; }
.facts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 1.4rem 0 1.8rem;
}
.facts div {
  border: 1px solid var(--rule);
  padding: 12px 14px;
  font-size: 13px;
  color: var(--soft);
}
.facts span { display: block; color: var(--ink); font-family: "IBM Plex Mono", monospace; font-size: 13px; margin-bottom: 4px; }
.hit { background: #f3d9a4; }
#jargon.searching > h1,
#jargon.searching > p,
#jargon.searching > ol,
#jargon.searching > ul,
#jargon.searching > blockquote,
#jargon.searching > hr { display: none; }
#jargon.searching > #find-empty { display: block; color: var(--stamp); }
#jargon.searching > h2[hidden],
#jargon.searching > h3[hidden],
#jargon.searching > .table-wrap[hidden] { display: none; }
details { border-bottom: 1px solid var(--rule); padding: 12px 0; }
summary { cursor: pointer; font-weight: 600; }
.choices { margin: 0.6rem 0; padding-left: 1.2rem; }
.why { color: var(--soft); font-size: 15px; }
.walk { display: flex; gap: 10px; align-items: flex-start; margin: 10px 0; font-size: 15px; line-height: 1.45; }
.walk input { margin-top: 4px; accent-color: var(--gold); }
.lab {
  margin: 2.4rem 0 0;
  padding-top: 1.6rem;
  border-top: 1px solid var(--rule);
}
.lab-tabs { display: flex; gap: 6px; flex-wrap: wrap; margin: 0 0 10px; }
.lab-tabs button, .lab-bar button {
  font: inherit;
  font-size: 13px;
  padding: 7px 12px;
  background: transparent;
  border: 1px solid var(--rule);
  color: var(--ink);
  cursor: pointer;
}
.lab-tabs button.on,
.lab-bar button#lab-run {
  background: var(--blotter);
  color: var(--blotter-ink);
  border-color: var(--blotter);
}
.lab-ed {
  width: 100%;
  min-height: 420px;
  padding: 12px 14px;
  background: var(--blotter);
  color: var(--blotter-ink);
  border: 1px solid #0a1612;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 13px;
  line-height: 1.45;
  resize: vertical;
  tab-size: 4;
}
.lab-ed:read-only { opacity: 0.92; }
.cm-s-blotter.CodeMirror {
  height: 420px;
  background: var(--blotter);
  color: var(--blotter-ink);
  border: 1px solid #0a1612;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 13px;
  line-height: 1.45;
}
.warmup .cm-s-blotter.CodeMirror { height: 280px; }
.cm-s-blotter .CodeMirror-gutters {
  background: #0c1a16;
  border-right: 1px solid #1a2e26;
}
.cm-s-blotter .CodeMirror-linenumber { color: #5e7468; }
.cm-s-blotter .CodeMirror-cursor { border-left: 1.5px solid var(--gold); }
.cm-s-blotter .CodeMirror-selected { background: rgba(166, 124, 45, 0.28); }
.cm-s-blotter .CodeMirror-activeline-background { background: rgba(255,255,255,0.035); }
.cm-s-blotter .CodeMirror-matchingbracket { color: var(--gold) !important; }
.cm-s-blotter.cm-readonly { opacity: 0.92; }
.cm-s-blotter span.cm-comment { color: #7a8f83; font-style: italic; }
.cm-s-blotter span.cm-string,
.cm-s-blotter span.cm-string-2 { color: #d4b06a; }
.cm-s-blotter span.cm-number { color: #e6c48a; }
.cm-s-blotter span.cm-keyword { color: #d36b78; }
.cm-s-blotter span.cm-def { color: #f4efe4; }
.cm-s-blotter span.cm-variable { color: var(--blotter-ink); }
.cm-s-blotter span.cm-variable-2,
.cm-s-blotter span.cm-variable-3 { color: #b9d0c4; }
.cm-s-blotter span.cm-builtin { color: #7eb8a4; }
.cm-s-blotter span.cm-operator { color: #c5b89a; }
.cm-s-blotter span.cm-meta,
.cm-s-blotter span.cm-decorator { color: var(--gold); }
.cm-s-blotter span.cm-atom,
.cm-s-blotter span.cm-property { color: #d4b06a; }
pre.cm-s-blotter.cm-static span { background: none; }
.lab-bar {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
  margin: 10px 0 8px;
}
#lab-status { font-size: 13px; color: var(--soft); }
.lab-out {
  background: var(--blotter);
  color: var(--blotter-ink);
  padding: 14px 16px;
  overflow: auto;
  max-height: 360px;
  white-space: pre-wrap;
  font-size: 12px;
}
.lab-out.pass { box-shadow: inset 3px 0 0 var(--gold); }
.lab-out.fail { box-shadow: inset 3px 0 0 var(--stamp); }
.lab-out.skip { box-shadow: inset 3px 0 0 var(--mute); }
.warmup .lab-ed { min-height: 280px; }
.wu-track {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(10, minmax(0, 1fr));
  gap: 4px;
  padding: 0;
  margin: 1.2rem 0 0.6rem;
}
.wu-track button {
  width: 100%;
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11px;
  letter-spacing: 0.04em;
  padding: 8px 0;
  background: transparent;
  border: 1px solid var(--rule);
  color: var(--ink);
  cursor: pointer;
}
.wu-track button:hover { border-color: var(--gold); }
.wu-track button.on { border-color: var(--stamp); color: var(--stamp); }
.wu-track button.done {
  background: var(--blotter);
  color: var(--gold);
  border-color: var(--blotter);
}
.wu-track button.done.on { box-shadow: inset 0 0 0 2px var(--gold); }
.wu-progress {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 12px;
  color: var(--soft);
  margin: 0 0 1.4rem;
}
.wu-lesson { margin: 0 0 1rem; }
.wu-lesson p, .wu-lesson li { font-size: 15px; }
#wu-run, #sb-run {
  background: var(--blotter);
  color: var(--blotter-ink);
  border-color: var(--blotter);
}
.sandbox .cm-s-blotter.CodeMirror { height: 320px; }
.sb-guide { padding-left: 1.2rem; }
.sb-guide li { font-size: 15px; margin: 0.35rem 0; }
@media (max-width: 820px) {
  .wu-track { grid-template-columns: repeat(5, minmax(0, 1fr)); }
}
.jarg {
  border-bottom: 1px dotted var(--stamp);
  background: rgba(143, 45, 60, 0.08);
  cursor: help;
}
.jarg:hover, .jarg:focus-visible {
  background: #f3d9a4;
  outline: none;
}
#gloss {
  position: fixed;
  z-index: 50;
  display: none;
  width: min(328px, calc(100vw - 24px));
  background: var(--blotter);
  color: var(--blotter-ink);
  padding: 12px 14px 14px;
  border-top: 3px solid var(--stamp);
  pointer-events: none;
}
#gloss.on { display: block; }
#gloss .gt {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--gold);
}
#gloss .gm { font-size: 14px; line-height: 1.45; margin-top: 6px; }
#gloss .gw { font-size: 12px; color: var(--mute); margin-top: 8px; line-height: 1.4; }
@media (max-width: 820px) {
  body { grid-template-columns: 1fr; }
  .blotter { height: auto; position: relative; }
  main { height: auto; }
}
@media print {
  .blotter, #gloss { display: none; }
  body { display: block; }
  .panel { display: block !important; page-break-before: always; }
  .panel#home { page-break-before: avoid; }
}
"""


JS = r"""
const panels = document.querySelectorAll('.panel');
function show(id) {
  const panel = document.getElementById(id);
  const already = panel && panel.classList.contains('on');
  panels.forEach(p => p.classList.toggle('on', p.id === id));
  document.querySelectorAll('.ticket').forEach(t => t.classList.toggle('on', t.dataset.go === id));
  if (!already) document.querySelector('main').scrollTop = 0;
  if (location.hash !== '#' + id) location.hash = id;
  if ((id === 'coding' || id === 'warmup' || id === 'sandbox') && window.primeQuantPy) {
    const el = document.getElementById(id === 'coding' ? 'lab-status' : id === 'warmup' ? 'wu-status' : 'sb-status');
    window.primeQuantPy(t => { if (el) el.textContent = t; });
  }
  if (window.ensureCodeMirror && panel && panel.querySelector('pre code, textarea.lab-ed, .CodeMirror')) {
    window.ensureCodeMirror().then(() => {
      if (window.colorQuantCode) window.colorQuantCode(panel);
      requestAnimationFrame(() => { if (window.refreshQuantEditors) window.refreshQuantEditors(); });
    });
  }
}
document.querySelectorAll('[data-go]').forEach(el => {
  if (el.tagName !== 'A') return;
  el.addEventListener('click', e => {
    e.preventDefault();
    show(el.dataset.go);
  });
});
const start = (location.hash || '#home').slice(1) || 'home';
show(document.getElementById(start) ? start : 'home');
window.addEventListener('hashchange', () => {
  const id = location.hash.slice(1);
  if (document.getElementById(id)) show(id);
});
const KEY = 'quantprep-ticks';
const ticks = JSON.parse(localStorage.getItem(KEY) || '{}');
document.querySelectorAll('input[data-tick]').forEach(box => {
  box.checked = !!ticks[box.dataset.tick];
  box.addEventListener('change', () => {
    ticks[box.dataset.tick] = box.checked;
    localStorage.setItem(KEY, JSON.stringify(ticks));
  });
});
const q = document.getElementById('find');
function normFind(s) {
  return s.toLowerCase().replace(/[/–—−-]+/g, ' ').replace(/\s+/g, ' ').trim();
}
function runFind() {
  const raw = q.value.trim();
  const n = normFind(raw);
  const jargon = document.getElementById('jargon');
  if (n) show('jargon');
  jargon.classList.toggle('searching', !!n);
  let termMatch = null;
  let other = null;
  if (!n) {
    jargon.querySelectorAll('h2, h3, .table-wrap').forEach(el => { el.hidden = false; });
  } else {
    jargon.querySelectorAll('h2, h3').forEach(h => { h.hidden = true; });
  }
  jargon.querySelectorAll('table').forEach(table => {
    let any = false;
    table.querySelectorAll('tbody tr').forEach(tr => {
      const cells = [...tr.children].map(td => normFind(td.textContent));
      const termHit = Boolean(n && cells[0] && cells[0].includes(n));
      const hit = !n || cells.some(c => c.includes(n));
      tr.style.display = hit ? '' : 'none';
      tr.classList.toggle('hit', Boolean(n && termHit));
      if (hit) any = true;
      if (n && termHit && !termMatch) termMatch = tr;
      else if (n && hit && !other) other = tr;
    });
    const wrap = table.closest('.table-wrap');
    if (wrap) wrap.hidden = Boolean(n && !any);
    if (wrap && !wrap.hidden) {
      const heading = wrap.previousElementSibling;
      if (heading && /^H[23]$/.test(heading.tagName)) heading.hidden = false;
    }
  });
  const first = termMatch || other;
  let empty = document.getElementById('find-empty');
  if (!empty) {
    empty = document.createElement('div');
    empty.id = 'find-empty';
    jargon.prepend(empty);
  }
  empty.hidden = !n || Boolean(first);
  empty.textContent = n && !first ? 'No Words match “' + raw + '”.' : '';
  if (first) requestAnimationFrame(() => first.scrollIntoView({ block: 'center' }));
}
q.addEventListener('input', runFind);
q.addEventListener('search', runFind);
"""


GLOSS_JS = r"""
(function bindGlossary() {
  const SKIP = new Set(["CODE", "PRE", "SCRIPT", "STYLE", "TEXTAREA", "INPUT"]);
  const items = [];
  for (const e of GLOSSARY) {
    for (const k of e.keys) {
      items.push({
        k,
        lower: k.toLowerCase(),
        sensitive: k.length <= 3 && k === k.toUpperCase(),
        term: e.term,
        mean: e.mean,
        why: e.why || ""
      });
    }
  }
  items.sort((a, b) => b.k.length - a.k.length);

  const wordy = /[A-Za-z0-9+\-\u00b5]/;
  function okBound(text, start, end) {
    const before = start === 0 ? "" : text[start - 1];
    const after = end >= text.length ? "" : text[end];
    if (before && wordy.test(before)) return false;
    if (after && wordy.test(after)) return false;
    return true;
  }
  function matchAt(text, i) {
    for (const it of items) {
      const n = it.k.length;
      if (i + n > text.length) continue;
      const slice = text.substr(i, n);
      const hit = it.sensitive ? slice === it.k : slice.toLowerCase() === it.lower;
      if (hit && okBound(text, i, i + n)) return it;
    }
    return null;
  }

  const root = document.querySelector("article");
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      const p = node.parentElement;
      if (!p || SKIP.has(p.tagName)) return NodeFilter.FILTER_REJECT;
      if (p.closest("#jargon table, .jarg, #gloss, .CodeMirror")) return NodeFilter.FILTER_REJECT;
      if (!node.nodeValue || !/[A-Za-z]/.test(node.nodeValue)) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    }
  });
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  for (const node of nodes) {
    const text = node.nodeValue;
    let i = 0;
    while (i < text.length && !matchAt(text, i)) i++;
    if (i >= text.length) continue;
    const frag = document.createDocumentFragment();
    i = 0;
    while (i < text.length) {
      const it = matchAt(text, i);
      if (!it) {
        let j = i + 1;
        while (j < text.length && !matchAt(text, j)) j++;
        frag.append(text.slice(i, j));
        i = j;
        continue;
      }
      const el = document.createElement("span");
      el.className = "jarg";
      el.textContent = text.substr(i, it.k.length);
      el.dataset.term = it.term;
      el.dataset.mean = it.mean;
      el.dataset.why = it.why;
      frag.append(el);
      i += it.k.length;
    }
    node.parentNode.replaceChild(frag, node);
  }

  const tip = document.createElement("div");
  tip.id = "gloss";
  tip.innerHTML = '<div class="gt"></div><div class="gm"></div><div class="gw"></div>';
  document.body.append(tip);

  function place(el) {
    tip.querySelector(".gt").textContent = el.dataset.term;
    tip.querySelector(".gm").textContent = el.dataset.mean;
    const why = el.dataset.why;
    const gw = tip.querySelector(".gw");
    gw.textContent = why ? "In this pack: " + why : "";
    gw.style.display = why ? "" : "none";
    tip.classList.add("on");
    tip.style.display = "block";
    const r = el.getBoundingClientRect();
    const tw = tip.offsetWidth;
    const th = tip.offsetHeight;
    let left = r.left + r.width / 2 - tw / 2;
    left = Math.max(8, Math.min(left, window.innerWidth - tw - 8));
    let top = r.top - th - 10;
    if (top < 8) top = r.bottom + 10;
    tip.style.left = left + "px";
    tip.style.top = top + "px";
  }
  function hide() {
    tip.classList.remove("on");
    tip.style.display = "";
  }

  root.addEventListener("pointerover", e => {
    const el = e.target.closest(".jarg");
    if (el) place(el);
  });
  root.addEventListener("pointerout", e => {
    const el = e.target.closest(".jarg");
    if (!el) return;
    if (e.relatedTarget && el.contains(e.relatedTarget)) return;
    hide();
  });
  root.addEventListener("focusin", e => {
    const el = e.target.closest(".jarg");
    if (el) place(el);
  });
  root.addEventListener("focusout", hide);
  document.querySelector("main").addEventListener("scroll", hide, { passive: true });
  window.addEventListener("resize", hide);
})();
"""


def _md_plain(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", s)
    return s.strip()


_GLOSS_DENY = {
    "ask", "offer", "bid", "mid", "quote", "desk", "fill", "hedge", "prime",
    "spot", "swap", "option", "vanilla", "exotic", "engine", "session", "client",
    "flow", "book", "bar", "tick", "label", "pair", "vol", "net", "q", "policy",
    "director", "vp", "values", "mindset", "credit", "macro", "forward", "now",
    "team", "arrival", "attention", "horizon", "regime", "conduct", "latency",
    "capacity", "override", "fallback", "carry", "distil", "algo", "time",
    "quoting", "hybrid",
}

_GLOSS_SHORT = {
    "IB", "GM", "FX", "RL", "IS", "CI", "ML", "DL", "QR", "QD", "BN", "FM", "EM",
    "PnL", "PoC", "TTC", "OFI", "NDF", "NDS", "AUC", "PIT", "PPO", "CQL", "IQL",
    "IPS", "CTR", "TCA", "QPS", "DMA", "LOB", "FIX", "MDP", "WMR", "SOR", "EMS",
    "HITL", "MRM", "PRA", "SFC", "SMF", "RAG", "ATM", "eFX", "LLM", "CVaR",
    "HKEX", "HKMA", "PCPD", "RACI", "CNH", "CNY", "G10", "RFQ", "PBOC",
    "RoTE", "SHAP", "VWAP", "TCN", "LSTM", "GBDT", "kdb+",
}

_GLOSS_EXTRA = {
    "markout": ["markouts"],
    "toxicity / toxic flow": ["toxic flow"],
    "purge / embargo": ["purged CV", "purged", "purged walk-forward"],
    "look-ahead / leakage": ["look-ahead", "lookahead", "leakage", "look ahead"],
    "e-trading platform": ["e-trading", "eTrading"],
    "pricing engine": ["pricing engines"],
    "desk assistant": ["desk-assistant", "desk assistants"],
    "walk-forward": ["walk-forward", "walk forward"],
    "kill switch": ["kill-switch"],
    "last look": ["last-look"],
    "fill / fill rate": ["fill rate", "fill-rate"],
    "bid / ask (offer)": ["bid/ask", "bid / ask"],
    "cny vs cnh": ["USDCNH"],
    "ss1/23": ["SS1/23", "SS1 / 23"],
    "poc / proof of concept": ["proof of concept"],
    "gbdt / lightgbm / xgboost": ["LightGBM", "XGBoost", "GBDT"],
    "llm / genai / agentic": ["GenAI"],
    "hitl": ["human-in-the-loop", "human in the loop"],
    "information set": ["information sets"],
    "feature store / pit / as-of join": ["point-in-time", "as-of join", "feature store"],
}


def _keep_gloss_key(k: str) -> bool:
    if len(k) < 2:
        return False
    if k.lower() in _GLOSS_DENY:
        return False
    if len(k) <= 3:
        return k in _GLOSS_SHORT or k.upper() in _GLOSS_SHORT
    return True


def _expand_gloss_keys(term: str) -> list[str]:
    raw = [term]
    for part in re.split(r"\s*/\s*|\s+vs\.?\s+", term):
        extras = re.findall(r"\(([^)]+)\)", part)
        core = re.sub(r"\s*\([^)]*\)\s*", " ", part).strip()
        raw.append(core)
        for extra in extras:
            extra = extra.strip()
            if extra in _GLOSS_SHORT or re.fullmatch(r"[A-Z]{2,5}", extra):
                if extra not in {"FX"}:  # too many hosts; mapped onto eFX instead
                    raw.append(extra)
    more: list[str] = []
    for k in raw:
        more.append(k.replace("–", "-").replace("—", "-"))
        more.append(k.replace("-", "–"))
    extra = _GLOSS_EXTRA.get(term.lower(), [])
    out: list[str] = []
    seen: set[str] = set()
    for k in raw + more + extra:
        k = re.sub(r"\s+", " ", k).strip(" .,;")
        if not _keep_gloss_key(k):
            continue
        lk = k.lower()
        if lk in seen:
            continue
        seen.add(lk)
        out.append(k)
    return out


def parse_glossary(md: str) -> list[dict]:
    entries: list[dict] = []
    for line in md.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        head = cells[0].lower()
        if head.startswith("term") or set(cells[0].replace(":", "")) <= set("- "):
            continue
        term = _md_plain(cells[0])
        meaning = _md_plain(cells[1])
        why = _md_plain(cells[2]) if len(cells) > 2 else ""
        if not term or not meaning:
            continue
        keys = _expand_gloss_keys(term)
        if not keys:
            continue
        entries.append({"term": term, "mean": meaning, "why": why, "keys": keys})
    return entries


def rewrite_pack_links(html_body: str) -> str:
    mapped = {
        "jargon.md": "#jargon",
        "seat.md": "#seat",
        "briefing.md": "#briefing",
        "landing.md": "#landing",
        "study-plan.md": "#plan",
        "01-ml.md": "#ml",
        "02-dl.md": "#dl",
        "03-coding.md": "#coding",
        "04-project.md": "#project",
        "one-pager.md": "#morning",
        "START_HERE.md": "#home",
        "coding": "#coding",
    }

    def sub(m: re.Match[str]) -> str:
        href = m.group(1)
        if href.startswith("http"):
            return m.group(0)
        base = href.rstrip("/").split("/")[-1]
        dest = mapped.get(base)
        return f'href="{dest}"' if dest else m.group(0)

    return re.sub(r'href="([^"]+)"', sub, html_body)


def warmup_payload() -> list[dict]:
    path = PACK / "warmup" / "sessions.py"
    spec = importlib.util.spec_from_file_location("quant_warmup_sessions", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    out = []
    for s in mod.SESSIONS:
        out.append(
            {
                "title": s["title"],
                "goal": s["goal"],
                "lesson": md_to_html(s["lesson"].strip()),
                "starter": s["starter"],
                "solution": s["solution"],
                "tests": s["tests"],
            }
        )
    return out


def strip_pack_nav(md: str) -> str:
    lines = []
    for line in md.split("\n"):
        if re.match(r"^\*\*\d+ of 8\*\*", line):
            continue
        if line.startswith("**Use on interview morning only.**"):
            continue
        lines.append(line)
    return "\n".join(lines)


def main() -> None:
    nav = []
    panels = []
    for sid, label, path, hint in SECTIONS:
        nav.append(
            f'<div class="ticket" data-go="{sid}">'
            f'<input type="checkbox" data-tick="{sid}">'
            f'<a href="#{sid}" data-go="{sid}">{html.escape(label)}'
            f"<small>{html.escape(hint)}</small></a></div>"
        )
        if sid == "home":
            body = HOME
        elif sid == "drills":
            body = DRILLS
        elif sid == "warmup":
            body = WARMUP_HTML
        elif sid == "sandbox":
            body = SANDBOX_HTML
        elif sid == "coding":
            body = rewrite_pack_links(md_to_html(strip_pack_nav(path.read_text(encoding="utf-8")))) + CODING_LAB
        else:
            body = rewrite_pack_links(md_to_html(strip_pack_nav(path.read_text(encoding="utf-8"))))
        panels.append(f'<section class="panel" id="{sid}">{body}</section>')

    glossary = parse_glossary((PACK / "jargon.md").read_text(encoding="utf-8"))
    runtime_js = (PACK / "warmup" / "runtime.js").read_text(encoding="utf-8")
    editor_js = (PACK / "warmup" / "editor.js").read_text(encoding="utf-8")
    warmup_js = (PACK / "warmup" / "warmup.js").read_text(encoding="utf-8")
    sandbox_js = (PACK / "warmup" / "sandbox.js").read_text(encoding="utf-8")
    lab_js = (PACK / "mocks" / "coding" / "lab.js").read_text(encoding="utf-8")
    script = (
        JS
        + "\nconst GLOSSARY = "
        + json.dumps(glossary, ensure_ascii=False)
        + ";\nconst CODING_STORE = "
        + json.dumps(KEY_CANDIDATE)
        + ";\nconst CODING = "
        + json.dumps(coding_files(), ensure_ascii=False)
        + ";\nconst WARMUP_STORE = "
        + json.dumps(KEY_WARMUP)
        + ";\nconst WARMUP = "
        + json.dumps(warmup_payload(), ensure_ascii=False)
        + ";\nconst SANDBOX_STORE = "
        + json.dumps(KEY_SANDBOX)
        + ";\n"
        + GLOSS_JS
        + "\n"
        + runtime_js
        + "\n"
        + editor_js
        + "\n"
        + warmup_js
        + "\n"
        + sandbox_js
        + "\n"
        + lab_js
    )
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>quantprep · AI for Quant</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<aside class="blotter">
  <h1>QUANTPREP</h1>
  <p>AI for Quant. Tick each ticket. Search filters Words. Dotted words explain themselves.</p>
  <input class="search" id="find" type="search" placeholder="Search Words: fill rate, NDF…" aria-label="Search Words">
  <nav>{"".join(nav)}</nav>
</aside>
<main>
<article>
{"".join(panels)}
</article>
</main>
<script>{script}</script>
</body>
</html>
"""
    OUT.write_text(html_doc, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
