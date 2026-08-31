# Step 5 — Policy (P)

Where a finding becomes a decision, and where we decided what the system is not allowed to do.

---

## The design problem

The obvious version of this node takes Step 4's slow-sector list and turns it into a flag. Sector enters the bottom tier, system raises an alert, someone downstream decides what the alert means.

We think that is the worst available option, and not because it is simplistic. It is because a bare flag has no stated purpose, and anything without a stated purpose will eventually be given one by whoever is holding it. A list of underserved sectors and a list of suspicious sectors are the same list. What separates them is entirely a matter of what the surrounding system permits, and a flag permits everything.

So the question here was not "what should the system do when a sector is slow." It was "what should the system be structurally incapable of doing, no matter who is operating it."

---

## Four layers

Each layer is independent, each produces a different kind of output, and each is grounded in a real document rather than in our own reasoning.

### Layer 1 — Context review

*Always on. Non-punitive by construction.*

Any sector in the slow tier triggers a prompt to investigate **why** before assuming there is a problem. Cultural preference for gold as a store of value, thin merchant margins that cannot absorb card-processing fees, and legitimate customer preference for privacy on large personal purchases are all fully consistent with what we observed.

This layer can never produce an enforcement action. It produces a question. That constraint is not a limitation we regret — the data genuinely cannot distinguish between those explanations, and a system that pretends otherwise is asserting something it does not know.

*Grounded in: ITU AI Readiness Report 2.0, Dimension 4 (Contextualization and Regional Impact).*

### Layer 2 — Sandbox pilot referral

*Positive action. Timed.*

Slow sectors are referred to SAMA's Regulatory Sandbox and the Fintech Saudi programme for a targeted support pilot. The recommended launch window is computed to land one to two months ahead of that sector's next major spending season, reusing the Ramadan tags built at the Collector.

The reasoning is behavioural rather than statistical: a nudge lands better immediately before people are already about to spend than at an arbitrary point in the year. In the current implementation this resolves to the same window for every referred sector, because the rule keys off a single national seasonal anchor. Per-sector anchors — Eid, the academic year, Hajj — would produce different windows and are the obvious next iteration. We have not built them, and we would rather say that than imply a granularity that does not exist.

*Grounded in: SAMA Regulatory Sandbox / Permitted Fintechs programme; Fintech Saudi Annual Fintech Report.*

### Layer 3 — The AML/CTF gate

*Dormant. Unconditionally. By construction.*

This is the layer we would most want someone to try to break rather than take on trust.

It reports **DORMANT** for every sector, always. Sector-level cluster membership can never, under any input to this system, be sufficient evidence to trigger it. The required evidence class is transaction-level or merchant-level, independently sourced. The available evidence class is sector-level monthly aggregate. These do not overlap, and no operation this pipeline can perform will make them overlap.

The distinction we care about is this: a policy that promises not to be misused is a sentence, and a sentence can be overridden by anyone with the authority to override sentences. A logic branch that does not exist cannot be taken. There is no path through this code that returns anything other than a refusal — not as a default case, as the only case. The dashboard exposes it as a button so that a reader can attempt an escalation on any sector, including the slowest, and watch the refusal with the evidence mismatch shown explicitly.

Slow digital-payment adoption is not a financial-crime signal. Treating it as one is the specific misuse this layer exists to prevent, and it is the misuse most likely to occur, because it requires no bad faith at all — only a reasonable person mistaking a correlation for a signal.

*Grounded in: SAMA AML/CTF Guidelines; SAMA Rules on Outsourcing (data-handling boundary).*

### Layer 4 — Transparency disclosure

*Accountability. Always on.*

Any sector spending two or more consecutive years in the bottom tier is flagged as requiring explicit disclosure, by name, in the next public fintech reporting cycle. All eight slow sectors scored the maximum of five out of five, because none broke out of the bottom tier at any point in the window.

This layer inverts the instinct that a sensitive finding should be restricted, and the inversion is the point. Consider the scenario where a lender begins treating "slow adoption sector" as a merchant risk proxy and prices credit accordingly. The harm there comes from an inference applied privately to firms that cannot see it, contest it, or correct it. A sector that is publicly and officially named as underserved is a sector whose merchants can point at the disclosure and challenge a decision made on that basis.

Restricting the finding protects the finding. Publishing it protects the people the finding is about.

*Grounded in: Fintech Saudi Annual Fintech Report (public KPI disclosure precedent).*

---

## Files

| File | What it is |
|---|---|
| `policy_engine.py` | The four layers |
| `output/policy_decisions.csv` | One row per sector: layer outcomes, plus the grounding document for each. Input to Step 6 |

## Running it

```bash
pip install pandas
python3 policy_engine.py
```

Expects `cluster_results.csv` and `collected_wide.csv` in this folder.

The output CSV carries the grounding documents as columns rather than leaving them in this README, so the Distributor and the Sink read them from the data. A downstream stage cannot drift out of sync with the policy that produced it if it is reading the policy rather than restating it.

---

## What this layer does not do

It prevents the system from taking the wrong action itself. That is narrower than preventing others from misusing its output, and the two are easy to conflate.

If the sector list were combined with merchant location by several lenders and used to produce something functionally close to geographic redlining, nothing in these four layers stops it. Addressing that would need an explicit purpose limitation attached to publication and a prohibition on using aggregate adoption tiers as an input to individual credit decisions — instruments that live in the regulatory framework rather than in our code.

We would rather name the boundary than claim a completeness we do not have. Knowing exactly where a safeguard stops is more useful than believing it goes further than it does.
