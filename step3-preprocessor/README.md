# Step 3 — Pre-processor (PP)

Validates and cleans Step 2's output, and builds the version of the data
that's actually shaped for modeling in Step 4.

## Files

- `preprocess.py` — the Preprocessor script; run with `python3 preprocess.py`
- `input_from_step2_*.csv` — copies of Step 2's output, used as input here
- `validation_report.txt` — the checks that were run and their results
- `sector_matrix_indexed.csv` — key output. Each sector rebased so Jan 2019 = 100
- `sector_matrix_growth.csv` — month-over-month % change per sector
- `preprocessed_wide.csv` — the confirmed-clean version of the merged monthly dataset
