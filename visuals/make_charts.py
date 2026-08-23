"""
make_charts.py
===============
ITU AI Readiness Hackathon (KSA) — Fintech track
Visual illustrations for Step 3 (Pre-processor) findings, and a simple
growth-tier binning of the 16 sectors.

INPUTS (from Step 3's output):
  - sector_matrix_indexed.csv   sectors rebased to 100 = Jan 2019
  - preprocessed_wide.csv       merged monthly dataset incl. covid_period flag

OUTPUTS (./output/):
  - chart1_all_sectors_indexed.png   every sector's rebased growth line,
                                      Jewelry highlighted as the laggard
  - chart2_growth_ranking.png        horizontal bar chart, sectors ranked
                                      by Dec-2023 index, colored by tier
  - chart3_ecommerce_covid_spike.png national e-commerce trend with the
                                      COVID period shaded
  - sector_growth_tiers.csv          the binning table (Sector, Dec-2023
                                      index, Tier)
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

IN_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(IN_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["figure.dpi"] = 150

JEWELRY = "Jewelry"
HIGHLIGHT_COLOR = "#d62728"   # red
NORMAL_COLOR = "#b0b0b0"      # light gray
ACCENT_COLOR = "#1f77b4"      # blue


def bin_growth_tier(value: float) -> str:
    if value < 450:
        return "Slow adopters"
    elif value < 900:
        return "Moderate adopters"
    else:
        return "Rapid adopters"


def chart1_lines(indexed: pd.DataFrame):
    month_cols = [c for c in indexed.columns if c != "Sector"]
    fig, ax = plt.subplots(figsize=(11, 6))

    for _, row in indexed.iterrows():
        sector = row["Sector"]
        values = row[month_cols].astype(float).values
        if sector == JEWELRY:
            continue  # draw it last, on top
        ax.plot(month_cols, values, color=NORMAL_COLOR, linewidth=1, alpha=0.7)

    jewelry_row = indexed[indexed["Sector"] == JEWELRY].iloc[0]
    ax.plot(
        month_cols,
        jewelry_row[month_cols].astype(float).values,
        color=HIGHLIGHT_COLOR,
        linewidth=3,
        label="Jewelry (laggard)",
    )

    ax.axhline(100, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.set_xticks(month_cols[::6])
    ax.set_xticklabels(month_cols[::6], rotation=45, ha="right")
    ax.set_ylabel("Index (Jan 2019 = 100)")
    ax.set_title(
        "POS transaction growth by sector, Jan 2019-Dec 2023\n"
        "(all 16 sectors, gray; Jewelry highlighted in red)"
    )
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart1_all_sectors_indexed.png"))
    plt.close(fig)


def chart2_ranking(indexed: pd.DataFrame) -> pd.DataFrame:
    last_col = indexed.columns[-1]
    ranked = indexed[["Sector", last_col]].copy()
    ranked.columns = ["Sector", "Index_Dec2023"]
    ranked["Tier"] = ranked["Index_Dec2023"].apply(bin_growth_tier)
    ranked = ranked.sort_values("Index_Dec2023")

    tier_colors = {
        "Slow adopters": HIGHLIGHT_COLOR,
        "Moderate adopters": "#ff9f1c",
        "Rapid adopters": "#2a9d8f",
    }
    colors = ranked["Tier"].map(tier_colors)

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.barh(ranked["Sector"], ranked["Index_Dec2023"], color=colors)
    ax.axvline(100, color="black", linewidth=0.8, linestyle="--", alpha=0.6)
    ax.set_xlabel("Index, Dec 2023 (Jan 2019 = 100)")
    ax.set_title("Sectors ranked by digital-payment growth, colored by tier")

    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in tier_colors.values()]
    ax.legend(handles, tier_colors.keys(), loc="lower right")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart2_growth_ranking.png"))
    plt.close(fig)

    return ranked.sort_values("Index_Dec2023", ascending=False)


def chart3_covid(wide: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(
        wide["Date"],
        wide["E-Commerce (Mada) - Number of Transactions"],
        color=ACCENT_COLOR,
        linewidth=2,
    )

    covid_dates = wide.loc[wide["covid_period"], "Date"]
    if len(covid_dates) > 0:
        ax.axvspan(
            covid_dates.iloc[0], covid_dates.iloc[-1],
            color=HIGHLIGHT_COLOR, alpha=0.15, label="COVID lockdown period"
        )

    ax.set_xticks(wide["Date"][::6])
    ax.set_xticklabels(wide["Date"][::6], rotation=45, ha="right")
    ax.set_ylabel("E-commerce transactions (Mada cards)")
    ax.set_title("National e-commerce trend, with COVID lockdown period highlighted")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart3_ecommerce_covid_spike.png"))
    plt.close(fig)


def main():
    indexed = pd.read_csv(os.path.join(IN_DIR, "sector_matrix_indexed.csv"))
    wide = pd.read_csv(os.path.join(IN_DIR, "preprocessed_wide.csv"))

    chart1_lines(indexed)
    ranked = chart2_ranking(indexed)
    chart3_covid(wide)

    ranked.to_csv(os.path.join(OUT_DIR, "sector_growth_tiers.csv"), index=False)

    print("Wrote 3 charts and 1 binning table to ./output/\n")
    print("Growth tiers:")
    print(ranked.to_string(index=False))


if __name__ == "__main__":
    main()
