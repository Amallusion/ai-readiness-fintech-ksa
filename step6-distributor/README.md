# Step 6 — Distributor (D)

Fans Step 5's one policy decision out into 3 stakeholder-specific
packets — instead of dumping everything on everyone.

## Files

- `distribute.py` — the script; run with `python3 distribute.py`
- `packet1_regulator_disclosure.md` — to SAMA/FSDP: Layer 4 only (which sectors need public disclosure)
- `packet2_sandbox_referral.md` — to Fintech Saudi/Sandbox team: Layer 2 only (pilot referrals + timing)
- `packet3_compliance_audit.md` — to SAMA AML/CTF office: Layer 3 only (assurance that the gate stayed dormant, and why)
- `chart7_routing_diagram.png` — the routing logic, visualized

## Why 3 packets instead of 1 report

A regulator doesn't need Ramadan pilot timing. A sandbox team doesn't need AML/CTF gate status. A compliance auditor doesn't need disclosure-cycle framing. Real institutions are siloed by function — so the Distributor routes each recipient only the slice of the decision that's actually theirs to act on.

**This directly mirrors ITU AI Readiness Dimension 7 ("Strategy Alignment"):** a top-level intent gets decomposed into sub-tasks, each assigned to the appropriate service provider — which is exactly what this script does with Step 5's one decision.
