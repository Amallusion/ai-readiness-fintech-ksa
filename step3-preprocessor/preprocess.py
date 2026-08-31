"""
preprocess.py
=============
ITU AI Readiness Hackathon (KSA) — Fintech track
STEP 3 of the Y.3172 pipeline: "PP" (Pre-processor)

WHAT THIS DOES
--------------
Takes the Collector's output (Step 2: collected_wide.csv,
sector_transactions_matrix.csv) and makes it model-ready:

  1. VALIDATE  - confirm no missing values, no zeros, correct data types,
                 and that the known "sector redefinition" footnote from
                 SAMA (Hotels split from Restaurants & Cafe; Electronics/
                 Furniture/Construction/Jewelry split from Miscellaneous)
                 does not create a break inside our Jan2019-Dec2023 window.

  2. INDEX     - rebase every sector's transaction count to start at 100
                 in Jan 2019 (like a stock market index). This makes
                 sectors of very different sizes (Restaurants: ~30,000/mo
                 vs Jewelry: ~700/mo) directly comparable by GROWTH SHAPE
                 rather than by raw size — required before any sensible
                 clustering in Step 4.

  3. GROWTH    - compute month-over-month % change for every sector, for
                 use in correlation/regression analysis in Step 4.

OUTPUTS (in ./output/):
  - validation_report.txt        plain-text summary of the checks run
  - sector_matrix_indexed.csv    sectors x months, rebased to 100 = Jan 2019
  - sector_matrix_growth.csv     sectors x months, month-over-month % change
  - preprocessed_wide.csv        collected_wide.csv, unchanged except with
                                  confirmed numeric dtypes (the "clean"
                                  version to hand to Step 4)
"""

import os

import pandas as pd

IN_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(IN_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

WIDE_PATH = os.path.join(IN_DIR, "collected_wide.csv")
MATRIX_PATH = os.path.join(IN_DIR, "sector_transactions_matrix.csv")


def validate(wide: pd.DataFrame, matrix: pd.DataFrame) -> list[str]:
    """Run sanity checks and return a list of human-readable report lines."""
    lines = []

    lines.append(f"Rows in collected_wide.csv (months): {len(wide)}")
    lines.append(f"Date range: {wide['Date'].min()} to {wide['Date'].max()}")

    numeric_cols = [
        c for c in wide.columns
        if c not in ("Date", "covid_period", "ramadan_month", "post_epayments_law")
    ]
    n_missing = wide[numeric_cols].isna().sum().sum()
    n_zero = (wide[numeric_cols] == 0).sum().sum()
    lines.append(f"Missing values in numeric columns: {n_missing}")
    lines.append(f"Exact-zero values in numeric columns: {n_zero}")

    sector_cols_to_check = [
        "Hotels - Number of Transactions",
        "Restaurants & Café - Number of Transactions",
        "Electronic & Electric Devices - Number of Transactions",
        "Furniture - Number of Transactions",
        "Construction & Building Materials - Number of Transactions",
        "Jewelry - Number of Transactions",
        "Miscellaneous Goods and Services - Number of Transactions",
    ]
    missing_or_zero_at_start = (
        wide.loc[0, sector_cols_to_check].isna().any()
        or (wide.loc[0, sector_cols_to_check] == 0).any()
    )
    lines.append(
        "Sector-redefinition footnote check (Hotels/Electronics/Furniture/"
        "Construction/Jewelry all have real, non-zero values from month 1): "
        + ("FAIL - discontinuity present" if missing_or_zero_at_start else "PASS")
    )

    for c in numeric_cols:
        if not pd.api.types.is_numeric_dtype(wide[c]):
            lines.append(f"WARNING: column '{c}' is not numeric")

    lines.append(f"\nSectors in matrix: {len(matrix)}")
    lines.append(f"Months in matrix: {matrix.shape[1] - 1}")

    return lines


def build_indexed_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    """Rebase each sector's row so the first month = 100."""
    month_cols = [c for c in matrix.columns if c != "Sector"]
    indexed = matrix.copy()
    base = indexed[month_cols[0]]
    for c in month_cols:
        indexed[c] = (indexed[c] / base) * 100
    return indexed


def build_growth_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    """Month-over-month percent change for each sector."""
    month_cols = [c for c in matrix.columns if c != "Sector"]
    growth = matrix[["Sector"]].copy()
    values = matrix[month_cols]
    pct = values.pct_change(axis=1) * 100
    for c in month_cols[1:]:
        growth[c] = pct[c]
    return growth


def main():
    wide = pd.read_csv(WIDE_PATH)
    matrix = pd.read_csv(MATRIX_PATH)

    report_lines = validate(wide, matrix)
    report_text = "\n".join(report_lines)
    print(report_text)

    with open(os.path.join(OUT_DIR, "validation_report.txt"), "w") as f:
        f.write(report_text + "\n")

    indexed = build_indexed_matrix(matrix)
    indexed.to_csv(os.path.join(OUT_DIR, "sector_matrix_indexed.csv"), index=False)

    growth = build_growth_matrix(matrix)
    growth.to_csv(os.path.join(OUT_DIR, "sector_matrix_growth.csv"), index=False)

    wide.to_csv(os.path.join(OUT_DIR, "preprocessed_wide.csv"), index=False)

    print("\nWrote:")
    print(f"  {os.path.join(OUT_DIR, 'validation_report.txt')}")
    print(f"  {os.path.join(OUT_DIR, 'sector_matrix_indexed.csv')}")
    print(f"  {os.path.join(OUT_DIR, 'sector_matrix_growth.csv')}")
    print(f"  {os.path.join(OUT_DIR, 'preprocessed_wide.csv')}")

    # Quick preview: which sectors ended highest/lowest on the rebased index
    last_col = indexed.columns[-1]
    ranked = indexed[["Sector", last_col]].sort_values(last_col)
    print(f"\nRebased index value in {last_col} (100 = Jan 2019 level), lowest to highest:")
    print(ranked.to_string(index=False))


if __name__ == "__main__":
    main()
