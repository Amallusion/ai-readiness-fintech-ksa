# Step 3 — Preprocessor (PP)

Where the data is checked, and where it is transformed so that comparing sectors means something.

---

## The transformation that decides everything

Restaurants and Cafés process tens of thousands of card transactions a month. Jewelry processes hundreds. If you feed those raw counts into a clustering algorithm and ask it to group sectors, it will do exactly what you asked and group them by size, because size is the largest source of variation in the numbers you handed it.

The result would look like a finding. It would be a restatement of the input.

The fix is borrowed directly from how financial indices are built. Every sector's series is rebased so that its own first month equals 100:

```
indexed_value(t) = ( raw_value(t) / raw_value(Jan 2019) ) × 100
```

After this, a value of 300 means three times its own January 2019 level, whether that sector started at 500 transactions a month or 50,000. The comparison becomes fair because every sector is now measured against itself.

This is the single most consequential line of code in the pipeline, and it is worth being clear about what it costs as well as what it buys. Rebasing removes the size dimension entirely. That is exactly what we want for comparing growth, and it is why Step 4 has to reintroduce scale from a different direction — through average ticket size — to say anything about mechanism. The transformation that makes the comparison possible also makes part of the story invisible, and knowing that in advance is the difference between choosing a method and inheriting one.

---

## What was checked before anything was transformed

Validation is the part of a pipeline that produces no output when it works, which is why it tends to get skipped. Four checks ran here, and all four passed:

- **No missing values** across the merged window
- **No exact-zero values**, which in an administrative series usually signals a reporting gap rather than genuine absence of activity
- **Correct numeric types** on every column
- **No structural discontinuity inside the analysis window**

The fourth one is the one worth explaining. SAMA's own source footnote documents that Hotels was split out of Restaurants & Café, and that Electronic & Electric Devices, Furniture, Construction & Building Materials, and Jewelry were split out of Miscellaneous Goods and Services at some point in the series' history. If that redefinition had happened inside our window, every affected sector would show an artificial jump that a model would happily interpret as growth.

The check confirmed all affected sectors already had distinct, non-zero values from the very first month of the window, meaning the redefinition predates our data. No correction was needed.

We are documenting a check that found nothing, which sounds like a strange thing to put in a README. It is here because "we found no problem" and "we did not look" produce identical-looking data, and only one of them is trustworthy.

---

## Growth rates

A separate month-over-month percentage change series is computed for every sector and written out alongside the indexed matrix.

This is not the same information as the index in a different format. The index is a level; the growth series is a rate. Any correlation or regression that should not be inflated by two series trending upward together needs the rate, not the level — and Step 4 makes exactly that comparison, showing that the correlation which looks strong on levels does not survive on differences.

Producing both here means that comparison is available later without going back to the raw data.

---

## Files

| File | What it is |
|---|---|
| `preprocessor.py` | Validation, rebasing, growth-rate computation |
| `output/sector_matrix_indexed.csv` | Sectors × months, Jan 2019 = 100. The main input to Step 4 |
| `output/sector_matrix_growth.csv` | Sectors × months, month-over-month % change |
| `output/validation_report.txt` | The four checks and their results |

## Running it

```bash
pip install pandas numpy
python3 preprocessor.py
```

Expects `collected_wide.csv` and `sector_transactions_matrix.csv` from Step 2 in this folder.

---

## One limitation worth stating

The baseline month is a choice, and it is not a neutral one. Rebasing to January 2019 means every subsequent result is expressed relative to whatever was happening in January 2019. Choose a different baseline and the rankings shift.

We chose it because it is the first month where both source series carry genuine values, so it is the only baseline that does not require discarding data or inventing it. But we could not find any Saudi standard governing methodological disclosure for administrative statistics used this way, which is one of the two policy gaps this project reports. The preprocessing stage is precisely where a defensible finding and a manufactured one become indistinguishable from the outside, and at present nothing requires anyone to show their working.
