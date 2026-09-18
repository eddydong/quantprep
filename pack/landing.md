# First 90 days — how you would start

**Not one of the four technical rounds.** Previous: [briefing.md](briefing.md). Next: [study-plan.md](study-plan.md). The technical project mock is [mocks/04-project.md](mocks/04-project.md).

Use this when they ask *how you would land*, in a fit conversation, or in the opening two minutes. Do **not** walk this into the project-based technical as if it were the case.

---

## What “started well” means

The bank is building **GM AI/ML as a greenfield** inside **centralised Markets Quant**. The HK Director is the APAC **senior technical authority**: FX **PoC** first, then scale, with a mandate that is **quant modelling + GenAI/agentic**. You translate desk pain into **tiered** models existing QR/QD/traders will **use**. You work **with** engineering. You do not replace the pricing engine or HK Equities Java, and you do not staff an SE org.

In 90 days the Global Head of GM AI/ML and the APAC Head of Markets will ask: **what did we turn on, who uses it, and what did it do to PnL and risk?**

Two rails: (A) FX quantitative PoC (B) GenAI/agentic.

---

## Funnel

**Kill now**

- Transformer on raw mid returns.
- Live RL on the pricing engine.
- Unconstrained LLM prices.
- Firm-wide “AI platform” with no user.

**Spike (4 weeks, two people)**

1. **FX statistical PoC:** toxicity / markout or RFQ win-rate for USDCNH + USDJPY Asia sessions.
2. **GenAI/agentic PoC:** desk-assistant tools for APAC hours (`get_mid`, `get_skew`, draft ticket) — never invented numbers; HKMA HITL.
3. Logging: if RFQ propensities are missing, the spike **is** the log.

**Production (one statistical + one workflow, different tiers)**

- **Skew assistant** (trader or rules commit). Metric: 1s/10s markout **and** fill ratio.
- **Agentic ticket draft** that can only **call** the pricer. Separate, lower model tier.

**Platform (must ship with it)**

- Point-in-time feature spec + golden ticks + MLflow registry + shadow harness that Equities can clone.

---

## Architecture

```
Desks (HK) ── pain, override, colour
   │
Research (HK Python, SageMaker) ── train, CPCV, notebooks
   │  feature spec + golden tests
Feature / model registry (London MLOps patterns)
   │
Shadow book ── dual run
   │
Hot path (SG pricing engine / HK algo box) ── distilled model or rules
   │
Desk assistant (workflow) ── tools to mid/skew; HITL
```

---

## Team (first 90 days)

- You — senior technical authority, hands-on on FX model #1.
- 1 applied scientist (forecasting / recommenders / uncertainty).
- 1 applied scientist (GenAI/agentic fundamentals) **once** Compliance has scoped tools — can be week 3, not day 90.
- 1 production-minded quant working **with** London/SG engineering.
- 0.5 London MLOps (matrix), 0.5 HK QR design partner.

Do not hire a software-engineering org. The seat forbade that identity.

---

## Controls

- Inventory all artefacts on day 30.
- **Tier 0** workflow (assistant) vs **Tier 1+** if auto-skew.
- Dual run, kill switch, session-level fallback.
- CNH: train **in-region** if required; no raw ticks in an unconstrained London notebook.
- GenAI: scope written; no RAG over other clients.

---

## 90-day calendar

| Week | Outcome |
| --- | --- |
| 1–2 | Stakeholder map; data access; model inventory; pick pair/session |
| 3–4 | PIT audit; leakage tests; baseline linear/GBDT |
| 5–6 | Shadow book live; trader override UX with eSales/eFX |
| 7–8 | CPCV + costed metrics; MRM pre-read; desk-assistant tool spec |
| 9–10 | Canary one pair/session; kill criteria signed |
| 11–12 | Review with London + APAC Markets: **on/off**, Equities clone plan |

### 18 months

Same **feature + shadow + registry** pattern for **HKEX algo fill probability** and a **Prime client-flow / utilisation** tool. Do not start those until FX canary is boring.

### Asks

- Tick + RFQ + markout access with a **named data owner**.
- Intro to SG pricing-engine engineering and HK Equities quant.
- MRM fast-track for **Tier 1 skew assistant**.
- Air cover to say no to a firm-wide LLM demo week 3.

---

## Fit questions that belong here, not in the technical case

Practise these out loud **after** you can walk the 90-day page. They are programme / identity questions.

1. London already has a USDJPY model. Why do we need you?
2. Why not hire six PhDs and publish?
3. How do you staff India (offshore tech centre) vs HK?
4. Equities already has kdb and Java algos. Do you replace them?
5. We are **not looking for software engineers**. Why did you talk about gRPC and 50µs?
6. HFT is not essential. Can you still be the technical authority?
7. You have been Director 2–3 years. What is **broader** about this remit?
8. Give me a **RACI** for a production incident at 02:00 London / 09:00 HK.

---

## Behavioural extras

Prepare STAR stories mapped to **challenge, drive, align, develop, stewardship**:

- **Challenge:** you stopped a launch; the number looked good.
- **Drive:** you landed a model through MRM.
- **Align:** you sat between two desks who wanted opposite loss functions.
- **Develop:** someone you hired or grew.
- **Stewardship:** client confidentiality or a conduct near-miss.

Keep each story **90 seconds**, with a **metric** and a **control**.
