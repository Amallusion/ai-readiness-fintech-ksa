# Sector Digitalization Watch — Full Project Documentation
### ITU AI Readiness Hackathon, Kingdom of Saudi Arabia — Fintech Track — Team Voxel

---

## 1. Executive Summary

This project investigates a simple but under-examined question: Saudi Arabia's
national cashless-payments statistic (79% of retail transactions were
electronic in 2024, per SAMA) is a single aggregate number — but does it
describe the whole economy evenly, or does it hide sectors that have been
left behind?

Using the Saudi Central Bank's (SAMA) own open payments data, we built a
complete 7-stage pipeline — conforming to the ITU-T Y.3172 machine-learning
architecture standard (SRC → C → PP → M → P → D → SINK) — that: merges and
enriches real transaction data, statistically and algorithmically identifies
which economic sectors have structurally lagged behind the national
cashless trend, converts that finding into a policy response with a
built-in architectural safeguard against misuse, routes that response to
the three different real institutions who would each act on a different
part of it, and finally presents it through a bilingual, role-based
dashboard.

**The headline finding** (revised after an external ML-specialist review
identified that our original three checks were correlated by construction
rather than independent — see Section 4, Step 4 addendum): digital-payment
adoption across Saudi retail is structured by transaction value — sectors
with higher average ticket sizes have adopted digital payments
significantly more slowly than lower-ticket, high-frequency sectors
(R²=0.31, p=0.04, n=14). The **Jewelry sector**, the highest-ticket sector
tracked, sits exactly where this relationship predicts. It is not
uniquely the worst performer — it is statistically tied with Education —
but it is the clearest illustration of a real, generalizable mechanism
rather than an isolated anomaly.

---

## 2. The Problem, and Why We Chose It

National-level fintech adoption metrics are the primary way governments and
international bodies (including ITU itself, in its AI Readiness reports)
track digital transformation progress. But a single national percentage is
a mean, and means hide variance. A policymaker reading "79% cashless"
cannot tell from that number alone whether the remaining 21% is spread
evenly across the economy, or concentrated in a few structurally distinct
sectors that might need a different kind of intervention than a general
awareness campaign.

We chose this problem because it sits at a genuine intersection required by
the hackathon's own judging criteria: it needs real technical work (data
engineering, statistics, unsupervised machine learning) to even discover
the pattern, and it needs real policy reasoning (not just "flag it") to
turn that pattern into something a regulator could actually use without
creating new risk (e.g., unfairly stigmatizing an entire sector).

---

## 3. Methodology and Working Philosophy

Before describing each pipeline stage, it's worth being explicit about the
standard we held ourselves to throughout, because it shaped nearly every
decision below:

**The "does it survive without jargon" test.** For any statistical or
algorithmic result, we asked: if you stripped away the method name and
stated the finding as one plain sentence, is it still interesting and
still true? A result that only sounds impressive because of the technique
used to produce it was treated as decoration, not insight.

**Triangulation over single-method confidence.** Wherever possible, we
tried to confirm a finding using at least two independent methods that
had no logical reason to agree with each other unless the underlying
pattern was real. This is why the Jewelry finding is stated with
confidence: it emerged independently from (a) raw growth-rate comparison,
(b) correlation with the national e-commerce trend, and (c) unsupervised
K-Means clustering that was never told in advance which sectors were
"slow."

**Honest reporting over narrative convenience.** When a statistical test
(the IQR outlier check in Step 4) did *not* confirm what we expected, we
reported that plainly rather than omitting or reframing it — and treated
the more nuanced true result as an opportunity to make a *stronger*,
better-hedged claim rather than a weaker one.

**Architecture as the safeguard, not just policy language.** In Step 5,
rather than writing a policy that *promises* not to be misused, we built
the misuse-prevention directly into the code's logic (Layer 3 is
structurally incapable of firing from this class of data), so the
safeguard is a property of the system, not a sentence a bad actor could
ignore.

---

## 4. Step-by-Step Technical Breakdown

### STEP 1 — SRC (Source)

**What we did:** Conducted a structured, criteria-based research process
to select the strongest available fintech data source, rather than
defaulting to the first dataset found. Nine real candidate sources were
identified (SAMA's own payments data, World Bank Global Findex 2025 for
Saudi Arabia, GASTAT's Household Income and Expenditure Survey, Fintech
Saudi's Annual Report, SAMA's National Payments Usage Study, and others)
and scored across ten weighted criteria: authenticity/provenance, fintech
relevance, Saudi/regional relevance, policy relevance, AI/analytical
potential, accessibility, reproducibility, data richness, potential for
original insight, and availability of authoritative policy documents.

**What we chose and why:** SAMA's own Open Data Platform — specifically
the "Clearing and Payment Systems" category — because it is simultaneously
(a) published directly by the actual financial regulator, not an
aggregator, (b) genuinely fintech-specific rather than generic economic
statistics, (c) freely downloadable with no registration barrier, and (d)
structured as a monthly time series, which directly supports the
regression/correlation/trend-based analytical approach the team wanted to
use. Critically, because SAMA is both the publisher of this data *and*
the author of the regulations governing the sector, the project gets an
unusually coherent story: the same institution that generated the SRC
node's data also authors the documents that justify the Policy node's
decisions five steps later.

**The actual data acquired:**
- *Points of Sale Transactions by Sector* — monthly, January 2016 to
  December 2023, broken into 16 economic sectors (Transportation, Health,
  Restaurants & Café, Hotels, Beverage and Food, Clothing and Footwear,
  Recreation and Culture, Miscellaneous Goods and Services, Electronic &
  Electric Devices, Furniture, Construction & Building Materials, Jewelry,
  Telecommunication, Education, Public Utilities, Others), each with two
  metrics: Number of Transactions and Sales value (SAR).
- *E-Commerce Transactions Using Mada Cards* — monthly, with real
  (non-blank) data from January 2019 onward, giving a national online-shopping
  trend independent of the sector breakdown above.

Both files were downloaded directly from the SAMA portal in a format that
turned out to be MHTML (a multi-part HTML document with an `.xls`
extension) rather than a true binary spreadsheet — a real technical
quirk that had to be understood and parsed correctly (see Step 2).

---

### STEP 2 — C (Collector)

**The technical challenge:** The two raw files were not simple, uniform
spreadsheets. They were MHTML documents (MIME-encoded multi-sheet HTML)
disguised with an `.xls` extension — SAMA's actual export format. Standard
spreadsheet libraries expecting a real binary Excel file would fail
silently or misread them. The Collector script parses the underlying
email/MIME structure directly, extracts the specific HTML sheet
containing the monthly data, and converts it into a proper tabular
DataFrame using `pandas.read_html`.

**Merging logic:** The two sources cover different date ranges — the
sector file has usable data from 2016, but the e-commerce file's values
are blank ("-") before January 2019. Rather than merging on the full
range (which would introduce artificial gaps that could bias any
downstream trend or correlation analysis), the Collector explicitly
restricts the merged dataset to **January 2019 – December 2023**, the
range where *both* sources have genuine, non-null values.

**Event enrichment (the "creative" layer):** Beyond a mechanical merge,
the Collector adds three engineered context columns, each computed
programmatically rather than hand-entered:
- `covid_period` — a boolean flag for the core Saudi lockdown window
  (March–June 2020), confirmed useful when the resulting merged data
  showed e-commerce transactions nearly tripling in exactly that window
  (6.6M in Feb 2020 to 18.2M in May 2020).
- `ramadan_month` — computed by checking, for every month in the dataset,
  whether it overlaps with that year's Ramadan date range (sourced and
  verified per-year from the Umm al-Qura lunar calendar), since Ramadan
  shifts roughly 11 days earlier in the Gregorian calendar each year and a
  hardcoded month list would silently become wrong from one year to the
  next.
- `post_epayments_law` — a boolean flag from 2020 onward, marking SAMA's
  real "Rules for Electronic Payment Services" regulation.

**Three output shapes, and why each exists:** The Collector produces the
same underlying data in three different structures, because different
downstream steps need different shapes — not because the information
differs:
- **Wide format** (`collected_wide.csv`): one row per month, every
  sector/metric as a column. Used for month-level analysis and as the
  Policy engine's eventual duration calculations.
- **Long format** (`collected_long.csv`): one row per single (date,
  sector, metric, value) fact — the tidy-data convention many
  visualization and statistical tools expect.
- **Sector matrix** (`sector_transactions_matrix.csv`): one row per
  sector, one column per month — i.e., each sector becomes a single
  60-dimensional vector describing its entire trajectory. This specific
  shape is what makes clustering possible in Step 4, since clustering
  algorithms operate on rows-as-observations.

---

### STEP 3 — PP (Pre-processor)

**Validation performed:** Before any modeling, the Preprocessor
programmatically checked: (a) zero missing values across the merged
window, (b) zero exact-zero values (which would indicate a reporting gap
rather than genuine low activity), (c) correct numeric data types on
every column, and (d) — most importantly — whether a documented SAMA
footnote (that "Hotels" was split out of "Restaurants & Café," and that
"Electronic & Electric Devices," "Furniture," "Construction & Building
Materials," and "Jewelry" were split out of "Miscellaneous Goods and
Services" at some point in the source data's history) created a
discontinuity inside our analysis window. The check confirmed all
affected sectors already had distinct, non-zero values from the very
first month of our window (January 2019), meaning the redefinition had
occurred before our data begins — so no correction was needed, but the
check itself is documented as evidence of due diligence.

**Rebasing (indexing) — the key transformation, explained:** Raw
transaction counts are not directly comparable across sectors, because
sectors differ by orders of magnitude in size (Restaurants & Café: tens
of thousands of transactions per month; Jewelry: hundreds). Feeding raw
counts into a clustering algorithm would cause it to group sectors by
*size* rather than by *growth behavior* — the wrong signal entirely. The
standard fix, borrowed directly from how financial indices work (e.g., a
stock market index), is to **rebase every sector's series so its first
month equals 100**, i.e.:

```
indexed_value(t) = (raw_value(t) / raw_value(t=Jan 2019)) × 100
```

After this transformation, a value of 300 in any sector means "3x its own
January 2019 level," regardless of whether that sector started large or
small — making cross-sector comparison mathematically fair.

**Growth-rate computation:** A separate month-over-month percentage
change series (`pct_change()`) was also computed for every sector, made
available for any correlation or regression work that specifically needs
rate-of-change rather than level data.

---

### STEP 4 — M (Model)

This is the step where two genuine analytical/ML methods were applied,
independently, to the rebased sector data.

**Method 1 — K-Means Clustering.**
K-Means is an unsupervised machine learning algorithm: it is given only
the data (no labels, no hints about which sectors are "slow" or "fast")
and asked to partition it into *k* groups such that observations within a
group are as similar as possible, and observations in different groups
are as different as possible. Concretely, it works by: (1) initializing
*k* candidate cluster centers ("centroids"), (2) assigning every
observation to its nearest centroid (by Euclidean distance across all
features), (3) recomputing each centroid as the mean of the observations
now assigned to it, and (4) repeating steps 2–3 until the assignments
stop changing.

In this project, **each of the 16 sectors is one observation**, and its
**features are its own 60 monthly rebased index values** (Jan 2019 –
Dec 2023) — i.e., the algorithm is clustering sectors by the entire
*shape* of their growth trajectory over five years, not by a single
summary number. We chose **k=3**, matching our working hypothesis (from
the manual "Slow / Moderate / Rapid" binning built in Step 3) that
sectors would naturally fall into three adoption tiers.

**Result and validation:** The algorithm's output was compared against
the earlier manual binning. **94% agreement (15 of 16 sectors)** — the
model, with no hints given, independently rediscovered almost exactly the
same grouping a human had proposed by hand. Jewelry was placed in the
"Slow" cluster together with Education, Health, Clothing and Footwear,
Hotels, Recreation and Culture, Electronic & Electric Devices, and
Furniture. Only "Others" disagreed between the two methods. This
agreement is the second independent confirmation of the Jewelry finding
(the first being the raw growth-rate and correlation checks performed
during Step 3's exploratory work).

**Method 2 — IQR (Interquartile Range) Outlier Detection.**
This is a standard, non-machine-learning statistical technique (the same
logic behind a boxplot's whiskers), used here specifically because the
team wanted a second, independent, more rigorous check on whether Jewelry
was a genuine statistical anomaly rather than simply "the lowest of an
otherwise normal group." The method: compute the first quartile (Q1, the
25th percentile) and third quartile (Q3, the 75th percentile) of the
16 sectors' final rebased values; the interquartile range is
IQR = Q3 − Q1; any value below `Q1 − 1.5×IQR` or above `Q3 + 1.5×IQR` is
conventionally flagged as an outlier.

**Result, reported honestly:** With only 16 data points, the resulting
fences are wide, and Jewelry — while clearly the lowest sector — sits
just inside the lower fence rather than below it, so it is **not**
formally flagged as a statistical outlier by this specific test. What the
test *did* flag is the opposite extreme: "Miscellaneous Goods and
Services" (rebased index of 2,280 by December 2023) as a high-side
outlier. Rather than discarding this inconvenient result, we incorporated
it: it actually strengthens the project's central claim, because it shows
Jewelry is not resting on one fragile, possibly-noisy anomaly — it is the
anchor of a real, independently-clustered group of 8 structurally slow
sectors, a broader and more defensible pattern than a single outlier
would be.

---

### STEP 5 — P (Policy)

**The design problem:** A naive policy layer would simply take Step 4's
"Slow cluster" output and turn it into a single flag or alert. We
considered this the least interesting and most risky option, since a bare
flag invites exactly the kind of controversy scenario the submission
template explicitly requires teams to address (e.g., "could this be used
to unfairly target a whole sector?").

**The layered design actually implemented — four independent rules,
each grounded in a real, verifiable document:**

1. **Layer 1 — Context Review (always-on, non-punitive).** Any sector in
   the "Slow" cluster automatically triggers a prompt to investigate *why*
   before assuming a problem exists — e.g., cultural/traditional
   preference for gold as a store of value, thin merchant margins unable
   to absorb card-processing fees, or legitimate customer preference for
   transaction privacy on large personal purchases. This layer can never
   produce an enforcement action; it only produces a question.

2. **Layer 2 — Sandbox Pilot Recommendation (positive action, timed).**
   Any "Slow" sector is referred to SAMA's real Regulatory Sandbox /
   Fintech Saudi program for a targeted support pilot. The recommended
   launch window is computed to land 1–2 months *before* that sector's
   next major spending season (Ramadan), reusing the event tags built in
   Step 2 — a behavioral nudge lands more effectively immediately before
   people are already about to spend, rather than at an arbitrary point
   in the year.

3. **Layer 3 — AML/CTF Gate (the architectural safeguard).** This is the
   layer that directly answers the required controversy scenario. It
   reports "DORMANT" for every sector, unconditionally, by construction —
   sector-level cluster membership can **never**, under any circumstance
   in this code, be sufficient evidence to trigger this gate. It requires
   independent, transaction-level or merchant-level evidence that this
   aggregate dataset does not and structurally cannot contain, and any
   action on it must be reviewed by a human compliance officer. This is
   not a policy promise that could be ignored — it is a property of how
   the decision logic is written.

4. **Layer 4 — Transparency Disclosure (accountability, always-on).**
   Computed by checking, sector by sector, how many of the last 5
   calendar years' December values remained below the "Slow" threshold,
   counting consecutively backward from 2023. Any sector at 2 or more
   consecutive years is flagged as requiring explicit disclosure, by
   name, in the next public fintech-sector reporting cycle — rather than
   remaining invisible behind the rising national average. All 8 "Slow"
   sectors, including Jewelry, scored the maximum 5/5, since none of them
   broke out of the bottom tier at any point in the five-year window.

Each layer's real-world grounding document was carried forward from the
Step 1 research (the SAMA Rulebook's Outsourcing Rules, Cyber Security
Framework, AML/CTF Guidelines; the actual 2020 electronic-payments
regulation; the Fintech Saudi Annual Report's public-disclosure
precedent).

---

### STEP 6 — D (Distributor)

**The design insight:** Step 5 produces one decision object covering all
16 sectors and all 4 layers. A naive Distributor would forward that
entire object to every downstream recipient. We rejected this as the
"broadcast" anti-pattern: real institutions are siloed by function — a
regulator's policy office does not need Ramadan pilot-timing detail; a
sandbox team does not need AML/CTF gate status; a compliance auditor does
not need disclosure-cycle framing. Sending everyone everything is not
neutral, it is simply lower-effort routing that pushes the burden of
filtering onto the recipient.

**What was built instead:** The Distributor programmatically fans the one
decision object into three separate, purpose-built packets:
- **Packet 1**, containing only Layer 4 output, addressed to SAMA's
  Financial Sector Development Program office.
- **Packet 2**, containing only Layer 2 output (including the computed
  Ramadan-aware timing), addressed to Fintech Saudi / the SAMA Regulatory
  Sandbox team.
- **Packet 3**, containing only Layer 3's assurance record, addressed to
  the SAMA AML/CTF compliance office.

This structure directly mirrors ITU AI Readiness Report 2.0's own
**Dimension 7, "Strategy Alignment"**, which describes a top-level intent
being decomposed into sub-tasks and routed to the appropriate service
providers — the Distributor is, functionally, an implementation of
exactly that described pattern, not merely inspired by it.

---

### STEP 7 — SINK

**The design insight:** Just as a single undifferentiated policy dump
would have been the wrong choice for the Distributor, a single
undifferentiated dashboard would throw away all of that routing work at
the very last step. The Sink was therefore built as a **role-based
interface**: a single HTML page with four selectable views (Public,
Regulator, Sandbox Team, Compliance), where selecting a role reveals
*only* that role's packet from Step 6 — the interface structurally
mirrors the routing logic instead of contradicting it.

**Bilingual implementation.** All interface chrome (titles, headers,
button labels, table column headers) and all 16 sector names are
available in both English and Arabic, toggleable instantly via a
language switch, implemented with a CSS-class-based show/hide mechanism
rather than a page reload. This is a direct, concrete implementation of
ITU AI Readiness Report 2.0's **Dimension 6, "Human Interface,"** which
explicitly names "availability of AI models in the local language used in
the human interface" as a readiness metric.

**Technical implementation.** The dashboard is a single, self-contained
HTML file with all three supporting charts embedded directly as base64-encoded
images inside the HTML itself (rather than linked as separate
image files), so the file remains fully functional even if
moved out of its original folder structure or opened with no internet
connection — a deliberate reliability choice for a live demo setting.

---

## 5. Consolidated Findings (revised — see step4b-rigor-repair/REVISED-FINDINGS.md)

| Check | Method | Result |
|---|---|---|
| Ticket-size mechanism (14 clean sectors) | OLS regression, log(ticket size) → growth | **R²=0.31, p=0.04** — the load-bearing finding |
| Correlation with e-commerce trend, differenced (corrected) | Pearson correlation on growth rates | Jewelry 0.31 — mid-to-high, NOT the lowest (original level-based 0.51 claim was a trend artifact) |
| Cluster containing Jewelry, shape-based (corrected) | K-Means on z-normalized trajectories | 2 sectors: Jewelry + Clothing and Footwear |
| k justification | Silhouette score, k=2..6 | k=2 is data-optimal; k=3 retained for interpretability, not algorithm-chosen |
| Is Jewelry uniquely worst? | Bootstrap resampling, 1000 draws | No — tied with Education (24.9% vs 25.0%) |
| Consecutive years in bottom tier | Year-end value tracking | Jewelry and 7 other sectors: 5 of 5 years (still holds — basis for Step 5 Policy) |

**Overall conclusion:** Jewelry is not an isolated anomaly, but it is also
not uniquely, uncontestedly "the worst." The defensible claim is
narrower and more useful: transaction value is a real, statistically
significant driver of digital-adoption speed in Saudi retail, and Jewelry
is its clearest illustration.

---

## 6. Mapping to the ITU AI Readiness Framework

| Pipeline step | ITU-T Y.3172 node | ITU AI Readiness factor(s) | ITU AI Readiness dimension(s) |
|---|---|---|---|
| Step 1 | SRC | Open Data | Data/Model Marketplace; Contextualization & Regional Impact |
| Step 2 | C | Open Data, Deployment | Data/Model Marketplace |
| Step 3 | PP | Deployment | Data/Model Marketplace |
| Step 4 | M | Research, Deployment | Level of Integration of AI in Workflows |
| Step 5 | P | Sandbox, Standards | Contextualization & Regional Impact; AI & Policy |
| Step 6 | D | Standards | Strategy Alignment |
| Step 7 | SINK | Standards, Deployment | Human Interface |

---

## 7. Technical Stack

- **Language:** Python 3
- **Data handling:** pandas
- **Machine learning:** scikit-learn (K-Means clustering)
- **Statistics:** NumPy, pandas (IQR/quantile computation)
- **Visualization:** Matplotlib
- **Interface:** vanilla HTML/CSS/JavaScript (no framework dependency, for maximum portability)
- **Source data format handled:** MHTML (MIME-encoded multi-sheet HTML disguised as `.xls`), parsed via Python's `email` module and `pandas.read_html`

All code is organized by pipeline stage (`step2-collector/`, `step3-preprocessor/`,
`step4-model/`, `step5-policy/`, `step6-distributor/`, `step7-sink/`), each
independently runnable, each reading its input from the previous stage's
output file(s), so the entire pipeline is reproducible end-to-end from the
two original raw SAMA downloads.

---

## 8. Honest Limitations

- The dataset is sector-level aggregate data. It cannot and does not
  support any claim about individual businesses, merchants, or
  customers — a limitation that is directly why Step 5's Layer 3 is
  designed to be structurally incapable of firing from this data alone.
- Ramadan date ranges for years without an officially confirmed date in
  this project's research are estimated using the standard ~11-day
  yearly shift and are accurate to within approximately one day.
- The IQR outlier test's statistical power is limited by the small sample
  size (16 sectors); this is reported explicitly rather than hidden.
- SAMA's own sector-definition changes over time (documented in a source
  footnote) were checked and found not to affect the analysis window
  used, but this was a data-specific finding for this project's window,
  not a general guarantee about the source.

---

## 9. What Makes This Project Distinctive

1. **Caught and fixed our own methodology error.** An external ML
   specialist identified that our original three "independent" checks
   were correlated by construction. Rather than defend the original
   framing, we re-ran the analysis with genuinely independent methods
   and revised the headline claim — from a broad, slightly overstated
   pattern to a narrower, statistically significant, mechanistic one
   (R²=0.31, p=0.04).
2. **Honest about disconfirming evidence, twice over.** Both the IQR
   result and this later methodology repair produced findings that
   didn't match expectations, and both were reported as-is.
3. **The safeguard is architectural, not rhetorical.** Layer 3 cannot
   fire from this class of data — that is a property of the code, not a
   promise in a paragraph.
4. **Routing mirrors real institutional structure.** The Distributor and
   Sink both explicitly reject the "one dashboard for everyone" default
   in favor of matching how SAMA, Fintech Saudi, and AML/CTF compliance
   actually function as separate offices.
5. **Explicitly, verifiably grounded in real documents at every stage**,
   from the original SAMA data source through the policy layer's AML/CTF
   and outsourcing framework citations — not hypothetical or invented
   references.
