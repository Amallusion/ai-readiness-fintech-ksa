# STEP 1 — SOURCE: Fintech Data Source Selection
*ITU AI Readiness Hackathon (KSA) — Team Voxel*
*Research completed via live web verification, Aug 2026. Revised post-download — see §9.*

---

## 1. Executive Verdict

**Recommended source: the Saudi Central Bank (SAMA) Open Data Platform — "Clearing and Payment Systems" category** (retail electronic-payment share, POS transaction volume/value, and related national payments time series), cross-referenced against the **"Monetary and Financial Statistics"** category on the same portal.

It is the only candidate that is simultaneously (a) published directly by Saudi Arabia's financial regulator, (b) genuinely fintech-specific (digital/cashless payments, not generic macro data), (c) freely downloadable with no registration, (d) naturally shaped for **trend analysis via regression/correlation**, and (e) surrounded by an unusually rich, real, citable body of SAMA policy documents — because the same institution that publishes the data also writes the rules governing it.

The World Bank's **Global Findex 2025 Saudi Arabia microdata** is the strongest backup if individual-level data for classification/clustering is preferred over a national trend. It is the only candidate that beats SAMA under any reasonable re-weighting of our criteria (§2.3).

---

## 2. Candidate Sources

### 2.1 Criteria and weights

Weights were fixed **before** scoring, derived from the hackathon brief's stated emphases (country-specific relevance, policy grounding, authentic sources) rather than tuned afterwards to favour a preferred candidate.

| Criterion | Weight | Rationale |
|---|---|---|
| Authenticity / provenance | 12% | Brief requires authentic, non-confidential, citable sources |
| Fintech relevance | 12% | Track requirement — must be fintech, not generic economics |
| Saudi / regional relevance | 12% | KSA-specific contextualization is an explicit judging dimension |
| Policy relevance | 14% | Highest weight: the P node and the KB mapping depend on it |
| AI / analytical potential | 12% | The M node must have something real to do |
| Accessibility | 8% | Practical constraint under hackathon time limits |
| Reproducibility | 8% | Judges must be able to re-run the pipeline |
| Data richness | 8% | Determines how much analysis is possible |
| Original-insight potential | 8% | Differentiation from default submissions |
| Policy documents available | 6% | Partly captured by policy relevance; weighted lower to avoid double-counting |
| **Total** | **100%** | |

### 2.2 Scores

Each criterion scored 0–10. Weighted total is the sum of (score × weight), expressed on the same 0–10 scale.

| # | Candidate | Auth. | Fintech | Saudi | Policy | AI | Access | Reprod. | Richness | Insight | Policy docs | **Weighted** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **SAMA Open Data — Clearing & Payment Systems** | 10 | 10 | 10 | 10 | 7 | 8 | 8 | 7 | 8 | 10 | **8.92** |
| 3 | World Bank Global Findex 2025 — Saudi Arabia (microdata) | 10 | 9 | 7 | 9 | 9 | 7 | 9 | 8 | 8 | 7 | **8.44** |
| 2 | SAMA Open Data — Monetary & Financial Statistics | 10 | 6 | 10 | 9 | 7 | 8 | 8 | 8 | 6 | 9 | **8.16** |
| 6 | GASTAT Household Income & Consumption Expenditure Survey 2023 | 10 | 4 | 10 | 8 | 8 | 8 | 8 | 9 | 7 | 6 | **7.88** |
| 5 | Fintech Saudi Annual Fintech Report (2024/2025, with SAMA/CMA/IA) | 10 | 10 | 10 | 9 | 4 | 6 | 6 | 5 | 5 | 9 | **7.64** |
| 4 | SAMA National Payments Usage Study (2021 & 2023 reports) | 10 | 9 | 10 | 8 | 5 | 6 | 6 | 5 | 6 | 8 | **7.52** |
| 7 | Financial Sector Development Program (FSDP) Annual Report 2024 | 10 | 7 | 10 | 10 | 3 | 7 | 7 | 4 | 5 | 10 | **7.44** |
| 8 | Saudi Payments Network ("mada") operational stats | 6\* | 9 | 10 | 6 | 5 | 5 | 5 | 5 | 5 | 6 | **6.40** |
| 9 | Kaggle "Credit Card Fraud Detection" (generic global dataset) | 6 | 8 | 1 | 2 | 9 | 10 | 9 | 6 | 2 | 1 | **5.38** |

*\*Authenticity scored 6, not 10, because mada's operational statistics could only be confirmed via a secondary source (Wikipedia) in this session, not via mada.com.sa directly — flagged UNVERIFIED, see §6.*

### 2.3 Sensitivity analysis

A weighted score is an arbitrary construction unless the ranking survives changes to the weights. We tested whether the winner is an artefact of our chosen weighting.

| Test | Result |
|---|---|
| Equal weights (10% each) | SAMA 8.80, Findex 8.30 — **SAMA wins** |
| Saudi-relevance weight set to **zero** (redistributed proportionally) | SAMA 8.77, Findex 8.64 — **SAMA wins** |
| Policy-docs weight set to **zero** | SAMA 8.85, Findex 8.53 — **SAMA wins** |
| SAMA's two strongest criteria (policy relevance + policy docs) **both removed** | SAMA 8.65, Findex 8.45 — **SAMA wins** |
| AI/analytical-potential weight raised | **Crossover at ≈29%.** Above that, **Findex wins** |

**Interpretation, stated plainly:** the SAMA selection is robust to every re-weighting we tested except one. If a team weighted raw analytical potential above roughly 29% of the total decision — that is, if the project were primarily a modelling exercise and only secondarily a policy exercise — Global Findex would be the correct choice. Since this hackathon's judging criteria are explicitly weighted toward country-specific policy grounding and knowledge-base value, that weighting is not the right one here. This is precisely why Findex is designated the backup (§7) rather than rejected.

### 2.4 Judgment notes

- Candidates #4, #5 and #7 are excellent for the **policy ecosystem** (§4) and for narrative and motivation, but they are PDF reports with summary KPIs, not structured data files — weak as the actual *Model (M)* input. Their weighted scores are dragged down by AI potential and richness, which is the correct outcome: they belong in the knowledge base, not at the SRC node.
- #6 (GASTAT) is a genuinely strong, large (122,325 households), well-structured Saudi government dataset — but it covers household income and expenditure, which is general economic statistics rather than fintech-specific, so it under-performs on the brief's explicit "fintech-relevant, not generic economic statistics" requirement.
- #9 (Kaggle fraud data) is included deliberately as the "attractive but weak" trap the brief warned against: technically easy and AI-suitable, but anonymized, non-Saudi, disconnected from any real regulator or policy, and used in essentially every fraud-detection tutorial and hackathon that exists. It scores highest of all candidates on accessibility (10) and near-highest on AI potential (9), and still finishes last — which is the whole point of scoring it.

---

## 3. Deep Analysis of the Winner

- **Source:** Saudi Central Bank (SAMA) Open Data Platform → "Clearing and Payment Systems" category (`sama.gov.sa/en-US/Publications/EconomicReports/Pages/report.aspx?cid=116`), plus "Monetary and Financial Statistics" (`cid=55`) for supporting series.
- **Publisher:** Saudi Central Bank (SAMA) — the Kingdom's central bank and financial-sector regulator (confirmed live at sama.gov.sa; portal launched per SAMA's own Dec 2021 announcement, `sama.gov.sa/en-us/news/pages/news-722.aspx`).
- **What it contains:** National time series on the payments and financial system — confirmed by SAMA's own published bulletins to include, among others: retail electronic-payment share (79% of retail transactions in 2024, up from 70% in 2023), POS terminal counts (2.1M as of mid-2025), POS transaction volume and value (weekly and annual), non-cash retail transaction counts (12.6bn in 2024), M3 money supply, private-sector credit, and SAIBOR interbank rates. The portal states data can be browsed by category or downloaded in Excel/CSV, with selectable time period and periodicity.
- **Coverage:** National (Saudi Arabia), typically monthly/quarterly/annual, with some indicators (e.g., weekly POS operations) published more frequently. **Several series carry a sector-level breakdown — see §9, which materially exceeded what we anticipated here.**
- **Accessibility:** Free, public, no login required, downloadable in Excel/CSV directly from a `.gov.sa` domain.
- **Licensing:** SAMA publishes this as open data via its own portal with no registration barrier. **UNVERIFIED:** the specific licence text and permitted-reuse terms were not captured in this session. Locate SAMA's open-data terms of use before making any formal open-licence claim in the report; until then, describe the data as "publicly published by SAMA without registration" rather than asserting a named licence.
- **Provenance:** As authoritative as it gets — first-party regulator data, not an aggregator.
- **Fintech relevance:** Direct — this *is* the digital-payments and cashless-economy data, the core of fintech.
- **Policy relevance:** Very high, and structurally elegant: SAMA is *both* the publisher of this data *and* the author of the rules governing electronic payments, outsourcing, AI use, and data handling in the sector (§4). The Y.3172 **Policy (P)** node can therefore cite the same institution that owns the **Source (SRC)** node. This is not a convenience — it is a structural property of the source that makes the whole pipeline internally coherent, and it is the single strongest argument for this choice.
- **Analytical potential:** Well suited to a **regression/correlation approach explaining a trend** rather than individual-level classification. Scored 7 rather than 9 at selection time on the assumption of a single national series; see §9 for how the sector breakdown changed this.
- **Originality:** Most teams under time pressure default to a generic Kaggle fraud dataset with no country grounding. Using the actual regulator's own live series, paired with the regulator's own rulebook, is a distinctive and hard-to-fake choice that directly demonstrates genuine knowledge contribution.
- **Limitations (important):** This is **aggregate/macro data**, not individual transaction- or customer-level data — no per-customer classifier can be built from it alone (§6). It is a JS-rendered portal; we confirmed the *categories* and several *specific published figures* via SAMA's own bulletins and news coverage, but could not machine-fetch the live download page to enumerate every column and date range in this session (the fetch timed out, likely a client-side-rendered SPA). **Manual download and verification was therefore made a precondition — see §8, discharged in §9.**

---

## 4. Policy Ecosystem Around the Source

All verified live this session directly from SAMA's own Rulebook portal or official PDFs, except where explicitly flagged.

| Organization | Document | Jurisdiction | Date | URL | Why it may matter later |
|---|---|---|---|---|---|
| SAMA | Rules on Outsourcing (incl. Principle 9 — Outsourcing) | Saudi Arabia | Orig. 2008 (Circular 424), revised Dec 2019 draft | `rulebook.sama.gov.sa/en/rules-outsourcing` and `rulebook.sama.gov.sa/en/principle-9-outsourcing`; PDF: `sama.gov.sa/en-US/RulesInstructions/FinanceRules/Outsourcing Rules - Revised v2 Final Draft-Dec-2019.pdf` | Governs any third-party, cloud or AI vendor used to build and host the solution |
| SAMA | Rules on Outsourcing for Finance Companies | Saudi Arabia | — | `rulebook.sama.gov.sa/en/rules-outsourcing-finance-companies` | Sector-specific variant if the use case touches finance companies rather than banks |
| SAMA | Cyber Security Framework (CSF), incl. cloud computing requirements | Saudi Arabia | First issued May 2017; in-Kingdom hosting / data-residency provisions | Referenced via `rulebook.sama.gov.sa` and secondary compliance summaries (Google Cloud / Oracle SAMA-mapping docs) | Governs where and how any AI system processing this data may host data (in-Kingdom by default) |
| SAMA | AML/CTF Guidelines | Saudi Arabia | Ongoing, aligned to FATF | Referenced via `rulebook.sama.gov.sa` | Directly relevant if the analysis touches unusual or anomalous payment patterns — becomes the grounding document for Policy Layer 3 |
| SAMA | Rules for Electronic Payment Services, 2020 | Saudi Arabia | 2020 | Referenced in market-research coverage of SAMA's own rule (mandates businesses over SAR 3M revenue to accept e-payments) | Explains *why* the e-payment trend rises — a direct regulatory link for the "existing solutions and gaps" narrative, and the basis for the `post_epayments_law` event flag in Step 2 |
| SAMA | National Payments Usage Study, 2021 and 2023 editions | Saudi Arabia | 2021 / 2023 | `sama.gov.sa/en-US/Documents/National_Payments_Usage_Study_en.pdf`; `sama.gov.sa/en-US/Documents/Report_on_Payments_Usage_Study_2023_en.pdf` | Independent SAMA survey validating the same cashless-adoption trend from the consumer and business side |
| Saudi Central Bank / CMA / Insurance Authority (via Fintech Saudi) | Annual Fintech Report 2024/2025 | Saudi Arabia | Sep 2025 (2024 edition) | `fintechsaudi.sa/en-us/Pages/Resources.aspx` | Tracks official fintech-sector KPIs and targets; public-disclosure precedent for Policy Layer 4 |
| Vision 2030 Program Office | Financial Sector Development Program (FSDP) Annual Report 2024 | Saudi Arabia | 2025 | `vision2030.gov.sa/media/wpsn44ab/fsdp_annual-report-2024_-en.pdf` | The top-level national strategy this rolls up to — supports the Strategy Alignment ITU dimension |
| SDAIA / National Data Management Office | Personal Data Protection Law (PDPL) | Saudi Arabia | Effective Sept 2024 | **UNVERIFIED — not directly confirmed this session.** Locate primary text via SDAIA/NDMO's official portal before citing | Governs any personal-data handling in the pipeline. Note: our final dataset is sector-level aggregate and contains no personal data, which limits but does not eliminate PDPL's relevance |
| SAMA | Regulatory Sandbox / "Permitted Fintechs" program | Saudi Arabia | Ongoing | **PARTIALLY VERIFIED** — existence confirmed via SAMA's own site navigation; exact page URL not captured this session. Locate via sama.gov.sa before citing | Maps directly to the ITU report's **Sandbox** factor and **Dimension 10 (AI & Policy)**; grounding document for Policy Layer 2 |

*None of these establish a specific policy gap at this stage — per method, gap identification comes after the model produces a finding.*

---

## 5. Why This Source Can Become a Strong Competition Project

**Chain:** SAMA payments time series → an analytical question about whether that growth is uniform or whether segments of the economy remain reliant on cash → a policy question about whether current rules (Electronic Payment Services 2020, AML/CTF, outsourcing and cloud, and PDPL) adequately anticipate an AI system that would monitor, forecast, or act on this trend — particularly around fairness, explainability, and oversight if such a system flagged anomalies or informed a consumer-protection or lending decision.

That last step is where the **M → P** node pairing becomes real, and where the controversy scenario the template requires can live: a system that identifies lagging segments could, if carelessly designed, be repurposed into a targeting or enforcement tool against those same segments. Designing against that is a Step 5 problem, but the risk is visible from the source selection onward, and naming it here is deliberate.

---

## 6. Risks / Reasons to Reject

- **Aggregate, not individual-level.** This source cannot support a per-customer classifier on its own. Global Findex or GASTAT microdata would be required for that. *This limitation later became a design asset: because the data structurally cannot identify individual merchants or customers, the Step 5 AML/CTF gate can be made incapable of firing from it.*
- **Portal is JS-rendered.** Category structure and several specific published figures were verified via SAMA's own bulletins and reputable coverage (Arab News, Argaam), but the live download interface could not be machine-fetched in this session (timeout). **Resolved by manual download — see §9.**
- **Series length varies.** Some indicators may have only a few years of history, limiting statistical power for a trend or regression story. **Partially resolved — see §9; the usable overlap window is 60 months, which is adequate but not generous.**
- **~~Thin on its own.~~ RESOLVED (§9).** At selection time we expected a single indicator to be a short number series and planned to combine 2–3 series for adequate signal. The sector-level breakdown discovered on download supersedes this concern: one national indicator became 16 parallel, comparable series. We record the original concern rather than deleting it, because the resolution was a fortunate discovery rather than a planned outcome.
- **mada operational stats (candidate #8)** were confirmed only via a secondary source this session. Do not cite Wikipedia as a final reference; go to `mada.com.sa` directly if these figures are used.
- **Licensing terms not captured.** See §3. Avoid asserting a named open licence until verified.

---

## 7. Backup Source

**World Bank Global Findex Database 2025 — Saudi Arabia** (individual-level microdata, ~1,018 respondents; DOI `10.48529/j2fd-af03`, catalog `microdata.worldbank.org/index.php/catalog/7970`).

Use this instead if classification or clustering across individuals (e.g., segmenting the population by financial-inclusion status) is judged more compelling than a national trend. It is globally standardized, DOI-citable, and directly tied to Vision 2030's financial-inclusion targets — but it is a global dataset with a Saudi subset (n=1,018), not a Saudi-native source, and while its aggregate country-level tables are freely downloadable, the individual microdata requires a free World Bank Microdata Library account.

Per §2.3, this is the only candidate that overtakes SAMA under any tested re-weighting, and it does so only when raw analytical potential is weighted above ~29% of the decision.

---

## 8. Source Decision (pre-download)

**SELECT WITH CONDITIONS.**

Conditions before moving to Step 2:

1. Manually visit `sama.gov.sa/en-US/Publications/EconomicReports/Pages/report.aspx?cid=116` (Clearing and Payment Systems) and `?cid=55` (Monetary and Financial Statistics), download the actual CSV/Excel for the series to be used, and confirm exact indicator names and date ranges.
2. Decide whether one indicator is sufficient or whether to combine 2–3 series for a richer trend story (recommended: combine).

**Provisional definition of SRC:**
> SRC = SAMA Open Data Platform, "Clearing and Payment Systems" category (retail electronic-payment share and/or POS transaction volume/value time series), supplemented if needed by "Monetary and Financial Statistics" (e.g., private-sector credit) from the same portal — downloaded directly as CSV/Excel from sama.gov.sa, no registration, no confidential material.

*Superseded by §9.*

---

## 9. Conditions Discharged — Retrieval Record

*Added after manual download. This section closes the conditions set in §8 and records what was actually obtained, including one respect in which the source exceeded expectations.*

**Portal visited manually:** `[TEAM: insert download date]`
**Registration required:** none. **Confidential material:** none.

**Files obtained:**

| File | Periodicity | Range as published | Structure |
|---|---|---|---|
| Points of Sale Transactions by Sector | Monthly | Jan 2016 – Dec 2023 | 16 economic sectors × 2 metrics (Number of Transactions, Sales value in SAR) |
| E-Commerce Transactions Using Mada Cards | Monthly | Values blank ("-") before Jan 2019; usable Jan 2019 onward | National series, independent of the sector breakdown |

**Sectors covered (16):** Transportation; Health; Restaurants & Café; Hotels; Beverage and Food; Clothing and Footwear; Recreation and Culture; Miscellaneous Goods and Services; Electronic & Electric Devices; Furniture; Construction & Building Materials; Jewelry; Telecommunication; Education; Public Utilities; Others.

**Usable analysis window:** **Jan 2019 – Dec 2023 (60 months)**, set by the later of the two sources' genuine-data start. Chosen in preference to merging the full 2016–2023 range, which would have introduced artificial gaps in the e-commerce series and biased any downstream trend or correlation work.

**Format finding.** Both files download with an `.xls` extension but are **MHTML** — MIME-encoded multi-sheet HTML, not binary Excel. Standard spreadsheet libraries fail silently or misread them. This is SAMA's actual export format and required a purpose-built parser at the Collector node (see Step 2).

**Material discovery not anticipated in §3.** The **sector-level breakdown** was not visible from the portal metadata we could reach remotely and does not appear in our selection analysis above. It is the single most consequential property of this source for this project:

- It resolves the "thin on its own" risk in §6 — one national indicator becomes 16 comparable series.
- It converts the project from a national-trend description into a **cross-sector variance question**, which is the actual research question the submission now answers.
- It raises the AI/analytical-potential score from **7 to 9** in retrospect (16 observations × 60 features makes unsupervised clustering possible, which a single national series would not). At 9, SAMA's weighted total rises to **9.16** and the crossover point against Findex in §2.3 disappears entirely.

We report this rather than silently updating the score, because a selection made partly on incomplete information and vindicated by later discovery is not the same thing as a selection made on complete information, and the distinction matters for anyone assessing our method.

**Final definition of SRC, as implemented:**

> **SRC** = Saudi Central Bank (SAMA) Open Data Platform, "Clearing and Payment Systems" category. Two files: *Points of Sale Transactions by Sector* (monthly, 16 sectors, Number of Transactions and Sales value) and *E-Commerce Transactions Using Mada Cards* (monthly, national). Downloaded directly from sama.gov.sa in MHTML-with-.xls-extension format, no registration, no confidential material. Merged analysis window Jan 2019 – Dec 2023 inclusive, 60 monthly observations per series. Retrieved `[TEAM: insert download date]`.

**Reproducibility note.** Government statistical series are subject to revision. Anyone re-running this pipeline against a later download may obtain slightly different values. The retrieval date above is the reference point; the raw downloaded files are committed to the repository unmodified alongside the parsing code, so the analysis is reproducible from the exact bytes we used regardless of subsequent portal revisions.

---

## Revision note

Changes from the pre-download version of this file: criterion weights made explicit and applied (§2.1–2.2); sensitivity analysis added (§2.3); licensing flagged UNVERIFIED (§3); sandbox URL downgraded to PARTIALLY VERIFIED (§4); "thin on its own" risk marked resolved with the original text retained (§6); retrieval record, format finding, sector-breakdown discovery and final SRC definition added (§9). No scores were altered retroactively; the §9 revision to AI/analytical potential is recorded as a post-hoc observation, not applied to the original table.
