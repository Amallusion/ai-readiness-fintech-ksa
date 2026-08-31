# Visuals

Figures for Step 3, and the growth-tier binning that Step 4 is later tested against.

---

## Why this folder is separate

A chart is an argument. It is easy to forget that, because a chart looks like a neutral rendering of numbers that already exist. But every chart makes a choice about what to emphasise, and the choice is invisible to the reader in a way that a sentence never is. Nobody checks a y-axis the way they check a claim.

So the rule here was that each figure has to be defensible as a statement, not just correct as a rendering. Two of them exist specifically to show where our own reasoning is weakest, which is not the usual reason to make a chart.

---

## The five figures

### 1. All sectors indexed, log scale

Every sector's rebased trajectory, with the eight persistently slow sectors drawn in red and Jewelry emphasised within that group.

Two decisions worth explaining. The scale is logarithmic because the fastest sector ends near 2280 and the slowest near 145; on a linear axis the top line sets the range and everything below 500 collapses into an unreadable band, which is precisely the region the analysis is about.

The highlight is the whole slow group rather than Jewelry alone. Earlier we drew Jewelry by itself and labelled it the laggard, and that framing asserts a uniqueness the analysis does not support. Eight sectors sat in the bottom tier every year. Jewelry is the clearest case, not an isolated one, and a group is also the stronger visual argument — one red line among fifteen grey ones looks like an anomaly, while eight looks like a structure.

### 2. Sectors ranked by December 2023 index

The bar chart, with values labelled and the two tier cuts drawn as vertical lines rather than left implicit in the colouring.

Drawing the cuts is the change that matters. A reader who sees only the colours has to trust that the boundaries were placed honestly. A reader who sees the lines can look at where they fall.

### 3. National e-commerce with the lockdown window

Evidence that the `covid_period` flag built at the Collector marks a real regime rather than a convenient label: transactions rise from 6.6 million in February 2020 to 18.2 million in May, inside the tagged window. Both values are annotated on the line, because the entire point of the chart is those two numbers and a reader should not have to estimate them off an axis.

### 4. IQR fences — the test that did not agree with us

This is the chart we would have had the most reason to leave out, which is why it is here.

We expected the interquartile-range test to confirm that the slowest sector is a statistical outlier. It does not. With sixteen observations the fences land at −458 and 1528, and Jewelry sits 602 points inside the lower one. The test flags the opposite extreme instead.

The lower fence being *negative* is the part worth pointing at, and the chart says so directly. A negative index is impossible, so the fence is not a threshold at all — it is an artefact of applying a rule designed for larger samples to sixteen points. Reporting this as "the test did not flag it" would be true and slightly misleading. Reporting that the test could not have flagged anything on the low side is the accurate version.

We would rather a reader see this than take our word that we reported a disconfirming result somewhere in the appendix.

### 5. Where the tier cuts came from

The sixteen sectors as points on a line, with the gap between each consecutive pair measured, and the two cut positions marked.

The cuts are at 450 and 900, and round numbers invite the reasonable suspicion that they were chosen to produce a convenient answer. They were not, and this chart is the evidence: the 900 cut sits inside the second-largest gap in the distribution (487 points, between Public Utilities and Others), and the 450 cut sits inside the third-largest (166 points, between Furniture and Transportation). Both fall in genuine discontinuities rather than slicing through a dense run of sectors.

The single largest gap, 906 points, sits between the two fastest sectors and is marked in grey because both of them are above either cut, so it was never a candidate boundary. Saying that is more useful than quietly omitting it and letting the reader assume the cuts took the top two gaps.

---

## Files

| File | What it needs |
|---|---|
| `make_charts.py` | The generator |
| `output/chart1_all_sectors_indexed.png` | `sector_matrix_indexed.csv` |
| `output/chart2_growth_ranking.png` | `sector_growth_tiers.csv` |
| `output/chart3_ecommerce_covid_spike.png` | `preprocessed_wide.csv` |
| `output/chart4_iqr_fences.png` | `sector_growth_tiers.csv` |
| `output/chart5_tier_cut_justification.png` | `sector_growth_tiers.csv` |
| `output/sector_growth_tiers.csv` | Regenerated when the indexed matrix is present |

## Running it

```bash
pip install pandas numpy matplotlib
python3 make_charts.py
```

Charts 2, 4 and 5 need only `sector_growth_tiers.csv`, which is in this folder, so they build immediately. Charts 1 and 3 need `sector_matrix_indexed.csv` and `preprocessed_wide.csv` from Step 3 copied in; the script reports which ones it skipped rather than failing.

---

## One caution about chart 2

The tier binning shown here is a manual construction, and Step 4 later compares its clustering output against it. That comparison should not be read as strong independent confirmation, because both the clustering and these bins derive largely from where each sector's series ends. Two methods measuring the same quantity will agree, and their agreement is not evidence.

We keep the chart because the ranking is real and the tiers are useful for communication. We keep this paragraph because a figure that gets cited as confirmation of something it cannot confirm is worse than no figure at all.
