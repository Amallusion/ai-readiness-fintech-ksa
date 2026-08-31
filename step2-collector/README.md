# Step 2 — Collector (C)

Turns the two raw SAMA exports into one clean, ready-to-analyze dataset.

## Files

- `raw/sector_pos_raw.xls` — raw SAMA export: POS transactions by 16 sectors, Jan 2016–Dec 2023
- `raw/ecommerce_raw.xls` — raw SAMA export: e-commerce transactions via Mada cards, Jan 1995–Jun 2026 (real data from Jan 2019)
- `collector.py` — the Collector script; run with `python3 collector.py`
- `collected_wide.csv` — **main output.** One row per month (Jan 2019–Dec 2023), every sector's transactions/sales as columns, plus event-tag columns (`covid_period`, `ramadan_month`, `post_epayments_law`)
- `collected_long.csv` — same data in tidy long format (Date, Sector, Metric, Value)
- `sector_transactions_matrix.csv` — one row per sector, one column per month — shaped for clustering in Step 4

## Why the date range is Jan 2019–Dec 2023

The sector file has real data from 2016, but the e-commerce file only has real data from Jan 2019 onward (earlier months are blank in SAMA's own export). Merging outside that shared window would create fake gaps, so the collected dataset is trimmed to the range where both sources have real numbers.

## A note on the raw file format

Both raw `.xls` files are not real binary Excel files — they're MHTML (a multi-sheet HTML document wrapped in a MIME envelope), which is what SAMA's export tool actually produces. `collector.py` parses that format directly rather than relying on a standard Excel reader.

## Early finding (worth carrying into Step 4)

Across two independent checks — growth from 2019 to 2023, and correlation with the national e-commerce trend — the **Jewelry sector stands out as the clear digitalization laggard** (only 1.35x transaction growth vs. up to 21.8x for other sectors; only 0.51 correlation with the e-commerce trend vs. 0.9+ for most others). Worth investigating further in Step 4 — high-value goods sectors may have distinct reasons (e.g. cash preference for large transactions) that connect to real AML/CTF policy.
