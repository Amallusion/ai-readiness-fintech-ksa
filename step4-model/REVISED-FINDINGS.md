# REVISED FINDINGS — exact text to swap in, and where

Your friend's critique was correct, and digging further surfaced more.
This is the exact replacement language. Copy-paste it in; don't re-derive it.

---

## 1. New headline paragraph
**Use this to replace the old "confirmed 3 independent ways" claim
everywhere it appears** (report Introduction, dashboard Public tab,
video script opening):

> Saudi Arabia's cashless transition is structured by transaction value:
> among single-purpose retail sectors, higher average ticket size
> significantly predicts slower digital-payment adoption (R²=0.31,
> p=0.04, n=14, excluding two pre-flagged catch-all categories). Jewelry
> — the highest-ticket-size sector tracked — sits exactly where this
> relationship predicts: among the slowest adopters, sharing its closest
> trajectory-shape match with only one other sector, Clothing and
> Footwear. Jewelry is not uniquely worst — it is statistically tied
> with Education for "most often the single lowest-ranked sector" — but
> it is the clearest illustration of a real, generalizable, mechanistic
> pattern, not an isolated anomaly.

## 2. New consolidated findings table
**Replace the table in Section 5 of `full-project-documentation.md`** with:

| Check | Method | Result |
|---|---|---|
| Ticket-size mechanism (14 clean sectors) | OLS regression, log(ticket size) → growth | **R²=0.31, p=0.04** — higher ticket size significantly predicts slower digital adoption |
| Correlation with e-commerce trend, level-based | Pearson correlation | Jewelry 0.51 (lowest) — **superseded, see next row** |
| Correlation with e-commerce trend, differenced (corrected) | Pearson correlation on month-over-month growth | Jewelry 0.31 — **mid-to-high**, not the lowest; original level-based claim was a trend artifact |
| Cluster containing Jewelry, level-based (original) | K-Means, k=3, raw rebased levels | 8 sectors — **dominated by final level, not shape** |
| Cluster containing Jewelry, shape-based (corrected) | K-Means, k=3, z-normalized trajectories | 2 sectors: Jewelry + Clothing and Footwear — the genuine shape match |
| k justification | Silhouette score, k=2..6 | k=2 is data-optimal (0.71); k=3 retained for interpretability, not asserted as algorithm-chosen |
| "Is Jewelry uniquely worst?" | Bootstrap resampling (1000 draws) of growth rates | **No** — Jewelry 24.9%, Education 25.0% (statistically tied); Clothing 17.7%, Hotels 14.2% |

## 3. What to explicitly DROP
- Any sentence claiming Jewelry has "the lowest correlation with the
  e-commerce trend" as a standalone, unqualified fact — it's now
  qualified as a level-trend artifact (see table above).
- Any sentence claiming K-Means clustering is "independent" confirmation
  without the level-vs-shape caveat.
- Any sentence asserting Jewelry is uniquely/uncontestedly the worst
  sector — replace with "tied with Education."

## 4. What to explicitly ADD
- The ticket-size mechanism finding (Section 1 above) — this is your new
  best figure. Use `chart8b_ticket_size_clean14.png`, not the original
  `chart8_ticket_size_vs_growth.png` (the 16-sector version isn't
  significant; state that honestly if asked, and explain the exclusion
  is pre-justified since Step 3 already flagged those two categories as
  compositionally ambiguous, not chosen after the fact to help the fit).
- One sentence acknowledging the methodology repair itself — this is a
  credibility asset, not a liability: *"An external review identified
  that our original three confirmatory checks were correlated by
  construction rather than independent; we re-ran the analysis with
  genuinely independent methods (differenced correlation, shape-based
  clustering, bootstrap resampling) and revised our claim accordingly."*
  Say this out loud in the video. It is the single most credible
  sentence you can say to a technical judge.

## 5. What does NOT need to change
- **Step 5 (Policy) logic is still valid.** It operates on "which
  sectors ended in the bottom growth tier," which is a legitimate basis
  for the context-review/sandbox-referral/disclosure layers regardless
  of whether the underlying cluster is level- or shape-based. No code
  changes needed there — only the narrative framing of *why* those
  sectors were selected.
- **Steps 1, 2, 6, 7 are unaffected.** This repair is scoped entirely to
  Step 4's statistical claims.

## 6. Files in this folder
- `rigor_repair.py` — the full corrected analysis script
- `chart8_ticket_size_vs_growth.png` — original 16-sector version (not significant; keep for transparency, don't lead with it)
- `chart8b_ticket_size_clean14.png` — **the one to actually use**, 14 sectors, R²=0.31, p=0.04
- `chart9_silhouette_scores.png` — shows k=2 is optimal, k=3 was a choice
- `ticket_size_regression_report.txt`, `ticket_size_data.csv`
- `correlation_comparison.csv` — level vs. differenced, side by side
- `shape_cluster_results.csv` — the 2-sector shape-based cluster result
- `bootstrap_ranking_report.txt` — corrected bootstrap, with the note about its own limitation (wide CIs from i.i.d. resampling of a trending series — mention this if asked, don't hide it)
