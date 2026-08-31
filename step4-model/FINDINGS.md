# Step 4 — Findings

Text for the report, dashboard and video script. Every number is reproducible
from `diagnostics.py`, which runs on the result CSVs in this folder.

---

## 1. Headline

> Saudi Arabia's cashless transition is structured by transaction value: across
> sectors, higher average ticket size is associated with slower digital-payment
> adoption (Spearman ρ = −0.46 across all 16 sectors, ρ = −0.49 across the 14
> single-purpose sectors; p ≈ 0.07 in both). The relationship is moderate and
> consistent, though it does not reach conventional significance at this sample
> size, and we report it as a mechanism the data supports rather than an
> established effect. Jewelry, the highest-ticket-size retail sector tracked, is
> among the slowest adopters — and sits materially *below* even what ticket size
> alone would predict, meaning transaction value explains part of its gap and
> something else explains the rest. Jewelry is not uniquely worst; it is the
> clearest illustration of a pattern that runs across the economy.

**On the two excluded categories.** Miscellaneous Goods and Services and Others
are catch-all aggregations of heterogeneous goods, for which an average ticket
size has no coherent meaning; Step 3's preprocessing check already flagged
Miscellaneous as compositionally unstable in SAMA's own source footnote. The
more useful point is that the rank correlation barely moves between 16 and 14
sectors (−0.46 vs −0.49). The exclusion does not create the relationship — it
removes two high-growth points that inflate residual variance in a least-squares
fit. State this before anyone asks.

---

## 2. Consolidated findings table

| Check | Method | Result |
|---|---|---|
| Ticket-size mechanism, rank-based | Spearman, all 16 and clean 14 | **ρ = −0.46 (p=0.072) and ρ = −0.49 (p=0.075)** — moderate, consistent, not significant at n=16 |
| Ticket-size mechanism, OLS | OLS on log₁₀(ticket size), n=14 | R²=0.31, p=0.040 — **fragile: 8 of 14 leave-one-out fits lose significance** |
| Where Jewelry sits on that fit | Residual analysis | −185, third most negative of 14. Slower than ticket size alone predicts |
| Correlation with e-commerce, levels | Pearson on levels | Mean \|r\| = 0.90 — measures shared upward trend, not a sector-specific relationship |
| Correlation with e-commerce, differenced | Pearson on month-over-month growth | Mean \|r\| = 0.17, range [−0.24, 0.33]. **0 of 16 sectors survive Bonferroni.** No sector-specific signal survives differencing |
| Cluster containing Jewelry, level space | K-Means k=3, raw rebased | 8 sectors — driven by final level rather than trajectory shape |
| Cluster containing Jewelry, shape space | K-Means k=3, z-normalized | Sizes **13 / 2 / 1**. Jewelry pairs with Clothing and Footwear, Education is a singleton — an outlier structure, not three tiers |
| Choice of k | Silhouette, k=2..6 | k=2 scores highest; cluster sizes reported alongside every score, since a near-singleton split scores high by construction. k=3 retained for interpretability, not asserted as optimal |
| Persistence in bottom tier | Year-end tracking, observed data | 8 sectors, 5 of 5 years — a direct observation with no modelling assumptions |
| Rank stability | Lowest-index count across observed month-ends | Resampling-free; see `rank_stability_report.txt` |

---

## 3. How to state each result

**Ticket size.** Lead with Spearman, not OLS. The rank statistic is insensitive
to the leverage points and is nearly identical across both samples, which is the
stronger claim. Mention the OLS fit second, with its fragility attached in the
same sentence.

**Correlation.** The finding is not about Jewelry's position in a ranking. It is
that differencing collapses the correlation for *every* sector — mean |r| falls
from 0.90 to 0.17 and none survives Bonferroni correction across 16 tests. The
level-based correlations were measuring the fact that two upward-trending series
trend upward. Say that plainly; it is a methodological point worth more than the
original number was.

**Clustering.** Always quote the cluster sizes. Describe the shape-space result
as identifying the sectors whose trajectory shape is least typical, not as a
discovered set of adoption tiers. Present k=3 as a choice made for
interpretability against the manual tiers, with the silhouette table shown so the
reader can see what the algorithm would have chosen.

**Persistence.** This is the most robust result in Step 4 and carries more of the
weight than the clustering does. Eight sectors sat in the bottom tier in every
one of five years. No model, no assumptions, no resampling.

---

## 4. The figure to lead with

`output/chart8c_ticket_size_with_fragility.png`

Left panel: the relationship, with the two excluded catch-all categories drawn as
hollow markers so the exclusion is visible rather than hidden, and both Spearman
coefficients in the subtitle.

Right panel: the leave-one-out p-value distribution against the 0.05 line, with
the eight crossings in red.

Presenting a result and its fragility in the same figure is the strongest rigor
signal available in a seven-minute slot, and very few submissions do it. Say:
*here is our main finding, and here is exactly how much weight it will bear.*

---

## 5. Limitations to carry into Section 8

- n=16 sectors is a small sample for any inferential claim. Every p-value here
  should be read as descriptive.
- Several analyses were run and one returned p<0.05; with no correction across
  those analyses, that is close to what chance alone would produce. This is why
  the ticket-size result is framed as suggestive rather than established.
- Differenced correlations use ~59 monthly observations; none survives Bonferroni
  correction across 16 sectors.
- The z-normalized clustering produces a degenerate partition at k=3, and its
  membership should not be read as adoption tiers.
- Ticket size is measured as a 2019 mean; sectors whose product mix shifted during
  the window are measured imprecisely.
- The data is sector-level aggregate and supports no claim about any individual
  business, merchant or customer.

---

## 6. Downstream impact

Steps 1, 2, 5, 6 and 7 are unaffected. The Policy node keys off which sectors
ended in the bottom growth tier, which none of the above disturbs — only the
explanation of *why* those sectors were selected changes.
