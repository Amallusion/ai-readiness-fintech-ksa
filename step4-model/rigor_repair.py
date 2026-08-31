"""
rigor_repair.py
================
ITU AI Readiness Hackathon (KSA) — Fintech track
Addresses external ML-specialist review of Step 4 (Model).

CRITIQUE BEING ADDRESSED
------------------------
Growth ratio, rebased Dec-2023 index, and level-based K-Means are all
near-deterministic functions of "where the series ends up" -- not three
independent checks. This script adds the genuinely independent checks and
repairs the specific claims that don't hold up:

  A. Average ticket size (Sales / Transactions) vs. digital growth --
     uses a dimension of the data (value-per-transaction) that is
     independent of trajectory shape/level. The mechanism check.
  B. Differenced-series (month-over-month growth rate) correlation with
     the e-commerce trend, alongside the original level-based one.
  C. Silhouette scores, k=2..6 -- justifies k=3 with evidence instead of
     asserting it.
  D. Z-normalized (standardized) clustering -- genuinely clusters on
     trajectory SHAPE, independent of final level, unlike the original.
  E. Bootstrap ranking stability -- how often Jewelry lands bottom across
     1000 month-resampled recomputations of the rebased index.

OUTPUTS (./output/):
  - chart8_ticket_size_vs_growth.png
  - ticket_size_regression_report.txt
  - correlation_comparison.csv   (level-based vs. differenced, side by side)
  - chart9_silhouette_scores.png
  - shape_cluster_results.csv    (z-normalized clustering vs. level clustering vs. manual)
  - bootstrap_ranking_report.txt
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

IN_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(IN_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

WIDE_PATH = os.path.join(IN_DIR, "collected_wide.csv")
INDEXED_PATH = os.path.join(IN_DIR, "sector_matrix_indexed.csv")
GROWTH_PATH = os.path.join(IN_DIR, "sector_matrix_growth.csv")
CLUSTERS_PATH = os.path.join(IN_DIR, "cluster_results.csv")

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["figure.dpi"] = 150

SECTORS = [
    "Transportation", "Health", "Restaurants & Café", "Hotels",
    "Beverage and Food", "Clothing and Footwear", "Recreation and Culture",
    "Miscellaneous Goods and Services", "Electronic & Electric Devices",
    "Furniture", "Construction & Building Materials", "Jewelry",
    "Telecommunication", "Education", "Public Utilities", "Others",
]

ANCHOR_LABELS = ["Jewelry", "Miscellaneous Goods and Services",
                  "Restaurants & Café", "Transportation"]


# ---------------------------------------------------------------------
# A. Average ticket size vs. digital growth
# ---------------------------------------------------------------------
def ticket_size_analysis(wide: pd.DataFrame, indexed: pd.DataFrame):
    wide_2019 = wide[wide["Date"].astype(str).str.startswith("2019")]
    end_col = indexed.columns[-1]  # 2023-12

    records = []
    for sector in SECTORS:
        txn_col = f"{sector} - Number of Transactions"
        sales_col = f"{sector} - Sales"
        mean_txn = wide_2019[txn_col].mean()
        mean_sales = wide_2019[sales_col].mean()
        avg_ticket = mean_sales / mean_txn  # SAR (thousand-riyal units carried through consistently)
        growth_index = indexed.loc[indexed["Sector"] == sector, end_col].values[0]
        records.append({"Sector": sector, "AvgTicket2019": avg_ticket,
                         "LogAvgTicket2019": np.log10(avg_ticket), "GrowthIndexDec2023": growth_index})

    df = pd.DataFrame(records)

    # OLS regression: log(ticket size) -> growth index
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df["LogAvgTicket2019"], df["GrowthIndexDec2023"]
    )
    r_squared = r_value ** 2

    # Bootstrap CI on the slope (resample sectors with replacement, n=16)
    rng = np.random.default_rng(42)
    n = len(df)
    boot_slopes = []
    for _ in range(2000):
        idx = rng.integers(0, n, n)
        bx = df["LogAvgTicket2019"].values[idx]
        by = df["GrowthIndexDec2023"].values[idx]
        if np.std(bx) == 0:
            continue
        s, *_ = stats.linregress(bx, by)
        boot_slopes.append(s)
    ci_lo, ci_hi = np.percentile(boot_slopes, [2.5, 97.5])

    report = (
        f"OLS regression: GrowthIndex ~ log10(AvgTicketSize2019)\n"
        f"  slope       = {slope:.2f}\n"
        f"  intercept   = {intercept:.2f}\n"
        f"  R-squared   = {r_squared:.3f}\n"
        f"  p-value     = {p_value:.4f}\n"
        f"  95% bootstrap CI on slope (n=16, resampled sectors, 2000 draws): "
        f"[{ci_lo:.2f}, {ci_hi:.2f}]\n"
        f"\nInterpretation: {'a doubling' if slope<0 else 'an increase'} in average ticket size is associated with "
        f"a change of {slope*np.log10(2):.1f} points in the Dec-2023 growth index "
        f"(per doubling of ticket size).\n"
    )
    with open(os.path.join(OUT_DIR, "ticket_size_regression_report.txt"), "w") as f:
        f.write(report)
    print(report)

    # Chart
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(df["AvgTicket2019"], df["GrowthIndexDec2023"], s=70,
               color="#1f77b4", alpha=0.75, zorder=3)
    xs = np.linspace(df["LogAvgTicket2019"].min(), df["LogAvgTicket2019"].max(), 100)
    ys = slope * xs + intercept
    ax.plot(10 ** xs, ys, color="#d62728", linewidth=2, zorder=2,
            label=f"OLS fit: R\u00b2={r_squared:.2f}, p={p_value:.3f}")
    ax.set_xscale("log")
    ax.set_xlabel("Average ticket size, 2019 (SAR, log scale)")
    ax.set_ylabel("Digital growth index, Dec 2023 (Jan 2019 = 100)")
    ax.set_title("Is digital adoption structured by transaction value?\n"
                  "Average ticket size vs. growth, all 16 sectors")
    for _, row in df.iterrows():
        if row["Sector"] in ANCHOR_LABELS:
            ax.annotate(row["Sector"], (row["AvgTicket2019"], row["GrowthIndexDec2023"]),
                        textcoords="offset points", xytext=(8, 6), fontsize=9.5)
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart8_ticket_size_vs_growth.png"))
    plt.close(fig)

    df.to_csv(os.path.join(OUT_DIR, "ticket_size_data.csv"), index=False)
    return df


# ---------------------------------------------------------------------
# B. Differenced-series correlation, compared to original level-based
# ---------------------------------------------------------------------
def differenced_correlation(wide: pd.DataFrame, growth: pd.DataFrame):
    ecom_level = wide["E-Commerce (Mada) - Number of Transactions"]
    ecom_growth = ecom_level.pct_change() * 100

    records = []
    for sector in SECTORS:
        level_col = f"{sector} - Number of Transactions"
        level_corr = wide[level_col].corr(ecom_level)

        if sector not in growth["Sector"].values:
            continue
        # sector_matrix_growth.csv is sectors-as-rows, months-as-columns
        sector_growth_row = growth[growth["Sector"] == sector].iloc[0]
        month_cols = [c for c in growth.columns if c != "Sector"]
        sector_growth_series = sector_growth_row[month_cols].astype(float).values
        ecom_growth_aligned = ecom_growth.values[1:]  # growth series is one shorter
        min_len = min(len(sector_growth_series), len(ecom_growth_aligned))
        diff_corr = np.corrcoef(
            sector_growth_series[-min_len:], ecom_growth_aligned[-min_len:]
        )[0, 1]

        records.append({"Sector": sector, "LevelCorrelation": level_corr,
                         "DifferencedCorrelation": diff_corr})

    df = pd.DataFrame(records).sort_values("DifferencedCorrelation")
    df.to_csv(os.path.join(OUT_DIR, "correlation_comparison.csv"), index=False)
    print("\nLevel-based vs. differenced (month-over-month growth) correlation with e-commerce trend:")
    print(df.to_string(index=False))
    return df


# ---------------------------------------------------------------------
# C. Silhouette scores, k=2..6
# ---------------------------------------------------------------------
def silhouette_analysis(indexed: pd.DataFrame):
    month_cols = [c for c in indexed.columns if c != "Sector"]
    X = indexed[month_cols].values

    ks = range(2, 7)
    scores = []
    for k in ks:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X)
        score = silhouette_score(X, labels)
        scores.append(score)

    best_k = list(ks)[int(np.argmax(scores))]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(list(ks), scores, marker="o", color="#0B6E4F", linewidth=2)
    ax.axvline(3, color="#d62728", linestyle="--", alpha=0.6, label="k=3 (used)")
    ax.set_xlabel("Number of clusters (k)")
    ax.set_ylabel("Silhouette score")
    ax.set_title("Silhouette analysis: is k=3 justified?")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart9_silhouette_scores.png"))
    plt.close(fig)

    report = f"Silhouette scores by k: {dict(zip(ks, [round(s,3) for s in scores]))}\n" \
             f"Best-scoring k: {best_k}\n" \
             f"k=3 {'IS' if best_k==3 else 'is NOT'} the silhouette-optimal choice; " \
             f"{'retained k=3 for interpretability against manual tiers.' if best_k!=3 else ''}"
    print("\n" + report)
    return best_k, scores


# ---------------------------------------------------------------------
# D. Z-normalized (shape-based) clustering vs. level-based vs. manual
# ---------------------------------------------------------------------
def shape_based_clustering(indexed: pd.DataFrame, level_clusters: pd.DataFrame):
    month_cols = [c for c in indexed.columns if c != "Sector"]
    X_level = indexed[month_cols].values

    # Standardize each sector's own trajectory (row-wise z-score)
    X_shape = StandardScaler().fit_transform(X_level.T).T  # standardize each row

    km_shape = KMeans(n_clusters=3, random_state=42, n_init=10)
    shape_labels = km_shape.fit_predict(X_shape)

    result = indexed[["Sector"]].copy()
    result["ShapeCluster"] = shape_labels

    merged = result.merge(
        level_clusters[["Sector", "ClusterLabel", "ManualTier"]], on="Sector"
    )

    # Does the shape-based cluster containing Jewelry match the level-based "Slow" group?
    jewelry_shape_cluster = merged.loc[merged["Sector"] == "Jewelry", "ShapeCluster"].values[0]
    same_shape_group = merged.loc[merged["ShapeCluster"] == jewelry_shape_cluster, "Sector"].tolist()

    merged.to_csv(os.path.join(OUT_DIR, "shape_cluster_results.csv"), index=False)
    print(f"\nShape-based (z-normalized) cluster containing Jewelry also contains: {same_shape_group}")
    slow_manual = set(level_clusters.loc[level_clusters["ClusterLabel"]=="Slow (model)", "Sector"])
    overlap = set(same_shape_group) & slow_manual
    print(f"Overlap with the original level-based 'Slow' cluster ({len(slow_manual)} sectors): "
          f"{len(overlap)} of {len(same_shape_group)} shape-cluster members ({len(overlap)}/{len(slow_manual)} of Slow cluster recovered)")
    return merged


# ---------------------------------------------------------------------
# E. Bootstrap ranking stability
# CORRECTED METHOD: the first version of this function resampled raw
# calendar rows with replacement, which silently broke the "Jan 2019 =
# fixed baseline" assumption (after shuffling, row 0 is no longer
# January). Fixed by bootstrap-resampling the month-over-month GROWTH
# RATES (i.i.d. resampling of returns, standard for financial/return
# series) and reconstructing a compounded path from a fixed start of
# 100, which preserves the fixed-baseline logic correctly.
# ---------------------------------------------------------------------
def bootstrap_ranking(growth: pd.DataFrame, n_boot: int = 1000):
    rng = np.random.default_rng(42)
    month_cols = [c for c in growth.columns if c != "Sector"]

    growth_rates = {}
    for sector in SECTORS:
        row = growth[growth["Sector"] == sector].iloc[0]
        rates = row[month_cols].astype(float).dropna().values / 100  # decimal growth rates
        growth_rates[sector] = rates

    n_obs = len(growth_rates["Jewelry"])
    bottom_counts = {s: 0 for s in SECTORS}
    all_final_values = {s: [] for s in SECTORS}

    for _ in range(n_boot):
        final_values = {}
        for sector in SECTORS:
            rates = growth_rates[sector]
            resampled = rng.choice(rates, size=n_obs, replace=True)
            path = 100.0
            for r in resampled:
                path *= (1 + r)
            final_values[sector] = path
            all_final_values[sector].append(path)

        bottom_sector = min(final_values, key=final_values.get)
        bottom_counts[bottom_sector] += 1

    pct = {s: c / n_boot * 100 for s, c in bottom_counts.items()}
    pct_sorted = dict(sorted(pct.items(), key=lambda x: -x[1]))

    report = "Bootstrap ranking stability, CORRECTED (1000 resamples of month-over-month\n" \
             "growth rates, compounded from a fixed Jan-2019=100 start):\n" \
             "How often each sector lands as the SINGLE LOWEST-ranked sector:\n"
    for s, p in pct_sorted.items():
        if p > 0:
            report += f"  {s}: {p:.1f}%\n"

    ci_report = "\n95% bootstrap interval on final (Dec-2023-equivalent) index value:\n"
    for s in SECTORS:
        lo, hi = np.percentile(all_final_values[s], [2.5, 97.5])
        ci_report += f"  {s}: [{lo:.0f}, {hi:.0f}]\n"

    full_report = report + ci_report
    with open(os.path.join(OUT_DIR, "bootstrap_ranking_report.txt"), "w") as f:
        f.write(full_report)
    print("\n" + full_report)
    return pct_sorted


def main():
    wide = pd.read_csv(WIDE_PATH)
    indexed = pd.read_csv(INDEXED_PATH)
    growth = pd.read_csv(GROWTH_PATH)
    clusters = pd.read_csv(CLUSTERS_PATH)

    print("=" * 70, "\nA. TICKET SIZE ANALYSIS\n", "=" * 70)
    ticket_size_analysis(wide, indexed)

    print("\n" + "=" * 70, "\nB. DIFFERENCED-SERIES CORRELATION\n", "=" * 70)
    differenced_correlation(wide, growth)

    print("\n" + "=" * 70, "\nC. SILHOUETTE ANALYSIS (justify k)\n", "=" * 70)
    silhouette_analysis(indexed)

    print("\n" + "=" * 70, "\nD. SHAPE-BASED (Z-NORMALIZED) CLUSTERING\n", "=" * 70)
    shape_based_clustering(indexed, clusters)

    print("\n" + "=" * 70, "\nE. BOOTSTRAP RANKING STABILITY\n", "=" * 70)
    bootstrap_ranking(growth)


if __name__ == "__main__":
    main()
