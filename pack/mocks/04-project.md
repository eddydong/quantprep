# Round 4 — Project / case (Director mock)

**8 of 8** in the pack. Previous: [03-coding.md](03-coding.md). Morning of: [../one-pager.md](../one-pager.md).

**Time:** 90 minutes (45 min working + 45 min interrogation)  
**Deliverable:** a structure you could put on one slide pack: problem, options, recommendation, 90-day plan, risks, ask.

This is the round that **hires or kills** a Director. Technical rounds proved you can think. This round proves APAC GM can **give you a team**.

---

## Case: “FX PoC, then the broad mandate”

**Prompt (read slowly, then start the clock).**

> You are the new **Director – Global Markets AI**, Hong Kong. You sit in a **centralised Quant** unit of the Investment Bank that exists **for Markets**. Headcount: **4–6 hybrid**. You are the **senior technical authority**, hands-on where required. The recruiter was explicit: **this is not a software-engineer hire**; coding competence and **GenAI fundamentals** are enough. HFT is **optional**. The team mandate is **extremely broad**: quantitative modelling, **GenAI and agentic** applications. You must **deliver initial use cases in FX as a proof of concept**, then scale across asset classes. London already has a desk assistant in production and SageMaker/MLflow patterns. Singapore hosts the pricing engine. HK/Tokyo host Equities algos. APAC Markets is pushing Equities and Prime.
>
> In 90 days the Global Head of GM AI/ML and the APAC Head of Markets will ask: **what did we turn on, who uses it, and what did it do to PnL and risk?**
>
> Design the programme. You must show **two rails**: (A) FX quantitative PoC (B) GenAI/agentic.

### Suggested structure (use it)

1. **Problem framing** (5 min) — whose pain, why now, why this bank.
2. **Use-case funnel** (10 min) — 8 ideas, kill 5, spike 3, pick 1 production + 1 platform.
3. **Architecture** (10 min) — data, research, shadow, hot path, GenAI vs statistical.
4. **Operating model** (10 min) — team, London/SG/HK RACI, on-call.
5. **Controls** (10 min) — SS1/23, HKMA, conduct, model tiering.
6. **90-day plan** (10 min) — weeks, milestones, metrics.
7. **18-month scaling** (5 min) — Equities/Prime without losing the FX win.
8. **Asks** (5 min) — data, access, air cover.

Interrogation will try to **break** your plan. Invite it.

---

## Interrogation bank (practise out loud)

1. London already has a USDJPY model. Why do we need you?
2. Why not hire six PhDs and publish?
3. Trader says ML is a religion. How do you get a **kill-switch culture**, not a science club?
4. Compliance: your recommender used client chat. What did you ingest?
5. Last-look is in the press again. Does your toxicity model make it **worse**?
6. SageMaker cannot hit our latency. So why did the posting mention it?
7. CNH data cannot leave HK. How do you train?
8. Your markout improved 0.2 bp and fill rate fell 8%. Did you succeed?
9. GPU spend is 4× the PnL. What do you cut?
10. A VP wants to put GPT-4 on the quote stream. You say?
11. Equities quant team already has kdb and Java algos. Do you replace them?
12. How do you staff India (offshore tech centre) vs HK?
13. What is **not** a model under SS1/23 in your estate?
14. Give me a **RACI** for a production incident at 02:00 London / 09:00 HK.
16. We are **not looking for software engineers**. Why did you talk about gRPC and 50µs?
17. HFT is not essential. Can you still be the technical authority?
18. The mandate is **quant modelling and agentic**. You only listed an FX skew model. Where is GenAI?
19. You have been Director 2–3 years. What is **broader** about this remit?

---

## Scoring rubric (grade yourself honestly)

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| **PnL literacy** | Metrics are AUC/accuracy | Mix of ML and desk metrics | Optimises a **costed franchise metric** and names the trade-off |
| **Sequencing** | Boils the ocean | FX listed first | FX **PoC** plus a **GenAI/agentic** rail; then Equities/Prime |
| **Stakeholder map** | “Work with traders” | Names desks | RACI across **London AI, SG eFX, HK QR/Prime, MRM, eSales** |
| **Architecture** | Cloud slogan | SageMaker mentioned | Research vs engine, **and** a GenAI tool path with HITL — you specify, engineering serves |
| **Controls** | “We will be responsible” | Inventory, validation | **Tiering**, HITL for GenAI, kill switch, dual-run, data residency |
| **Team** | Generic org chart | 4–6 roles | AI/ML people who can code; **not** an SE shop; hire less until a user exists |
| **No** | Never kill ideas | Kills DL theatre | Kills **specific** ideas with a reason the desk respects |
| **Voice** | IC who wants headcount | Manager | **Director**: air cover, trade-offs, names what you will not do |

**Pass:** average ≥ 4 and no 1s on PnL, controls, or sequencing.

---

## A strong reference plan (do not memorise; internalise)

### Framing

The bank is building **GM AI/ML as a greenfield** inside **centralised Markets Quant**. The HK Director is the APAC **senior technical authority**: FX **PoC** first, then scale, with a mandate that is **quant modelling + GenAI/agentic**. You translate desk pain into **tiered** models existing QR/QD/traders will **use**. You work **with** engineering. You do not replace the pricing engine or HK Equities Java, and you do not staff an SE org.

### Funnel (example)

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

### Architecture

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

### Team (first 90 days)

- You — senior technical authority, hands-on on FX model #1.
- 1 applied scientist (forecasting / recommenders / uncertainty).
- 1 applied scientist (GenAI/agentic fundamentals) **once** Compliance has scoped tools — can be week 3, not day 90.
- 1 production-minded quant working **with** London/SG engineering.
- 0.5 London MLOps (matrix), 0.5 HK QR design partner.

Do not hire a software-engineering org. The seat forbade that identity.

### Controls

- Inventory all artefacts on day 30.
- **Tier 0** workflow (assistant) vs **Tier 1+** if auto-skew.
- Dual run, kill switch, session-level fallback.
- CNH: train **in-region** if required; no raw ticks in an unconstrained London notebook.
- GenAI: scope written; no RAG over other clients.

### 90-day calendar

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

## Mini-cases (if they pivot)

Sit these in 20 minutes each after the main case.

**M1. The researcher’s notebook is in production.** Overnight job on a desktop, no tests, making money. What do you do in week 1 vs week 8? (Do not kill PnL on day one; wrap, test, dual-run, then retire the desktop.)

**M2. Prime wants an LLM over client inventory.** Conduct, information barriers, who the user is, why a **constrained tool** beats a chatbot.

**M3. Build vs buy.** Vendor claims 20 bp TCA improvement. How you trial (A/B, capacity, last-look policy alignment, data egress, kill).

**M4. Incident.** Model widened everyone at Tokyo open, franchise volume collapsed. Walk the **bridge**: detect, kill, fallback, client comms, post-mortem, who speaks.

---

## Behavioural extras

Prepare STAR stories mapped to **challenge, drive, align, develop, stewardship**:

- **Challenge:** you stopped a launch; the number looked good.
- **Drive:** you landed a model through MRM.
- **Align:** you sat between two desks who wanted opposite loss functions.
- **Develop:** someone you hired or grew.
- **Stewardship:** client confidentiality or a conduct near-miss.

Keep each story **90 seconds**, with a **metric** and a **control**.
