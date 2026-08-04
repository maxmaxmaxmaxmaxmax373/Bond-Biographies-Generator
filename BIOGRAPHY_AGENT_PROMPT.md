# Extended Prompt: Bond Biography Enrichment Agent

This is the reusable prompt for turning a raw auto-generated bond chapter into a polished,
publication-quality biography. Workflow: (1) pick a bond with ample price data (see the
coverage note in `QUICK_REFERENCE.md` — only 77 of 2,857 issues have ≥12 monthly price
observations), (2) generate the raw draft, (3) hand this prompt — with the bracketed slots
filled in — to a Claude agent.

## Step 0 — Pick a bond and generate the raw draft

```bash
python3 bond_biography_agent.py --bond-id <L1_ID>
```

(On this machine, use `/Users/thomassargent/anaconda3/bin/python3` — the system Python 3.9
has a broken PyTables wheel.)

## The prompt (fill in the [BRACKETED] slots)

---

You are enriching an auto-generated "bond biography" Jupyter notebook into a polished,
publication-quality chapter for a book based on the Hall–Payne–Sargent U.S. Federal Bond
Database (Payne, Szoke, Hall & Sargent, QJE 2025). Work in the `Bond-Biographies-Generator`
project folder.

YOUR BOND: L1 ID [ID] — "[TREASURY NAME]", coupon [X]%, issued [DATE].
[2–5 sentences of orienting historical context: authorizing act, why it was issued, what
era its price series spans, and the major events its prices should reflect. This is the
one slot that benefits from human/Claude judgment before launching the agent.]

STEP 1 — Study the reference template. Read
`enhanced_chapters/chapter_20044_Louisiana_Six_Per_Cent_Stock_enhanced.ipynb` in full.
Absorb its structure, section ordering, markdown voice (scholarly but readable narrative
economic history), how it interleaves narrative markdown with code cells, how it cites
sources, and how it interprets charts in prose. [Optionally: also skim whichever other
enhanced chapter is historically adjacent to this bond.]

STEP 2 — Read the raw draft `chapter_[ID]_[NAME].ipynb` in full. It contains
auto-generated metadata, charts, statistics, and `<!-- ENRICH: ... -->` markers flagging
where hand-written narrative is needed.

STEP 3 — Produce the enhanced notebook at
`enhanced_chapters/chapter_[ID]_[NAME]_enhanced.ipynb`. Rules:

- Preserve ALL code cells from the draft essentially unchanged (they load `data/` files
  and draw the charts). Add small code cells only if the template does something analogous.
- Replace every `<!-- ENRICH -->` marker with substantive historical narrative in the
  template's voice. Cover at minimum: [LIST OF TOPICS — the authorizing legislation, the
  fiscal/political circumstances of issue, the bond's mechanics, the events behind the
  major price moves, and how the bond's life ended].
- ACCURACY IS PARAMOUNT: state only well-established historical facts. Do not invent
  quotations, precise figures, or archival citations you are not certain of. Where a
  detail is uncertain, write in general terms rather than fabricate.
- Include a references section citing real, standard works (e.g., Bayley's *National Loans
  of the United States*, Studenski & Krooss, era-specific classics), following the
  citation style of the template.
- The notebook must remain valid nbformat 4 JSON — build with `nbformat` and validate.

STEP 4 — Verify: execute the finished notebook end-to-end from the project folder:

```bash
python3 -m jupyter nbconvert --to notebook --execute --inplace \
  "enhanced_chapters/chapter_[ID]_[NAME]_enhanced.ipynb"
```

Code cells resolve `data/` relative to the working directory — run nbconvert with cwd =
the project root, and make the path logic work from `enhanced_chapters/` (copy the
approach used by the existing enhanced notebooks). Fix any execution errors and re-run
until all cells execute cleanly.

Return a short report: file path written, cell count, ENRICH markers replaced,
confirmation that execution succeeded, and any caveats about historical claims kept
deliberately general.

---

## Bonds written so far

Enhanced: 20044, 20048, 20101, 20162, 40007, 20023, 20121, 20021, 20022, 20096, 20131,
20043, 20052, 20064, 20083, 20166 (all 16 headline issues in `QUICK_REFERENCE.md`),
plus 20089, 20090 (Mexican War loans), 20108 (Ten-Forties), 20168, 20169 (3rd/4th
Liberty), 20045, 20056, 20058 (1814-era, from the old raw drafts), 20129 (Loan of
1925 — the Belmont–Morgan gold loan; longest continuous price series), 20120 (4.5%
Loan of 1891 — the refunding's middle leg), 20130 (Ten-Twenty of 1898 — the
Spanish-American War popular loan), 20114/20115/20116 (Consols of 1865/1867/1868 —
the 7-30 conversion trio), 20128 (Loan of 1904 — Cleveland's 1894 gold-defense sales),
and 20132/20133/20134 (Panama Canal Series 1906/1908/1911 — the last a bond without
the circulation privilege, the era's controlled experiment).
Cross-referenced arcs: Hamilton funding trio (20021/20022/20023) + Quasi-War 8s (20043)
+ exchange operation (20045); War of 1812 (20048 → 20052 → 20056/20058 → 20064);
antebellum/Mexican War (20083 → 20089 → 20090); Civil War (20096 → 20101 → 20108);
refunding/gold standard (20121 → 20131); WWI Liberty sequence (20162 → 20166 → 20168 →
20169, ending in the gold-clause abrogation and Perry v. United States).

Second tier complete (August 2026): 20042, 20051, 20069, 20084, 20086, 20092, 20093,
20109, 20113, 20119, 20163, 20164, 20167, 20170, 20171 — all 49 issues on the
candidate lists are now written and in the book. Remaining unwritten issues with ≥12
price observations are mostly Treasury-note records, continuations (20123/20125/20127),
small 1820s loans, and 1920s Treasury notes — check coverage in `data/BondPrice.csv`
before choosing further chapters.
