# Jargon used in this pack

**1 of 8** in the pack. Next: [seat.md](seat.md).

Read this **before** Briefing if you are not from markets. Every term below appears later in this page.

How to use it: read **section 0** once (the picture). Then skim the section that matches the round you are sitting. Search the A–Z list at the end when a mock drops a word you do not know.

---

## 0. The picture in one trade

A **Global Markets** desk at a bank does two jobs at once:

1. **Show a price** so a client can buy or sell (spot dollars for offshore yuan, a stock, a bond…).
2. **Manage the leftover risk** after the client trades — the bank is now long or short something.

A simplified FX example:

- The bank **quotes** USDCNH **7.7800 bid / 7.7804 ask**.
- **Bid** = price at which the bank will **buy**. **Ask** = price at which it will **sell**. The gap is the **spread** (here 4 **pips**).
- **Mid** is the midpoint, 7.7802. That is the “fair” number people argue about; it is not what the client pays.
- A corporate treasurer **lifts the ask** (buys CNH from the bank). The bank is now **short CNH** — that leftover is **inventory**.
- One second later, the market mid is 7.7810. The bank is short something that just got more expensive. That one-second move against the fill is a **markout**. Repeated markouts from the same clients are **toxic flow** / **adverse selection**.
- The trader **widens** (makes the spread larger) or **skews** (makes one side worse) so the next informed client is less likely to pick them off. They may also **hedge** (buy CNH back in another market).
- If this happens electronically on **the e-trading platform**, it is **eFX**. If a salesperson emails a **request for quote (RFQ)**, a human or a model still has to answer with a price.

Almost every jargon word in this pack is a name for a piece of that loop: the **price**, the **leftover risk**, the **client**, the **machine that shows the price**, or the **test that says the model is not cheating**.

Your job in the interview is not to *be* the trader. It is to build ML that this loop will **turn on**: a number they trust, a **kill switch**, and a metric in **PnL** (profit and loss), not in Kaggle AUC.

---

## 1. A leading IB, the franchise, the people

| Term | Plain English | Why it is in the pack |
| --- | --- | --- |
| **Investment Bank (IB)** | The part of the bank that serves companies and investors, not UK current accounts. Global Markets sits inside it. | Your customer is IB / GM, not the retail bank. |
| **Global Markets (GM)** | Sales and trading: prices, liquidity, hedging, financing for institutions. | The organisation you serve. |
| **Franchise** | The client relationships and the flow they send the bank, not a McDonald’s. “Protect the franchise” = do not chase 0.1 bp of trading profit if you lose the client. | Project round: fill rate vs markout is a franchise trade-off. |
| **FICC** | **F**ixed **I**ncome, **C**urrencies, **C**ommodities — bonds, rates, FX, credit, etc. | H1 2026 still the larger GM slice. |
| **Equities** | Stocks, equity derivatives, electronic cash trading, parts of prime. | The growth story in recent prints at a leading IB. |
| **Macro** | Rates + FX (and sometimes commodities) as one family. | FX sits in Macro. |
| **Credit** | Corporate bonds and credit derivatives. | Part of GM; not the first 90-day use case. |
| **Prime / Prime Services / QPS** | Financing and services for hedge funds: borrow stock, leverage, clearing, low-latency access. **QPS** = quantitative prime services. | HK has a Prime quant bench; APAC growth is partly here. |
| **DMA** | Direct market access — the client’s order hits the exchange through the bank’s pipes. | Prime / equities electronic. |
| **Intermediation vs financing** | **Intermediation** = trading/spreads. **Financing** = lending, prime, repo — more stable revenue. | the bank strategy mix; do not talk as if only spread capture exists. |
| **RoTE** | Return on tangible equity — profit versus the capital the desk consumes. | IB metric; not a model metric. |
| **Greenfield** | A new team with no legacy product to babysit (yet). | The GM AI/ML function. |
| **Centralised Quant** | A Quant group that sits in the IB and serves Markets desks, rather than reporting into a single trading desk or into CIB Tech. | Where this Director role sits. |
| **Senior technical authority** | The person in the room who can still be wrong about a model and be believed — hands-on, not a pure manager. | The typical seat’s words for you. |
| **Agentic** | A GenAI system that **calls tools** (get mid, draft ticket) in a loop, rather than only writing text. | On the typical seat as part of a “broad mandate.” |
| **PoC / proof of concept** | A first use case that is real enough to learn from, then scale. | “Initial use cases within FX.” |
| **TTC / total comp** | Base + bonus + anything else in the year. | Recruiter language, not a number here. |
| **QR / QD** | **Quant researcher** (signals, models) vs **quant developer** (production code, data, latency). | The two tribes besides traders. |
| **Trader / eSales / eTrading** | **Trader** owns the book. **eSales** covers electronic clients. **eTrading** is the electronic platform team. | Your users. |
| **Desk** | The team that owns a product’s risk (eFX desk, equities algo desk). | “The desk will not turn it on” is a real veto. |
| **VP / Director** | Bank titles. VP is senior IC or small-team lead. **Director** is people + P&L/programme ownership. | You are interviewing Director. |
| **RACI** | Who is **R**esponsible, **A**ccountable, **C**onsulted, **I**nformed. | Project round. |
| **People-leader craft** | Listen, energise, align across the enterprise, develop others. | Behavioural round. |
| **Behavioural themes** | Risk and controls, change, business acumen, stewardship. | Closing interviews. |
| **offshore tech centre** | India / nearshore tech and ops bench. | “How do you staff India vs HK?” |
| **Hybrid team** | Some London, some HK, maybe SG; not all in one room. | 4–6 headcount. |

---

## 2. Prices, books, and how the desk gets paid

| Term | Plain English | Why it is in the pack |
| --- | --- | --- |
| **PnL** | Profit and loss. The only scoreboard that counts on a desk. | Optimise this (after costs), not AUC. |
| **Quote** | The live bid and ask you show. | Models that “price” usually **change the quote**. |
| **Bid / ask (offer)** | Buy price / sell price of the *dealer*. | Coding mock quotes. |
| **Mid** | Average of bid and ask, or a model’s fair value. | Predicted “mid” is a common ML target. |
| **Spread / half-spread** | Ask minus bid. Half-spread is the cost to trade one way vs mid. | Wider = safer for the bank, worse for the client. |
| **Pip / pipette** | FX tick: in USDCNH, 0.0001 is often a pip. | “2 bp” is a size of edge. |
| **Basis point (bp)** | 0.01%. 1 bp of USD 100m = $10,000. | “Markout improved 0.2 bp.” |
| **Inventory** | The bank’s leftover position after client trades. | Skew and Avellaneda quotes exist to dump inventory. |
| **Skew (quoting)** | Make bid and ask **asymmetric** so you attract the side you want. Not the options “skew” unless said in an options sentence. | First FX use case: skew assistant. |
| **Widen / tighten** | Increase / decrease the spread. | Toxicity model output. |
| **Fill / fill rate** | A quote that actually trades. Fill rate = how often you get hit. | Trade-off vs markout. If you never get filled you “won” on toxicity and lost the franchise. |
| **Hedge** | Offset the inventory in another instrument or venue. | Deep hedging = a learned hedge policy. |
| **Greeks / delta** | Sensitivities of an option price (delta ≈ how much the option moves when the underlying moves). | Risk still wants Greeks even if a neural net hedges. |
| **Markout** | How the mid moved **after** you filled, at 50ms / 1s / 10s. Positive for you = you captured spread; negative = you were picked off. | The desk metric for a toxicity model. |
| **Toxicity / toxic flow** | Flow that systematically markouts against you — often faster or better-informed clients. | Core eFX ML problem. |
| **Adverse selection** | The people who choose to trade with you know more than you. | Same idea as toxicity, older name. |
| **Last look** | On some FX streams the bank can **reject** a trade after the client clicks, if the market moved. Controversial. | A toxicity score used as last-look is a conduct + press problem. |
| **Internalization** | Fill the client against the bank’s own book instead of sending to the market. | Quality of internalization is a PnL + franchise metric. |
| **TCA** | Transaction cost analysis — did the client get a good deal vs a benchmark? | Vendor claims; eSales analytics. |
| **Slippage** | You wanted 100 at 10.00 and got 10.03. | Execution algos. |
| **Capacity** | How large a signal or algo can be before it eats itself. | Researchers over-claim; Directors ask this. |
| **Override** | Trader ignores the model. | If they cannot override, they will not switch it on. |
| **Kill switch** | Instantly disable the model and fall back to a dumb/safe policy. | Non-negotiable in the project round. |
| **Shadow book / paper book** | Model runs as if live but **does not** quote. You compare would-have PnL. | 90-day milestone. |
| **Dual-run** | Old and new models run together. | SS1/23-friendly go-live. |
| **Canary** | Turn on for a tiny slice (one pair, one session, one client tier). | Weeks 9–10. |
| **Fallback** | What you do when the model is sick: last approved model, or a wide conservative quote. | Incident answer. |
| **Session** | Tokyo / HK / London / NY hours. Tokyo lunch is famously thin. | “London model fails in Asia.” |
| **Tick / bar** | A tick is one market-data update. A **bar** is a bucket (1-second, 1-minute OHLC). | Coding: no look-ahead across bars. |
| **Tick size** | Minimum price increment. | Microprice/OFI break if you ignore it. |
| **Notional** | Face amount of the trade (USD 10m). | Size-weights markouts. |
| **Book** | The book of positions, or the **order book** (see LOB). | Context decides. |

---

## 3. Products (what the client trades)

| Term | Plain English | Why it is in the pack |
| --- | --- | --- |
| **Spot** | Exchange two currencies now (in FX, “now” is T+1 or T+2). | Core eFX. |
| **Forward** | Agree a rate today, exchange later. Price mostly from **interest-rate differential**, not a forecast. | FX product set. |
| **Swap (FX)** | Spot + forward in opposite directions; a funding product. | the FX platform product list. |
| **NDF** | **Non-deliverable forward** — settle the difference in USD; used when the currency does not fully deliver offshore (KRW, TWD, INR, IDR, PHP…). | APAC FX; Singapore NDF algos. |
| **NDS** | Non-deliverable swap. | FX platform product list. |
| **Option / vanilla / exotic** | Right to transact at a strike. **Vanilla** = call/put. **Exotic** = barriers, touch, etc. | Recommenders: which product to show. |
| **ATM** | At-the-money option (strike near spot). | Deep-hedging toy tenor. |
| **25d RR** | 25-delta **risk reversal** — a quote of call vs put vol; the market’s “skew” in the **options** sense. | Vol-surface research; not first 90 days. |
| **Vol / implied vol / vol surface** | **Vol** = how much it moves. **Implied vol** = vol baked into option prices. **Surface** = that number by strike and maturity. | DL on surfaces; no-arbitrage constraints. |
| **G10 vs EM** | G10 = most liquid currencies (USD, EUR, JPY, GBP, CHF, CAD, AUD, NZD, NOK, SEK — lists vary). **EM** = emerging-market currencies, often NDFs. | CNH/KRW ≠ EURUSD. |
| **Pair** | USDCNH, USDJPY — always **base/quote** convention. | Per-pair vs global model. |
| **Algo (execution)** | Software that slices a large order over time (VWAP, POV, implementation shortfall). | Equities HK; FX NDF algos. |
| **IS / POV / arrival** | **Implementation shortfall** = vs arrival price. **POV** = percent of volume. **Arrival** = the first mid you saw. | Execution objectives. |
| **Child order** | One slice of a parent algo order. | RL vs Hawkes child-order policy. |

---

## 4. FX in Asia (the local dialect)

| Term | Plain English | Why it is in the pack |
| --- | --- | --- |
| **CNY vs CNH** | **CNY** = onshore mainland yuan. **CNH** = offshore (HK) yuan, the one international banks trade more freely. | USDCNH is the first-pair example. |
| **USDCNH / USDJPY / USDKRW** | Dollar versus those currencies. | Specialists vs global backbone. |
| **Fixing** | An official or WM/Refinitiv snapshot used to settle benchmarks and some corporate orders. | Turn models **off** or special-case around fixes. |
| **WMR** | WM/Refinitiv 4pm London FX fix — huge fixing. | Calendar feature. |
| **Tokyo fix / CNY fix** | Local benchmark prints. | Same. |
| **Carry** | Earn the interest differential by holding a currency. | Macro colour, not a model. |
| **PBOC** | People’s Bank of China. | CNH regime shifts. |
| **Data residency** | Some data (sometimes CNH-related, always client) must stay in-region. | “CNH cannot leave HK.” |

---

## 5. Electronic trading and the e-trading platform

| Term | Plain English | Why it is in the pack |
| --- | --- | --- |
| **e-trading platform** | The bank's cross-asset electronic trading surface. | Your production surface. |
| **pricing engine** | The local **pricing engine** (Singapore for APAC FX) — ultra-low-latency quotes. | Hot path. Not SageMaker. |
| **desk assistant** | GenAI assistant on the FX platform to help **initiate** trades. Already in production at several houses. | Workflow/LLM case; **must not invent mids**. |
| **own-book fill** | Execute against **the bank's own** liquidity. | Principal risk. |
| **mixed-venue execution** | Mix the bank's liquidity with **external** venues. | Different toxicity mix. |
| **Manual / benchmark orders** | Route to a human trader, or target a fix. | Fallback. |
| **Streaming vs RFQ** | **Streaming** = live bid/ask always on. **RFQ** = client asks “price me 50m.” | Different models and logs. |
| **FIX** | A standard protocol for orders. | How machines connect. |
| **MDP** | Multi-dealer platform (Bloomberg, FXall, 360T). | Client access. |
| **eFX** | Electronic FX market making and execution. | First use-case franchise. |
| **SOR** | Smart order router — decides which exchange/venue to send an equities order to. | HK/Tokyo hosting. |
| **Co-lo / co-location** | Servers **in the same building** as the exchange. | HK Equities; latency. |
| **Latency / hot path / 50µs** | **Latency** = delay. **Hot path** = the code that must answer in microseconds or milliseconds. 50µs = 0.00005 seconds. | Why GBDT in Python is not on the pricing engine. |
| **Distil** | Train a big model, copy its behaviour into a tiny fast one. | Research vs hot path. |
| **kdb+ / q** | Column-store time-series DB used on many trading floors. **q** is its language. | HK Equities quants. |
| **LOB / limit order book** | The ladder of bids and asks at the exchange. | DL-on-images temptation; usually the wrong 90-day plan. |
| **internal crossing book** | Dark / internal crossing and single-dealer equities liquidity. | e-trading Equities. |
| **HKEX** | Hong Kong stock exchange. | Equities algo case. |
| **Follow-the-sun** | Coverage handed Tokyo → HK/SG → London → NY. | eSales. |
| **EMS** | Execution management system — where tickets actually go. | desk assistant → ticket. |

---

## 6. Microstructure words the coding round uses

| Term | Plain English | Why it is in the pack |
| --- | --- | --- |
| **Microstructure** | The physics of *how* trades happen at the tick: queues, spreads, who is informed. | Coding + ML features. |
| **OFI** | Order-flow imbalance — a signed measure of whether the bid or the ask is getting stronger. | Coding problem 2. |
| **Microprice** | Mid weighted by sizes: more size on the bid pulls the “fair” price toward the ask. | Not the same as mid. |
| **EWMA** | Exponentially weighted moving average — yesterday’s value decays, today’s tick matters more. **Causal** = only uses the past. | Fair-value smoother. |
| **Avellaneda–Stoikov** | A classic formula: if you are long, you **lower** both bid and ask so you sell more. **Gamma** = risk aversion; **kappa** = how dense the book is. | Coding problem 3. |
| **Reservation price** | Inventory-adjusted “personal mid.” | Same. |
| **Quotes cross** | Bid above ask — a bug. You must clip. | Coding. |
| **Almgren–Chriss** | Classic **optimal execution** (how to sell a lot without crashing the price). | Bandits for execution live in this family. |
| **Kyle / Glosten–Milgrom** | Theory: the market maker loses to informed flow and survives on noise traders. | Last-look / toxicity conversation. |
| **Hawkes** | A model where events (trades) make more events more likely for a while. | Simple child-order / flow model vs RL. |
| **Information set** | Everything the decision-maker is **allowed** to know at time t. | If the label or a feature is not in the information set, it is cheating. |
| **Look-ahead / leakage** | Using the future (tomorrow’s close, the same-bar return) as if you had it. | The silent way ML “works” and then loses money. |
| **Causal (time)** | Feature at t uses only data ≤ t. Different from **causal inference** (what if we had tightened the spread?). | Both appear; do not mix them up. |

---

## 7. Machine learning as used on a desk

| Term | Plain English | Why it is in the pack |
| --- | --- | --- |
| **Label / horizon** | What you predict, and **how far ahead**. A 1-second mid-move label uses the next 1 second of data. | Overlap → purge. |
| **Feature store / PIT / as-of join** | A library of features computed as they would have been **at that timestamp**. **Point-in-time (PIT)** = no restated history. **As-of join** = “last value known at t.” | Researchers and Java must share this. |
| **Walk-forward** | Train on the past, test on the **next** block of time. Never shuffle rows. | ML round. |
| **Purge / embargo** | Delete train samples whose label window **overlaps** the test window, plus a gap (**embargo**) around it. | Lopez de Prado; coding problem 1. |
| **CPCV** | Combinatorial purged CV — many different holdout combinations so you get a **distribution** of Sharpes, not one lucky year. | Go-live gate. |
| **Triple-barrier** | Label: did price hit profit / stop / time-out first? | Lopez de Prado; embargo still needed. |
| **Non-stationarity / regime** | The world changed (Tokyo lunch, PBOC, a new matching engine). Yesterday’s model is the wrong sport. | Fallback > “retrain often.” |
| **Covariate shift** | Input distribution moved. | Same family. |
| **Calibration** | When the model says 30% toxic, it **is** toxic 30% of the time. **AUC** only ranks. Policies need probabilities. | Last-look / widen. |
| **Reliability diagram** | Plot predicted probability vs actual frequency. | Calibration check. |
| **Platt / isotonic** | Two ways to map a score to a probability. Isotonic can overfit small books. | Online calibration. |
| **Brier / logloss** | Proper scores for probabilities. | Monitor these; ship on markouts. |
| **AUC** | How well you **rank** positives vs negatives. Silent on cost and calibration. | The metric trap. |
| **GBDT / LightGBM / XGBoost** | Gradient-boosted decision trees. Default on **tabular** tick features. | “Trees still win.” |
| **SHAP** | Attribution of a prediction to features. **Not** a causal effect. | Do not say SHAP ⇒ “if we tighten, win-rate rises.” |
| **Bandit / contextual bandit / UCB / Thompson** | Learn by **trying** actions (which spread, which product) and seeing reward. Exploration **costs real money**. | multi-stakeholder; recommenders. |
| **IPS / SNIPS / propensity** | Offline estimate of “what if we had shown a different price?” using the **logged probability** of the old policy. If you did not log it, you **cannot** evaluate. | Recommender eval. |
| **Two-tower / FM / CTR** | Recommender architectures. **CTR** = click-through rate — the wrong objective if it dumps risk on the desk. **FM** = factorisation machine. | Multi-stakeholder ranking. |
| **Next-best action** | What the salesperson or bot should do next. | eSales. |
| **Multiple testing / deflated Sharpe** | You tried 400 features; some “work” by chance. Deflated Sharpe haircuts for that. | Kill the researcher’s t>2 fishing. |
| **Sharpe** | Average return / volatility. Easy to fake with leakage or selection. | Report a CPCV **distribution**. |
| **Online learning / freeze** | Updating a **tiny** parameter live vs **freezing** the approved model. Full retrain is often a **new model** for MRM. | B4 in ML mock. |
| **Temperature / intercept** | Small knobs on a frozen classifier to recalibrate. | Allowed-ish intraday update. |
| **VWAP** | Volume-weighted average price. If it includes the **current** bar, it leaks. | A1 in ML mock. |
| **Realised vol** | How much it actually moved. Same-window realised vol can leak the return you predict. | A1. |
| **Class imbalance / focal loss** | Toxic trades are rare. Accuracy of 98% can be a model that never flags toxic. | A9. |
| **Cost-sensitive threshold** | Choose the cut-off using **money**, not F1. | Same. |
| **Hierarchical model** | Shared backbone + per-pair residual. | A10. |

---

## 8. Deep learning and GenAI

| Term | Plain English | Why it is in the pack |
| --- | --- | --- |
| **DL / net / transformer / LSTM / TCN** | Deep nets. **Transformer** = attention. **LSTM** = old sequence net. **TCN** = causal convolutions over time. | Usually **lose** to trees on raw FX returns. |
| **Receptive field** | How far back a causal net can see. If it sees through an **unpublished fix**, that is leakage. | A2 in DL mock. |
| **Teacher forcing** | Train the net on **true** past labels; live it must eat **its own** outputs. Gap = it falls apart live. | DL MCQ. |
| **Batch-norm (BN)** | Normalise using **batch** statistics. A live tick is not a training batch; sessions mix. | Do not use on eFX streams. |
| **LayerNorm / RMSNorm** | Normalise within the vector; more internable online. | Replacement. |
| **Attention ≠ causality** | Weights in a fitted average, not “this tick **caused** CNH.” | Trader explanation trap. |
| **Deep hedging** | Train a **policy** (what to buy/sell each step) to a **risk measure** of final P&L, with spreads and gaps, instead of copying Black–Scholes delta. | DL case. |
| **CVaR / expected shortfall** | Average of the **worst** tail of losses. A typical deep-hedge objective. | Same. |
| **Greeks-free** | The policy does not explicitly target delta. Risk will still **ask** for Greeks. | Say no to replacing the engine before shadow. |
| **RL / PPO / CQL / IQL / offline RL** | Reinforcement learning. **PPO** = a common **live-interaction** algorithm — **not** for live FX. **CQL/IQL** = **offline** (learn from logs). | Sim-to-real gap; need logged propensities. |
| **Sim-to-real** | Simulator ≠ the market. | Why RL stays in the lab. |
| **Policy** | A mapping from state → action (hedge, child order, spread). | Different from a **score**. |
| **LLM / GenAI / agentic** | Language models; generative AI; **agentic** = the model calls **tools** in a loop. | desk assistant. |
| **RAG** | Retrieval-augmented generation: search docs, then write. Failure = **wrong or leaked** docs, stale numbers. | No RAG over other clients’ tickets. |
| **Vector DB / Bedrock / SageMaker** | Vector DB stores embeddings for RAG. **Bedrock** = AWS hosted foundation models. **SageMaker** = AWS train/serve for *research-speed* ML. | Research-speed path; not the 50µs path. |
| **Hallucination** | Fluent, wrong. A **made-up mid** is a trading incident. | Tools for numbers. |
| **HITL** | Human-in-the-loop. | HKMA GenAI. |
| **Fine-tune vs prompt vs tools** | Change model weights vs instructions vs **calling** `get_mid()`. | Prefer tools for prices. |
| **DeepBSDE / operator net** | Nets that solve pricing PDEs/BSDEs. | Research, not Q3 desk widget. |
| **MC-dropout** | Dropout at **predict** time for uncertainty. Usually too slow / unapproved at quote time. | DL MCQ. |
| **No-arb / butterfly / calendar** | Option prices cannot allow riskless profit. A VAE on a vol surface must **project** back onto those constraints. | DL B3. |
| **Two-speed** | Slow cloud research vs **hot** engine. Same tests. | Architecture. |

---

## 9. Production, MLOps, controls

| Term | Plain English | Why it is in the pack |
| --- | --- | --- |
| **MLOps** | The plumbing: train, register, deploy, monitor, roll back. | London engineering. |
| **MLflow** | Experiment + **model registry** (which binary is approved). | engineering's stack. |
| **Feature hash** | A fingerprint of the feature code the model was trained on. Pin it. | B2. |
| **Golden ticks / golden dataset** | A frozen replay file. If the engine changes, tests fail. | LOB upgrade story. |
| **CI** | Automated tests on every change. | Venue-change tests. |
| **On-call** | Who gets paged at 3am. | RACI. |
| **Model inventory / tiering** | The list of models and **how dangerous** each is (chatbot draft vs auto-skew). | SS1/23. |
| **MRM** | Model risk management team — independent challengers. | You partner; you do not “self-validate.” |
| **SS1/23** | UK PRA rules: model risk is its **own** risk. Identify, govern, develop, validate, monitor. Includes AI/ML. | Project controls. |
| **PRA / HKMA / PCPD / SFC** | UK bank supervisor; HK banking supervisor; HK privacy commissioner; HK markets regulator. | Dual-hat: UK group + HK entity. |
| **SMF / SMCR** | UK senior manager functions / conduct regime. Someone **named** owns model risk. | “Who is accountable?” |
| **Conduct** | Treating clients fairly; no abuse of information. | Recommenders, last-look, chat RAG. |
| **Information barriers / walls** | You must not use Client A’s confidential flow to price Client B. | Prime LLM mini-case. |
| **Model change vs parameter update** | Retraining trees = often a **change**. Tweaking an intercept may be a **parameter**. Agree this **in writing** with MRM. | B4. |
| **gRPC / REST / schema registry** | How services talk; how feature layouts stay compatible. | QD needs. |
| **Observability** | Logs of predictions, features, PnL. | Incident. |

---

## 10. Papers and names dropped as if everyone had read them

| Term | Plain English | Enough to say |
| --- | --- | --- |
| **Lopez de Prado** | *Advances in Financial Machine Learning* — purged CV, embargo, CPCV, triple-barrier. | “We will not shuffle financial labels.” |
| **Buehler et al.** | Deep hedging paper. | Policy + frictions + risk measure. |
| **Gu–Kelly–Xiu** | Empirical result: trees beat many fancy models on **tabular** return prediction. | Defend GBDT. |
| **Black–Scholes** | The textbook option formula in a frictionless world. | Deep hedge exists because that world is false. |

---

## A–Z jump list

Adverse selection · Agentic · Algo · Almgren–Chriss · Ask · ATM · Attention · AUC · Avellaneda–Stoikov · Bandit · e-trading platform · pricing engine · desk assistant · Batch-norm · Bedrock · Bid · bp · Brier · Calibration · Canary · Centralised Quant · Child order · CNH / CNY · Co-lo · Conduct · CPCV · CQL / IQL · CTR · CVaR · Deep hedging · Desk · Distil · DMA · Dual-run · eFX · eSales · Embargo · eTrading · EWMA · Exotic · Fallback · Feature store · FICC · Fill rate · FIX · Fixing · Franchise · G10 · GBDT · Greeks · Greenfield · Hallucination · Hawkes · Hedge · HITL · Horizon · Hot path · HKEX · HKMA · Information set · Internalization · Inventory · IPS · IS · kdb+ · Kill switch · Label · Last look · Latency · Leakage · People-leader craft · LLM · LOB · Lopez de Prado · Macro · Markout · MDP · Microprice · Mid · MLflow · MLOps · MRM · NDF · Next-best action · OFI · Offline RL · Override · PIT · Platt · PnL · PoC · POV · own-book fill · PPO · PRA · Prime · Purge · QPS · QR / QD · Quote · RACI · RAG · RFQ · Regime · Receptive field · Reservation price · RL · RoTE · SageMaker · Session · SHAP · Shadow book · Sharpe · Senior technical authority · Skew · Slippage · SMCR · SOR · Spot · Spread · SS1/23 · Streaming · TCA · Teacher forcing · Tick · Tiering · Tokyo lunch · Toxicity · Transformer · Triple-barrier · TTC · Two-tower · Vanilla · Vector DB · Vol surface · VWAP · Walk-forward · WMR · Widen

If a mock uses a word that is still opaque, pause and redefine it in the interview. Directors who translate for the trader outperform Directors who only perform fluency.
