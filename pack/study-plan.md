# Study plan and round design

**4 of 8** in the pack. Previous: [briefing.md](briefing.md). Next: [mocks/01-ml.md](mocks/01-ml.md). 

Assume **10–14 days**. If you have less, do the **bold** items only.

## What the four rounds are testing (Director edition)

| Round | Surface | What a GM panel is actually buying |
| --- | --- | --- |
| **ML** | Forecasting, recommenders, uncertainty, leakage, trees vs linear, calibration, bandits | Can you be the **senior technical authority** the typical seat asked for? |
| **DL / GenAI** | When DL loses; **agentic** tools; RAG; hallucination; RL only in sim | **Fundamentals** of modern GenAI. Not an expert at all topics. |
| **Coding** | Python, information set, leaky backtest | **Competent** coding. They are **not** hiring a software engineer. |
| **Project** | FX PoC + GenAI rail, 4–6, Quant-central, governance | Broader Director remit: APAC, team, strategy, PnL. |

They will also sample **risk and controls** and **APAC stakeholder craft** (HK desks vs Singapore eFX vs London AI/ML).

## 14-day plan

### Days 1–2 — franchise and story

- If you are not from markets or quant research, read `jargon.md` **once end-to-end**.
- Read `seat.md` and map **seven STAR stories** to the requirement list.
- Read `briefing.md` twice. Write your **2-minute opening** from the typical seat (centralised Quant, not SE, FX PoC, GenAI + modelling).
- Map three named internal clients: eFX trader / eSales, Equities algo quant (equities-algo-quant), Prime quant (prime-quant). For each, one pain, one model, one metric, one control.
- Prepare **two war stories**: (1) a model you killed, (2) a model you productionised through governance. Use numbers.

### Days 3–5 — ML

- Lopez de Prado: chapter on **purged CV, embargo, CPCV**, triple-barrier, fractionally differentiated features (conceptual).
- Calibration (reliability diagrams, Platt/isotonic — and why isotonic can overfit small books).
- Trees vs linear for tabular tick features; SHAP **without** pretending it is causal.
- Recommenders: implicit feedback, two-tower vs FM/kernel FM, multi-objective (client utility vs desk risk).
- Bandits: UCB, Thompson, contextual; exploration on a priced stream is **real money**.
- Sit mock `mocks/01-ml.md` timed. Redo any miss as a whiteboard.

### Days 6–8 — DL

- Why LSTMs fail on financial ticks (non-stationarity, label horizon vs receptive field, teacher forcing ≠ live).
- Temporal convolutions, TCN, and **transformers on returns** — usually lose to GBDT unless the representation is rich (LOB images, surfaces).
- Deep hedging: convex risk measures, friction, CVaR; what “Greek-free” means and what Risk will still ask for.
- RL: offline / batch-constrained, sim-to-real gap, conservative Q; never “PPO on live FX”.
- LLM: RAG vs fine-tune vs **tools**; agentic loop; hallucination of **prices**; HITL. The typical seat wants **fundamentals**, not every paper.
- Sit mock `mocks/02-dl.md`.

### Days 9–11 — coding

The typical seat: competent at coding, **not** a software-engineer interview.

- Implement `mocks/coding/candidate.py` until `pytest` is green.
- Then **delete your solutions from working memory** and re-implement from the problem statements in 90 minutes.
- Extra: write a 20-line critique of a messy pandas backtest (the debug problem).
- Do **not** grind leetcode system design, kdb, or Java unless a later interviewer asks.

### Days 12–13 — project and leadership

- Sit `mocks/04-project.md` with a timer. Record yourself.
- Two rails on the slide: **FX PoC** and **GenAI/agentic**. The typical seat called the mandate extremely broad.
- Hiring: first three **AI/ML** roles; what you will **not** hire (a SE shop, an HFT team).
- Tough questions: “We’re not looking for software engineers”; “HFT isn’t essential — why 50µs?”; “Why not just use London models?”

### Day 14 — integration

- Full mock: 30 min ML rapid-fire, 30 min DL, 45 min coding, 45 min project.
- Sleep. Do not cram new papers the night before.

## Whiteboard openers to keep on a card

1. **Validation:** “Walk-forward, purge the embargo by the label horizon, report a **Purged Combinatorial CV** distribution, not a single Sharpe.”
2. **Metric:** “I optimise a **cost-adjusted markout** (or RFQ win-rate at target spread), and I **monitor** logloss/Brier. I do not ship on AUC.”
3. **DL:** “I need a representation DL uniquely provides (LOB tensor, surface, language). Otherwise GBDT + online calibration.”
4. **GenAI:** “No naked prices from an LLM. Tools for mid/skew; LLM for intent and workflow. Human-in-the-loop until the tier says otherwise.”
5. **Team:** “I am the senior AI/ML authority for APAC Markets Quant. I work **with** engineering. I am not staffing an SE org.”

## Question bank you should have a 90-second answer for

- Why the bank, why GM, why HK, why now?
- Why FX first if Equities is the growth story?
- How do you measure success in six months? In eighteen?
- Walk me through a pricing model you would **not** put on the pricing engine.
- How do you work with a trader who has been burned by ML?
- SS1/23: is a gradient-boosted mid a “model”? Who is the SMF?
- How do London, Singapore, and HK split data, IP, and on-call?
- CNH flow is not EURUSD flow. What changes in the model?
- How would you use the desk assistant without creating a conduct incident?
- Describe how you develop others and align across the enterprise.
