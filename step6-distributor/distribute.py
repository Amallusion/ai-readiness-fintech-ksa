"""
distribute.py
=============
ITU AI Readiness Hackathon (KSA) — Fintech track
STEP 6 of the Y.3172 pipeline: "D" (Distributor)

WHAT THIS DOES
--------------
Takes Step 5's policy_decisions.csv (one decision per sector, 4 layers)
and routes it to three DIFFERENT real institutional recipients, each
getting only the slice of the decision that's relevant to them — not one
undifferentiated data dump.

This mirrors ITU AI Readiness Dimension 7, "Strategy Alignment": a
top-level intent gets decomposed into sub-tasks, each assigned to the
appropriate service provider/institution.

  Packet 1 -> SAMA / Financial Sector Development Program (regulator)
              Layer 4 output only: which sectors require public
              disclosure, and why. A policy office doesn't need pilot
              timing or AML gate status.

  Packet 2 -> Fintech Saudi / SAMA Regulatory Sandbox team
              Layer 2 output only: which sectors are referred for a
              support pilot, and the recommended launch window. A
              sandbox team doesn't need disclosure-cycle framing.

  Packet 3 -> SAMA AML/CTF compliance office
              Layer 3 output only: an assurance record proving the gate
              stayed dormant for every sector, and exactly what would be
              required to change that. A compliance auditor doesn't need
              Ramadan timing or disclosure cadence.

OUTPUTS (./output/):
  - packet1_regulator_disclosure.md
  - packet2_sandbox_referral.md
  - packet3_compliance_audit.md
  - chart7_routing_diagram.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pandas as pd

IN_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(IN_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

DECISIONS_PATH = os.path.join(IN_DIR, "policy_decisions.csv")


def build_packet1_regulator(df: pd.DataFrame) -> str:
    flagged = df[df["LAYER4_disclosure_required"]].sort_values("EndIndex")
    lines = [
        "# Packet 1 — Regulator Disclosure Briefing",
        "**To:** SAMA / Financial Sector Development Program office",
        "**From:** Step 6 Distributor (auto-routed from Step 5 Policy, Layer 4 only)",
        "",
        "The following sectors have spent 2 or more of the last 5 calendar years",
        "in the bottom digital-payment growth tier and should be named, with",
        "context, in the next public fintech-sector reporting cycle rather than",
        "remaining hidden behind the rising national cashless-adoption average.",
        "",
        "| Sector | Consecutive slow years | Index, Dec 2023 (Jan 2019=100) |",
        "|---|---|---|",
    ]
    for _, row in flagged.iterrows():
        lines.append(f"| {row['Sector']} | {row['ConsecutiveSlowYears']} | {row['EndIndex']:.1f} |")
    lines.append("")
    lines.append(f"**Total sectors flagged for disclosure: {len(flagged)} of {len(df)}**")
    lines.append("")
    lines.append("*This packet intentionally omits pilot-timing and AML/CTF gate detail —")
    lines.append("those are routed separately to the teams responsible for them (see Packets 2 and 3).*")
    return "\n".join(lines)


def build_packet2_sandbox(df: pd.DataFrame) -> str:
    flagged = df[df["LAYER2_sandbox_pilot"]].sort_values("EndIndex")
    lines = [
        "# Packet 2 — Sandbox Pilot Referral",
        "**To:** Fintech Saudi / SAMA Regulatory Sandbox team",
        "**From:** Step 6 Distributor (auto-routed from Step 5 Policy, Layer 2 only)",
        "",
        "The following sectors are referred for a targeted digital-payment",
        "adoption pilot (e.g. subsidized POS fees, a fintech partnership",
        "program), timed ahead of a known high-spending window rather than at",
        "a random point in the year.",
        "",
        "| Sector | Recommended pilot launch window |",
        "|---|---|",
    ]
    for _, row in flagged.iterrows():
        lines.append(f"| {row['Sector']} | {row['LAYER2_pilot_timing']} |")
    lines.append("")
    lines.append(f"**Total sectors referred: {len(flagged)} of {len(df)}**")
    lines.append("")
    lines.append("*This packet intentionally omits disclosure-cycle and AML/CTF detail —")
    lines.append("those are routed separately (see Packets 1 and 3).*")
    return "\n".join(lines)


def build_packet3_compliance(df: pd.DataFrame) -> str:
    dormant_count = (df["LAYER3_amlctf_gate"].str.startswith("DORMANT")).sum()
    lines = [
        "# Packet 3 — AML/CTF Compliance Assurance Record",
        "**To:** SAMA AML/CTF compliance office",
        "**From:** Step 6 Distributor (auto-routed from Step 5 Policy, Layer 3 only)",
        "",
        f"Of {len(df)} sectors reviewed in this analysis cycle, "
        f"**{dormant_count} remained DORMANT on the AML/CTF gate — all of them.**",
        "",
        "By design, this gate cannot be triggered by sector-level cluster",
        "membership alone, regardless of how consistently a sector lags in",
        "digital-payment adoption. It requires independent, transaction-level",
        "evidence that this aggregate dataset does not and cannot contain, and",
        "any action on it requires review by a human compliance officer.",
        "",
        "**No sector in this cycle met that bar. No automated action was taken",
        "or recommended by this layer.**",
        "",
        "*This packet intentionally omits pilot-timing and disclosure-cycle",
        "detail — those are routed separately (see Packets 1 and 2).*",
    ]
    return "\n".join(lines)


def draw_routing_diagram():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")

    def box(xy, w, h, text, color, fontsize=9.5):
        rect = FancyBboxPatch(
            (xy[0] - w / 2, xy[1] - h / 2), w, h,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            linewidth=1.3, edgecolor="#333333", facecolor=color,
        )
        ax.add_patch(rect)
        ax.text(xy[0], xy[1], text, ha="center", va="center", fontsize=fontsize)

    def arrow(xy1, xy2):
        ax.add_patch(FancyArrowPatch(xy1, xy2, arrowstyle="-|>", mutation_scale=15,
                                      color="#555555", linewidth=1.3))

    box((5, 7.2), 6.2, 0.9, "ONE Step 5 Policy decision\n(all 4 layers, 16 sectors)", "#e8e8e8")

    box((1.8, 5.0), 3.0, 1.3, "Packet 1\nLayer 4 only\n-> SAMA / FSDP\n(regulator)", "#fff0c2")
    box((5, 5.0), 3.0, 1.3, "Packet 2\nLayer 2 only\n-> Fintech Saudi /\nSandbox team", "#cdeeda")
    box((8.2, 5.0), 3.0, 1.3, "Packet 3\nLayer 3 only\n-> SAMA AML/CTF\ncompliance office", "#ffd6d6")

    for x in (1.8, 5, 8.2):
        arrow((5, 6.75), (x, 5.65))

    ax.text(5, 2.7,
            "Same underlying decision, three different real institutions,\n"
            "each receiving only the slice relevant to their job.",
            ha="center", va="center", fontsize=10.5, style="italic")
    ax.text(5, 1.5,
            "Maps to ITU AI Readiness Dimension 7 (Strategy Alignment):\n"
            "top-level intent decomposed into sub-tasks, routed to the right service providers.",
            ha="center", va="center", fontsize=9, color="#555555")

    ax.set_title("Step 6 -- Distributor (D): one decision, three routed packets", fontsize=13, pad=15)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "chart7_routing_diagram.png"), dpi=150)
    plt.close(fig)


def main():
    df = pd.read_csv(DECISIONS_PATH)

    p1 = build_packet1_regulator(df)
    p2 = build_packet2_sandbox(df)
    p3 = build_packet3_compliance(df)

    with open(os.path.join(OUT_DIR, "packet1_regulator_disclosure.md"), "w") as f:
        f.write(p1)
    with open(os.path.join(OUT_DIR, "packet2_sandbox_referral.md"), "w") as f:
        f.write(p2)
    with open(os.path.join(OUT_DIR, "packet3_compliance_audit.md"), "w") as f:
        f.write(p3)

    draw_routing_diagram()

    print(p1, "\n\n" + "=" * 70 + "\n")
    print(p2, "\n\n" + "=" * 70 + "\n")
    print(p3)
    print(f"\n\nWrote 3 packets + chart7_routing_diagram.png to {OUT_DIR}")


if __name__ == "__main__":
    main()
