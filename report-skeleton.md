# AI Readiness Hackathon – KSA Final Submission Template
*(Copy everything below into your Google Doc. Sections marked 🔲 still need Steps 4–7.)*

---

**Team name:** [fill in]
**Members name:** [fill in — up to 4]
**Solution name:** [fill in — working title, e.g. "Sector Digitalization Watch"]
**Contact details:** [fill in]

---

## 1. Introduction

*Draft — polish once Steps 4–7 are done:*

Saudi Arabia's cashless-payments transformation, under Vision 2030's
Financial Sector Development Program, is often reported as a single
national number (e.g. 79% of retail transactions were electronic in
2024). That headline figure hides real variation: some sectors of the
economy have gone almost fully digital, while others have barely moved.
This project uses the Saudi Central Bank's (SAMA) own open payments data
to surface which sectors are lagging, why that might matter for policy
(e.g. AML/CTF oversight of high-value cash transactions), and to build
[🔲 describe the actual tool/output once Step 4–6 are built].

## 2. Description of the use case and gaps in existing solutions

**The problem:** National cashless-adoption statistics are reported in
aggregate, masking sector-level disparities that matter for targeted
policy intervention.

**Existing approach and its gap:** SAMA and Fintech Saudi publish annual
reports tracking national-level KPIs against Vision 2030 targets, but
these do not systematically flag *which* sectors are structurally behind,
nor connect specific laggards to the specific regulatory frameworks that
might explain or address the gap.

**Our solution:** [🔲 finish once Step 4 (Model) and Step 6 (Distributor) are
built — describe the clustering/analysis + how the output reaches a user]

**The value:** turns a single national cashless % into an actionable,
sector-by-sector signal that a regulator, bank, or fintech could act on.

## 3. Mapped documents

| Node | Use case (this project) | Documents (policies, strategies, AI-relevant regulations) |
|---|---|---|
| **SRC** | SAMA Open Data Platform — POS transactions by sector (Jan 2016–Dec 2023) and e-commerce transactions via Mada cards (real data from Jan 2019) | See full scored list in `step1-source-selection.md` |
| **C** | `collector.py` — merges both SAMA exports, trims to the shared Jan 2019–Dec 2023 window, adds event tags (COVID period, Ramadan months, post-2020 e-payments law) | SAMA "Rules for Electronic Payment Services" (2020); SAMA National Payments Usage Study 2021/2023 |
| **PP** | `preprocess.py` — validates for missing/zero values, confirms the SAMA sector-redefinition footnote doesn't break our window, rebases each sector to an index (Jan 2019 = 100) and computes month-over-month growth | — |
| **M** | 🔲 [fill in once built — e.g. clustering sectors by growth-tier / trend shape] | 🔲 [e.g. any methodology/benchmarking standard used] |
| **P** | 🔲 [fill in — the rule for what happens with the Model's output, and which real regulation justifies it] | 🔲 SAMA AML/CTF Guidelines; SAMA Rules on Outsourcing; SAMA Cyber Security Framework — see `step1-source-selection.md` §4 for full list with links |
| **D** | 🔲 [fill in — how the decision is passed onward] | 🔲 SAMA Cloud Computing Framework (in-Kingdom hosting) if relevant |
| **SINK** | 🔲 [fill in — who/what finally sees the output, e.g. a dashboard] | — |

*(See `step1-source-selection.md` for the full policy ecosystem table with
live links — Rules on Outsourcing, Cyber Security Framework, AML/CTF
Guidelines, the 2020 e-payments regulation, Fintech Saudi Annual Report,
FSDP Annual Report.)*

## 4. Evaluation scenarios

**Step 1:** [🔲 draft once Step 6/7 exist — e.g. "the tool is deployed and
used by a regulator/bank to monitor sector-level digitalization"]

**Step 2 (complication):** [🔲 e.g. "six months in, it's noticed that the
Jewelry sector remains flagged as a laggard — is this a data-quality issue,
a genuine business pattern, or a red flag?"]

**Step 3 (resolution via the knowledge base):** [🔲 e.g. how the Policy (P)
node's rules — grounded in the real AML/CTF guidance — determine the
appropriate response, distinguishing a benign explanation from one that
warrants escalation]

**Controversy case (required):** [🔲 what happens if the finding is
misused or misread — e.g. could flagging "Jewelry is cash-heavy" be
misused to unfairly target a whole sector or specific businesses without
due process? What guardrail in the Policy node prevents that?]

---

## Not part of the template, but keep for your own reference:

**Early findings, confirmed 3 independent ways:**
- Jewelry: lowest 5-yr growth (1.35x vs up to 21.8x for others)
- Jewelry: lowest correlation with national e-commerce trend (0.51 vs 0.9+ for most)
- Jewelry: lowest rebased index at Dec 2023 (144.6 vs up to 2,280 for others)

**Charts ready to embed:** `visuals/chart1_all_sectors_indexed.png`,
`chart2_growth_ranking.png`, `chart3_ecommerce_covid_spike.png`
