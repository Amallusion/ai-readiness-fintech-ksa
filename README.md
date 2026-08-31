# Sector Digitalization Watch

**ITU AI Readiness Hackathon — Kingdom of Saudi Arabia | Fintech Track | Team Voxel**

A seven-stage machine learning pipeline conforming to ITU-T Y.3172, built on the Saudi Central Bank's own open payments data, that asks whether the national cashless transition has reached the whole economy or only part of it.

---

## Why this project exists

Saudi Arabia reported that 79% of retail transactions were electronic in 2024. It is a good number and it is a real achievement. It is also an average, and an average is a summary of a distribution it does not show you.

So the question we started with was simple: is the remaining 21% spread thinly across the economy, or is it concentrated in a few sectors that have not moved? Those two situations produce an identical headline and require completely different responses. A general awareness campaign is a reasonable answer to the first. It is close to useless as an answer to the second.

Answering that required real technical work, because the pattern is not visible without it. Acting on the answer required real policy reasoning, because a system that identifies underserved sectors is one design decision away from being a system that penalises them. Both halves are in this repository.

---

## What we found

Eight of the sixteen sectors SAMA tracks sat in the bottom growth tier in every one of the five years from 2019 to 2023, without exception. That is a direct observation with no modelling assumptions attached, and it is the most robust result here.

The more interesting question was why, and the answer appears to be transaction value. Sectors where people spend more per purchase digitised more slowly (Spearman ρ = −0.46 across all sixteen sectors, ρ = −0.49 across the fourteen single-purpose sectors, p ≈ 0.07 in both). We present that as a mechanism the data supports rather than an established effect, and Step 4 explains exactly how much weight it will bear.

Jewelry has the highest average ticket size of any retail sector tracked and the lowest growth index at the end of the window. It also sits below what ticket size alone would predict, which is worth saying plainly: transaction value explains part of the gap and something else explains the rest.

---

## The pipeline

| Stage | Node | What it does | Folder |
|---|---|---|---|
| 1 | **SRC** | Structured selection of the data source from nine real candidates, with weights, sensitivity analysis and a retrieval record | `step1-source/` |
| 2 | **C** | Parses SAMA's MHTML export, merges the two series, tags each month with real economic events | `step2-collector/` |
| 3 | **PP** | Validates the merged data and rebases every sector to its own baseline so sectors of different sizes can be compared fairly | `step3-preprocessor/` |
| 4 | **M** | Clustering, ticket-size regression, and the diagnostics that show how much each result can bear | `step4-model/` |
| 5 | **P** | Four independent policy layers, each grounded in a named document, one of which cannot fire by construction | `step5-policy/` |
| 6 | **D** | Fans one decision into three packets addressed to three separate institutions | `step6-distributor/` |
| 7 | **SINK** | Bilingual, role-based dashboard where the output finally reaches a person | `step7-sink/` |

Each folder runs independently and reads its input from the previous stage's output, so the whole pipeline is reproducible end to end from the two original SAMA downloads.

---

## Running it

```bash
pip install pandas numpy scipy scikit-learn matplotlib

cd step2-collector    && python3 collector.py
cd ../step3-preprocessor && python3 preprocessor.py
cd ../step4-model     && python3 analysis.py
cd ../step5-policy    && python3 policy_engine.py
cd ../step6-distributor && python3 distributor.py
cd ../step7-sink      && python3 build_dashboard.py
```

The deliverable is `step7-sink/output/dashboard.html`. Open it in any browser. No server, no internet, no dependencies.

---

## Data

Saudi Central Bank (SAMA) Open Data Platform, Clearing and Payment Systems category. Two files, both publicly published with no registration and no confidential material:

- **Points of Sale Transactions by Sector** — monthly, 16 sectors, transaction counts and sales values
- **E-Commerce Transactions Using Mada Cards** — monthly, national

Merged analysis window: January 2019 to December 2023, sixty monthly observations. Retrieved `[DATE]`. The raw downloads are committed unmodified alongside the parsing code, so the analysis reproduces from the exact bytes we used regardless of any later revision to the published series.

---

## Knowledge base

Every stage is mapped to real, citable Saudi policy documents. The full table is in the technical report; the sources are:

- SAMA Rules for Electronic Payment Services (2020)
- SAMA Cyber Security Framework, including in-Kingdom hosting provisions
- SAMA Rules on Outsourcing
- SAMA AML/CTF Guidelines
- SAMA Regulatory Sandbox / Permitted Fintechs programme
- SAMA National Payments Usage Study, 2021 and 2023
- Fintech Saudi Annual Fintech Report
- Vision 2030 Financial Sector Development Program Annual Report 2024
- SDAIA AI Ethics Principles
- ITU AI Readiness Report 2.0, Dimensions 4, 6 and 7

Two nodes could not be mapped. That is reported as a finding rather than left blank — see the technical report, §3.1.

---

## How we worked

Three rules held throughout, and they shaped nearly every decision in these folders.

**Strip the jargon and see if it survives.** For any statistical result we asked: stated as one plain sentence with no method name attached, is this still interesting and still true? Anything that only sounded impressive because of the technique used to produce it was treated as decoration.

**Report what you found, not what you expected.** The interquartile-range outlier test did not confirm what we assumed it would. It is in the repository anyway, with the interpretation adjusted rather than the result reframed. So is the leave-one-out analysis showing that our most quotable p-value is fragile. A result presented alongside its own weaknesses is worth more than one presented without them, and it is also the only version that stays true when someone checks.

**Build the safeguard, do not promise it.** Step 5's AML/CTF gate is not a policy sentence saying the system will not be misused for financial-crime targeting. It is a property of the decision logic: there is no branch that returns anything but a refusal, because the evidence class this data contains can never satisfy the evidence class that gate requires. The dashboard exposes it as a button so you can test it rather than trust it.

---

## What we would say if you only read one thing

It is easy to build a system that is correct. It is harder to build one that stays correct when someone uses it for a purpose you did not intend. The analysis in this repository took a few days. The architecture that keeps the analysis from being turned into an enforcement tool took most of the thinking.
