# Step 4 — Model

Statistical analysis for the M node of the Y.3172 pipeline: does Saudi Arabia's
cashless transition reach every sector evenly, and if not, what structures the
difference?

## Read this first

`FINDINGS.md` — the results, how to state each one, and the limitations to carry
into the report. Written to be pasted straight into the submission.

## Files

| File | What it is |
|---|---|
| `FINDINGS.md` | **Start here.** Results and report-ready text. |
| `analysis.py` | Full analysis. Needs the four pipeline CSVs listed below. |
| `diagnostics.py` | Robustness checks. Runs on the result CSVs in this folder alone — already run, output in `output/`. |
| `output/chart8c_ticket_size_with_fragility.png` | **The lead figure.** |
| `output/diagnostics_report.txt` | Leverage, rank-correlation, significance-threshold and cluster-size results |
| `output/leave_one_out.csv` | Per-sector leave-one-out fits |
| `ticket_size_data.csv` | Average ticket size and growth index by sector |
| `correlation_comparison.csv` | Level vs differenced correlation with the e-commerce trend |
| `shape_cluster_results.csv` | Shape-space clustering vs level-space vs manual tiers |

## Running it

`diagnostics.py` needs nothing beyond this folder:

```bash
pip install pandas numpy scipy matplotlib
python3 diagnostics.py
```

`analysis.py` additionally needs four files from earlier pipeline stages copied
into this folder:

```
collected_wide.csv          # Step 2
sector_matrix_indexed.csv   # Step 3
sector_matrix_growth.csv    # Step 3
cluster_results.csv         # level-based clusters + manual tiers
```

Then:

```bash
pip install scikit-learn
python3 analysis.py
```

It exits with a clear message listing anything missing rather than failing
partway through.

## What the analysis does

**A. Ticket size as a mechanism.** Average ticket size (Sales ÷ Transactions) is
a dimension of the data independent of trajectory level and shape, so it tests
whether adoption is *structured* by transaction value rather than merely
describing which sectors ended lowest. Reported with OLS, Spearman, leave-one-out
fragility, and a control for sector size.

**B. Correlation with the national e-commerce trend, on levels and differences.**
Two upward-trending series correlate highly regardless of any underlying
relationship, so the differenced series is the informative one. Reported with the
|r| thresholds needed for significance, uncorrected and Bonferroni.

**C+D. Clustering in level space and shape space,** with silhouette scores and
cluster sizes disclosed at every k. Sizes matter: a high silhouette produced by
splitting off one or two extreme sectors is an outlier detector scoring well, not
evidence of population structure.

**E. Rank stability,** two ways. A resampling-free count of how often each sector
holds the lowest rebased index across the observed month-ends, which makes no
distributional assumptions, plus a moving block bootstrap (block = 12 months)
that preserves within-year autocorrelation and seasonality.

## Methodological stance

n = 16 sectors is a small sample. Every p-value here is reported as descriptive,
alongside the diagnostics that show how much weight it can bear. Where a result
is fragile, the fragility is reported next to the result rather than in a
footnote.

## For the video

Show `chart8c_ticket_size_with_fragility.png` full-screen: *here is the finding,
and here on the right is exactly how much weight it will bear — eight of fourteen
sectors, removed individually, push it above significance.*
