"""
collector.py
============
ITU AI Readiness Hackathon (KSA) — Fintech track
STEP 2 of the Y.3172 pipeline: "C" (Collector)

WHAT THIS DOES
--------------
Takes the two raw files exported from the Saudi Central Bank (SAMA) Open
Data Platform ("Source" / SRC node) and turns them into one clean,
analysis-ready dataset ("Collector" / C node):

  1. sector_pos_raw.xls   -> "Points of Sale Transactions by Sectors"
                              (Jan 2016 - Dec 2023, monthly, 16 sectors)
  2. ecommerce_raw.xls    -> "E-Commerce Transactions Using Mada Cards"
                              (Jan 1995 - Jun 2026, monthly; real values
                              only start Jan 2019)

Both raw files are MHTML ("web page") files saved with an .xls extension
(SAMA's export format) — a multi-sheet HTML document, not a real binary
Excel file. This script parses that format directly.

It produces three outputs (in ./output/):
  - collected_wide.csv     one row per month, every sector + e-commerce
                            metric as columns, plus event-tag columns.
                            This is the main "Collector" deliverable.
  - collected_long.csv     tidy format: Date, Sector, Metric, Value.
  - sector_transactions_matrix.csv
                            rows = sectors, columns = months, values =
                            Number of Transactions. Shaped for clustering
                            in Step 4 (each row is one sector's trend).

EVENT TAGS ADDED
-----------------
  - covid_period        True for the core Saudi lockdown window
                         (Mar 2020 - Jun 2020)
  - ramadan_month        True if any part of Ramadan falls in that month
                         (approximate, Umm al-Qura calendar, +/-1 day)
  - post_epayments_law  True from 2020 onward, marking SAMA's "Rules for
                         Electronic Payment Services" (2020)

SHARED DATE WINDOW
-------------------
File 1 has real data Jan 2016 - Dec 2023. File 2 has real data only from
Jan 2019 onward (earlier months are blank in the source). The merged
output is trimmed to Jan 2019 - Dec 2023, the range where BOTH sources
have real numbers, so no fake gaps are introduced.
"""

import email
from email import policy
import io
import os

import pandas as pd

RAW_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(RAW_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

SECTOR_FILE = os.path.join(RAW_DIR, "sector_pos_raw.xls")
ECOM_FILE = os.path.join(RAW_DIR, "ecommerce_raw.xls")

SHARED_START = "2019-01"
SHARED_END = "2023-12"

# Approximate Ramadan date ranges in Saudi Arabia (Umm al-Qura calendar).
# Confirmed years (2020, 2021, 2022) come from official Saudi moon-sighting
# announcements; other years are estimated using the ~11-day yearly shift
# and are accurate to within about 1 day.
RAMADAN_RANGES = {
    2016: ("2016-06-06", "2016-07-05"),
    2017: ("2017-05-27", "2017-06-24"),
    2018: ("2018-05-16", "2018-06-14"),
    2019: ("2019-05-06", "2019-06-03"),
    2020: ("2020-04-24", "2020-05-23"),
    2021: ("2021-04-13", "2021-05-12"),
    2022: ("2022-04-02", "2022-05-01"),
    2023: ("2023-03-23", "2023-04-20"),
}

COVID_START = "2020-03"
COVID_END = "2020-06"


def _get_sheet_html(path: str, location: str) -> str:
    """Pull one named part (e.g. 'sheet2.htm') out of a SAMA MHTML export."""
    with open(path, "rb") as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
    for part in msg.walk():
        if part.get("Content-Location") == location:
            return part.get_content()
    raise ValueError(f"Could not find {location} inside {path}")


def _load_monthly_table(path: str) -> pd.DataFrame:
    """Load the 'Monthly' sheet (sheet2.htm) of a SAMA export as a DataFrame."""
    html = _get_sheet_html(path, "sheet2.htm")
    df = pd.read_html(io.StringIO(html))[0]
    return df


def load_sector_data() -> pd.DataFrame:
    """Return tidy long-format sector POS data: Date, Sector, Metric, Value."""
    df = _load_monthly_table(SECTOR_FILE)

    # Drop the trailing "Foot Notes" rows (non-data rows at the bottom).
    date_col = df.columns[0]
    df = df[df[date_col].astype(str).str.match(r"^[A-Za-z]{3} \d{4}$")].copy()

    date_series = pd.to_datetime(df[date_col], format="%b %Y").dt.to_period("M")

    records = []
    for col in df.columns[1:]:
        # col is a tuple like (..., ..., 'Transportation', 'Number of Transactions')
        sector = col[2]
        metric = col[3]
        if sector in ("Total", "Unnamed: 0_level_2"):
            continue  # skip the grand total column, we recompute what we need
        values = pd.to_numeric(
            df[col].astype(str).str.replace(",", "").replace("-", pd.NA), errors="coerce"
        )
        for d, v in zip(date_series, values):
            records.append({"Date": d, "Sector": sector, "Metric": metric, "Value": v})

    long_df = pd.DataFrame.from_records(records)
    return long_df


def load_ecommerce_data() -> pd.DataFrame:
    """Return tidy long-format e-commerce data: Date, Sector, Metric, Value."""
    df = _load_monthly_table(ECOM_FILE)
    date_col = df.columns[0]
    df = df[df[date_col].astype(str).str.match(r"^[A-Za-z]{3} \d{4}$")].copy()

    date_series = pd.to_datetime(df[date_col], format="%b %Y").dt.to_period("M")

    records = []
    for col in df.columns[1:]:
        metric = col[3]  # 'Sales (In Thousand Riyals)' or 'Number of Transactions'
        values = pd.to_numeric(
            df[col].astype(str).str.replace(",", "").replace("-", pd.NA), errors="coerce"
        )
        for d, v in zip(date_series, values):
            records.append(
                {"Date": d, "Sector": "E-Commerce (Mada)", "Metric": metric, "Value": v}
            )

    long_df = pd.DataFrame.from_records(records)
    return long_df


def add_event_tags(wide_df: pd.DataFrame) -> pd.DataFrame:
    """Add covid_period, ramadan_month, post_epayments_law boolean columns."""
    wide_df = wide_df.copy()
    month_start = wide_df["Date"].dt.to_timestamp(how="start")
    month_end = wide_df["Date"].dt.to_timestamp(how="end")

    wide_df["covid_period"] = wide_df["Date"].astype(str).between(COVID_START, COVID_END)

    def _is_ramadan(row_start, row_end, year):
        if year not in RAMADAN_RANGES:
            return False
        r_start, r_end = (pd.Timestamp(x) for x in RAMADAN_RANGES[year])
        return not (row_end < r_start or row_start > r_end)

    ramadan_flags = []
    for start, end, year in zip(month_start, month_end, wide_df["Date"].dt.year):
        # a Ramadan that starts near year-end can spill into the next month's
        # year bucket, so check both the row's own year and the next one
        flag = _is_ramadan(start, end, year) or _is_ramadan(start, end, year - 1)
        ramadan_flags.append(flag)
    wide_df["ramadan_month"] = ramadan_flags

    wide_df["post_epayments_law"] = wide_df["Date"].dt.year >= 2020

    return wide_df


def build_wide_table(sector_long: pd.DataFrame, ecom_long: pd.DataFrame) -> pd.DataFrame:
    combined_long = pd.concat([sector_long, ecom_long], ignore_index=True)
    combined_long["Metric"] = combined_long["Metric"].replace(
        {
            "Sales (In Thousand Riyals)": "Sales",
        }
    )
    combined_long["Column"] = combined_long["Sector"] + " - " + combined_long["Metric"]

    wide = combined_long.pivot_table(
        index="Date", columns="Column", values="Value", aggfunc="first"
    ).reset_index()
    wide = wide.sort_values("Date").reset_index(drop=True)

    # Trim to the shared window where BOTH sources have real data.
    wide = wide[
        (wide["Date"].astype(str) >= SHARED_START) & (wide["Date"].astype(str) <= SHARED_END)
    ].reset_index(drop=True)

    wide = add_event_tags(wide)
    return wide


def build_sector_matrix(sector_long: pd.DataFrame) -> pd.DataFrame:
    """One row per sector, one column per month, values = Number of Transactions.
    Shaped for clustering: each row is a sector's trend vector across time."""
    txn = sector_long[sector_long["Metric"] == "Number of Transactions"].copy()
    txn = txn[
        (txn["Date"].astype(str) >= SHARED_START) & (txn["Date"].astype(str) <= SHARED_END)
    ]
    matrix = txn.pivot_table(index="Sector", columns="Date", values="Value", aggfunc="first")
    matrix.columns = [str(c) for c in matrix.columns]
    return matrix.reset_index()


def main():
    print("Loading raw sector POS data (SRC 1)...")
    sector_long = load_sector_data()
    print(f"  -> {sector_long['Sector'].nunique()} sectors, "
          f"{sector_long['Date'].nunique()} months of raw history")

    print("Loading raw e-commerce data (SRC 2)...")
    ecom_long = load_ecommerce_data()
    real_ecom = ecom_long.dropna(subset=["Value"])
    print(f"  -> real e-commerce data covers "
          f"{real_ecom['Date'].min()} to {real_ecom['Date'].max()}")

    print("Merging on the shared date window "
          f"({SHARED_START} to {SHARED_END}) and adding event tags...")
    wide = build_wide_table(sector_long, ecom_long)
    long_out = pd.concat([sector_long, ecom_long], ignore_index=True)
    long_out = long_out[
        (long_out["Date"].astype(str) >= SHARED_START)
        & (long_out["Date"].astype(str) <= SHARED_END)
    ]
    matrix = build_sector_matrix(sector_long)

    wide_path = os.path.join(OUT_DIR, "collected_wide.csv")
    long_path = os.path.join(OUT_DIR, "collected_long.csv")
    matrix_path = os.path.join(OUT_DIR, "sector_transactions_matrix.csv")

    wide.to_csv(wide_path, index=False)
    long_out.to_csv(long_path, index=False)
    matrix.to_csv(matrix_path, index=False)

    print("\nDone. Wrote:")
    print(f"  {wide_path}   ({wide.shape[0]} rows x {wide.shape[1]} cols)")
    print(f"  {long_path}   ({long_out.shape[0]} rows)")
    print(f"  {matrix_path}   ({matrix.shape[0]} sectors x {matrix.shape[1]-1} months)")

    print("\nEvent tag counts in the collected window:")
    print(f"  covid_period months: {int(wide['covid_period'].sum())}")
    print(f"  ramadan_month months: {int(wide['ramadan_month'].sum())}")
    print(f"  post_epayments_law months: {int(wide['post_epayments_law'].sum())}")


if __name__ == "__main__":
    main()
