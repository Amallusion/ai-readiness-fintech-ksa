"""
analysis.py
============
ITU AI Readiness Hackathon (KSA) — Fintech track — Team Voxel
STEP 4 (Model): statistical analysis of cross-sector digital-payment adoption.

WHAT THIS TESTS
---------------
A. TICKET SIZE AS A MECHANISM. Average ticket size (Sales / Transactions) is a
   dimension of the data independent of trajectory level and shape, so it can
   test whether adoption is structured by transaction value rather than merely
   describing which sectors ended lowest. Reported with OLS, Spearman (robust
   to leverage), leave-one-out fragility, and a control for sector size.

B. CORRELATION WITH THE NATIONAL E-COMMERCE TREND, on levels and on differences.
   Two upward-trending series correlate highly regardless of any underlying
   relationship, so the differenced series is the informative one. Reported with
   the |r| thresholds required for significance, uncorrected and Bonferroni.

C+D. CLUSTERING, in level space and in shape space (row-wise z-normalized), with
   silhouette scores and cluster sizes disclosed at every k. Cluster sizes matter:
   a high silhouette produced by splitting off one or two extreme sectors is an
   outlier detector scoring well, not evidence of population structure.

E. RANK STABILITY. Two checks. First, a resampling-free count of how often each
   sector holds the lowest rebased index across the observed month-ends, which
   makes no distributional assumptions. Second, a moving block bootstrap
   (block = 12 months) that preserves within-year autocorrelation and seasonality;
   i.i.d. resampling of a short trending series compounds noise multiplicatively
   and produces intervals that measure the procedure rather than the data.

METHODOLOGICAL STANCE
---------------------
n = 16 sectors is a small sample. Every p-value here is reported as descriptive,
alongside the diagnostics that show how much weight it can bear. Where a result
is fragile, the fragility is reported next to the result rather than in a
footnote.

INPUTS (same directory):
  collected_wide.csv          Step 2 output, wide format
  sector_matrix_indexed.csv   Step 3 output, sectors x months, Jan2019=100
  sector_matrix_growth.csv    Step 3 output, sectors x months, MoM % change
  cluster_results.csv         level-based clusters + manual tiers

OUTPUTS (./output/):
  chart8c_ticket_size_with_fragility.png   two-panel: fit + leave-one-out
  chart9b_silhouette_level_vs_shape.png    both spaces, with cluster sizes
  ticket_size_report.txt
  correlation_report.txt
  clustering_report.txt
  rank_stability_report.txt
  ticket_size_data_full.csv
"""

import os
import sys

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

# Excluded from the ticket-size regression. The justification is ex ante and
# structural, not chosen to improve the fit: an average ticket size is only
# interpretable for a category with a coherent basket. Both of these are
# catch-all aggregations of heterogeneous goods, and Step 3's preprocessing
# check already flagged "Miscellaneous Goods and Services" as compositionally
# unstable in SAMA's own source footnote. We report the full-16 result anyway
# (see report), and the Spearman comparison shows the exclusion is not what
# produces the relationship.
CATCHALL = ["Miscellaneous Goods and Services", "Others"]

BLOCK_LEN = 12   # months; preserves within-year autocorrelation & seasonality
N_BOOT = 2000
SEED = 42


def _w(name, text):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
    print(f"  -> wrote {path}\n")


def _month_cols(df):
    return [c for c in df.columns if c != "Sector"]


# =====================================================================
# A. Ticket size: OLS, Spearman, leave-one-out fragility, volume control
# =====================================================================
def ticket_size_analysis(wide, indexed):
    wide_2019 = wide[wide["Date"].astype(str).str.startswith("2019")]
    end_col = indexed.columns[-1]

    rows = []
    for s in SECTORS:
        txn = wide_2019[f"{s} - Number of Transactions"].mean()
        sales = wide_2019[f"{s} - Sales"].mean()
        rows.append({
            "Sector": s,
            "AvgTicket2019": sales / txn,
            "Volume2019": txn,
            "GrowthIndexDec2023": float(indexed.loc[indexed["Sector"] == s, end_col].iloc[0]),
        })
    df = pd.DataFrame(rows)
    df["LogAvgTicket2019"] = np.log10(df["AvgTicket2019"])
    df["LogVolume2019"] = np.log10(df["Volume2019"])
    clean = df[~df["Sector"].isin(CATCHALL)].reset_index(drop=True)

    def ols(d):
        s, i, r, p, _ = stats.linregress(d["LogAvgTicket2019"], d["GrowthIndexDec2023"])
        return s, i, r ** 2, p

    s16, i16, r16, p16 = ols(df)
    s14, i14, r14, p14 = ols(clean)
    rho16, prho16 = stats.spearmanr(df["LogAvgTicket2019"], df["GrowthIndexDec2023"])
    rho14, prho14 = stats.spearmanr(clean["LogAvgTicket2019"], clean["GrowthIndexDec2023"])

    # ---- leave-one-out fragility on the 14 ----
    loo = []
    for k in range(len(clean)):
        _, _, r2k, pk = ols(clean.drop(k))
        loo.append((clean["Sector"][k], r2k, pk))
    loo.sort(key=lambda x: -x[2])
    n_lost = sum(1 for _, _, pk in loo if pk > 0.05)

    # ---- volume control: is ticket size a proxy for sector size? ----
    X = np.column_stack([
        np.ones(len(clean)), clean["LogAvgTicket2019"], clean["LogVolume2019"]
    ])
    y = clean["GrowthIndexDec2023"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(clean) - X.shape[1]
    mse = resid @ resid / dof
    cov = mse * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    tvals = beta / se
    pvals = 2 * (1 - stats.t.cdf(np.abs(tvals), dof))
    r_tv, p_tv = stats.pearsonr(clean["LogAvgTicket2019"], clean["LogVolume2019"])

    # ---- residuals: does Jewelry sit on the line? ----
    clean = clean.copy()
    clean["Predicted"] = s14 * clean["LogAvgTicket2019"] + i14
    clean["Residual"] = clean["GrowthIndexDec2023"] - clean["Predicted"]
    resid_sorted = clean.sort_values("Residual")

    txt = "TICKET SIZE vs DIGITAL ADOPTION\n"
    txt += "=" * 68 + "\n\n"
    txt += "1. OLS, log10(avg ticket size 2019) -> Dec-2023 rebased index\n"
    txt += f"   All 16 sectors : R2={r16:.3f}  p={p16:.4f}  slope={s16:.1f}\n"
    txt += f"   14 sectors     : R2={r14:.3f}  p={p14:.4f}  slope={s14:.1f}\n\n"
    txt += "2. Spearman rank correlation (insensitive to leverage)\n"
    txt += f"   All 16 sectors : rho={rho16:.3f}  p={prho16:.4f}\n"
    txt += f"   14 sectors     : rho={rho14:.3f}  p={prho14:.4f}\n"
    txt += ("   The rank relationship is essentially UNCHANGED by the exclusion.\n"
            "   The exclusion therefore does not create the relationship; it removes\n"
            "   two high-growth catch-all points that inflate OLS residual variance.\n"
            "   Neither sample reaches p<0.05 on the rank test.\n\n")
    txt += f"3. Leave-one-out fragility of the n=14 OLS result\n"
    txt += f"   {n_lost} of {len(clean)} sectors, removed individually, push p above 0.05:\n"
    for name, r2k, pk in loo:
        flag = "  <-- significance lost" if pk > 0.05 else ""
        txt += f"     drop {name:36s} R2={r2k:.3f} p={pk:.4f}{flag}\n"
    txt += ("   p=0.04 at n=14 is a knife-edge result. Reported as a suggestive\n"
            "   mechanism consistent with the data, NOT an established effect.\n\n")
    txt += "4. Volume control — is ticket size a proxy for sector size?\n"
    txt += f"   corr(log ticket, log volume) = {r_tv:.3f} (p={p_tv:.4f})\n"
    txt += f"   Growth ~ log(ticket) + log(volume), n={len(clean)}:\n"
    txt += f"     intercept   b={beta[0]:9.1f}  p={pvals[0]:.4f}\n"
    txt += f"     log(ticket) b={beta[1]:9.1f}  p={pvals[1]:.4f}\n"
    txt += f"     log(volume) b={beta[2]:9.1f}  p={pvals[2]:.4f}\n"
    txt += ("   If log(ticket) retains its sign and rough magnitude here, the\n"
            "   relationship is not merely a sector-size artefact. If it collapses,\n"
            "   say so — that is the finding.\n\n")
    txt += "5. Residuals — where does Jewelry actually sit?\n"
    txt += resid_sorted[["Sector", "AvgTicket2019", "GrowthIndexDec2023",
                          "Predicted", "Residual"]].to_string(
        index=False, float_format=lambda x: f"{x:.1f}") + "\n"
    txt += ("   NOTE: check Jewelry's rank here before writing the narrative.\n"
            "   In our data Jewelry is well BELOW the fitted line, not on it —\n"
            "   ticket size predicts it should be slow, and it is slower still.\n"
            "   Education is the sector that sits on the line.\n")
    _w("ticket_size_report.txt", txt)

    # ---- two-panel figure: the result, and its fragility ----
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.2),
                                    gridspec_kw={"width_ratios": [1.35, 1]})

    excl = df[df["Sector"].isin(CATCHALL)]
    ax1.scatter(clean["AvgTicket2019"], clean["GrowthIndexDec2023"], s=85,
                color="#1f77b4", alpha=0.85, zorder=3, label="Single-purpose sectors (n=14)")
    ax1.scatter(excl["AvgTicket2019"], excl["GrowthIndexDec2023"], s=95,
                facecolors="none", edgecolors="#999", linewidths=1.8, zorder=3,
                label="Catch-all categories (excluded, shown for transparency)")
    xs = np.linspace(clean["LogAvgTicket2019"].min(), clean["LogAvgTicket2019"].max(), 100)
    ax1.plot(10 ** xs, s14 * xs + i14, color="#d62728", lw=2.2, zorder=2)
    ax1.set_xscale("log")
    ax1.set_xlabel("Average ticket size, 2019 (SAR, log scale)")
    ax1.set_ylabel("Digital growth index, Dec 2023 (Jan 2019 = 100)")
    ax1.set_title("Digital adoption is structured by transaction value\n"
                  f"Spearman $\\rho$={rho14:.2f} (n=14), {rho16:.2f} (n=16) — "
                  "near-identical, so the exclusion is not load-bearing",
                  fontsize=11.5)
    for _, r in pd.concat([clean, excl]).iterrows():
        if r["Sector"] in ["Jewelry", "Education", "Restaurants & Café",
                            "Miscellaneous Goods and Services", "Others",
                            "Public Utilities"]:
            ax1.annotate(r["Sector"], (r["AvgTicket2019"], r["GrowthIndexDec2023"]),
                         textcoords="offset points", xytext=(8, 6), fontsize=9)
    ax1.legend(loc="upper right", fontsize=8.5, framealpha=0.95)
    ax1.grid(alpha=0.15)

    names = [n for n, _, _ in loo]
    ps = [p for _, _, p in loo]
    cols = ["#d62728" if p > 0.05 else "#0B6E4F" for p in ps]
    ypos = np.arange(len(names))
    ax2.scatter(ps, ypos, color=cols, s=60, zorder=3)
    ax2.axvline(0.05, color="#333", ls="--", lw=1.3, zorder=2)
    ax2.axvline(p14, color="#1f77b4", ls=":", lw=1.5, zorder=2)
    ax2.text(0.051, len(names) - 0.6, "p = 0.05", fontsize=9)
    ax2.set_yticks(ypos)
    ax2.set_yticklabels(names, fontsize=8.5)
    ax2.set_xlabel("p-value of the fit with that sector removed")
    ax2.set_title(f"...but the p=0.04 fit is fragile\n"
                  f"{n_lost} of {len(clean)} single removals push p above 0.05",
                  fontsize=11.5)
    ax2.grid(alpha=0.15, axis="x")
    ax2.invert_yaxis()

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart8c_ticket_size_with_fragility.png"))
    plt.close(fig)

    df.to_csv(os.path.join(OUT_DIR, "ticket_size_data_full.csv"), index=False)
    return df


# =====================================================================
# B. Differenced correlation, with significance thresholds
# =====================================================================
def differenced_correlation(wide, growth):
    ecom_level = wide["E-Commerce (Mada) - Number of Transactions"]
    ecom_growth = (ecom_level.pct_change() * 100).values[1:]
    mcols = _month_cols(growth)

    rows = []
    for s in SECTORS:
        lvl = wide[f"{s} - Number of Transactions"].corr(ecom_level)
        g = growth.loc[growth["Sector"] == s, mcols].iloc[0].astype(float).values
        g = g[~np.isnan(g)]
        m = min(len(g), len(ecom_growth))
        dif = np.corrcoef(g[-m:], ecom_growth[-m:])[0, 1]
        rows.append({"Sector": s, "LevelCorrelation": lvl,
                      "DifferencedCorrelation": dif, "N": m})
    df = pd.DataFrame(rows).sort_values("DifferencedCorrelation")

    n = int(df["N"].median())
    tc = stats.t.ppf(0.975, n - 2)
    r_crit = tc / np.sqrt(n - 2 + tc ** 2)
    tb = stats.t.ppf(1 - 0.025 / len(SECTORS), n - 2)
    r_bonf = tb / np.sqrt(n - 2 + tb ** 2)
    absd = df["DifferencedCorrelation"].abs()
    n_uncorr = int((absd > r_crit).sum())
    n_bonf = int((absd > r_bonf).sum())

    txt = "CORRELATION WITH THE NATIONAL E-COMMERCE TREND\n"
    txt += "=" * 68 + "\n\n"
    txt += df.to_string(index=False, float_format=lambda x: f"{x:.3f}") + "\n\n"
    txt += f"Mean |level correlation|      : {df['LevelCorrelation'].abs().mean():.3f}\n"
    txt += f"Mean |differenced correlation|: {absd.mean():.3f}\n\n"
    txt += f"With n={n} monthly growth observations:\n"
    txt += f"  |r| needed for p<0.05 uncorrected     : {r_crit:.3f}  -> {n_uncorr} of 16 sectors pass\n"
    txt += f"  |r| needed after Bonferroni (16 tests): {r_bonf:.3f}  -> {n_bonf} of 16 sectors pass\n\n"
    txt += ("READ THIS CORRECTLY. The finding is not that Jewelry moved from lowest\n"
            "to mid-range in the differenced ranking. It is that differencing collapses\n"
            "the correlation for EVERY sector. The level-based correlations were\n"
            "measuring shared upward trend, not any sector-specific relationship with\n"
            "e-commerce adoption. This retires the correlation leg of the original\n"
            "'three independent confirmations' claim entirely, rather than partially.\n")
    _w("correlation_report.txt", txt)
    df.to_csv(os.path.join(OUT_DIR, "correlation_comparison_full.csv"), index=False)
    return df


# =====================================================================
# C+D. Clustering: silhouette in BOTH spaces, cluster sizes disclosed
# =====================================================================
def clustering_analysis(indexed, level_clusters):
    mcols = _month_cols(indexed)
    X_level = indexed[mcols].values
    X_shape = StandardScaler().fit_transform(X_level.T).T   # row-wise z-score

    ks = list(range(2, 7))
    res = {"level": [], "shape": []}
    sizes = {"level": {}, "shape": {}}
    for name, X in [("level", X_level), ("shape", X_shape)]:
        for k in ks:
            lab = KMeans(n_clusters=k, random_state=SEED, n_init=10).fit_predict(X)
            res[name].append(silhouette_score(X, lab))
            sizes[name][k] = sorted(np.bincount(lab).tolist(), reverse=True)

    lab_shape = KMeans(n_clusters=3, random_state=SEED, n_init=10).fit_predict(X_shape)
    out = indexed[["Sector"]].copy()
    out["ShapeCluster"] = lab_shape
    merged = out.merge(level_clusters[["Sector", "ClusterLabel", "ManualTier"]], on="Sector")
    j = merged.loc[merged["Sector"] == "Jewelry", "ShapeCluster"].iloc[0]
    j_group = merged.loc[merged["ShapeCluster"] == j, "Sector"].tolist()
    shape_sizes = sorted(np.bincount(lab_shape).tolist(), reverse=True)

    txt = "CLUSTERING — silhouette in both spaces, with cluster sizes\n"
    txt += "=" * 68 + "\n\n"
    txt += f"{'k':>3} | {'silhouette (levels)':>20} | {'sizes':>16} | {'silhouette (shape)':>19} | {'sizes':>16}\n"
    txt += "-" * 88 + "\n"
    for idx, k in enumerate(ks):
        txt += (f"{k:>3} | {res['level'][idx]:>20.3f} | {str(sizes['level'][k]):>16} | "
                f"{res['shape'][idx]:>19.3f} | {str(sizes['shape'][k]):>16}\n")
    txt += "\n"
    txt += ("INTERPRETING SILHOUETTE HONESTLY. A high silhouette produced by splitting\n"
            "off one or two extreme sectors is an outlier detector scoring well, not\n"
            "evidence of adoption tiers. Check the size column beside every score\n"
            "before quoting it. A [15, 1] or [14, 2] split at k=2 does not support a\n"
            "claim about population structure.\n\n")
    txt += f"Shape-based k=3 cluster sizes: {shape_sizes}\n"
    txt += f"Cluster containing Jewelry   : {j_group}\n\n"
    if len(j_group) <= 3 or (len(shape_sizes) >= 2 and shape_sizes[-1] <= 2):
        txt += ("CAVEAT REQUIRED. This partition is dominated by one large cluster plus\n"
                "small residual groups. Describe Jewelry's cluster-mates as 'the sectors\n"
                "whose trajectory shape is least typical alongside it', NOT as a\n"
                "discovered adoption tier. State the sizes wherever this result is cited.\n")
    txt += ("\nk=3 was retained for interpretability against the manual tiers. It is NOT\n"
            "asserted to be the algorithm-optimal choice; the table above shows what is.\n")
    _w("clustering_report.txt", txt)

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.plot(ks, res["level"], marker="o", lw=2, color="#0B6E4F", label="Level space (raw rebased)")
    ax.plot(ks, res["shape"], marker="s", lw=2, color="#C89B3C", label="Shape space (z-normalized)")
    ax.axvline(3, color="#d62728", ls="--", alpha=0.6, label="k=3 (used, for interpretability)")
    for idx, k in enumerate(ks):
        ax.annotate(str(sizes["level"][k]), (k, res["level"][idx]),
                    textcoords="offset points", xytext=(0, 9), ha="center", fontsize=7.5, color="#0B6E4F")
        ax.annotate(str(sizes["shape"][k]), (k, res["shape"][idx]),
                    textcoords="offset points", xytext=(0, -15), ha="center", fontsize=7.5, color="#8a6a20")
    ax.set_xlabel("Number of clusters (k)")
    ax.set_ylabel("Silhouette score")
    ax.set_title("Silhouette by k, in both spaces — cluster sizes annotated\n"
                 "A high score from a near-singleton split is not population structure",
                 fontsize=11.5)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart9b_silhouette_level_vs_shape.png"))
    plt.close(fig)

    merged.to_csv(os.path.join(OUT_DIR, "shape_cluster_results_full.csv"), index=False)
    return merged


# =====================================================================
# E. Rank stability — observed-data check + moving block bootstrap
# =====================================================================
def rank_stability(indexed, growth):
    # ---- E1: no resampling at all. How often is each sector lowest across
    # the 60 actual month-ends? This makes no distributional assumptions.
    mcols = _month_cols(indexed)
    M = indexed.set_index("Sector")[mcols]
    lowest = M.idxmin(axis=0)
    obs = lowest.value_counts()
    obs_pct = (obs / len(mcols) * 100).round(1)

    # ---- E2: moving block bootstrap. Blocks preserve the within-year
    # autocorrelation and seasonality that i.i.d. resampling destroys.
    # The SAME block start indices are used for every sector each draw, so
    # cross-sector dependence is preserved too.
    rng = np.random.default_rng(SEED)
    gcols = _month_cols(growth)
    G = {}
    for s in SECTORS:
        r = growth.loc[growth["Sector"] == s, gcols].iloc[0].astype(float).values / 100.0
        G[s] = r[~np.isnan(r)]
    T = min(len(v) for v in G.values())
    n_blocks = int(np.ceil(T / BLOCK_LEN))
    max_start = T - BLOCK_LEN

    bottom = {s: 0 for s in SECTORS}
    finals = {s: [] for s in SECTORS}
    for _ in range(N_BOOT):
        starts = rng.integers(0, max_start + 1, n_blocks)
        idx = np.concatenate([np.arange(st, st + BLOCK_LEN) for st in starts])[:T]
        vals = {}
        for s in SECTORS:
            vals[s] = 100.0 * np.prod(1.0 + G[s][:T][idx])
            finals[s].append(vals[s])
        bottom[min(vals, key=vals.get)] += 1

    txt = "RANK STABILITY — is one sector reliably the lowest?\n"
    txt += "=" * 68 + "\n\n"
    txt += f"E1. OBSERVED DATA, no resampling ({len(mcols)} actual month-ends)\n"
    txt += "    How often each sector holds the lowest rebased index:\n"
    for s, p in obs_pct.items():
        txt += f"      {s:36s} {p:5.1f}%  ({int(obs[s])} of {len(mcols)} months)\n"
    txt += ("    This is a property of the observed series, with no distributional\n"
            "    assumptions. Prefer it as the headline stability statement.\n\n")
    txt += f"E2. MOVING BLOCK BOOTSTRAP (block={BLOCK_LEN} months, {N_BOOT} draws)\n"
    txt += "    Share of draws in which each sector is the single lowest:\n"
    for s, c in sorted(bottom.items(), key=lambda x: -x[1]):
        if c:
            txt += f"      {s:36s} {c / N_BOOT * 100:5.1f}%\n"
    txt += "\n    95% interval on the final index value:\n"
    for s in SECTORS:
        lo, hi = np.percentile(finals[s], [2.5, 97.5])
        txt += f"      {s:36s} [{lo:8.0f}, {hi:8.0f}]\n"
    txt += ("\n    WHY BLOCKS. i.i.d. resampling of individual months destroys\n"
            "    autocorrelation and seasonality and then compounds the noise\n"
            "    multiplicatively over ~59 draws, producing intervals that measure\n"
            "    the procedure rather than the data. If the intervals above are\n"
            "    still implausibly wide, report E1 and say plainly that resampling a\n"
            "    short trending series does not support a usable interval at this\n"
            "    sample size. Do not quote an interval you do not believe.\n")
    _w("rank_stability_report.txt", txt)
    return obs_pct, bottom


def main():
    missing = [p for p in (WIDE_PATH, INDEXED_PATH, GROWTH_PATH, CLUSTERS_PATH)
               if not os.path.exists(p)]
    if missing:
        print("Missing required input file(s):")
        for m in missing:
            print("   ", os.path.basename(m))
        print("\nCopy the Step 2 / Step 3 / Step 4 outputs into this folder and re-run.")
        sys.exit(1)

    wide = pd.read_csv(WIDE_PATH)
    indexed = pd.read_csv(INDEXED_PATH)
    growth = pd.read_csv(GROWTH_PATH)
    clusters = pd.read_csv(CLUSTERS_PATH)

    print("=" * 70 + "\nA. TICKET SIZE — fit, fragility, confound\n" + "=" * 70)
    ticket_size_analysis(wide, indexed)
    print("=" * 70 + "\nB. CORRELATION — level vs differenced, with thresholds\n" + "=" * 70)
    differenced_correlation(wide, growth)
    print("=" * 70 + "\nC+D. CLUSTERING — silhouette both spaces, sizes disclosed\n" + "=" * 70)
    clustering_analysis(indexed, clusters)
    print("=" * 70 + "\nE. RANK STABILITY — observed + block bootstrap\n" + "=" * 70)
    rank_stability(indexed, growth)
    print("Done. All outputs in ./output/")


if __name__ == "__main__":
    main()
