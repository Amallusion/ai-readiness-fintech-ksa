# Step 4 — Model (M)

Where the pattern is found, and where we work out how much weight it will bear.

---

## The distinction this stage is built around

There is a difference between describing which sectors ended lowest and explaining what makes a sector likely to end low. The first is a ranking. The second is a mechanism, and only the second generalises to a sector this dataset does not contain.

Most of the effort here went into that distinction, because a ranking is easy to produce and easy to over-read. If you rank sectors by growth, cluster them by growth, and then observe that the clusters agree with the ranking, you have not confirmed anything. You have measured the same quantity three times and been reassured by the agreement. Three methods only corroborate each other if they could have disagreed.

So the test we needed was one that used a dimension of the data independent of the growth trajectories themselves.

---

## What we found

**Persistence.** Eight of sixteen sectors sat in the bottom growth tier in every one of the five years, without exception. No model, no assumptions, no resampling — a direct observation of the series. It is the most robust result in this folder and it carries more of the argument than the clustering does.

**Mechanism.** Average ticket size, computed as sales value divided by transaction count, is a property of *how people pay in a sector* rather than of how that sector's series moved. It is inversely related to digital adoption: sectors where people spend more per purchase digitised more slowly.

> Spearman ρ = −0.46 across all sixteen sectors, ρ = −0.49 across the fourteen single-purpose sectors, p ≈ 0.07 in both.

We report it as a mechanism the data supports rather than an established effect, and the hedge is deliberate rather than decorative. Sixteen sectors is a small sample. The least-squares fit on the fourteen single-purpose sectors reaches R² = 0.31 at p = 0.04, but leave-one-out analysis shows that removing any one of eight individual sectors pushes it back above the conventional threshold.

A result that fragile should be presented with its fragility attached to it, in the same sentence, not separated from it by a page break. What gives us confidence the relationship is real is not the p-value. It is that the rank correlation barely moves between the sixteen- and fourteen-sector samples, which means the exclusion of two catch-all categories is not what produces the relationship.

**Where Jewelry actually sits.** It has the highest average ticket size of any retail sector tracked and the lowest final index. It also sits materially *below* what ticket size alone predicts — third most negative residual of fourteen. Transaction value explains part of its gap and something else explains the rest. Education, not Jewelry, is the sector that sits on the fitted line.

---

## Results, and how to read each one

| Check | Method | Result |
|---|---|---|
| Ticket size, rank-based | Spearman, 16 and 14 sectors | ρ = −0.46 (p=0.072), ρ = −0.49 (p=0.075). Moderate, consistent, not significant at this sample size |
| Ticket size, OLS | OLS on log₁₀(ticket size), n=14 | R²=0.31, p=0.040 — **8 of 14 leave-one-out fits lose significance** |
| Jewelry's position on the fit | Residual analysis | −185, third most negative of 14 |
| Correlation with e-commerce, levels | Pearson on levels | Mean \|r\| = 0.90 — measures shared upward trend |
| Correlation with e-commerce, differenced | Pearson on month-over-month growth | Mean \|r\| = 0.17. **0 of 16 survive Bonferroni** |
| Clustering, level space | K-Means, k=3, raw rebased | 8 sectors, driven by final level rather than trajectory shape |
| Clustering, shape space | K-Means, k=3, z-normalized | Sizes **13 / 2 / 1** — an outlier structure, not three tiers |
| Choice of k | Silhouette, k=2..6 | Sizes reported beside every score. k=3 retained for interpretability, not asserted as optimal |
| Rank stability | Lowest-index count across observed month-ends | Resampling-free — see `rank_stability_report.txt` |

Two of these deserve a note, because the obvious reading is not the useful one.

**The correlation result is not about Jewelry.** On levels, Jewelry's correlation with the national e-commerce trend was the lowest of any sector, and that looked like a finding. It is not. Two series that both trend upward will correlate highly regardless of any relationship between them, so the level correlations were measuring shared trend for every sector, not anything specific to one. Once differenced, mean absolute correlation falls from 0.90 to 0.17 and none of the sixteen survives Bonferroni correction. The finding is that the whole measure carries no sector-specific signal. That is a more useful thing to know than a ranking would have been.

**A high silhouette score is not automatically structure.** If splitting one extreme sector off from the other fifteen produces a clean separation, the score will be high, and it will be describing an outlier rather than a population. This is why cluster sizes are printed beside every silhouette value in the output, and why the shape-space partition at k=3 — thirteen, two, one — is described as identifying the sectors whose trajectory is least typical rather than as a discovered set of adoption tiers.

---

## Files

| File | What it is |
|---|---|
| `FINDINGS.md` | **Start here.** The results, how to state each one, and what to concede |
| `analysis.py` | Full analysis. Needs the four pipeline CSVs listed below |
| `diagnostics.py` | Robustness checks. Runs on the result CSVs in this folder alone |
| `output/chart8c_ticket_size_with_fragility.png` | **The lead figure** |
| `output/diagnostics_report.txt` | Leverage, rank-correlation, significance thresholds, cluster sizes |
| `output/leave_one_out.csv` | Per-sector leave-one-out fits |

## Running it

```bash
pip install pandas numpy scipy matplotlib
python3 diagnostics.py                    # needs nothing beyond this folder
```

`analysis.py` additionally needs `collected_wide.csv`, `sector_matrix_indexed.csv`, `sector_matrix_growth.csv` and `cluster_results.csv` copied in, plus scikit-learn. It exits with a clear message listing anything missing rather than failing partway through.

---

## The figure

`output/chart8c_ticket_size_with_fragility.png` is two panels. On the left, the relationship, with the two excluded catch-all categories drawn as hollow markers so the exclusion is visible rather than hidden. On the right, the leave-one-out p-value distribution against the 0.05 line, with the eight crossings marked in red.

Putting a result and its own fragility in one image was a deliberate choice. It is tempting to show only the left panel, and the left panel alone is not dishonest. But a reader who sees only the fit has to take our word for how much it means, and a reader who sees both does not have to take our word for anything.

---

## Limitations

- Sixteen sectors is a small sample. Every p-value here should be read as descriptive.
- Several analyses were run and one returned a result below the conventional threshold, which is close to what chance alone would produce. This is why the ticket-size mechanism is presented as suggestive rather than established.
- The interquartile-range outlier test did not flag the slowest sector; with sixteen observations the fences are wide, and it flagged the opposite extreme instead. It is reported as it came out.
- Ticket size is measured as a 2019 mean, so sectors whose product mix shifted during the window are measured imprecisely.
- The data is sector-level aggregate and supports no claim about any individual business, merchant or customer.

That last limitation is also a design asset. Because this data structurally cannot identify a merchant, Step 5's AML/CTF gate can be made incapable of firing from it — the constraint that limits what we can say is the same constraint that makes the safeguard real rather than promised.
