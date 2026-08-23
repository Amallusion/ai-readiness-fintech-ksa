Team Voxel — ITU AI Readiness Hackathon (KSA)

Fintech track. Full pipeline per ITU-T Y.3172: SRC → C → PP → M → P → D → SINK

Progress
Step	Node	Status	Folder
1	SRC (Source)	✅ Done	step1-source-selection.md
2	C (Collector)	✅ Done	step2-collector/
3	PP (Pre-processor)	✅ Done	step3-preprocessor/ + visuals/
4	M (Model)	✅ Done	step4-model/
5	P (Policy)	✅ Done	step5-policy/
6	D (Distributor)	✅ Done	step6-distributor/
7	SINK	✅ Done	step7-sink/

All 7 pipeline steps complete.

What this project is

Using Saudi Central Bank (SAMA) open data on point-of-sale transactions by economic sector (2019–2023) plus national e-commerce transaction data, to identify which sectors of the Saudi economy have lagged behind the Kingdom's cashless-payments push — and turn that into real, safeguarded action grounded in actual SAMA policy.

Headline finding, confirmed 3 independent ways (growth rate, correlation with the national e-commerce trend, and an independent K-Means clustering with 94% agreement to manual tiers): 8 of 16 sectors, led by Jewelry, are consistent digitalization laggards.

What the pipeline does with that finding: a 4-layer policy engine (Step 5) turns it into a context-review prompt, a Ramadan-timed sandbox pilot referral, a transparency-disclosure requirement — and, critically, an AML/CTF gate that is dormant by design and can never be triggered by sector-level data alone. That decision is routed (Step 6) to three different real institutions, each getting only their relevant slice, and lands (Step 7) on a bilingual (EN/Arabic), role-based dashboard.

Folder guide
step1-source-selection.md — how and why we picked the SAMA data (with scored alternatives, and the real SAMA policy documents found)
step2-collector/ — raw files + the script that merges them + event tags (COVID period, Ramadan months, post-2020 e-payments law)
step3-preprocessor/ — validation checks + the rebased/growth versions of the data, ready for modeling
visuals/ — 3 charts + the sector growth-tier binning table
step4-model/ — K-Means clustering (94% agreement with manual tiers) + an honestly-reported IQR/boxplot outlier check
step5-policy/ — the 4-layer decision engine (context review, sandbox referral, AML/CTF dormant-by-design gate, transparency disclosure) + the full Jewelry case memo, which doubles as the report's required controversy-scenario answer
step6-distributor/ — routes one decision into 3 stakeholder-specific packets (regulator, sandbox team, compliance office)
step7-sink/ — dashboard.html, the final bilingual, role-based demo screen

Each subfolder has its own README explaining exactly what's inside and why.

Team Voxel
Mohamd Bremo
Thamer Al Kahtani
Ayman Mohammed
Abdulelah Hejazi
Submission checklist (ITU AI Readiness Hackathon KSA)
 Technical report, 5 pages max (see report-skeleton.md for the outline — all 🔲 placeholders now have real content available across the folders above)
 Demo video, 7 minutes max
 This GitHub repo, working code
 Knowledge base links (policy/strategy sources — see Step 1 doc's Policy Ecosystem table, plus the documents cited in Step 5 and Step 6)
 Submit by Aug 31, 23:59 KSA time
