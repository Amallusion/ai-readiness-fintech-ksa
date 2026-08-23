# Step 5 — Policy (P)

A layered decision engine — 4 independent rules, each grounded in a real
document — that turns Step 4's cluster output into actual actions, with a
built-in architectural safeguard against misuse.

## Files

- `policy.py` — the script; run with `python3 policy.py`
- `policy_decisions.csv` — all 16 sectors, every layer's verdict
- `policy_case_jewelry.md` — the full reasoning trail for the headline case, written as a real policy memo (this doubles as the answer to the required "controversy scenario" in the report)
- `chart6_policy_flowchart.png` — the 4-layer decision logic, visualized

## The 4 layers

1. **Context review** (always-on, non-punitive) — investigate *why* before assuming anything's wrong
2. **Sandbox pilot recommendation** (positive action) — refers slow sectors to SAMA's real Regulatory Sandbox / Fintech Saudi program, timed 1-2 months ahead of the next Ramadan (reusing the event tags from Step 2)
3. **AML/CTF gate** (the safeguard) — reports DORMANT for every sector, by design. Cluster membership alone can never trigger this; it requires independent transaction-level evidence this dataset doesn't and can't contain, reviewed by a human
4. **Transparency disclosure** — any sector 2+ consecutive years in the bottom tier must be named, with context, in the next public reporting cycle

## Result

8 sectors (including Jewelry, 5/5 years in the bottom tier) trigger Layers 1, 2, and 4. **Zero sectors ever trigger Layer 3** from this data alone — that's not a finding, it's the design working as intended.
