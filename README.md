# [Your Solution Name] — ITU AI Readiness Hackathon (KSA)

Fintech track. Full pipeline per ITU-T Y.3172: **SRC → C → PP → M → P → D → SINK**

## Progress

| Step | Node | Status | Folder |
|---|---|---|---|
| 1 | SRC (Source) | ✅ Done | `step1-source-selection.md` |
| 2 | C (Collector) | ✅ Done | `step2-collector/` |
| 3 | PP (Pre-processor) | ✅ Done | `step3-preprocessor/` + `visuals/` |
| 4 | M (Model) | ✅ Done | — |
| 5 | P (Policy) | ✅ Done | — |
| 6 | D (Distributor) | ✅ Done | — |
| 7 | SINK | ✅ Done | — |

## What this project is

Using Saudi Central Bank (SAMA) open data on point-of-sale transactions by
economic sector (2016–2023) plus national e-commerce transaction data, to
identify which sectors of the Saudi economy have lagged behind the
Kingdom's cashless-payments push — and connect that finding to real
financial-sector policy (SAMA regulations, AML/CTF guidelines, Vision 2030
targets).

**Headline finding so far:** the Jewelry sector is a consistent
digitalization laggard — confirmed three independent ways (lowest
5-year growth, lowest correlation with the national e-commerce trend,
lowest rebased growth index) — a pattern plausibly connected to AML/CTF
considerations around large cash transactions in high-value goods.

## Folder guide

- `step1-source-selection.md` — how and why we picked the SAMA data (with
  scored alternatives, and the real SAMA policy documents found)
- `step2-collector/` — raw files + the script that merges them + event tags
  (COVID period, Ramadan months, post-2020 e-payments law)
- `step3-preprocessor/` — validation checks + the rebased/growth versions
  of the data, ready for modeling
- `visuals/` — 3 charts + the sector growth-tier binning table

Each subfolder has its own README explaining exactly what's inside and why.

## Team Voxel

- Mohamd Bremo
- Thamer Al Kahtani
- Ayman Mohammed
- Abdulelah Hejazi

## Submission checklist (ITU AI Readiness Hackathon KSA)

- [ ] Technical report, 5 pages max (see `report-skeleton.md` for the outline)
- [ ] Demo video, 7 minutes max
- [ ] This GitHub repo, working code
- [ ] Knowledge base links (policy/strategy sources — see Step 1 doc's
      Policy Ecosystem table, and Step 5 once built)
- [ ] Submit by Aug 31, 23:59 KSA time
