# Bond Biographies Generator — Beginner's Guide

This toolkit automatically generates "bond biography" Jupyter notebook chapters from the Hall-Payne-Sargent U.S. Federal Bond Database (1776–1960, 2,857 issues). Each generated chapter includes: bond metadata, historical context, price/quantity charts, volatility analysis, related-bond comparisons, and more.

> **This guide assumes zero Python experience.** If you already know Python, jump to the [Quick Start](#quick-start-experienced-users) section at the bottom.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Step 1: Install Python](#step-1-install-python)
3. [Step 2: Open a Terminal and Enter the Project Folder](#step-2-open-a-terminal-and-enter-the-project-folder)
4. [Step 3: Install the Required Python Packages](#step-3-install-the-required-python-packages)
5. [Step 4: Generate a Bond Chapter Notebook](#step-4-generate-a-bond-chapter-notebook)
6. [Step 5: Open the Generated Notebook](#step-5-open-the-generated-notebook)
7. [About the `enhanced_chapters` Folder](#about-the-enhanced_chapters-folder)
8. [Troubleshooting](#troubleshooting)
9. [Quick Start (Experienced Users)](#quick-start-experienced-users)

---

## Project Structure

After downloading the folder, the contents look like this:

```
Bond-Biographies-Generator/
├── README.md                        ← This file
├── bond_biography_agent.py          ← Main program: auto-generates bond chapters
├── Functions.py                     ← Helper functions for loading data
├── requirements.txt                 ← Lists every Python package this tool needs
│
├── data/                            ← Database files (do NOT modify)
│   ├── BondDF.h5                    ← Main database (HDF5, 2,857 bond issues)
│   ├── BondList.csv                 ← Bond metadata
│   ├── BondPrice.csv                ← Monthly price data
│   ├── BondQuant.csv                ← Monthly quantity data
│   ├── Macaulay_table2_railroad_bond_prices.xlsx
│   ├── Macaulay_table3_railroad_bond_yields.xlsx
│   └── gold_price_greenbacks_1862_1878.csv  ← Monthly greenback price of $100 gold (for gold-unit charts)
│
└── enhanced_chapters/               ← 5 polished sample chapters (already generated + edited)
    ├── chapter_20044_Louisiana_Six_Per_Cent_Stock_enhanced.ipynb  ★ TEMPLATE
    ├── chapter_20048_Six_Per_Cent_Loan_of_1812_enhanced.ipynb
    ├── chapter_20101_FiveTwenties_of_1862_enhanced.ipynb
    ├── chapter_20162_1st_Liberty_Loan_enhanced.ipynb
    └── chapter_40007_Currency_Sixes_enhanced.ipynb
```

---

## Step 1: Install Python

### Mac users

1. Open a browser and go to https://www.python.org/downloads/
2. The page auto-detects your system and shows a big yellow button: **"Download Python 3.x.x"**. Click it.
3. Once downloaded, double-click the `.pkg` file and click "Continue" through every screen, then "Install".
4. After installation, **open the Terminal app** (found in `Applications / Utilities / Terminal`, or press `Cmd + Space` and type "Terminal").
5. In the terminal, type the following and press Enter to verify the installation:
   ```bash
   python3 --version
   ```
   If it prints something like `Python 3.11.5`, you're good.

### Windows users

1. Open a browser and go to https://www.python.org/downloads/, click "Download Python 3.x.x".
2. Double-click the downloaded `.exe`. **⚠️ Important: at the bottom of the installer window, check the box "Add Python to PATH"** before clicking "Install Now".
3. After installation, press `Win + R`, type `cmd`, and press Enter to open Command Prompt.
4. Verify by running:
   ```bash
   python --version
   ```
   A version number means it worked.

> **Note:** On Mac, the commands are usually `python3` and `pip3`. On Windows, they're usually `python` and `pip`. This guide uses the Mac form (`python3`); Windows users should mentally swap `python3` → `python` and `pip3` → `pip`.

---

## Step 2: Open a Terminal and Enter the Project Folder

1. Open Terminal (Mac) or Command Prompt (Windows).
2. Type `cd ` (note the **space** after `cd`), then **drag the entire `Bond-Biographies-Generator` folder into the terminal window**. The path will be auto-filled. For example:
   ```bash
   cd /Users/yourname/Desktop/Bond-Biographies-Generator
   ```
3. Press Enter. If no error appears, you're now inside the project folder.
4. Type `ls` (Mac) or `dir` (Windows) and press Enter. You should see `bond_biography_agent.py`, `README.md`, etc. — confirming you're in the right place.

---

## Step 3: Install the Required Python Packages

Python on its own only ships with basic functionality; data analysis and plotting require extra "packages". All dependencies are pinned in `requirements.txt`.

**With your terminal inside the project folder** (see Step 2), run:

```bash
pip3 install -r requirements.txt
```

This downloads and installs everything automatically. The first install can take several minutes — you'll see scrolling download progress, which is normal.

You're done when you see something like `Successfully installed ...`. If you hit a red `ERROR`, see [Troubleshooting](#troubleshooting) below.

---

## Step 4: Generate a Bond Chapter Notebook

The main program `bond_biography_agent.py` offers several modes. **Stay in the terminal** (still inside the project folder) and try one of these.

### Mode A: Interactive mode (recommended for newcomers)

```bash
python3 bond_biography_agent.py --interactive
```

The program walks you through it step by step: it lists bond categories, asks you which bond ID to generate, and produces an `.ipynb` notebook file.

### Mode B: Generate by bond ID

If you already know the ID you want (e.g. `20044` is Louisiana Six Per Cent Stock):

```bash
python3 bond_biography_agent.py --bond-id 20044
```

### Mode C: Search by name

```bash
python3 bond_biography_agent.py --search "Louisiana"
```

This lists every bond whose name matches "Louisiana", and you can then use Mode B to generate by ID.

To search and immediately generate the first match:

```bash
python3 bond_biography_agent.py --search "Louisiana" --generate-first
```

### Mode D: List all bond categories

Not sure what's available? Browse the categories first:

```bash
python3 bond_biography_agent.py --list-categories
```

### Custom output filename

By default the file is named like `chapter_20044_xxx.ipynb`. To pick your own name:

```bash
python3 bond_biography_agent.py --bond-id 20044 --output my_chapter.ipynb
```

A successful run drops a new `.ipynb` file into the project folder.

---

## Step 5: Open the Generated Notebook

`.ipynb` is the Jupyter Notebook format. Open it with Jupyter or VS Code.

### Option 1: Jupyter (simplest)

In the terminal:

```bash
jupyter notebook
```

A browser tab opens with a file listing. Click your `.ipynb` file to open it. Inside the notebook, press `Shift + Enter` to run cells one at a time, or use the menu **Cell → Run All** to execute everything at once.

### Option 2: VS Code

1. Install VS Code: https://code.visualstudio.com/
2. Open VS Code, then install two extensions: search for "Python" and "Jupyter" and click Install on each.
3. Open the `Bond-Biographies-Generator` folder in VS Code, double-click your `.ipynb` file, and click "Run All" in the top toolbar.

---

## About the `enhanced_chapters` Folder

The 5 notebooks in `enhanced_chapters/` are **sample chapters that were generated by this tool and then manually polished**. They show what a complete, publication-ready bond biography looks like, including:

- Auto-generated charts and statistical analysis (produced by `bond_biography_agent.py`)
- Hand-written historical narrative, contextual interpretation, and bibliographic references

### Recommended workflow

1. **Study the template:** open [chapter_20044_Louisiana_Six_Per_Cent_Stock_enhanced.ipynb](enhanced_chapters/chapter_20044_Louisiana_Six_Per_Cent_Stock_enhanced.ipynb) (the ★ reference template) to see what a finished chapter looks like.
2. **Generate a new chapter:** use `bond_biography_agent.py` to produce a raw notebook for a bond you're interested in. The auto-generated draft contains `<!-- ENRICH: ... -->` markers that flag where qualitative narrative is needed.
3. **Polish from the raw version:** treat the auto-generated notebook as your starting point. Following the writing style in `enhanced_chapters/`, fill in historical narrative and citations to gradually refine it into a final chapter.

> In short: `enhanced_chapters/` is the "reference answer", `bond_biography_agent.py` produces the "rough draft", and the final product is "draft + manual polish".

---

## Troubleshooting

**Q1: `pip3 install` says `command not found`?**
Python isn't installed correctly or isn't on your system PATH. Windows users: reinstall Python and make sure "Add Python to PATH" is checked. Mac users: try `python3 -m pip install -r requirements.txt` instead.

**Q2: Error `No module named 'tables'` or `'openpyxl'`?**
Install the missing package directly:
```bash
pip3 install tables
pip3 install openpyxl
```

**Q3: Charts don't display in Jupyter?**
Add this line at the top of the first code cell, then re-run:
```python
%matplotlib inline
```

**Q4: Running `python3 bond_biography_agent.py ...` says it can't find a data file?**
Make sure your terminal's current directory is the `Bond-Biographies-Generator/` folder (see Step 2). If you're in the wrong directory, the program won't find the `data/` subfolder.

**Q5: Want to see every command-line option the program supports?**
```bash
python3 bond_biography_agent.py --help
```

---

## Quick Start (Experienced Users)

```bash
cd Bond-Biographies-Generator
pip install -r requirements.txt
python bond_biography_agent.py --bond-id 20044            # generate by ID
python bond_biography_agent.py --search "Liberty"         # search by name
python bond_biography_agent.py --interactive              # interactive mode
jupyter notebook                                          # open the .ipynb
```

Data source: Payne, Szoke, Hall & Sargent, *Quarterly Journal of Economics* (2025). Covers 2,857 U.S. federal bond issues, 1776–1960.

---

## Data corrections log

- **4 October 2026.** Two `BondList` fields corrected in both `BondList.csv` and `BondDF.h5`:
  - ID 20133 (Panama Canal Loan, Series 1908), `Price Sold`: 1.0299 → 1.02436. The 1908 series sold at 102.436 (Treasury Department, *Information Respecting United States Bonds*, 1915, p. 17); 102.99 was the November 1907 sale of Series 1906 bonds.
  - ID 20171 (Victory Liberty Loan 3¾%), `Redeemable After Date`: 1922-12-15 → 1922-06-15. The 3¾% notes were redeemed on June 15, 1922; the quantity series ends in May 1922.
- `BondDF.h5` was repacked with its original blosc compression. `BondPrice` and `BondQuant` are unchanged.
- Chapters that plot the four one-month prints flagged as artifacts (Loan of 1848, Dec 1859; Panama 2s of 1908, Dec 1919; Victory 4¾s, Jan 1920; Second Liberty 4s, May 1920) drop those prints in their data-loading cell (`ARTIFACT_PRINTS`). The database itself still contains them.
