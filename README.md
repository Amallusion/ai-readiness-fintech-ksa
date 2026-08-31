# Team Voxel — ITU AI Readiness Hackathon (KSA)

Fintech track. Full pipeline per ITU-T Y.3172: **SRC → C → PP → M → P → D → SINK**

## Progress

| Step | Node | Status | Folder |
|---|---|---|---|
| 1 | SRC (Source) | ✅ Done | `step1-source-selection.md` |
| 2 | C (Collector) | ✅ Done | `step2-collector/` |
| 3 | PP (Pre-processor) | ✅ Done | `step3-preprocessor/` + `visuals/` |
| 4 | M (Model) | ✅ Done, revised | `step4-model/` + `step4b-rigor-repair/` |
| 5 | P (Policy) | ✅ Done | `step5-policy/` |
| 6 | D (Distributor) | ✅ Done | `step6-distributor/` |
| 7 | SINK | ✅ Done | `step7-sink/` |

**All 7 pipeline steps complete.**

## What this project is

Using Saudi Central Bank (SAMA) open data on point-of-sale transactions by
economic sector (2019–2023) plus national e-commerce transaction data, to
identify which sectors of the Saudi economy have lagged behind the
Kingdom's cashless-payments push — and turn that into real, safeguarded
action grounded in actual SAMA policy.

**Headline finding, revised after external ML review (see
`step4b-rigor-repair/REVISED-FINDINGS.md`):** digital-payment adoption in
Saudi retail is structured by transaction value — higher average ticket
size significantly predicts slower digitalization (R²=0.31, p=0.04, 14
clean sectors). Jewelry, the highest-ticket sector tracked, sits exactly
where this predicts. It is not uniquely worst (statistically tied with
Education), but it is the clearest case of a real, generalizable pattern.

**What the pipeline does with that finding:** a 4-layer policy engine
(Step 5) turns it into a context-review prompt, a Ramadan-timed sandbox
pilot referral, a transparency-disclosure requirement — and, critically,
an AML/CTF gate that is **dormant by design** and can never be triggered
by sector-level data alone. That decision is routed (Step 6) to three
different real institutions, each getting only their relevant slice, and
lands (Step 7) on a bilingual (EN/Arabic), role-based dashboard.

## Folder guide

- `step1-source-selection.md` — how and why we picked the SAMA data (with scored alternatives, and the real SAMA policy documents found)
- `step2-collector/` — raw files + the script that merges them + event tags (COVID period, Ramadan months, post-2020 e-payments law)
- `step3-preprocessor/` — validation checks + the rebased/growth versions of the data, ready for modeling
- `visuals/` — 3 charts + the sector growth-tier binning table
- `step4-model/` — original K-Means clustering + IQR/boxplot check
- `step4b-rigor-repair/` — **read this first if reviewing findings** — external ML review response: ticket-size mechanism (R²=0.31, p=0.04), differenced correlation, shape-based clustering, silhouette k-justification, corrected bootstrap. Contains `REVISED-FINDINGS.md` with the exact corrected claims.
- `step5-policy/` — the 4-layer decision engine (context review, sandbox referral, AML/CTF dormant-by-design gate, transparency disclosure) + the full Jewelry case memo, which doubles as the report's required controversy-scenario answer
- `step6-distributor/` — routes one decision into 3 stakeholder-specific packets (regulator, sandbox team, compliance office)
- `step7-sink/` — `dashboard.html`, the final bilingual, role-based demo screen

Each subfolder has its own README explaining exactly what's inside and why.

## Team Voxel

- Mohamd Bremo
- Thamer Al Kahtani
- Ayman Mohammed
- Abdulelah Hejazi

## Submission checklist (ITU AI Readiness Hackathon KSA)

- [ ] Technical report, 5 pages max (see `report-skeleton.md` for the outline — all 🔲 placeholders now have real content available across the folders above)
- [ ] Demo video, 7 minutes max
- [x] This GitHub repo, working code
- [ ] Knowledge base links (policy/strategy sources — see Step 1 doc's Policy Ecosystem table, plus the documents cited in Step 5 and Step 6)
- [ ] Submit by Aug 31, 23:59 KSA time
