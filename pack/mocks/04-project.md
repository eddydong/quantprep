# Round 4 — Project / scenario (technical)

**8 of 8** in the pack. Previous: [03-coding.md](03-coding.md). How you’d start the job: [../landing.md](../landing.md). Morning of: [../one-pager.md](../one-pager.md).

**Time:** 90 minutes (45 min working + 45 min interrogation)  
**Deliverable:** a diagnosis and a technical recommendation you could defend at a whiteboard: decision, information set, metrics, model, serving, what you would not do, kill criteria.

This is still a **technical** round. It is not a 90-day org plan, a hiring deck, or “how I would start as Director.” That material lives in [Landing](../landing.md). Here they put a **messy live problem** in front of you and listen for whether you can think like the senior technical authority.

---

## Case: the toxicity score that “worked”

**Prompt (read slowly, then start the clock).**

> APAC eFX streams **USDCNH** on the e-trading platform during the Asia session. Six weeks ago a **GBDT toxicity score** went live: if `P(toxic) > 0.6` the engine **last-looks or widens**. A researcher reported **AUC 0.71** on a **random 70/30 split**. The model **retrains every night on yesterday’s fills**. The score is fit in Python on **SageMaker** and pushed toward the **pricing engine**; eFX says the engine budget is about **80µs**.
>
> Since go-live:
> - 1-second **markout improved 0.2 bp**
> - **fill rate fell 8%**
> - CNH **corporate** flow in the London/Asia overlap **collapsed**
> - a salesperson: “the model hates our franchise clients”
> - Compliance asks whether **last-look is now worse for one client class**
>
> eSales also wants the **desk assistant to tell the client why we widened**, live.
>
> Diagnose. Then propose what you would **measure**, what you would **change** (label, split, model, threshold, serving), what you would **not** do, and how you would **know to kill it**. Do not design a 90-day programme or a 4–6 person org chart.

### Suggested structure (use it)

1. **Restate the decision** (5 min) — what the model is allowed to change (last-look / widen / skew), whose PnL, what “good” cannot be.
2. **Diagnose** (15 min) — why the reported AUC can be real and the desk still be losing; leakage; label construction; feedback loops; client mix.
3. **Technical design** (15 min) — information set, validation, metric, model class, calibration, threshold, where inference actually runs.
4. **The desk-assistant ask** (5 min) — tools vs invented prices; tiering; what must not go in the prompt.
5. **Ship / kill** (5 min) — shadow vs canary, fallback quote, signed kill criteria, CNH residency if it bites this pair.

Interrogation will try to **break the diagnosis**. Invite it.

---

## Interrogation bank (practise out loud)

1. AUC 0.71 — why is that the wrong headline?
2. What is wrong with training only on **fills**?
3. Walk the **information set** at quote time vs the label window.
4. How does **last-look** poison the next day’s labels?
5. Markout +0.2 bp, fill −8%. Did you succeed?
6. How would you test “we are disadvantaging a client class”?
7. SageMaker cannot hit 80µs. So what actually ships, and what is SageMaker for?
8. How do you **distil**, and what drift would make you roll back the small model?
9. CNH ticks cannot leave HK. How do you train and validate?
10. The desk assistant explains the widen without inventing a mid or RAG-ing other clients. How?
11. Would you turn **last-look off** and only widen? Why?
12. London has a USDJPY toxicity model. What transfers, and what breaks on USDCNH?
13. A VP wants GPT-4 on the quote stream. You say?
14. What is the **fallback quote** when the kill switch fires?
15. Is the toxicity score a “model” under SS1/23? Is the assistant sentence?
16. How do you A/B when the policy **changes who fills**?
17. Inventory was ignored. How does it enter the decision without turning this into a second pricer you do not own?
18. The desk wants it “fixed this week.” What is the one-week patch vs the real fix?

---

## Scoring rubric (grade yourself honestly)

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| **Diagnosis** | “Retrain a bigger model” | Names one bug | Separates **leakage, selection, metric, policy feedback, client mix** |
| **Information set** | Features listed | Mentions time | Decision time vs label window; no future; embargo |
| **Metric** | AUC / accuracy | Adds markout | **Costed markout and fill / franchise**; threshold as a policy, not a default 0.6 |
| **Model / serving** | Cloud slogan | GBDT mentioned | Offline fit vs **engine budget**; distil or rules; SageMaker is not the hot path |
| **Conduct** | “Be fair” | Mentions last-look | **Client-class rates**, last-look optics, no protected-class proxies |
| **GenAI** | Chatbot on prices | “Don’t hallucinate” | **Tools** to mid/skew/reason-code; HITL; **different tier** from the toxicity model |
| **Kill** | Hope | Kill switch named | Fallback quote, dual-run, signed off-criteria, residency |
| **Voice** | Strategy deck | Mix of org and tech | **Technical case**: you would change *this*, not hire a team |

**Pass:** average ≥ 4 and no 1s on diagnosis, metric, or information set.

---

## A strong reference (do not memorise; internalise)

### Restate

The model is not “predicting toxicity.” It is a **policy**: last-look or widen on USDCNH streaming. Success is **franchise PnL** — markout **and** fill, by client segment and session — not AUC. Last-look is a conduct surface, not a free option.

### Diagnose (the actual bugs)

- **Random 70/30** on tick data with a forward markout label **leaks**. Overlapping windows, no purge, no embargo.
- **Train on fills only.** Rejects, last-look declines, and “widened so they left” never enter the label. The model is scored on the survivors of yesterday’s policy. Nightly retrain **locks that in**.
- **AUC 0.71** can be true and useless. The desk uses a **threshold**. They need **calibration** (reliability by session/size) and a **costed** threshold: expected markout saved vs franchise fill lost.
- **+0.2 bp / −8% fill** is not a win by default. Corporate CNH in overlap is exactly the franchise they cannot scare. Segment the metric: HF vs corporate, overlap vs Tokyo morning, size buckets.
- **Last-look as a function of a score** changes who gets filled, which changes tomorrow’s training mix — a **feedback loop**. It can also look like systematically worse treatment of a client class.
- **SageMaker → 80µs** is a category error. The engine cannot wait on a Python GBDT in the cloud. Offline research vs distilled linear / small net / rules **on the pricing engine**.

### Technical design

- **Label:** 1s and 10s markout **and** fill, with size; not a binary “toxic” cooked to maximise AUC. If you keep a toxic flag, define it from **post-trade markout given fill**, not from “the last-look fired.”
- **Split:** walk-forward, purge by horizon, embargo. Report a **CPCV distribution**, not one lucky week.
- **Features:** lagged OFI, spread vs session, inventory, time-to-fix, CNH-CNY basis, own last-N markouts, venue mix — all **as-of decision time**. No same-window realised vol of the mid you are defending.
- **Model:** GBDT or penalised linear **offline**. Distil to whatever the engine will take. No transformer on mids. No live RL. No LLM mid.
- **Threshold:** chosen on **costed** shadow PnL, by session, with a cap on fill-rate damage. Override stays with the trader.
- **Serving:** feature contract + golden ticks; inference next to the pricing engine or a pre-computed skew table; SageMaker for fit and batch eval only.

### Desk assistant

Different artefact, **lower tier**. The bot **calls** `get_mid`, `get_skew`, `get_reason_code` (approved vocabulary: “wider because inventory / session / last-look policy”). It does not compute the score, does not RAG other clients, does not invent a number. HITL while client-facing. SS1/23: a drafted sentence is not a pricing model **unless** you let it commit risk.

### Ship / kill

- Shadow the new label/threshold against the live policy **before** touching last-look.
- Canary one session (not all CNH corporates first).
- Kill switch: revert to pre-model widen rules / last-look policy. Fallback must be a **quote**, not “error.”
- Off-criteria signed: fill-rate drop vs a named client segment, or markout worse than baseline, or a client-class reject gap.
- CNH: train in-region if required.

### What you say no to this week

Bigger net. Lower the 0.6 because AUC looked good. GPT on the stream. Replacing the pricing engine. A firm-wide AI platform. Hiring a team to “own the problem” instead of changing the label.

---

## Mini-cases (if they pivot)

Still technical scenarios. Sit these in 20 minutes each after the main case.

**M1. The researcher’s notebook is in production.** Overnight job on a desktop, no tests, making money. What do you do in week 1 vs week 8? (Do not kill PnL on day one; wrap, test, dual-run, then retire the desktop.)

**M2. Prime wants an LLM over client inventory.** Conduct, information barriers, who the user is, why a **constrained tool** beats a chatbot.

**M3. Build vs buy.** Vendor claims 20 bp TCA improvement. How you trial (A/B, capacity, last-look policy alignment, data egress, kill).

**M4. Incident.** Model widened everyone at Tokyo open, franchise volume collapsed. Walk the **bridge**: detect, kill, fallback, client comms, post-mortem — technically, who inspects which log.
