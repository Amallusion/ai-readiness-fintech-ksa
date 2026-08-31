"""
diagnostics.py
===============
ITU AI Readiness Hackathon (KSA) — Fintech track — Team Voxel
STEP 4 (Model): robustness diagnostics.

Computes the leverage, rank-correlation and significance-threshold checks that
determine how much weight the headline results can bear. Runs on the Step 4
result files alone, so it can be re-verified without re-running the full
pipeline.

Checks performed:
  A. Ticket size — OLS and Spearman on all 16 sectors and on the 14
     single-purpose sectors; leave-one-out fragility; residual analysis.
  B. Correlation with the national e-commerce trend — level vs differenced,
     with the |r| thresholds needed for significance, uncorrected and Bonferroni.
  C. Shape-based clustering — cluster sizes, and what they imply about how the
     partition should be described.

INPUTS  (same directory): ticket_size_data.csv, correlation_comparison.csv,
                          shape_cluster_results.csv
OUTPUTS (./output/)     : diagnostics_report.txt
                          chart8c_ticket_size_with_fragility.png
                          leave_one_out.csv
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

IN_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(IN_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["figure.dpi"] = 150

CATCHALL = ["Miscellaneous Goods and Services", "Others"]
LABEL = ["Jewelry", "Education", "Restaurants & Café", "Public Utilities",
         "Miscellaneous Goods and Services", "Others"]


def ols(d):
    s, i, r, p, _ = stats.linregress(d["LogAvgTicket2019"], d["GrowthIndexDec2023"])
    return s, i, r ** 2, p


def main():
    out = []
    df = pd.read_csv(os.path.join(IN_DIR, "ticket_size_data.csv"))
    clean = df[~df["Sector"].isin(CATCHALL)].reset_index(drop=True)

    s16, i16, r16, p16 = ols(df)
    s14, i14, r14, p14 = ols(clean)
    rho16, prho16 = stats.spearmanr(df["LogAvgTicket2019"], df["GrowthIndexDec2023"])
    rho14, prho14 = stats.spearmanr(clean["LogAvgTicket2019"], clean["GrowthIndexDec2023"])

    out.append("A. TICKET SIZE — fit and fragility")
    out.append("=" * 68)
    out.append(f"  OLS,  all 16 : R2={r16:.3f}  p={p16:.4f}")
    out.append(f"  OLS,      14 : R2={r14:.3f}  p={p14:.4f}  slope={s14:.1f}")
    out.append(f"  Spearman, 16 : rho={rho16:.3f}  p={prho16:.4f}")
    out.append(f"  Spearman, 14 : rho={rho14:.3f}  p={prho14:.4f}")
    out.append("  The rank relationship barely moves between 16 and 14 sectors, so")
    out.append("  the two-sector exclusion is not what produces the relationship —")
    out.append("  it removes two high-growth points that inflate OLS residual")
    out.append("  variance. Neither sample reaches p<0.05 on the rank test.")
    out.append("")

    loo = []
    for k in range(len(clean)):
        _, _, r2k, pk = ols(clean.drop(k))
        loo.append({"DroppedSector": clean["Sector"][k], "R2": r2k, "p": pk,
                     "SignificanceLost": pk > 0.05})
    loo_df = pd.DataFrame(loo).sort_values("p", ascending=False)
    n_lost = int(loo_df["SignificanceLost"].sum())
    loo_df.to_csv(os.path.join(OUT_DIR, "leave_one_out.csv"), index=False)

    out.append(f"  Leave-one-out: {n_lost} of {len(clean)} single removals push p above 0.05")
    for _, r in loo_df.iterrows():
        flag = "  <-- significance lost" if r["SignificanceLost"] else ""
        out.append(f"    drop {r['DroppedSector']:36s} R2={r['R2']:.3f} p={r['p']:.4f}{flag}")
    out.append("  p=0.04 at n=14 is a knife-edge. Report as suggestive, not established.")
    out.append("")

    clean = clean.copy()
    clean["Predicted"] = s14 * clean["LogAvgTicket2019"] + i14
    clean["Residual"] = clean["GrowthIndexDec2023"] - clean["Predicted"]
    rs = clean.sort_values("Residual")
    out.append("  Residuals (most negative first):")
    out.append(rs[["Sector", "GrowthIndexDec2023", "Predicted", "Residual"]].to_string(
        index=False, float_format=lambda x: f"{x:.1f}"))
    jr = int(rs.reset_index().index[rs.reset_index()["Sector"] == "Jewelry"][0]) + 1
    out.append(f"  Jewelry residual rank: {jr} of {len(clean)} (most negative = 1).")
    out.append("  Jewelry does NOT sit on the fitted line — it is well below it.")
    out.append("  Education is the sector that sits on the line (residual ~ -6).")
    out.append("")

    cc = pd.read_csv(os.path.join(IN_DIR, "correlation_comparison.csv"))
    n = 59
    tc = stats.t.ppf(0.975, n - 2)
    r_crit = tc / np.sqrt(n - 2 + tc ** 2)
    tb = stats.t.ppf(1 - 0.025 / 16, n - 2)
    r_bonf = tb / np.sqrt(n - 2 + tb ** 2)
    absd = cc["DifferencedCorrelation"].abs()

    out.append("B. CORRELATION — differencing collapses it for every sector")
    out.append("=" * 68)
    out.append(f"  mean |level correlation|       = {cc['LevelCorrelation'].abs().mean():.3f}")
    out.append(f"  mean |differenced correlation| = {absd.mean():.3f}")
    out.append(f"  range of differenced r         = [{cc['DifferencedCorrelation'].min():.3f}, "
               f"{cc['DifferencedCorrelation'].max():.3f}]")
    out.append(f"  |r| for p<0.05 at n={n}          = {r_crit:.3f}  -> {(absd > r_crit).sum()} of 16 pass")
    out.append(f"  |r| after Bonferroni (16 tests) = {r_bonf:.3f}  -> {(absd > r_bonf).sum()} of 16 pass")
    out.append("  The finding is not that Jewelry moved to mid-range. It is that the")
    out.append("  level correlations were measuring shared upward trend for ALL sectors")
    out.append("  and carry no sector-specific signal. This retires the correlation leg")
    out.append("  of the original 'three independent confirmations' claim entirely.")
    out.append("")

    sc = pd.read_csv(os.path.join(IN_DIR, "shape_cluster_results.csv"))
    sizes = sc["ShapeCluster"].value_counts().sort_index()
    jc = sc.loc[sc["Sector"] == "Jewelry", "ShapeCluster"].iloc[0]
    mates = sc.loc[sc["ShapeCluster"] == jc, "Sector"].tolist()
    out.append("C. SHAPE CLUSTERING — the partition is degenerate")
    out.append("=" * 68)
    out.append(f"  cluster sizes at k=3: {sizes.tolist()}")
    out.append(f"  Jewelry's cluster    : {mates}")
    out.append("  One large cluster plus a pair plus a singleton is an outlier detector,")
    out.append("  not three adoption tiers. Describe these as the sectors whose")
    out.append("  trajectory shape is least typical, and always quote the sizes.")
    out.append("  Silhouette was never run in shape space — only on levels. Run it.")
    out.append("")

    text = "\n".join(out)
    with open(os.path.join(OUT_DIR, "diagnostics_report.txt"), "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(text)

    # ---- two-panel hero figure ----
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.2),
                                    gridspec_kw={"width_ratios": [1.35, 1]})
    excl = df[df["Sector"].isin(CATCHALL)]
    ax1.scatter(clean["AvgTicket2019"], clean["GrowthIndexDec2023"], s=85,
                color="#1f77b4", alpha=0.85, zorder=3, label="Single-purpose sectors (n=14)")
    ax1.scatter(excl["AvgTicket2019"], excl["GrowthIndexDec2023"], s=95,
                facecolors="none", edgecolors="#999", linewidths=1.8, zorder=3,
                label="Catch-all categories (excluded, shown anyway)")
    xs = np.linspace(clean["LogAvgTicket2019"].min(), clean["LogAvgTicket2019"].max(), 100)
    ax1.plot(10 ** xs, s14 * xs + i14, color="#d62728", lw=2.2, zorder=2)
    ax1.set_xscale("log")
    ax1.set_xlabel("Average ticket size, 2019 (SAR, log scale)")
    ax1.set_ylabel("Digital growth index, Dec 2023 (Jan 2019 = 100)")
    ax1.set_title("Digital adoption is structured by transaction value\n"
                  f"Spearman $\\rho$={rho14:.2f} (n=14) vs {rho16:.2f} (n=16) — "
                  "the exclusion is not load-bearing", fontsize=11.5)
    offsets = {"Miscellaneous Goods and Services": (-12, -18),
               "Others": (10, 4), "Jewelry": (10, -4), "Education": (-64, 10),
               "Restaurants & Café": (10, 2), "Public Utilities": (8, 6)}
    for _, r in df.iterrows():
        if r["Sector"] in LABEL:
            ha = "right" if offsets.get(r["Sector"], (0, 0))[0] < 0 else "left"
            ax1.annotate(r["Sector"], (r["AvgTicket2019"], r["GrowthIndexDec2023"]),
                         textcoords="offset points",
                         xytext=offsets.get(r["Sector"], (8, 6)),
                         fontsize=9, ha=ha)
    ax1.set_ylim(top=df["GrowthIndexDec2023"].max() * 1.16)
    ax1.legend(loc="lower left", fontsize=8.5, framealpha=0.95)
    ax1.grid(alpha=0.15)

    names = loo_df["DroppedSector"].tolist()
    ps = loo_df["p"].tolist()
    cols = ["#d62728" if p > 0.05 else "#0B6E4F" for p in ps]
    ypos = np.arange(len(names))
    ax2.scatter(ps, ypos, color=cols, s=60, zorder=3)
    ax2.axvline(0.05, color="#333", ls="--", lw=1.3, zorder=2)
    ax2.axvline(p14, color="#1f77b4", ls=":", lw=1.5, zorder=2)
    ax2.text(0.0515, 0.15, "p = 0.05", fontsize=9)
    ax2.text(p14 - 0.0035, len(names) - 0.4, "full n=14 fit", fontsize=8,
             color="#1f77b4", rotation=90, va="top")
    ax2.set_yticks(ypos)
    ax2.set_yticklabels(names, fontsize=8.5)
    ax2.set_xlabel("p-value of the fit with that sector removed")
    ax2.set_title(f"...but the p=0.04 fit is fragile\n"
                  f"{n_lost} of {len(clean)} single removals push p above 0.05",
                  fontsize=11.5)
    ax2.grid(alpha=0.15, axis="x")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart8c_ticket_size_with_fragility.png"))
    plt.close(fig)
    print(f"\n-> wrote {OUT_DIR}/chart8c_ticket_size_with_fragility.png")


if __name__ == "__main__":
    main()
