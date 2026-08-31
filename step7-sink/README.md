# Step 7 — Sink

The last node, and the only one a person actually sees.

---

## What this stage is for

Every stage before this one produces a file. This one produces the moment where the work either reaches someone or does not. It is easy to treat the interface as presentation — the part you do once the real work is finished. I think that gets it backwards. An analysis nobody can act on has the same practical value as an analysis nobody ran.

Two decisions shaped everything here, and both were about refusing an easier option.

---

## Decision one: show each role only its own packet

Step 6 fanned one decision into three packets addressed to three separate institutions. A single comprehensive dashboard would have discarded that work at the exact moment it mattered, which is the moment a person is looking at it.

So this Sink has a role selector. Pick Public, Regulator, Sandbox Team or Compliance, and see only that role's packet. Each panel states which packet it carries and what has been routed elsewhere, so a reader who opens one tab can tell the sparseness is deliberate rather than incomplete work.

There is also an Architecture tab, which is explicitly not a role. It is the one view that shows all three packets at once, and it exists so the routing itself can be inspected. A system that hides its own structure is asking to be trusted; one that exposes it is asking to be checked, and the second is the better request.

## Decision two: demonstrate the safeguard rather than assert it

Layer 3 is the strongest claim this project makes — that the AML/CTF gate is structurally incapable of firing from sector-level data. The easy version is a callout box saying so.

But a callout box asks the reader to believe us, and believing us is precisely the thing that should not be required. So the Compliance panel lets you attempt an escalation yourself. Pick any sector, including the slowest, and request review. The refusal comes back with the evidence classes laid out side by side: required is transaction-level or merchant-level, available is sector-level aggregate, match is none. Click again on a different sector and the refusal counter increments.

There is no branch in that logic that returns anything else. Not as a fallback — as the only outcome. That is the difference between a safeguard and a promise, and it is worth clicking to see rather than reading to accept.

---

## Bilingual, including direction

The interface, all sixteen sector names, and the escalation output are available in Arabic, and switching language also switches document direction to right-to-left, updates `<html lang>` and `dir`, and mirrors table alignment and callout borders.

This is the concrete implementation of ITU AI Readiness Report 2.0, **Dimension 6 (Human Interface)** — availability in the local language used at the interface. Rendering Arabic left-to-right would have been a translation rather than a localisation, and it would have undercut the exact claim this panel exists to support. A feature that is present but wrong is worse than one that is absent, because it invites the reader to stop checking.

---

## Files

| File | What it is |
|---|---|
| `build_dashboard.py` | The generator |
| `output/dashboard.html` | **The deliverable.** Double-click, opens in any browser, no server or internet needed |
| `policy_decisions.csv` | Input from Step 5 |
| `chart2_growth_ranking.png` | Public view |
| `chart6_policy_flowchart.png` | Compliance view |
| `chart7_routing_diagram.png` | Architecture view |

## Running it

```bash
pip install pandas
python3 build_dashboard.py
```

Charts are embedded as base64 directly in the HTML, so the file works offline and survives being moved out of the repository. Missing chart files degrade to a visible notice rather than a broken image or a crash.

**Before submitting:** set `RETRIEVED_ON` at the top of the script to the actual SAMA download date and rebuild. The script prints a reminder if you forget. Government statistical series get revised, and a dashboard with no retrieval date is not reproducible even in principle.

---

## Demo sequence

1. Open it. The `SRC → C → PP → M → P → D → SINK` breadcrumb tells a viewer where this artefact sits in Y.3172 before anyone says a word.
2. **Public tab.** The finding: eight of sixteen sectors, all five years. Then open the "what this analysis cannot tell you" disclosure and read a line of it aloud. Volunteering the limitation is worth more than the finding.
3. **Regulator, then Sandbox.** Point at the packet notes. Each role sees one of three, and the absences are routing rather than gaps.
4. **Compliance.** Select Jewelry — the slowest sector, the one most likely to be targeted — and attempt the escalation. Read the refusal. Click a second sector so the counter moves.
5. **Architecture.** The routing diagram, then the paragraph conceding that the model-manual agreement figure is not strong independent confirmation. Conceding the weak point before anyone finds it is worth more than the number was.
6. **العربية.** The interface flips to Arabic and to right-to-left. Run the escalation again in Arabic.

---

## Two things we chose to explain rather than hide

The disclosure column reads 5 for every listed sector, and the pilot window is identical across all referrals. Both are genuine computed outputs, and both look like placeholders.

The first is the finding itself: the threshold for disclosure is two consecutive years, and every flagged sector cleared it at the maximum. The second is a real limitation: Layer 2 keys off one national seasonal anchor rather than per-sector seasonality.

We annotated both rather than removing them, and added a column to each table that does vary. A uniform column with no explanation reads as carelessness. A uniform column with a reason reads as a result, which is what it is.
