# Step 7 — Sink

The final destination: a single, self-contained HTML dashboard — where a
real person actually sees the pipeline's output.

## Files

- `build_dashboard.py` — the script that generates it; run with `python3 build_dashboard.py`
- `dashboard.html` — **the actual deliverable.** Just double-click it, opens in any browser, no server or internet needed (all charts are embedded as base64 directly in the file)

## How to use it for the demo video

1. Open `dashboard.html` in a browser
2. Click through the 4 role tabs: **Public → Regulator → Sandbox Team → Compliance**
3. Click the **"العربية"** button top-right to show the bilingual interface
4. This is your screen-recording material for the 7-minute video

## Design decisions (worth saying out loud in the report/video)

- **Role-based, not one-size-fits-all** — mirrors Step 6's routing exactly. A regulator, a sandbox team, and a compliance officer each see only their own packet, not a raw data dump.
- **Bilingual (EN/Arabic)** — interface chrome and all 16 sector names available in Arabic. Direct, concrete answer to ITU AI Readiness **Dimension 6 (Human Interface)**: "availability of AI models in the local language used in the human interface."
- **Fully self-contained** — no external dependencies, works offline, survives being moved out of the repo folder. Reliable for a live demo where you don't want to depend on Wi-Fi.
