# STEP 1 — SOURCE: Fintech Data Source Selection
*ITU AI Readiness Hackathon (KSA) — research completed via live web verification, Aug 2026*

---

## 1. Executive Verdict

**Recommended source: the Saudi Central Bank (SAMA) Open Data Platform — "Clearing and Payment Systems" category** (retail electronic-payment share, POS transaction volume/value, and related national payments time series), cross-referenced against the **"Monetary and Financial Statistics"** category on the same portal. It is the only candidate that is simultaneously (a) published directly by Saudi Arabia's financial regulator, (b) genuinely fintech-specific (digital/cashless payments, not generic macro data), (c) freely downloadable with no registration, (d) naturally shaped for a **trend analysis via regression/correlation** (exactly the method you said you want to use), and (e) surrounded by an unusually rich, real, citable body of SAMA policy documents — because the same institution that publishes the data also writes the rules governing it. The World Bank's **Global Findex 2025 Saudi Arabia microdata** is the strongest backup if you want individual-level data for classification/clustering instead of a national trend.

---

## 2. Candidate Sources

Scored out of 10 per criterion (not summed — see judgment notes below the table).

| # | Candidate | Authenticity | Fintech relevance | Saudi relevance | Policy relevance | AI/analytical potential | Accessibility | Reproducibility | Data richness | Original-insight potential | Policy docs available |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **SAMA Open Data — Clearing & Payment Systems** | 10 | 10 | 10 | 10 | 7 | 8 | 8 | 7 | 8 | 10 |
| 2 | SAMA Open Data — Monetary & Financial Statistics | 10 | 6 | 10 | 9 | 7 | 8 | 8 | 8 | 6 | 9 |
| 3 | World Bank Global Findex 2025 — Saudi Arabia (microdata) | 10 | 9 | 7 | 9 | 9 | 7 | 9 | 8 | 8 | 7 |
| 4 | SAMA National Payments Usage Study (2021 & 2023 reports) | 10 | 9 | 10 | 8 | 5 | 6 | 6 | 5 | 6 | 8 |
| 5 | Fintech Saudi Annual Fintech Report (2024/2025, with SAMA/CMA/IA) | 10 | 10 | 10 | 9 | 4 | 6 | 6 | 5 | 5 | 9 |
| 6 | GASTAT Household Income & Consumption Expenditure Survey 2023 | 10 | 4 | 10 | 8 | 8 | 8 | 8 | 9 | 7 | 6 |
| 7 | Financial Sector Development Program (FSDP) Annual Report 2024 | 10 | 7 | 10 | 10 | 3 | 7 | 7 | 4 | 5 | 10 |
| 8 | Saudi Payments Network ("mada") operational stats | 6* | 9 | 10 | 6 | 5 | 5 | 5 | 5 | 5 | 6 |
| 9 | Kaggle "Credit Card Fraud Detection" (generic global dataset) | 6 | 8 | 1 | 2 | 9 | 10 | 9 | 6 | 2 | 1 |

*\*Score 6 because I could only confirm mada's operational statistics via a secondary source (Wikipedia) this session, not mada.com.sa directly — flagged UNVERIFIED, see §6.*

**Judgment notes:**
- Candidates #4, #5, #7 are excellent for the **Policy Ecosystem** (§4 below) and for narrative/motivation, but they're PDF reports with summary KPIs, not structured data files — weak as the actual *Model (M)* input.
- #6 (GASTAT) is a genuinely strong, large (122,325 households), well-structured Saudi government dataset — but it's household income/expenditure, which is general economic statistics, not fintech-specific, so it under-performs on the brief's explicit "fintech-relevant, not generic economic statistics" requirement.
- #9 (Kaggle fraud data) is included deliberately as the "attractive but weak" trap the brief warned against: technically easy and AI-suitable, but anonymized/non-Saudi, disconnected from any real regulator or policy, and used in essentially every fraud-detection tutorial and hackathon that exists — it fails "original insight" and "policy relevance" badly.

---

## 3. Deep Analysis of the Winner

- **Source:** Saudi Central Bank (SAMA) Open Data Platform → "Clearing and Payment Systems" category (`sama.gov.sa/en-US/Publications/EconomicReports/Pages/report.aspx?cid=116`), plus "Monetary and Financial Statistics" (`cid=55`) for supporting series.
- **Publisher:** Saudi Central Bank (SAMA) — the Kingdom's central bank and financial-sector regulator (confirmed live at sama.gov.sa; portal launched per SAMA's own Dec 2021 announcement, "sama.gov.sa/en-us/news/pages/news-722.aspx").
- **What it contains:** National time series on the payments and financial system — confirmed by SAMA's own published bulletins to include, among others: retail electronic-payment share (79% of retail transactions in 2024, up from 70% in 2023), POS terminal counts (2.1M as of mid-2025), POS transaction volume/value (weekly and annual), non-cash retail transaction counts (12.6bn in 2024), M3 money supply, private-sector credit, and SAIBOR interbank rates. The portal itself states data can be browsed by category or downloaded in Excel/CSV, with selectable time period and periodicity.
- **Coverage:** National (Saudi Arabia), typically monthly/quarterly/annual, with some indicators (e.g., weekly POS operations) published even more frequently.
- **Accessibility:** Free, public, no login required, downloadable in Excel/CSV directly from a `.gov.sa` domain.
- **Provenance:** As authoritative as it gets — first-party regulator data, not an aggregator.
- **Fintech relevance:** Direct — this *is* the digital-payments/cashless-economy data, the core of fintech.
- **Policy relevance:** Very high, and structurally elegant: SAMA is *both* the publisher of this data *and* the author of the rules governing electronic payments, outsourcing, AI use, and data handling in the sector (§4). That means your Y.3172 "Policy (P)" node can cite the same institution that owns the "Source (SRC)" node — a coherent, defensible story.
- **Analytical potential:** Well suited to your stated approach — **regression/correlation to explain a trend** (e.g., the trajectory of e-payment adoption over time, or the relationship between POS growth and private-sector credit growth) rather than individual-level classification.
- **Originality:** Most teams under time pressure default to a generic Kaggle fraud dataset with no country grounding. Using the actual regulator's own live series, paired with the regulator's own rulebook, is a distinctive and hard-to-fake choice that directly demonstrates "genuine knowledge contribution."
- **Limitations (important):** This is **aggregate/macro data**, not individual transaction- or customer-level data — you cannot build a per-customer classifier from it alone (see §6). It's a JS-rendered portal; I could confirm the *categories* and several *specific published figures* via SAMA's own bulletins and news coverage, but I could not machine-fetch the live download page to list every exact column/date range in this session (the fetch timed out — likely a client-side-rendered SPA). **Before finalizing, your team must manually visit the portal and download the actual file(s)** for the specific series you intend to use, and record the exact indicator names and date ranges.

---

## 4. Policy Ecosystem Around the Source

All verified live this session, directly from SAMA's own Rulebook portal or official PDFs:

| Organization | Document | Jurisdiction | Date | URL | Why it may matter later |
|---|---|---|---|---|---|
| SAMA | Rules on Outsourcing (incl. Principle 9 — Outsourcing) | Saudi Arabia | Orig. 2008 (Circular 424), revised Dec 2019 draft | `rulebook.sama.gov.sa/en/rules-outsourcing` and `rulebook.sama.gov.sa/en/principle-9-outsourcing` ; PDF: `sama.gov.sa/en-US/RulesInstructions/FinanceRules/Outsourcing Rules - Revised v2 Final Draft-Dec-2019.pdf` | Governs any third-party/cloud/AI vendor used to build and host your solution |
| SAMA | Rules on Outsourcing for Finance Companies | Saudi Arabia | — | `rulebook.sama.gov.sa/en/rules-outsourcing-finance-companies` | Sector-specific variant if your use case touches finance companies rather than banks |
| SAMA | Cyber Security Framework (CSF), incl. Cloud Computing requirements | Saudi Arabia | First issued May 2017; in-Kingdom hosting/data-residency provisions | Referenced via `rulebook.sama.gov.sa` and secondary compliance summaries (Google Cloud/Oracle SAMA-mapping docs) | Governs where/how any AI system processing this data may host data (in-Kingdom by default) |
| SAMA | AML/CTF Guidelines | Saudi Arabia | Ongoing, aligned to FATF | Referenced via `rulebook.sama.gov.sa` | Directly relevant if your "trend" touches unusual/anomalous payment patterns |
| SAMA | "Rules for Electronic Payment Services, 2020" | Saudi Arabia | 2020 | Referenced in market-research coverage of SAMA's own rule (mandates businesses over SAR 3M revenue to accept e-payments) | Explains *why* the e-payment trend you'd analyze is rising — direct causal/regulatory link for your "existing solutions & gaps" narrative |
| SAMA | National Payments Usage Study, 2021 and 2023 editions | Saudi Arabia | 2021 / 2023 | `sama.gov.sa/en-US/Documents/National_Payments_Usage_Study_en.pdf` ; `sama.gov.sa/en-US/Documents/Report_on_Payments_Usage_Study_2023_en.pdf` | Independent SAMA survey validating the same cashless-adoption trend from the consumer/business side |
| Saudi Central Bank / CMA / Insurance Authority (via Fintech Saudi) | Annual Fintech Report 2024/2025 | Saudi Arabia | Sep 2025 (2024 edition) | `fintechsaudi.sa/en-us/Pages/Resources.aspx` | Tracks official fintech-sector KPIs/targets (companies, jobs, investment) your project's insight could speak to |
| Vision 2030 Program Office | Financial Sector Development Program (FSDP) Annual Report 2024 | Saudi Arabia | 2025 | `vision2030.gov.sa/media/wpsn44ab/fsdp_annual-report-2024_-en.pdf` | The top-level national strategy this all rolls up to — good for the "Strategy Alignment" ITU dimension |
| SDAIA / National Data Management Office | Personal Data Protection Law (PDPL) | Saudi Arabia | Effective Sept 2024 | **Not directly verified this session** — locate primary text via SDAIA/NDMO's official portal before citing | Governs any personal data handling in your pipeline; flagged UNVERIFIED per your instructions until your team pulls the primary URL |
| SAMA | Regulatory Sandbox / "Permitted Fintechs" program | Saudi Arabia | Ongoing | Confirmed to exist via SAMA's own site navigation; exact page URL not captured this session — locate via sama.gov.sa before citing | Directly maps to the ITU report's **Sandbox** factor and **Dimension 10 (AI & Policy)** |

*None of these establish a specific "policy gap" yet — per instructions, that comes later.*

---

## 5. Why This Source Can Become a Strong Competition Project

**Chain:** SAMA payments time series (electronic-payment share, POS volume/value) → an analytical question about whether that growth is uniform or shows stalls/plateaus/segments still reliant on cash → a policy question about whether current rules (Electronic Payment Services 2020, AML/CTF, outsourcing/cloud, and the still-unverified PDPL) adequately anticipate an AI system that would monitor, forecast, or act on this trend — e.g., around fairness, explainability, or oversight if such a system flagged anomalies or informed a lending/consumer-protection decision. That last step is exactly where your Model (M) → Policy (P) node pairing becomes real, and where the "controversy scenario" the template asks for can live. (Full Model and Policy design is intentionally left for later steps.)

---

## 6. Risks / Reasons to Reject

Being direct, as instructed:

- **Aggregate, not individual-level.** This source cannot support a *per-customer* classifier (e.g., "who is likely to be excluded/at risk") on its own. If your team wants that, you need Global Findex or GASTAT microdata instead or alongside it.
- **Portal is JS-rendered.** I verified the category structure and several specific published figures via SAMA's own bulletins and reputable coverage (Arab News, Argaam), but I could not machine-fetch the live download interface in this session (timeout). **This must be manually confirmed by your team before you commit** — go to the portal, pick your series, download the actual file, and check column names/date coverage.
- **Series length varies.** Some indicators may only have a few years of history, which limits statistical power for a trend/regression story — check the actual date range once downloaded.
- **Thin on its own.** A single indicator (e.g., "% electronic transactions") is a fairly short number series. You'll likely want to combine 2–3 related series (e-payment share, POS volume, private-sector credit) to have enough signal for a meaningful correlation analysis.
- **mada operational stats (candidate #8)** were only confirmed via a secondary source this session — do not cite Wikipedia as your final reference; go to `mada.com.sa` directly if you want to use these figures.

---

## 7. Backup Source

**World Bank Global Findex Database 2025 — Saudi Arabia** (individual-level microdata, ~1,018 respondents; DOI: `10.48529/j2fd-af03`, catalog: `microdata.worldbank.org/index.php/catalog/7970`). Use this instead if your team decides classification/clustering across individuals (e.g., segmenting the population by financial-inclusion status) is more compelling than a national trend. It is globally standardized, DOI-citable, and directly tied to Saudi Vision 2030's financial-inclusion targets — but is a global dataset with a Saudi subset (n=1,018), not a Saudi-native source, and its aggregate country-level tables are freely downloadable while the individual microdata requires a free World Bank Microdata Library account.

---

## 8. Source Decision

**SELECT WITH CONDITIONS.**

Conditions before moving to Step 2:
1. Your team manually visits `sama.gov.sa/en-US/Publications/EconomicReports/Pages/report.aspx?cid=116` (Clearing and Payment Systems) and `?cid=55` (Monetary and Financial Statistics), downloads the actual CSV/Excel for the specific series you'll use, and confirms exact indicator names and date ranges.
2. You decide whether one indicator is enough or whether to combine 2–3 series for a richer trend story (recommended: combine).

**Official definition of SRC for Step 2:**
> SRC = Saudi Central Bank (SAMA) Open Data Platform — "Clearing and Payment Systems" category (retail electronic-payment share and/or POS transaction volume/value time series), supplemented if needed by the "Monetary and Financial Statistics" category (e.g., private-sector credit) from the same portal — downloaded directly as CSV/Excel from sama.gov.sa, no registration, no confidential material.
