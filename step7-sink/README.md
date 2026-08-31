# Step 7 — Sink

The final Y.3172 node: a single, self-contained HTML dashboard — where the
pipeline's output finally reaches a real person.

## Files

| File | Role |
|---|---|
| `build_dashboard.py` | The generator. Run with `python3 build_dashboard.py` (requires `pandas`). |
| `policy_decisions.csv` | Input from Step 5 (Policy). The script also accepts `input_from_step5_policy_decisions.csv`. |
| `chart2_growth_ranking.png` | Public view chart |
| `chart6_policy_flowchart.png` | Compliance view chart |
| `chart7_routing_diagram.png` | Architecture view chart |
| `output/dashboard.html` | **The deliverable.** Double-click, opens in any browser, no server or internet needed. |

## Before submitting

Set `RETRIEVED_ON` at the top of `build_dashboard.py` to the actual date the SAMA
files were downloaded, then rebuild. The script prints a reminder if you forget.
Government statistical series get revised, so a dashboard with no retrieval date
is not reproducible even in principle.

## Demo script for the 7-minute video

1. **Open `dashboard.html`.** Point at the `SRC → C → PP → M → P → D → SINK` breadcrumb
   in the header — the judge immediately knows where this artifact sits in Y.3172.
2. **Public tab.** State the finding: 8 of 16 sectors lagged in all 5 years. Open the
   "What this analysis cannot tell you" disclosure and read one line of it out loud —
   volunteering the limitation is worth more than the finding itself.
3. **Regulator → Sandbox tabs.** Point out the grey packet notes: each role sees one
   packet of three, and the absences are deliberate routing, not missing work.
4. **Compliance tab — the money shot.** Select **Jewelry** (the slowest sector, the one
   most likely to be targeted) and click **Attempt escalation**. Read the refusal:
   evidence required is transaction-level, evidence available is sector-level aggregate,
   no match. Click it a second time on a different sector so the refusal counter
   increments. Say the line: *the safeguard is a property of the code, not a promise in
   a paragraph.*
5. **Architecture tab.** Show the routing diagram, then the model/manual agreement
   paragraph — including the sentence conceding that agreement is not strong independent
   confirmation. Conceding the weak point before a judge finds it is worth more than the
   15/16 number.
6. **Click العربية.** The whole interface flips to Arabic **and to right-to-left**.
   Re-run the escalation in Arabic to show the refusal is localised too.

## Design decisions worth saying out loud

- **Role-based, not one-size-fits-all.** Mirrors Step 6's routing exactly. Each panel
  declares which packet it carries, so a judge who clicks one tab can tell the sparseness
  is intentional.
- **The AML/CTF safeguard is demonstrated, not asserted.** Policy Layer 3 is the strongest
  claim in the project. A callout asks the reader to trust it; the escalation button lets
  them test it. There is deliberately no branch in the gate logic that returns anything
  other than a refusal — the refusal is not a default case, it is the only case.
- **Bilingual including direction.** Interface chrome, all 16 sector names, and the
  escalation output are available in Arabic, and switching language switches
  `<html lang>`, `dir`, table alignment, and callout borders. This is the concrete
  implementation of ITU AI Readiness **Dimension 6 (Human Interface)**; Arabic rendered
  left-to-right would have undercut the claim it exists to support.
- **Limitations are on the dashboard, not just in the report.** The Public view carries
  the benign-explanation disclosure; the Architecture view carries the full limitations
  list including the IQR non-result.
- **Uniform columns are explained, not hidden.** The disclosure column reads 5 for every
  sector and the pilot window is identical across referrals. Both are genuine computed
  outputs, so each is annotated to say why it is uniform, and each table carries an
  additional column that does vary.
- **Fully self-contained.** Charts embedded as base64; works offline, survives being moved
  out of the repo. Missing chart files degrade to a visible notice rather than a broken
  image or a crash.

## Changes from the previous build

- Added RTL direction handling and `<html lang>`/`dir` switching (previously Arabic
  rendered left-to-right, on the one panel making a local-language claim).
- Added the interactive Layer 3 escalation demo.
- Replaced the "3× independent checks agreed" headline stat, which overstated the
  independence of three level-derived methods, with the 5-of-5-years persistence figure.
- Moved the routing diagram out of the global footer, where it was visible under every
  role and contradicted the routing thesis, into a new non-role **Architecture** tab.
- Added packet-of-3 notes to each role panel.
- Added source, analysis window and retrieval date to the footer.
- Added collapsible limitations disclosures to the Public and Architecture views.
- Added a computed gap-vs-median column to both tables and a priority rank to the sandbox
  table, so neither table has a column with no variance.
- Layer 3 gate text and grounding documents are now read from the Step 5 CSV rather than
  hardcoded, so the Sink cannot drift out of sync with the Policy node.
- Input CSV filename resolution and graceful handling of missing chart files.
