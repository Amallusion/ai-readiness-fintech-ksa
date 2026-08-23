"""
model.py
========
ITU AI Readiness Hackathon (KSA) — Fintech track
STEP 4 of the Y.3172 pipeline: "M" (Model)

WHAT THIS DOES
--------------
Takes Step 3's rebased sector index (sector_matrix_indexed.csv — each
sector's monthly transaction count, Jan 2019 = 100) and applies two
independent analytical methods:

  1. CLUSTERING (K-Means, k=3)
     Groups the 16 sectors purely by the SHAPE of their 60-month growth
     trajectory — the algorithm is not told in advance which sectors are
     "slow" or "fast." We then compare its groupings against the manual
     growth-tier binning from Step 3 to see whether an unsupervised model
     independently rediscovers the same pattern a human found by hand.

  2. IQR OUTLIER CHECK (boxplot statistics)
     A standard statistical test: using the Interquartile Range (IQR) of
     final index values across all 16 sectors, flag any sector whose value
     falls below Q1 - 1.5*IQR — the conventional definition of a
     statistical outlier, not just "the lowest of the group."

OUTPUTS (./output/):
  - cluster_results.csv        Sector, Cluster, manual Tier, Agreement
  - iqr_outlier_report.txt     the IQR calculation and outlier verdict
  - chart4_clusters.png        each sector's trajectory, colored by cluster
  - chart5_boxplot_outliers.png boxplot of final index values, Jewelry marked
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

IN_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(IN_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

INDEXED_PATH = os.path.join(IN_DIR, "sector_matrix_indexed.csv")
TIERS_PATH = os.path.join(IN_DIR, "manual_growth_tiers.csv")

N_CLUSTERS = 3
RANDOM_STATE = 42

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["figure.dpi"] = 150


def run_clustering(indexed: pd.DataFrame) -> pd.DataFrame:
    month_cols = [c for c in indexed.columns if c != "Sector"]
    X = indexed[month_cols].values

    km = KMeans(n_clusters=N_CLUSTERS, random_state=RANDOM_STATE, n_init=10)
    labels = km.fit_predict(X)

    result = indexed[["Sector"]].copy()
    result["Cluster"] = labels

    # Label clusters by their average ending value, so "Cluster 0" reads as
    # "Slow" instead of an arbitrary number.
    end_col = month_cols[-1]
    result["EndIndex"] = indexed[end_col].values
    cluster_means = result.groupby("Cluster")["EndIndex"].mean().sort_values()
    rename = {
        cluster_means.index[0]: "Slow (model)",
        cluster_means.index[1]: "Moderate (model)",
        cluster_means.index[2]: "Rapid (model)",
    }
    result["ClusterLabel"] = result["Cluster"].map(rename)
    return result


def compare_to_manual(cluster_result: pd.DataFrame, manual: pd.DataFrame) -> pd.DataFrame:
    manual = manual.rename(columns={"Tier": "ManualTier"})
    merged = cluster_result.merge(manual[["Sector", "ManualTier"]], on="Sector")

    def _same_bucket(row):
        # "Slow adopters" (manual) vs "Slow (model)" -> compare first word
        return row["ManualTier"].split()[0] == row["ClusterLabel"].split()[0]

    merged["Agreement"] = merged.apply(_same_bucket, axis=1)
    return merged[["Sector", "ClusterLabel", "ManualTier", "Agreement", "EndIndex"]].sort_values(
        "EndIndex"
    )


def run_iqr_check(indexed: pd.DataFrame) -> tuple[str, pd.DataFrame]:
    end_col = indexed.columns[-1]
    values = indexed[["Sector", end_col]].rename(columns={end_col: "EndIndex"})

    q1 = values["EndIndex"].quantile(0.25)
    q3 = values["EndIndex"].quantile(0.75)
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr

    values["IsOutlier"] = (values["EndIndex"] < lower_fence) | (values["EndIndex"] > upper_fence)

    report_lines = [
        f"Q1 (25th percentile): {q1:.1f}",
        f"Q3 (75th percentile): {q3:.1f}",
        f"IQR: {iqr:.1f}",
        f"Lower fence (Q1 - 1.5*IQR): {lower_fence:.1f}",
        f"Upper fence (Q3 + 1.5*IQR): {upper_fence:.1f}",
        "",
        "Outlier sectors (outside the fences):",
    ]
    outliers = values[values["IsOutlier"]].sort_values("EndIndex")
    if len(outliers) == 0:
        report_lines.append("  None — no sector falls outside the statistical fences.")
    else:
        for _, row in outliers.iterrows():
            direction = "LOW" if row["EndIndex"] < lower_fence else "HIGH"
            report_lines.append(f"  {row['Sector']}: {row['EndIndex']:.1f} ({direction} outlier)")

    return "\n".join(report_lines), values


def chart4_clusters(indexed: pd.DataFrame, cluster_result: pd.DataFrame):
    month_cols = [c for c in indexed.columns if c != "Sector"]
    color_map = {"Slow (model)": "#d62728", "Moderate (model)": "#ff9f1c", "Rapid (model)": "#2a9d8f"}

    fig, ax = plt.subplots(figsize=(11, 6))
    for _, row in indexed.iterrows():
        sector = row["Sector"]
        label = cluster_result.loc[cluster_result["Sector"] == sector, "ClusterLabel"].values[0]
        values = row[month_cols].astype(float).values
        lw = 3 if sector == "Jewelry" else 1.3
        ax.plot(month_cols, values, color=color_map[label], linewidth=lw, alpha=0.9 if lw == 3 else 0.6)

    ax.axhline(100, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.set_xticks(month_cols[::6])
    ax.set_xticklabels(month_cols[::6], rotation=45, ha="right")
    ax.set_ylabel("Index (Jan 2019 = 100)")
    ax.set_title("K-Means clustering (k=3) of sector growth trajectories\n(color = cluster the model assigned, not a manual label)")
    handles = [plt.Line2D([0], [0], color=c, lw=3) for c in color_map.values()]
    ax.legend(handles, color_map.keys(), loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart4_clusters.png"))
    plt.close(fig)


def chart5_boxplot(iqr_values: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 6))
    bp = ax.boxplot(iqr_values["EndIndex"], vert=True, widths=0.4, patch_artist=True)
    bp["boxes"][0].set_facecolor("#cfe8ff")

    for _, row in iqr_values.iterrows():
        jitter = np.random.uniform(-0.05, 0.05)
        color = "#d62728" if row["Sector"] == "Jewelry" else ("#333333" if row["IsOutlier"] else "#888888")
        size = 60 if row["Sector"] == "Jewelry" else 25
        ax.scatter(1 + jitter, row["EndIndex"], color=color, s=size, zorder=3)
        if row["Sector"] == "Jewelry" or row["IsOutlier"]:
            ax.annotate(row["Sector"], (1 + jitter, row["EndIndex"]),
                        textcoords="offset points", xytext=(10, 0), fontsize=9)

    ax.set_xticks([1])
    ax.set_xticklabels(["All 16 sectors, Dec 2023 index"])
    ax.set_ylabel("Index (Jan 2019 = 100)")
    ax.set_title("Boxplot / IQR check: is Jewelry a statistical outlier,\nnot just the lowest of a normal range?")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart5_boxplot_outliers.png"))
    plt.close(fig)


def main():
    indexed = pd.read_csv(INDEXED_PATH)
    manual = pd.read_csv(TIERS_PATH)

    cluster_result = run_clustering(indexed)
    comparison = compare_to_manual(cluster_result, manual)
    comparison.to_csv(os.path.join(OUT_DIR, "cluster_results.csv"), index=False)

    print("Clustering result vs. manual binning:")
    print(comparison.to_string(index=False))
    agreement_rate = comparison["Agreement"].mean()
    print(f"\nAgreement between model clusters and manual tiers: {agreement_rate:.0%}")

    iqr_report, iqr_values = run_iqr_check(indexed)
    print("\n" + iqr_report)
    with open(os.path.join(OUT_DIR, "iqr_outlier_report.txt"), "w") as f:
        f.write(iqr_report + "\n")

    chart4_clusters(indexed, cluster_result)
    chart5_boxplot(iqr_values)

    print("\nWrote cluster_results.csv, iqr_outlier_report.txt, chart4_clusters.png, chart5_boxplot_outliers.png")


if __name__ == "__main__":
    main()
