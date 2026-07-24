# Bond Biographies — Quick Reference

Two things: (1) where the bond code numbers live, (2) how to generate a biography.
Longer, zero-Python-experience version: [`README.md`](README.md).

**The "project folder"** is the `Bond-Biographies-Generator` directory itself — the folder that
holds `bond_biography_agent.py`, `requirements.txt`, and the `data/` and `enhanced_chapters/`
subfolders. **Every path in this document is written relative to that folder**, so run every
command with your terminal `cd`'d into it.

---

## 1. The bond code numbers

Every bond in the dataset has an integer code called **`L1 ID`**. The master list is:

**[`data/BondList.csv`](data/BondList.csv)** — 2,857 issues, 1776–1960, one row per issue.
Column 1 is the `L1 ID`; the human-readable name is in `Treasury's Name Of Issue`.
(It also carries authorizing act, issue/redemption dates, coupon rate and frequency,
callability, price sold, authorized amount — 48 columns in all.)

The same `L1 ID` keys the two time-series files:
[`data/BondPrice.csv`](data/BondPrice.csv) (monthly prices) and
[`data/BondQuant.csv`](data/BondQuant.csv) (monthly quantities),
both indexed by `(L1 ID, Series)`. [`data/BondDF.h5`](data/BondDF.h5) is the same three
tables bundled in one HDF5 file.

### ID blocks

The first digit of the ID encodes the top-level category:

| ID block | Category | Count |
|---|---|---|
| `10001`–`10003` | Pre-1790 domestic debt | 3 |
| `20001`–`22811` | Interest bearing (marketable + non-marketable) | 2,811 |
| `30001`–`30019` | Non-interest bearing (currency) | 19 |
| `40001`–`40023` | Other (old debt, prepayments, Pacific Railroad…) | 23 |

Within the interest-bearing block, by sub-category:

| Sub-category | ID range | Count |
|---|---|---|
| Foreign Loan | 20001–20018 | 18 |
| Temporary Loan | 20019–20102 | 19 |
| Long Term Bond | 20021–20131 | 73 |
| Treasury Note (pre-1920) | 20050–20136 | 17 |
| Certificates of Indebtedness | 20081–22805 | 250 |
| Panama Canal Bond | 20132–20174 | 6 |
| Liberty Loan | 20162–22802 | 23 |
| War Savings / Savings Bonds | 20172–22809 | 123 |
| Treasury Bond | 20179–22803 | 81 |
| Treasury Note (post-1920) | 20236–22804 | 134 |
| Treasury Bill | 20496–22806 | 1,613 |
| Special Issues (non-marketable) | 21613–22800 | 387 |

### Headline issues (the ones with real price history)

| L1 ID | Name | Coupon | First issued | Monthly price obs |
|---|---|---|---|---|
| `20021` | Six Per Cent Stock of 1790 | 6.0% | 1790 | 382 |
| `20022` | Deferred Six Per Cent Stock of 1790 | 6.0% | 1790 | 381 |
| `20023` | Three Per Cent Stock of 1790 | 3.0% | 1790 | 488 |
| `20043` | Eight Per Cent. Loan of 1800 | 8.0% | 1800 | 98 |
| `20044` | Louisiana Six Per Cent. Stock | 6.0% | 1804 | 135 |
| `20048` | Six Per Cent. Loan of 1812 | 6.0% | 1812 | 150 |
| `20052` | Sixteen Million Loan of 1813 | 6.0% | 1813 | 182 |
| `20056` | Ten Million Loan of 1814 | 6.0% | 1814 | 64 |
| `20064` | Seven Per Cent. Stock of 1815 | 7.0% | 1815 | 88 |
| `20083` | Loan of 1842 | 6.0% | 1842 | 205 |
| `20096` | Loan of February 1861 | 6.0% | 1861 | 243 |
| `20101` | Five-Twenties of 1862 | 6.0% | 1862 | 154 |
| `20121` | Four Percent Loan of 1907 | 4.0% | 1878 | 357 |
| `20131` | Consols of 1930 | 2.0% | 1900 | 262 |
| `20162` | 1st Liberty Loan of 1917 | 3.5% | 1917 | 103 |
| `20166` | 2nd Liberty Loan of 1917 | 4.0% | 1917 | 97 |

Note: only **77 of the 2,857 issues have 12 or more monthly price observations.** For the
rest, the generator still produces a chapter, but with the price sections empty — so it is
worth checking coverage before picking an ID.

### Looking an ID up from the command line

Run from the project folder; the script is [`bond_biography_agent.py`](bond_biography_agent.py) at the root.

```bash
python3 bond_biography_agent.py --search "Louisiana"      # name → ID
python3 bond_biography_agent.py --list-categories         # all categories + counts
```

Or in Python / a notebook:

```python
import pandas as pd
BondList = pd.read_csv("data/BondList.csv", index_col=0)   # index = L1 ID
BondList.loc[20044]                                        # one bond
BondList[BondList["Treasury's Name Of Issue"].str.contains("Liberty", na=False)]
```

---

## 2. Generating a bond biography

One-time setup — from inside the project folder, install the pinned packages listed in
[`requirements.txt`](requirements.txt) (project root):

```bash
pip3 install -r requirements.txt
```

Then, still in the project folder, run the generator
[`bond_biography_agent.py`](bond_biography_agent.py) (project root):

```bash
# by ID — the usual case
python3 bond_biography_agent.py --bond-id 20044

# by name, then generate
python3 bond_biography_agent.py --search "Liberty"
python3 bond_biography_agent.py --search "Liberty" --generate-first

# guided prompts
python3 bond_biography_agent.py --interactive

# custom output filename
python3 bond_biography_agent.py --bond-id 20044 --output my_chapter.ipynb
```

Output: a notebook named `chapter_<ID>_<name>.ipynb`, written to the **project folder root**
(e.g. `--bond-id 20044` produces
[`chapter_20044_Louisiana_Six_Per_Cent_Stock_.ipynb`](chapter_20044_Louisiana_Six_Per_Cent_Stock_.ipynb)
there). Four such raw drafts already sit in the root —
[`chapter_20045_Exchanged_Six_Per_Cent_Stock_of_1807.ipynb`](chapter_20045_Exchanged_Six_Per_Cent_Stock_of_1807.ipynb),
[`chapter_20056_Ten_Million_Loan_of_1814.ipynb`](chapter_20056_Ten_Million_Loan_of_1814.ipynb),
[`chapter_20058_Undesignated_Loan_of_1814.ipynb`](chapter_20058_Undesignated_Loan_of_1814.ipynb).
Open one in VS Code or `jupyter notebook` and run all cells to render the charts.

Verified example — `--bond-id 20044` prints:

```
Generating enhanced biography for: Louisiana Six Per Cent. Stock
  Bond ID: 20044          Coupon: 6.0%        Issued: March 31, 1804
  Price data: Yes (135 observations)
  Quantity data: Yes (144 observations)
  Historical events overlapping: 7
  Significant price events detected: 10
  Related bonds found: 14
  Chapter saved to: chapter_20044_Louisiana_Six_Per_Cent_Stock_.ipynb  (24 cells)
```

### A good way to generate stable enhanced notebooks

1. Open Claude Code and copy the paths of two notebooks: the newly generated but rudimentary
   one (in the project root, e.g.
   [`chapter_20056_Ten_Million_Loan_of_1814.ipynb`](chapter_20056_Ten_Million_Loan_of_1814.ipynb)),
   and the polished Louisiana notebook that serves as the reference,
   [`enhanced_chapters/chapter_20044_Louisiana_Six_Per_Cent_Stock_enhanced.ipynb`](enhanced_chapters/chapter_20044_Louisiana_Six_Per_Cent_Stock_enhanced.ipynb).

2. Ask Claude to learn from the structure of that reference notebook, and supplement the
   contents as much as possible but be careful of false information.

3. You may need to chat multiple rounds to obtain a very good result. Learning from the
   reference notebook is a good start.
---

## 3. What comes out, and what still needs a human

Each generated chapter contains: bond metadata and terms, era/historical context, a
lifecycle timeline, quantity-outstanding chart, price chart with summary statistics,
rolling volatility, automatically detected large price moves matched against a built-in
historical event list, an approximate YTM, a related-bonds comparison, and suggested
references.

Everywhere qualitative narrative is needed, the draft leaves an `<!-- ENRICH: ... -->`
marker. Those are the spots for hand-written history and citations.

Five chapters have already been through that polish pass, in
[`enhanced_chapters/`](enhanced_chapters/):

| File (path relative to project folder) | Bond |
|---|---|
| [`enhanced_chapters/chapter_20044_Louisiana_Six_Per_Cent_Stock_enhanced.ipynb`](enhanced_chapters/chapter_20044_Louisiana_Six_Per_Cent_Stock_enhanced.ipynb) | ★ style template |
| [`enhanced_chapters/chapter_20048_Six_Per_Cent_Loan_of_1812_enhanced.ipynb`](enhanced_chapters/chapter_20048_Six_Per_Cent_Loan_of_1812_enhanced.ipynb) | War of 1812 |
| [`enhanced_chapters/chapter_20101_FiveTwenties_of_1862_enhanced.ipynb`](enhanced_chapters/chapter_20101_FiveTwenties_of_1862_enhanced.ipynb) | Civil War 5-20s |
| [`enhanced_chapters/chapter_20162_1st_Liberty_Loan_enhanced.ipynb`](enhanced_chapters/chapter_20162_1st_Liberty_Loan_enhanced.ipynb) | WWI |
| [`enhanced_chapters/chapter_40007_Currency_Sixes_enhanced.ipynb`](enhanced_chapters/chapter_40007_Currency_Sixes_enhanced.ipynb) | Pacific Railroad |

Workflow: generate the draft → fill in the `ENRICH` blocks following the template's voice.

---

## Gotchas

- **Run the command from the project folder** (`Bond-Biographies-Generator`) — the script
  resolves `data/` and writes output relative to it.
- **`ImportError: Import pytables failed`** — the loader reads
  [`data/BondDF.h5`](data/BondDF.h5) first, which needs PyTables: `pip3 install tables`.
- **On Windows** use `python` / `pip` instead of `python3` / `pip3`.
- Empty price/quantity sections in a chapter usually mean that issue simply has no price
  series in the data (see coverage note above), not a bug.

Data source: Payne, Szoke, Hall & Sargent, *QJE* (2025) — 2,857 U.S. federal bond issues, 1776–1960.
