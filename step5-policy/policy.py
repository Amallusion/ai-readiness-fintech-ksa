"""
policy.py
=========
ITU AI Readiness Hackathon (KSA) — Fintech track
STEP 5 of the Y.3172 pipeline: "P" (Policy)

WHAT THIS DOES
--------------
Takes Step 4's Model output (cluster assignments) and applies a LAYERED
policy engine — not a single flag, four distinct, real-document-grounded
rules that combine to decide what happens to each sector. Designed
specifically so that no sector can be individually penalized based on
sector-level clustering alone — see LAYER 3.

LAYER 1 — Contextual review (always-on, non-punitive)
  Any sector in the "Slow" cluster automatically gets a CONTEXT_REVIEW
  flag: a prompt to investigate WHY (cultural/religious purchasing norms,
  merchant fee economics, customer privacy preference for high-value
  goods) before assuming anything is wrong. Never an enforcement action.

LAYER 2 — Support pilot recommendation (positive action, timed)
  Any "Slow" sector gets a SANDBOX_PILOT recommendation, referencing
  SAMA's real Regulatory Sandbox / Fintech Saudi program. Timed to launch
  1-2 months BEFORE that sector's next high-spending window (Ramadan),
  using the event tags built in Step 2 — a nudge lands better right
  before people are about to spend, not at a random time.

LAYER 3 — AML/CTF tiered gate (dormant by design)
  This is the architectural safeguard answering the required
  "controversy" scenario. It documents that any AML/CTF-relevant action
  requires INDEPENDENT, transaction-level evidence that this
  aggregate, sector-level dataset does not and cannot contain.
  Sector cluster membership alone can NEVER move this gate — it always
  reports DORMANT here, on principle, regardless of any sector's data.

LAYER 4 — Transparency disclosure (accountability, always-on)
  Any sector that has spent 2+ of the last 5 calendar years in the
  bottom growth tier must be named, with context, in the next public
  reporting cycle (mirroring Fintech Saudi's Annual Fintech Report) —
  rather than being invisible behind the rising national average.

OUTPUTS (./output/):
  - policy_decisions.csv   one row per sector, every layer's verdict
  - policy_case_jewelry.md the full reasoning trail for the headline case,
                            written as a real policy memo
  - chart6_policy_flowchart.png   visual of the 4-layer decision logic
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pandas as pd

IN_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(IN_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

CLUSTERS_PATH = os.path.join(IN_DIR, "cluster_results.csv")
INDEXED_PATH = os.path.join(IN_DIR, "sector_matrix_indexed.csv")

SLOW_THRESHOLD = 450  # matches the Step 3 manual binning boundary
YEAR_END_COLS = ["2019-12", "2020-12", "2021-12", "2022-12", "2023-12"]

# Real documents found and verified in Step 1 (see step1-source-selection.md)
DOC_LAYER1 = "ITU AI Readiness report, Dimension 4 (Contextualization & Regional Impact)"
DOC_LAYER2 = "SAMA Regulatory Sandbox / \"Permitted Fintechs\" program; Fintech Saudi Annual Fintech Report"
DOC_LAYER3 = "SAMA AML/CTF Guidelines; SAMA Rules on Outsourcing (data-handling boundary)"
DOC_LAYER4 = "Fintech Saudi Annual Fintech Report (public KPI disclosure precedent)"


def compute_consecutive_slow_years(indexed: pd.DataFrame) -> pd.DataFrame:
    """For each sector, count how many of the last 5 calendar years ended
    with the sector still below the Slow-tier threshold, counting back
    consecutively from 2023."""
    year_ends = indexed[["Sector"] + YEAR_END_COLS].copy()
    records = []
    for _, row in year_ends.iterrows():
        consecutive = 0
        for col in reversed(YEAR_END_COLS):  # 2023 backwards
            if row[col] < SLOW_THRESHOLD:
                consecutive += 1
            else:
                break
        records.append({"Sector": row["Sector"], "ConsecutiveSlowYears": consecutive})
    return pd.DataFrame(records)


def next_ramadan_lead_months() -> str:
    """The dataset ends Dec 2023; Ramadan 2024 began ~March 10, 2024.
    Recommend launching 1-2 months ahead."""
    return "Jan-Feb 2024 (approx. 1-2 months ahead of Ramadan 2024, ~March 10 2024)"


def run_policy(clusters: pd.DataFrame, duration: pd.DataFrame) -> pd.DataFrame:
    df = clusters.merge(duration, on="Sector")

    df["LAYER1_context_review"] = df["ClusterLabel"] == "Slow (model)"
    df["LAYER2_sandbox_pilot"] = df["ClusterLabel"] == "Slow (model)"
    df["LAYER2_pilot_timing"] = df["LAYER2_sandbox_pilot"].apply(
        lambda x: next_ramadan_lead_months() if x else "N/A"
    )
    # LAYER 3 is dormant for every sector, unconditionally, by design.
    df["LAYER3_amlctf_gate"] = "DORMANT (requires independent transaction-level evidence)"
    df["LAYER4_disclosure_required"] = df["ConsecutiveSlowYears"] >= 2

    df["DOC_LAYER1"] = DOC_LAYER1
    df["DOC_LAYER2"] = df["LAYER2_sandbox_pilot"].apply(lambda x: DOC_LAYER2 if x else "N/A")
    df["DOC_LAYER3"] = DOC_LAYER3
    df["DOC_LAYER4"] = df["LAYER4_disclosure_required"].apply(lambda x: DOC_LAYER4 if x else "N/A")

    return df


def write_jewelry_memo(decisions: pd.DataFrame):
    row = decisions[decisions["Sector"] == "Jewelry"].iloc[0]
    memo = f"""# Policy Decision Record — Jewelry sector

**Model input:** Jewelry, cluster = {row['ClusterLabel']}, end-of-period index =
{row['EndIndex']:.1f} (Jan 2019 = 100), {row['ConsecutiveSlowYears']} consecutive
years in the bottom growth tier as of Dec 2023.

## Layer 1 — Context review: {"TRIGGERED" if row['LAYER1_context_review'] else "not triggered"}
Before any other action, this is a prompt to investigate WHY — not an
accusation. Plausible non-problematic explanations for a jewelry sector
lagging behind cashless adoption include: cultural/traditional preference
for gold as a store of value, thinner merchant margins that can't absorb
POS transaction fees on high-value items, or legitimate customer
preference for transaction privacy on large personal purchases.
*Grounded in: {row['DOC_LAYER1']}.*

## Layer 2 — Sandbox pilot recommendation: {"TRIGGERED" if row['LAYER2_sandbox_pilot'] else "not triggered"}
Recommended action: refer the sector to SAMA's existing Regulatory
Sandbox / Fintech Saudi program for a targeted digital-payment adoption
pilot (e.g. subsidized POS fees for jewelry merchants, a fintech
partnership program). Recommended launch window: {row['LAYER2_pilot_timing']}
— timed ahead of a known high-spending period rather than launched at a
random point in the year.
*Grounded in: {row['DOC_LAYER2']}.*

## Layer 3 — AML/CTF gate: {row['LAYER3_amlctf_gate']}
This is the safeguard. Cash-heavy, high-value-goods sectors are a
legitimate AML/CTF interest area — but this project's data is
SECTOR-LEVEL AGGREGATE ONLY. It contains no transaction-level, merchant-
level, or customer-level detail. **This layer cannot be triggered by
sector cluster membership alone, under any circumstances** — it requires
independent evidence this dataset does not and cannot provide, reviewed
by a human compliance officer, not an automated decision.
*Grounded in: {row['DOC_LAYER3']}.*

## Layer 4 — Public disclosure: {"REQUIRED" if row['LAYER4_disclosure_required'] else "not required"}
Jewelry has been in the bottom tier for {row['ConsecutiveSlowYears']} of the
last 5 years — above the 2-year disclosure threshold. It should be named,
with context, in the next public fintech-sector reporting cycle, instead
of remaining invisible behind the national 79% cashless headline figure.
*Grounded in: {row['DOC_LAYER4']}.*

## Answer to the required "controversy" scenario
**Could this be misused to unfairly target the Jewelry sector or its
businesses?** No safeguard here is a promise — it is architectural:
Layers 1, 2, and 4 are supportive or transparency-only and cannot harm a
business. Layer 3, the only layer with any punitive potential, is
DORMANT by construction for every sector in this dataset, because sector
membership is not, and is never treated as, evidence of wrongdoing.
"""
    with open(os.path.join(OUT_DIR, "policy_case_jewelry.md"), "w") as f:
        f.write(memo)
    return memo


def draw_flowchart():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    def box(xy, w, h, text, color, fontsize=9.5):
        rect = FancyBboxPatch(
            (xy[0] - w / 2, xy[1] - h / 2), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            linewidth=1.3, edgecolor="#333333", facecolor=color,
        )
        ax.add_patch(rect)
        ax.text(xy[0], xy[1], text, ha="center", va="center", fontsize=fontsize, wrap=True)

    def arrow(xy1, xy2):
        ax.add_patch(FancyArrowPatch(xy1, xy2, arrowstyle="-|>", mutation_scale=15,
                                      color="#555555", linewidth=1.3))

    box((5, 9.3), 5.6, 0.9, "MODEL OUTPUT:\nSector = 'Slow (model)' cluster", "#e8e8e8", 10)

    box((1.8, 7.4), 3.2, 1.1, "LAYER 1\nContext review\n(always-on, non-punitive)", "#cfe8ff")
    box((5, 7.4), 3.2, 1.1, "LAYER 2\nSandbox pilot rec.\n(Ramadan-timed)", "#cdeeda")
    box((8.2, 7.4), 3.2, 1.1, "LAYER 4\nTransparency disclosure\n(if >=2 consecutive yrs)", "#fff0c2")

    for x in (1.8, 5, 8.2):
        arrow((5, 8.85), (x, 7.95))

    box((5, 5.2), 6.4, 1.2,
        "LAYER 3 -- AML/CTF gate\nDORMANT by design for every sector.\nRequires INDEPENDENT transaction-level evidence.\nSector membership alone can NEVER trigger this.",
        "#ffd6d6", 9.5)
    arrow((5, 6.85), (5, 5.8))

    box((5, 3.1), 7.2, 1.1, "Only a HUMAN compliance officer,\nwith independent evidence, can act here.", "#e8e8e8")
    arrow((5, 4.6), (5, 3.65))

    ax.text(5, 1.6,
            "Result: sector clustering alone can only ever produce SUPPORT or TRANSPARENCY.\n"
            "It can never, by itself, produce an enforcement action.",
            ha="center", va="center", fontsize=10.5, style="italic")

    ax.set_title("Step 5 -- Policy (P): layered decision logic", fontsize=13, pad=15)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart6_policy_flowchart.png"), dpi=150)
    plt.close(fig)


def main():
    clusters = pd.read_csv(CLUSTERS_PATH)
    indexed = pd.read_csv(INDEXED_PATH)

    duration = compute_consecutive_slow_years(indexed)
    decisions = run_policy(clusters, duration)
    decisions.to_csv(os.path.join(OUT_DIR, "policy_decisions.csv"), index=False)

    print("Policy decisions (all sectors):")
    print(decisions[["Sector", "ClusterLabel", "ConsecutiveSlowYears",
                      "LAYER1_context_review", "LAYER2_sandbox_pilot",
                      "LAYER3_amlctf_gate", "LAYER4_disclosure_required"]].to_string(index=False))

    memo = write_jewelry_memo(decisions)
    print("\n" + "=" * 70)
    print(memo)

    draw_flowchart()
    print(f"\nWrote policy_decisions.csv, policy_case_jewelry.md, chart6_policy_flowchart.png to {OUT_DIR}")


if __name__ == "__main__":
    main()
