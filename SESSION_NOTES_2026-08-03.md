# Session Notes — August 3, 2026

## What happened

In one Claude Code session, the enhanced-chapter library grew from **5 to 24 chapters**.
Tom Sargent asked Claude to read `QUICK_REFERENCE.md` and `README.md`, assemble an
extended prompt for agents that write bond biographies, and execute it — first on two
bonds, then, in successive rounds, on every remaining issue with substantial price data,
plus the three old raw drafts in the project root.

## The method

Each chapter was produced by the same repeatable pipeline:

1. **Generate the raw draft** with the toolkit:
   `python3 bond_biography_agent.py --bond-id <ID>` (run from the project root).
2. **Launch an enrichment agent** with a parameterized extended prompt — saved as
   [`BIOGRAPHY_AGENT_PROMPT.md`](BIOGRAPHY_AGENT_PROMPT.md) — that instructs the agent to:
   - study the ★ Louisiana template
     (`enhanced_chapters/chapter_20044_Louisiana_Six_Per_Cent_Stock_enhanced.ipynb`)
     plus whichever existing enhanced chapter is historically adjacent;
   - read the raw draft and replace every `<!-- ENRICH -->` marker with narrative in the
     template's voice, covering a bond-specific list of topics;
   - **verify price/quantity claims against the database before writing them**, and
     attribute inexplicable auto-detected "events" to thin quotations or bookkeeping
     rather than inventing market stories;
   - hedge uncertain details, invent no quotations or citations, and cite only standard
     works (Bayley, Dewey, Studenski & Krooss, era classics, Payne–Szőke–Hall–Sargent 2025);
   - preserve the draft's code cells (changing only `data/BondDF.h5` → `../data/BondDF.h5`
     so notebooks run from `enhanced_chapters/`, plus modest chart-annotation additions);
   - execute the finished notebook end-to-end with `jupyter nbconvert --execute` and fix
     any errors.
3. **Independent verification** in the main session: every notebook re-checked for valid
   nbformat, full execution with zero error outputs, and zero leftover `ENRICH` markers.

Agents ran in parallel waves of 2–5. Bonds forming narrative arcs were sequenced so later
chapters could cross-reference finished siblings (e.g., the 1814 loans were written after
the 1813 syndicate loan and the 7s of 1815).

## Chapters written this session (19 new, in order)

**Round 1 — two pilots**
| ID | Bond | Note |
|---|---|---|
| 20023 | Three Per Cent Stock of 1790 | Longest price series then unwritten (488 obs); Hamilton's funding, Panic of 1792, Jacksonian extinction |
| 20121 | Four Percent Loan of 1907 | Sherman refunding, resumption, Panic of 1893, circulation-privilege premium |

**Round 2 — completing the Hamilton funding trio**
| 20021 | Six Per Cent Stock of 1790 | Benchmark security; $8-per-$100 redemption cap; Bank of the U.S. subscriptions |
| 20022 | Deferred Six Per Cent Stock of 1790 | Measured convergence to the 6s: spread ~$42 (1790–92) → $3 (1800) → 0 (1801) |

**Round 3 — Civil War and gold-standard pairs**
| 20096 | Loan of February 1861 | Secession-crisis loan; verified the series records greenback quotations after 1862 |
| 20131 | Consols of 1930 | 2% gold bonds priced by the circulation privilege; retired with national bank notes, 1935 |

**Round 4 — the remaining headline issues**
| 20043 | Eight Per Cent Loan of 1800 | Quasi-War borrowing; premium-decay path, never below par |
| 20052 | Sixteen Million Loan of 1813 | Girard–Astor–Parish syndicate at 88; birth of American underwriting |
| 20064 | Seven Per Cent Stock of 1815 | Treasury notes funded into 7s at the war's end |
| 20083 | Loan of 1842 | Federal credit restored amid the state-default crisis |
| 20166 | 2nd Liberty Loan of 1917 | Birth of the statutory debt limit; low of $84.36 (Aug 1920); 1927 call |

**Round 5, Wave A — coverage-scan candidates** (after scanning `data/BondPrice.csv`)
| 20089 | Loan of 1847 | Corcoran & Riggs; London placement; Guthrie buybacks |
| 20090 | Loan of 1848 | Sold above par six years after the 1842 credit drought |
| 20108 | Ten-Forties of 1864 | Chase's failed 5% experiment; 1879 refunding cliff |
| 20168 | 3rd Liberty Loan | Non-convertible, non-callable 4¼% standard; 1928 maturity |
| 20169 | 4th Liberty Loan | Gold-clause abrogation; *Perry v. United States* (1935) |

**Round 5, Wave B — the three old raw drafts**
| 20045 | Exchanged Six Per Cent Stock of 1807 | Zero price observations — chapter built honestly around quantity data and exchange mechanics |
| 20056 | Ten Million Loan of 1814 | 88 → 80 sequential borrowing; most-favored-lender clause |
| 20058 | Undesignated Loan of 1814 | Residual 1814 classification, described as such, with a closing "Caveat, Honestly Stated" section |

## Data-integrity findings the agents surfaced

- Wartime (1862–65) prices for Civil War-era bonds are **greenback quotations**, verified
  by comparing bond prices against the gold premium; several auto-detected "events" are
  currency-unit effects, not credit events.
- Several auto-detected price spikes are **data artifacts** (e.g., 20090's Dec 1859 print
  of 133.56; 20166's isolated May 1920 spike; gap artifacts in the 1814 loans' series) and
  are flagged as such in the chapters instead of being narrativized.
- 20045 has **no price data at all**; 20056's price series contains **no wartime
  quotations** — both chapters state this plainly.
- Auto-generated event matches sometimes pair price/quantity moves with coincidental
  dates (Gettysburg vs. contractual 1863 redemptions; the National Banking Act vs.
  greenback depreciation); the chapters disclaim these explicitly.
- The standardized YTM formula is flagged wherever it misleads (no-maturity redemption-
  capped stocks; the deferred 6s' pre-1801 deferral period).

## The library now

24 enhanced chapters in [`enhanced_chapters/`](enhanced_chapters/), forming six
cross-referenced arcs:

1. **Hamilton's funding system**: 20021 → 20022 → 20023, with 20043 (Quasi-War 8s) and
   20045 (the 1807 exchange) as codas
2. **War of 1812**: 20048 → 20052 → 20056/20058 → 20064
3. **Antebellum / Mexican War**: 20083 → 20089 → 20090 (plus 20044 Louisiana and
   40007 Currency Sixes from before)
4. **Civil War**: 20096 → 20101 → 20108
5. **Refunding / gold standard**: 20121 → 20131
6. **WWI Liberty sequence**: 20162 → 20166 → 20168 → 20169, ending in *Perry v. United
   States*

## Environment notes

- The system Python 3.9 (`/usr/bin/python3`) has a broken PyTables wheel on this Mac;
  everything ran with `/Users/thomassargent/anaconda3/bin/python3` (generator and
  `jupyter nbconvert`). Recorded in Claude's project memory.
- Raw drafts remain in the project root; enhanced chapters resolve data via `../data/`.

## Files created or modified this session

- 19 new `enhanced_chapters/chapter_*_enhanced.ipynb`
- 11 new raw drafts `chapter_*.ipynb` in the project root (inputs to enrichment)
- [`BIOGRAPHY_AGENT_PROMPT.md`](BIOGRAPHY_AGENT_PROMPT.md) — the reusable extended
  prompt, with the roster of written bonds and ranked remaining candidates
- This file

## Where to go next

Best remaining candidates by price coverage: **20129 Loan of 1925 (778 obs — the longest
price series in the entire dataset)**, 20130 Ten-Twenty of 1898 (571), 20120 4½% Loan of
1891 (534), the Consols of 1865/1867/1868, the Loan of 1904, the three Panama Canal
loans, the Five-Twenties of 1864/1865, and the converted Liberty issues. Those would
essentially complete the Gilded Age and round out the Civil War and WWI families. See the
candidate list in `BIOGRAPHY_AGENT_PROMPT.md`.

Human review remains the final step: the agents were instructed to hedge rather than
invent, and their per-chapter reports (relayed in the session) list exactly which claims
were kept deliberately general — but the historian's eye is the referee.
