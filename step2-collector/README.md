# Step 2 — Collector (C)

The node that turns two awkward downloads into one dataset worth analysing.

---

## What this stage is actually for

A collector sounds like the least interesting stage in a pipeline. It moves data from one place to another. But almost every decision that constrains what the model can later find is made here, quietly, before anyone has written a line of analysis. Which rows are kept, which are dropped, what counts as a missing value, and what context is attached to each observation — all of it is settled at this stage and inherited by every stage after it.

So the question we held here was not "how do we load the files." It was "what is the honest shape of this data, and what have we implicitly assumed by choosing it."

---

## Three things that had to be solved

### 1. The files are not what they claim to be

SAMA's exports arrive with an `.xls` extension. They are not Excel files. They are MHTML — MIME-encoded, multi-sheet HTML documents — and a standard spreadsheet library will either fail on them or, worse, read them incorrectly without saying so.

The collector parses the underlying MIME structure directly, extracts the specific sheet containing the monthly series, and converts it to a proper DataFrame. This is not elegant work and it is not a research contribution, but it is the difference between an analysis built on the real numbers and one built on whatever a mis-parse produced. We mention it because it is exactly the kind of problem that never appears in a methods section and always appears in practice.

### 2. The two series do not cover the same period

The sector file has usable data from 2016. The e-commerce file is blank before January 2019.

The tempting move is to merge across the full range and let the gaps sit there. We did not, because those gaps are not neutral. A correlation or trend computed across a window where one series is absent for three years is not measuring what it appears to measure. The collector therefore restricts the merged dataset to **January 2019 to December 2023**, the window where both sources have genuine values.

That costs us three years of sector history. It buys sixty months where every number is real, and we would rather have the second thing.

### 3. Months are not interchangeable

A month in a payments series is not just a position on a timeline. It sits inside a lockdown, or a religious season, or a regulatory regime. Treating all sixty months as equivalent throws away context the data already contains.

The collector adds three engineered columns, each computed rather than typed in by hand:

- **`covid_period`** — the core Saudi lockdown window, March to June 2020. The merged data confirms this is a real regime and not a label: e-commerce transactions rose from 6.6 million in February 2020 to 18.2 million in May.
- **`ramadan_month`** — computed per year against the Umm al-Qura lunar calendar. Ramadan moves roughly eleven days earlier in the Gregorian calendar each year, so a hardcoded list of months is correct when you write it and silently wrong within two years. This is the kind of error that produces a plausible result nobody questions.
- **`post_epayments_law`** — from 2020 onward, marking SAMA's real Rules for Electronic Payment Services. It is the regulatory reason the trend being measured exists, and it belongs in the data rather than only in the write-up.

---

## Three output shapes, and why that is not redundancy

The collector writes the same information three ways. This looks wasteful until you try to use one shape for every purpose.

| File | Shape | Used by |
|---|---|---|
| `collected_wide.csv` | One row per month, every sector-metric as a column | Month-level analysis; Step 5's duration calculations |
| `collected_long.csv` | One row per (date, sector, metric, value) fact | Tidy-data convention that most visualisation and statistical tools expect |
| `sector_transactions_matrix.csv` | One row per sector, one column per month | Step 4's clustering — this shape turns each sector into a single 60-dimensional vector describing its whole trajectory |

The third one is the load-bearing choice. Clustering algorithms treat rows as observations, so a sector only becomes something that can be clustered once it is a row. That is a structural decision made here, at the collector, three stages before anyone runs a model.

---

## Files

| File | What it is |
|---|---|
| `collector.py` | The script. Parses, merges, enriches, writes three shapes. |
| `output/collected_wide.csv` | Wide format |
| `output/collected_long.csv` | Long format |
| `output/sector_transactions_matrix.csv` | Sector matrix, input to Step 3 |

## Running it

```bash
pip install pandas lxml
python3 collector.py
```

It expects the two raw SAMA downloads in this folder. They are committed unmodified, so this reproduces from the exact bytes we used.

---

## What we would flag

The Ramadan dates for years without an officially confirmed entry in our source research are estimated using the standard eleven-day shift, and are accurate to roughly one day. For a monthly series that is immaterial. We say it anyway, because the point of documenting an assumption is that someone else can decide whether it matters to them, and that decision is not ours to make on their behalf.
