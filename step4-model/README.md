# Step 4 — Model 


## Files

| File | What it is |
|---|---|
| `REVISED-FINDINGS-v2.md` | **Start here.** Corrected claims, ready to paste. |
| `diagnostics_from_v1_outputs.py` | Runs on the v1 result CSVs alone — no pipeline data needed. Already run; output is in `output/`. |
| `rigor_repair_v2.py` | Full corrected analysis. **Needs your four pipeline CSVs** (see below). |
| `output/diagnostics_report.txt` | Leverage, rank, significance-threshold and cluster-degeneracy results |
| `output/chart8c_ticket_size_with_fragility.png` | **The new hero figure** |
| `output/leave_one_out.csv` | Per-sector leave-one-out fits |
| `ticket_size_data.csv`, `correlation_comparison.csv`, `shape_cluster_results.csv` | v1 result files, used as input to the diagnostics |
| `v1-original/` | Everything from the first repair round, kept for the audit trail |

## To run the full v2 analysis

`rigor_repair_v2.py` needs four files from earlier pipeline stages copied into
this folder:

```
collected_wide.csv          # Step 2
sector_matrix_indexed.csv   # Step 3
sector_matrix_growth.csv    # Step 3
cluster_results.csv         # Step 4
```

Then:

```bash
pip install pandas numpy scipy scikit-learn matplotlib
python3 rigor_repair_v2.py
```

It exits with a clear message listing anything missing rather than failing
partway through.

## What v2 fixes

**The bootstrap (over-correction).** v1 resampled month-over-month growth rates
i.i.d., which destroys autocorrelation and seasonality and then compounds the
noise multiplicatively over ~59 draws. Its own 95% intervals span up to five
orders of magnitude — Education came out as [0, 168187]. That instrument cannot
support the "Jewelry is tied with Education" conclusion drawn from it. v2
replaces it with a resampling-free count over the 60 actual month-ends, plus a
moving block bootstrap (block = 12 months) that preserves autocorrelation.

**The correlation reading (under-correction).** v1 noted Jewelry moved to
mid-range once differenced. True, but the real finding is that *every* sector
collapses: mean |r| falls from 0.90 to 0.17, and 0 of 16 survive Bonferroni
correction. The level-based correlations were measuring shared upward trend, not
any sector-specific relationship. That retires the correlation leg completely
rather than partially.

**The clustering (under-correction).** The z-normalized k=3 partition has sizes
13/2/1 — one large cluster, a pair, and a singleton. That is an outlier detector,
not three adoption tiers. v2 discloses cluster sizes at every k and runs
silhouette in shape space, which v1 only did on levels.

**Fragility, untested in v1.** Leave-one-out shows 8 of 14 single sector removals
push p above 0.05. Meanwhile Spearman is nearly identical on 16 and 14 sectors
(−0.46 vs −0.49), which is the useful result: the two-sector exclusion is not what
produces the relationship, so the exclusion is defensible *and* not load-bearing.

**A confound, untested in v1.** Average ticket size may be a proxy for sector
size. v2 adds a regression on log(ticket size) and log(2019 volume) together.

## For the video

Show `chart8c_ticket_size_with_fragility.png` full-screen and say: *here is our
main finding, and here on the right is how fragile it is — eight of fourteen
sectors, removed individually, push it above significance.* Presenting a result
and its own fragility in one figure is the strongest rigor signal available in a
seven-minute slot, and almost nobody does it.

Then deliver the repair sentence from `REVISED-FINDINGS-v2.md` §4. Two documented
rounds of self-correction beat a clean first result.
