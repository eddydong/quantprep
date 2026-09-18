# Industry briefing: AI for Global Markets

**3 of 8** in the pack. Previous: [seat.md](seat.md). Next: [landing.md](landing.md).

Research snapshot for a generic APAC GM AI/ML Director seat. Map every mock answer back to [The seat](seat.md).

If **bid/ask, markout, eFX, purged CV, pricing engine, SS1/23** are not already fluent, read [Words](jargon.md) first.

## 1. What this job actually is

You are a **Director – Global Markets AI** for APAC, sitting in Hong Kong, inside a **centralised Quant business** of the Investment Bank that exists **for Markets**. Front-office aligned, **direct influence on trading outcomes**. You are not a lone alpha researcher, not a CIB Tech engineering lead, and not a desk HFT engineer.

The mandate, in the usual words:

- **Build and lead** a hybrid AI/ML team of **4–6**.
- **Own** programmes **ideation → production and governance**.
- **Partner** with trading desks and APAC business leadership on use cases with **measurable PnL**.
- Work **across** stakeholders, **engineering teams**, and governance — you do not replace engineering.
- Apply **price forecasting, recommenders, reinforcement learning, decision-making under uncertainty**.
- **Initial use cases in FX**, proof of concept, then **scale across asset classes**.
- **Responsible AI** and model governance.
- Mandate described as **extremely broad**: **quantitative modelling, GenAI, and agentic applications**.
- You are the **senior technical authority** and stay **hands-on where required**.
- Typical profile: already **Director ~2–3 years**, now a **broader** remit (APAC + team + strategy).
- **AI/LLM initiatives** and team-building are listed requirements.
- **eTrading / HFT: advantageous, not essential.**
- Recruiter note, typical: they are **not looking for software engineers**. Coding competence + **fundamentals of modern GenAI**; you do not need to be an expert at all topics.

A parallel IC/VP posting (*AI/ML Modeller – Global Markets*, London / SG / HK) is the **bench** you will hire: Python/PyTorch, SageMaker, eFX/alpha a plus, NLP/LLMs. Your interview mixes **Director judgement** with enough **hands-on technical depth** to be that authority — not a staff-engineer algorithms screen.

**How this should change your voice:** lead with **Quant + GenAI/agentic + FX PoC + governance**. Do not lead with “I will own the 50µs stack.” That is engineering’s job; your job is to bring models they can put on it.

## 2. The franchise, in one page

**A leading IB.** Markets at a house like this already often has a **production FX desk assistant** used to help colleagues initiate trades. GenAI is usually: pilots with measurable outcomes, then scale, inside a control framework.

**Recent Markets mix at a leading IB (the pattern, not a ticker):**

- Global Markets is still “the house that Fixed Income built.”
- **Equities is the growth lean** — often approaching ~30% of Markets revenue in a strong print, with a sharp quarterly jump when cash and prime fire.
- There is a **regional tilt toward Asia**, helping global clients access Asian markets, including through **Prime**. A large share of that Prime growth is usually attributed to the **top 100 Markets clients**.
- Financing vs intermediation mix is a stated strategic guardrail.

**Do not** walk in talking only about G10 spot eFX. The franchise that is growing APAC wallet is **Equities + Prime + financing**, while **FX remains the most natural first AI production surface**.

## 3. Global Markets and the e-trading platform

GM sells **execution, liquidity, risk solutions, and financing** to institutions and corporates. Asset-class map:

- **Macro**: G10 and major EM rates and FX.
- **Equities**: cash, electronic, equity derivatives, systematic, prime.
- **Credit**, **securitised products**, **prime services**, **fixed-income financing**.

The **e-trading platform** is the cross-asset electronic surface (Equities, FICC, futures, FX). For FX specifically:

- Products: spot, forwards, swaps, NDFs/NDS, vanilla and exotic options.
- Execution: streaming, RFQ, **own-book fill** (principal liquidity), **mixed-venue execution** (internal + external venues), **Manual** (trader / benchmarks).
- Access: proprietary UI, FIX API, MDPs (Bloomberg, FXall, FX Connect, 360T).
- Analytics: pre-trade volume, post-trade TCA.
- A **desk assistant**: client/colleague-facing GenAI on the FX platform.
- Follow-the-sun eSales from Asia open to NY close; FX is marketed as 24/5.
- Cloud-based architecture is now part of the public FX story (continuous enhancement).

**APAC electronic footprint (important geographically):**

- **eFX hubs**: New York, London, Tokyo, plus a **Singapore pricing/trading engine** at a leading IB (MAS FX hub strategy) — often a fourth global FX hub. Local co-lo, lower latency, NDF algos.
- **Equities algos and Smart Order Router**: hosted in **Hong Kong and Japan** private DCs; HK is co-located with the primary exchange. Direct feeds for HK and Japan; vendor feeds for other APAC exchanges.

So a HK AI Director “starting with FX” is **not** sitting on top of the Singapore matching engine. You sit in **centralised Markets Quant** in HK: the **APAC technical authority** who partners with London GM AI/ML, Singapore eFX **engineering**, and HK/Tokyo desks. Say that — then stop short of pretending you are the engine owner. The seat is explicit: not a software-engineer hire; HFT is optional.

## 4. Org map (roles, not names)

Reporting lines for an HK AI seat are rarely published. Treat these as **seats**, not people to name-drop.

| Seat | Why it matters |
| --- | --- |
| Head of Global Markets | Global P&L owner of the franchise you serve |
| CEO, Asia Pacific | Regional CEO |
| Head of Markets, APAC | Likely a primary **business sponsor**. Often Equities-heavy. Platform + client growth brief. |
| Global Head of AI/ML, Global Markets (usually London) | Building the **new GM AI/ML team**. Public themes tend to be LLMs, e-trading, recommenders, **deep hedging**, responsible AI. |
| AI/ML & Quant Engineering, Markets (London) | Engineering counterpart: LLM FX chatbot, recommenders + RAG, time-series alpha, MLflow, SageMaker/AWS. |
| Front-office AIML quants in London | Signals the global team is being staffed with **research-grade** people, not only engineers. |
| APAC Head of Quant & Product (HK) — Equities algorithmic trading | A core **internal client**: algo design, microstructure, kdb+/R/Java. |
| Quant Prime Services (HK) | A core **internal client** on prime / low-latency equities / QPS. |

**Implication:** first allies are **eFX + eSales** (PnL, desk assistant already in production at several houses) and **HK Equities/Prime quants** (APAC growth). Sequence: **FX proof of concept**, then scale. Do not pick a fight between FX and Equities. Do not staff this as an engineering org.

Behavioural language that plays at a leading IB without sounding like a poster:

- Risk and controls, change and transformation, business acumen, strategic thinking, technology.
- People-leader craft: listen, energise, align across the enterprise, develop others.

## 5. Industry: what “AI for Markets” means in 2026

Sell-side Markets AI has split into four stacks. A Director who conflates them fails the technical case.

| Stack | Job | Failure mode |
| --- | --- | --- |
| **Pricing / internalization / eFX** | Fair value, skew, toxicity, last-look policy, inventory, hedge, RFQ win-rate | Look-ahead, regime break, toxic flow, overfit microstructure |
| **Execution / algos** | Arrival, POV, IS, NDF algos, SOR, child-order placement | Ignoring market impact, venue fees, information leakage |
| **Distribution / sales** | Next-best product, client propensity, RFQ routing, research-to-sales, desk assistant | Recommending products the desk cannot risk; fairness/conduct |
| **Workflow / GenAI** | Trade initiation, TCA narrative, research search, code assist | Hallucinated prices, uncontrolled tool use, data leakage |

Peer pattern (JPM, GS, Citi, MS, BBVA, flow specialists): **tree models and online linear still dominate alpha and pricing**; **DL** wins on limit-order-book images, options surfaces, and hedging policies; **LLMs / agents** win on **interface and workflow**, not on mid. Several banks have already **productised an FX GenAI interface**. The seat wants someone who can run **both** rails: quantitative modelling **and** GenAI/agentic.

APAC-specific market facts the desk will assume you know:

- **CNH vs CNY**, USDCNH as the offshore deliverable, NDFs for KRW, TWD, INR, IDR, PHP.
- Fixings (WMR, local fixes) as **benchmark risk**, not a toy.
- Tokyo/HK/SG session structure; JPY and AUD as G10 in Asia hours; CNH/KRW vol around US-China and local events.
- **Last look**, internalization, markouts (50ms / 1s / 10s), and the optics of those at a leading IB.
- HK as **relationship and equities/prime hub**; Singapore as **eFX engine hub**.

## 6. What the three quant tribes need from you

This is the job. Memorise it. Every technical answer should end with *who consumes it*.

### Researchers (QR)

They need a **research contract**, not a science fair.

- Point-in-time data, as-of joins, corporate-action and fixing calendars.
- Feature store with embargo and purge (no label leakage).
- Experiment tracking (London engineering stories already use **MLflow**).
- Honest metrics: **PnL after costs, capacity, drawdown**, not only AUC.
- A path from notebook → library → shadow → production, with them remaining intellectually in the loop.
- GPU/SageMaker access **without** turning every idea into a six-month cloud programme.
- Permission to publish internally; some of the global heads come from a paper-writing culture.

Your failure mode with researchers: **over-engineering MLOps before a first signal**, or **killing research curiosity** with governance theatre.

### Developers (QD / eTrading / data engineers)

They need **interfaces, SLAs, and boring reliability**. You **partner**; you do not become them. The seat is not hiring a software engineer.

- Stable feature schemas and model contracts.
- Latency budgets when a model **does** sit near the pricing engine: a research ensemble does not belong on the hot path; a distilled linear or small net might. **HFT is optional on your CV** — still know when to hand the last mile to Singapore/HK engine owners.
- Deterministic replay, golden datasets, CI that fails on metric drift.
- Kill switch, canary, dual-run, rollback. Observability: prediction, feature, and PnL dashboards.
- Clear ownership: who gets paged at 3am HK / 3am London.

Your failure mode with developers: **shadow IT notebooks in production**, or **promising to rewrite their engine**.

### Traders (and eSales)

They need **control, narrative, and money**.

- A number they can argue with: mid, skew, edge, confidence, inventory implication.
- Override. If the model cannot be overridden, it will not be switched on.
- Regime flags (“Asia lunch, low volume, widen”).
- Hedging implication, not just a predicted return.
- Client-colour without leaking other clients’ flow (conduct).
- Speed: a 70% model this week beats a transformer next year.

Your failure mode with traders: **black-box theatre**, or **optimising a loss that is not their P&L**.

### How a 4–6 person hybrid team should look (a defensible opening)

The seat wants **AI/ML technical excellence**, not an SE shop.

1. **You** — senior technical authority; hands-on on model #1 (FX forecast / skew).
2. **Applied scientist** — price forecasting / recommenders / decision under uncertainty.
3. **Applied scientist (GenAI/agentic)** — desk-assistant-class tools, RAG, HITL; **fundamentals**, not a research-LLM tourist.
4. **Production-minded quant** — Python, PIT features, working **with** London/SG engineering (registry, shadow). Not “Head of MLOps.”
5–6. **Rotators** from existing HK QR (Equities algo, Prime) as design partners.

Hire **less** than six until a desk is using an artefact. Empty seats beat a tourist team. Matrix in London MLOps rather than cloning it.

## 7. Controls: you will be asked

A leading IB is **PRA-regulated**. HK is an **HKMA authorised** presence. Markets models sit in **model-risk** even when they are “just a pricer”.

**PRA SS1/23** (model risk as a risk in its own right): identification and tiering; governance and SMF accountability; development/implementation/use; independent validation; ongoing monitoring. Explicitly includes **AI/ML**.

**HKMA**: 2019 high-level AI principles (governance, design/development, ongoing monitoring). 2019 BDAI consumer-protection principles (explainability: no “black-box excuse”). 2024 GenAI consumer-protection circular: human-in-the-loop at early deployment, defined scope, hallucination risk, validation. PCPD AI guidance on privacy.

**Conduct**: UK SMCR / Individual Accountability; sales-practice and best-execution for algos; information barriers; client confidentiality in recommenders.

A Director phrase that plays well: *We will not put a model in a higher tier than the decision it influences. A desk assistant that drafts a ticket is not a pricing model. An eFX mid that auto-quotes is.*

## 8. Intellectual fingerprint of a typical GM AI head

Expect questions near this published taste:

- **Recommenders** with multiple stakeholders (client, salesperson, desk risk, inventory) — not YouTube CTR.
- **Bandits / contextual bandits** for execution, pricing exploration, or next-best action.
- **Deep hedging** and friction-aware hedging policies vs Greek matching.
- **Rough vol / non-Markovian** kernels and when ML “lifts” a model to something computable.
- **Fairness / partial debiasing** — in Markets this translates to **conduct, client segmentation, and not systematically disadvantaging a client class**.
- End-to-end: *what changed for the stakeholder?*

Do not name-drop papers unless you can discuss them. Do read at least:

- Buehler, Gonon, Teichmann, Wood — Deep Hedging.
- Lopez de Prado — *Advances in Financial Machine Learning* (purged CV, embargo, CPCV).
- Almgren–Chriss; Avellaneda–Stoikov; Glosten–Milgrom / Kyle.
- Gu, Kelly, Xiu — empirical asset pricing with ML (trees still win a lot of tabular prediction).
- Recent eFX markout / last-look / internalization literature at a conceptual level.

## 9. How to talk about the role in the opening two minutes

A tight script you can adapt:

> A leading IB is investing in a **centralised Markets Quant** AI/ML function. I would be the APAC **Director and senior technical authority** in Hong Kong: a hybrid team of **4–6**, **hands-on** on the first models, **competent at coding and modern GenAI** — not a software-engineering hire, and HFT only if a desk later needs it. The sequence is **FX proof of concept first**, then scale, with a mandate that is deliberately **broad**: quantitative modelling **and agentic/GenAI**. I would land one FX slice the desk can kill (forecasting or skew, measured in markout **and** fill rate) **and** an APAC desk-assistant tool path that never invents a price, under PRA/HKMA tiering. Then I clone the rails for Equities/Prime so APAC Markets has a local Quant AI engine, not a London slideshow.

## 10. Sources (public)

- Typical GM AI/ML Director and modeller postings (London / SG / HK), 2025–2026.
- H1 / Q2 2026 results pattern at a leading IB (GM mix, Equities, Asia, Prime) — read the house you are sitting.
- Public FX platform pages: streaming, RFQ, own-book vs mixed-venue, desk assistants.
- APAC electronic footprint: Singapore FX engines (MAS hub), HK/Japan equities co-lo.
- PRA SS1/23; HKMA 2019 AI principles and 2024 GenAI consumer-protection circular.
