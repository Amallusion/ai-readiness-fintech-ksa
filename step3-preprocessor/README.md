# Step 3 — Pre-processor (PP)

Validates and cleans Step 2's output, and builds the version of the data
that's actually shaped for modeling in Step 4.

## Files

- `preprocess.py` — the Preprocessor script; run with `python3 preprocess.py`
- `input_from_step2_*.csv` — copies of Step 2's output, used as input here
- `validation_report.txt` — the checks that were run and their results
- `sector_matrix_indexed.csv` — **key output.** Each sector rebased so Jan 2019 = 100. A sector at 300 in a later month means "3x growth since Jan 2019" — this is what makes sectors of very different sizes comparable, and what Step 4's clustering should use.
- `sector_matrix_growth.csv` — month-over-month % change per sector, for correlation/regression work
- `preprocessed_wide.csv` — the confirmed-clean version of the merged monthly dataset

## What was checked

- No missing values, no zero values, in the Jan 2019–Dec 2023 window
- All numeric columns are actually numeric (not text)
- The "sector redefinition" footnote from SAMA (Hotels split out of Restaurants & Café; Electronics/Furniture/Construction/Jewelry split out of Miscellaneous) does **not** create a break inside our window — every sector already has real, distinct values from month 1

## What the rebased index already shows

Ranked lowest to highest growth since Jan 2019 (100 = starting point):

| Sector | Index, Dec 2023 |
|---|---|
| Jewelry | 144.6 (only +45%) |
| Education | 224.2 |
| Health | 279.5 |
| ... | ... |
| Restaurants & Café | 811.7 |
| Public Utilities | 887.0 |
| Miscellaneous Goods and Services | 2,280.2 (23x growth) |

Jewelry is the clear laggard — confirmed now on a proper, comparable scale, not just raw transaction counts. This is a strong, defensible candidate for Step 4's clustering to isolate as its own group ("slow digitalizers").
