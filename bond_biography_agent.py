#!/usr/bin/env python3
"""
Bond Biography Agent (Enhanced)
================================
Automatically generates comprehensive bond biography chapters as Jupyter notebooks.

Uses the Hall-Payne-Sargent US Federal Bond Database (2,857 issues, 1776-1960)
to extract bond features, perform advanced price/quantity analysis, detect
significant events, find related bonds, and produce richly formatted notebook
chapters with data-driven narrative.

Usage:
    python bond_biography_agent.py --bond-id 20044
    python bond_biography_agent.py --search "Louisiana"
    python bond_biography_agent.py --list-categories
    python bond_biography_agent.py --interactive

Requirements:
    pip install pandas numpy matplotlib nbformat tables
"""

import argparse
import sys
import pandas as pd
import numpy as np
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from pathlib import Path
from datetime import datetime


# ─── Historical Knowledge Base ─────────────────────────────────────────────────

HISTORICAL_EVENTS = [
    # Wars
    {"start": "1775-04-19", "end": "1783-09-03", "name": "American Revolution", "category": "war"},
    {"start": "1798-07-07", "end": "1800-09-30", "name": "Quasi-War with France", "category": "war"},
    {"start": "1801-05-10", "end": "1805-06-10", "name": "First Barbary War", "category": "war"},
    {"start": "1812-06-18", "end": "1815-02-18", "name": "War of 1812", "category": "war"},
    {"start": "1846-04-25", "end": "1848-02-02", "name": "Mexican-American War", "category": "war"},
    {"start": "1861-04-12", "end": "1865-04-09", "name": "Civil War", "category": "war"},
    {"start": "1898-04-25", "end": "1898-08-12", "name": "Spanish-American War", "category": "war"},
    {"start": "1917-04-06", "end": "1918-11-11", "name": "World War I (US participation)", "category": "war"},
    {"start": "1941-12-07", "end": "1945-09-02", "name": "World War II (US participation)", "category": "war"},
    # Financial Crises
    {"start": "1792-03-01", "end": "1792-04-30", "name": "Panic of 1792", "category": "crisis"},
    {"start": "1796-01-01", "end": "1797-12-31", "name": "Panic of 1796-97", "category": "crisis"},
    {"start": "1819-01-01", "end": "1821-12-31", "name": "Panic of 1819", "category": "crisis"},
    {"start": "1837-05-10", "end": "1843-12-31", "name": "Panic of 1837", "category": "crisis"},
    {"start": "1857-08-24", "end": "1858-12-31", "name": "Panic of 1857", "category": "crisis"},
    {"start": "1873-09-18", "end": "1879-03-01", "name": "Panic of 1873 / Long Depression", "category": "crisis"},
    {"start": "1893-05-05", "end": "1897-06-01", "name": "Panic of 1893", "category": "crisis"},
    {"start": "1907-10-01", "end": "1908-02-01", "name": "Panic of 1907", "category": "crisis"},
    {"start": "1920-01-01", "end": "1921-07-01", "name": "Depression of 1920-21", "category": "crisis"},
    {"start": "1929-10-29", "end": "1933-03-01", "name": "Great Depression onset", "category": "crisis"},
    # Key Legislation & Fiscal Events
    {"start": "1789-09-02", "end": "1789-09-02", "name": "Treasury Department established", "category": "legislation"},
    {"start": "1790-08-04", "end": "1790-08-04", "name": "Hamilton's Funding Act", "category": "legislation"},
    {"start": "1791-02-25", "end": "1791-02-25", "name": "First Bank of the US chartered", "category": "legislation"},
    {"start": "1803-04-30", "end": "1803-04-30", "name": "Louisiana Purchase Treaty", "category": "legislation"},
    {"start": "1811-03-03", "end": "1811-03-03", "name": "First Bank charter expires", "category": "legislation"},
    {"start": "1816-04-10", "end": "1816-04-10", "name": "Second Bank of the US chartered", "category": "legislation"},
    {"start": "1836-03-03", "end": "1836-03-03", "name": "Second Bank charter expires", "category": "legislation"},
    {"start": "1862-02-25", "end": "1862-02-25", "name": "Legal Tender Act (greenbacks)", "category": "legislation"},
    {"start": "1862-07-01", "end": "1862-07-01", "name": "Pacific Railway Act", "category": "legislation"},
    {"start": "1863-02-25", "end": "1863-02-25", "name": "National Banking Act", "category": "legislation"},
    {"start": "1864-06-03", "end": "1864-06-03", "name": "National Banking Act (revised)", "category": "legislation"},
    {"start": "1869-03-18", "end": "1869-03-18", "name": "Public Credit Act", "category": "legislation"},
    {"start": "1875-01-14", "end": "1875-01-14", "name": "Specie Payment Resumption Act", "category": "legislation"},
    {"start": "1879-01-01", "end": "1879-01-01", "name": "Resumption of specie payments", "category": "monetary"},
    {"start": "1900-03-14", "end": "1900-03-14", "name": "Gold Standard Act", "category": "legislation"},
    {"start": "1913-12-23", "end": "1913-12-23", "name": "Federal Reserve Act", "category": "legislation"},
    {"start": "1917-04-24", "end": "1917-04-24", "name": "First Liberty Loan Act", "category": "legislation"},
    {"start": "1933-04-05", "end": "1933-04-05", "name": "Gold confiscation (Executive Order 6102)", "category": "monetary"},
    {"start": "1934-01-30", "end": "1934-01-30", "name": "Gold Reserve Act", "category": "monetary"},
    # Major Events
    {"start": "1803-12-20", "end": "1803-12-20", "name": "Louisiana Territory transferred to US", "category": "other"},
    {"start": "1814-08-24", "end": "1814-08-24", "name": "British burn Washington, D.C.", "category": "other"},
    {"start": "1814-12-24", "end": "1814-12-24", "name": "Treaty of Ghent (War of 1812 ends)", "category": "other"},
    {"start": "1848-01-24", "end": "1848-01-24", "name": "California Gold Rush begins", "category": "other"},
    {"start": "1861-04-12", "end": "1861-04-12", "name": "Fort Sumter attacked", "category": "other"},
    {"start": "1863-07-01", "end": "1863-07-03", "name": "Battle of Gettysburg", "category": "other"},
    {"start": "1865-04-14", "end": "1865-04-14", "name": "Lincoln assassinated", "category": "other"},
    {"start": "1869-05-10", "end": "1869-05-10", "name": "Transcontinental Railroad completed", "category": "other"},
    {"start": "1869-09-24", "end": "1869-09-24", "name": "Black Friday gold panic", "category": "crisis"},
]

LITERATURE_MAP = {
    "always": [
        "Payne, J., Szoke, A., Hall, G. & Sargent, T. (2025). *Quarterly Journal of Economics*.",
        "Bayley, R. A. (1881). *The National Loans of the United States, From July 4, 1776 to June 30, 1880*.",
    ],
    "period": {
        (1776, 1815): [
            "Dewey, D. R. (1918). *Financial History of the United States*. Longmans, Green and Co.",
            "Perkins, E. (1994). *American Public Finance and Financial Services, 1700-1815*. Ohio State University Press.",
        ],
        (1815, 1870): [
            "Dewey, D. R. (1918). *Financial History of the United States*.",
            "Studenski, P. & Krooss, H. E. (1952). *Financial History of the United States*. McGraw-Hill.",
        ],
        (1860, 1920): [
            "Friedman, M. & Schwartz, A. J. (1963). *A Monetary History of the United States, 1867-1960*. Princeton University Press.",
            "Studenski, P. & Krooss, H. E. (1952). *Financial History of the United States*. McGraw-Hill.",
        ],
        (1917, 1945): [
            "Rockoff, H. (2012). *America's Economic Way of War*. Cambridge University Press.",
            "Kang, S. W. & Rockoff, H. (2015). 'Capitalizing Patriotism: The Liberty Loans of World War I.' *Financial History Review*, 22(1): 45-78.",
        ],
    },
}


# ─── Historical Context Helpers ────────────────────────────────────────────────

def _parse_date(s):
    """Safely parse a date string."""
    try:
        return pd.Timestamp(s)
    except Exception:
        return pd.NaT


def get_overlapping_events(start_date, end_date):
    """Find historical events that overlap with a bond's lifetime."""
    if pd.isna(start_date) or pd.isna(end_date):
        if pd.isna(start_date) and pd.isna(end_date):
            return []
        # Use whichever date is available with a 20-year window
        anchor = start_date if pd.notna(start_date) else end_date
        start_date = anchor - pd.DateOffset(years=1)
        end_date = anchor + pd.DateOffset(years=20)

    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)
    results = []
    for evt in HISTORICAL_EVENTS:
        evt_start = _parse_date(evt["start"])
        evt_end = _parse_date(evt["end"])
        if pd.isna(evt_start) or pd.isna(evt_end):
            continue
        if evt_start <= end_ts and evt_end >= start_ts:
            results.append(evt)
    return sorted(results, key=lambda e: _parse_date(e["start"]))


def get_era_description(start_date, end_date):
    """Generate a human-readable description of the bond's era."""
    events = get_overlapping_events(start_date, end_date)
    if not events:
        return "a period in American history"

    wars = [e["name"] for e in events if e["category"] == "war"]
    crises = [e["name"] for e in events if e["category"] == "crisis"]
    legislation = [e["name"] for e in events if e["category"] == "legislation"]

    parts = []
    if wars:
        parts.append("the " + ", ".join(wars[:2]))
    if crises:
        parts.append("the " + ", ".join(crises[:2]))
    if not parts and legislation:
        parts.append("significant fiscal legislation including " + legislation[0])

    if not parts:
        return "a transformative period in American fiscal history"
    return " and ".join(parts[:2])


def suggest_references(bond_info):
    """Suggest relevant references based on bond category and era."""
    refs = list(LITERATURE_MAP["always"])

    issue_year = None
    if pd.notna(bond_info.get("first_issue_date")) and bond_info["first_issue_date"] != "N/A":
        try:
            issue_year = pd.Timestamp(bond_info["first_issue_date"]).year
        except Exception:
            pass

    if issue_year:
        for (y1, y2), period_refs in LITERATURE_MAP["period"].items():
            if y1 <= issue_year <= y2:
                for r in period_refs:
                    if r not in refs:
                        refs.append(r)
    return refs


# ─── Data Loading ──────────────────────────────────────────────────────────────

DATA_DIR = Path(__file__).parent / "data"


def load_bond_database():
    """Load the bond database from CSV files."""
    bond_list_path = DATA_DIR / "BondList.csv"
    bond_price_path = DATA_DIR / "BondPrice.csv"
    bond_quant_path = DATA_DIR / "BondQuant.csv"

    if not bond_list_path.exists():
        print(f"Error: BondList.csv not found at {bond_list_path}")
        sys.exit(1)

    colsfinaldates = [
        "Authorizing Act Date", "First Issue Date", "First Redemption Date",
        "Final Redemption Date", "Redeemable After Date", "Payable Date"
    ]
    BondList = pd.read_csv(bond_list_path, index_col=0)
    for col in colsfinaldates:
        if col in BondList.columns:
            BondList[col] = pd.to_datetime(BondList[col], errors='coerce')

    BondPrice = pd.read_csv(bond_price_path)
    BondPrice = BondPrice.set_index(['L1 ID', 'Series'], drop=True).transpose()
    BondPrice.index = pd.to_datetime(BondPrice.index)

    BondQuant = pd.read_csv(bond_quant_path)
    BondQuant = BondQuant.set_index(['L1 ID', 'Series'], drop=True).transpose()
    BondQuant.index = pd.to_datetime(BondQuant.index)

    return BondList, BondPrice, BondQuant


def load_bond_database_h5():
    """Load from HDF5 if available (faster)."""
    h5_path = DATA_DIR / "BondDF.h5"
    if not h5_path.exists():
        return load_bond_database()
    store = pd.HDFStore(str(h5_path), mode="r")
    BondList = store["BondList"]
    BondQuant = store["BondQuant"]
    BondPrice = store["BondPrice"]
    store.close()
    return BondList, BondPrice.transpose(), BondQuant.transpose()


# ─── Basic Bond Analysis ──────────────────────────────────────────────────────

def get_bond_info(BondList, bond_id):
    """Extract comprehensive bond information."""
    if bond_id not in BondList.index:
        return None
    row = BondList.loc[bond_id]
    return {
        'id': bond_id,
        'name': row.get("Treasury's Name Of Issue", "Unknown"),
        'category_l1': row.get('Category L1', 'N/A'),
        'category_l2': row.get('Category L2', 'N/A'),
        'category_l3': row.get('Category L3', 'N/A'),
        'authorizing_act': row.get('Authorizing Act', 'N/A'),
        'authorizing_act_date': row.get('Authorizing Act Date', 'N/A'),
        'first_issue_date': row.get('First Issue Date', 'N/A'),
        'first_redemption_date': row.get('First Redemption Date', 'N/A'),
        'final_redemption_date': row.get('Final Redemption Date', 'N/A'),
        'redeemable_after_date': row.get('Redeemable After Date', 'N/A'),
        'term': row.get('Term Of Loan', 'N/A'),
        'coupon_rate': row.get('Coupon Rate', 'N/A'),
        'coupons_per_year': row.get('Coupons Per Year', 'N/A'),
        'callable': 'Yes' if row.get('Callable', 0) == 1.0 else 'No',
        'coin': 'Yes' if row.get('Coin', 0) > 0 else 'No',
        'authorized_amount': row.get('Authorized Amount', 'N/A'),
        'price_sold': row.get('Price Sold', 'N/A'),
    }


def get_price_data(BondPrice_T, bond_id):
    """Get price time series for a bond."""
    try:
        s = BondPrice_T.loc[(bond_id, 'Average')]
        return pd.to_numeric(s, errors='coerce').dropna()
    except KeyError:
        return pd.Series(dtype=float)


def get_quantity_data(BondQuant_T, bond_id, series_type='Public Holdings'):
    """Get quantity time series for a bond."""
    try:
        s = BondQuant_T.loc[(bond_id, series_type)]
        return s[s.notna()]
    except KeyError:
        # Fall back to Total Outstanding
        try:
            s = BondQuant_T.loc[(bond_id, 'Total Outstanding')]
            return s[s.notna()]
        except KeyError:
            return pd.Series(dtype=float)


# ─── Advanced Analysis ─────────────────────────────────────────────────────────

def compute_price_statistics(price_series):
    """Compute summary statistics for bond prices."""
    if len(price_series) == 0:
        return {}
    return {
        'mean_price': round(float(price_series.mean()), 2),
        'min_price': round(float(price_series.min()), 2),
        'max_price': round(float(price_series.max()), 2),
        'std_price': round(float(price_series.std()), 2),
        'first_price': round(float(price_series.iloc[0]), 2),
        'last_price': round(float(price_series.iloc[-1]), 2),
        'first_date': str(price_series.index[0].date()),
        'last_date': str(price_series.index[-1].date()),
        'n_observations': len(price_series),
    }


def compute_period_statistics(price_series, bond_info):
    """Break price history into lifecycle phases and compute stats for each."""
    if len(price_series) == 0:
        return []

    periods = []
    breakpoints = []
    issue = bond_info.get('first_issue_date')
    first_red = bond_info.get('first_redemption_date')
    final_red = bond_info.get('final_redemption_date')

    if pd.notna(issue) and issue != 'N/A':
        breakpoints.append(("Issue", pd.Timestamp(issue)))
    if pd.notna(first_red) and first_red != 'N/A':
        breakpoints.append(("First Redemption", pd.Timestamp(first_red)))
    if pd.notna(final_red) and final_red != 'N/A':
        breakpoints.append(("Final Redemption", pd.Timestamp(final_red)))

    breakpoints.sort(key=lambda x: x[1])
    # Add series boundaries
    all_points = [(None, price_series.index[0])] + breakpoints + [(None, price_series.index[-1])]

    for i in range(len(all_points) - 1):
        start_label, start_date = all_points[i]
        end_label, end_date = all_points[i + 1]
        segment = price_series[(price_series.index >= start_date) & (price_series.index <= end_date)]
        if len(segment) < 2:
            continue
        label = f"{start_date.strftime('%Y-%m')} to {end_date.strftime('%Y-%m')}"
        if start_label and end_label:
            label = f"{start_label} to {end_label} ({label})"
        elif end_label:
            label = f"Start to {end_label} ({label})"
        elif start_label:
            label = f"{start_label} to End ({label})"

        periods.append({
            'period': label,
            'mean': round(float(segment.mean()), 2),
            'std': round(float(segment.std()), 2),
            'min': round(float(segment.min()), 2),
            'max': round(float(segment.max()), 2),
            'n_obs': len(segment),
        })
    return periods


def compute_volatility_analysis(price_series, window=12):
    """Compute rolling volatility and max drawdown."""
    if len(price_series) < window:
        return {}
    rolling_std = price_series.rolling(window=window).std().dropna()
    cummax = price_series.cummax()
    drawdown = (price_series - cummax) / cummax * 100
    max_dd = float(drawdown.min())
    max_dd_date = drawdown.idxmin()
    peak_date = price_series[:max_dd_date].idxmax()
    monthly_returns = price_series.pct_change().dropna() * 100

    return {
        'rolling_std': rolling_std,
        'max_drawdown_pct': round(max_dd, 2),
        'max_drawdown_peak': str(peak_date.date()),
        'max_drawdown_trough': str(max_dd_date.date()),
        'monthly_returns': monthly_returns,
        'avg_monthly_return': round(float(monthly_returns.mean()), 3),
    }


def detect_significant_events(price_series, quant_series, threshold_pct=5.0):
    """Detect months with abnormal price/quantity changes."""
    events = []
    if len(price_series) > 1:
        pct_change = price_series.pct_change().dropna() * 100
        for date, change in pct_change.items():
            if abs(change) >= threshold_pct:
                evt_type = "price_spike" if change > 0 else "price_drop"
                nearest = _find_nearest_historical_event(date)
                events.append({
                    'date': date,
                    'type': evt_type,
                    'magnitude': round(float(change), 2),
                    'value': round(float(price_series.loc[date]), 2),
                    'nearest_event': nearest,
                })

    if len(quant_series) > 1:
        q_numeric = pd.to_numeric(quant_series, errors='coerce').dropna()
        if len(q_numeric) > 1:
            q_change = q_numeric.pct_change().dropna() * 100
            for date, change in q_change.items():
                if abs(change) >= 20:
                    evt_type = "quantity_increase" if change > 0 else "quantity_decrease"
                    nearest = _find_nearest_historical_event(date)
                    events.append({
                        'date': date,
                        'type': evt_type,
                        'magnitude': round(float(change), 2),
                        'value': round(float(q_numeric.loc[date]), 2),
                        'nearest_event': nearest,
                    })
    return sorted(events, key=lambda e: e['date'])


def _find_nearest_historical_event(date, max_months=6):
    """Find the nearest historical event within max_months of a date."""
    date_ts = pd.Timestamp(date)
    best = None
    best_dist = pd.Timedelta(days=max_months * 31)
    for evt in HISTORICAL_EVENTS:
        evt_start = _parse_date(evt["start"])
        evt_end = _parse_date(evt["end"])
        if pd.isna(evt_start):
            continue
        # Distance to event start or end
        dist = min(abs(date_ts - evt_start), abs(date_ts - evt_end))
        if dist < best_dist:
            best_dist = dist
            best = evt["name"]
    return best


def compute_quantity_lifecycle(quant_series):
    """Analyze the quantity lifecycle of a bond."""
    if len(quant_series) == 0:
        return {}
    q = pd.to_numeric(quant_series, errors='coerce').dropna()
    if len(q) == 0:
        return {}
    peak_val = float(q.max())
    peak_date = q.idxmax()
    # Find when quantity first appears and last appears
    nonzero = q[q > 0]
    if len(nonzero) == 0:
        return {}
    return {
        'peak_outstanding': peak_val,
        'peak_outstanding_millions': round(peak_val / 1e6, 2),
        'peak_date': str(peak_date.date()),
        'first_date': str(nonzero.index[0].date()),
        'last_date': str(nonzero.index[-1].date()),
        'total_months': len(nonzero),
    }


def compute_ytm_approximation(price, coupon_rate, years_to_maturity):
    """Approximate yield to maturity using the standard formula."""
    if any(pd.isna(x) or x == 'N/A' for x in [price, coupon_rate, years_to_maturity]):
        return None
    try:
        price = float(price)
        coupon_rate = float(coupon_rate)
        n = float(years_to_maturity)
        if n <= 0 or price <= 0:
            return None
        C = coupon_rate  # annual coupon payment per $100 face
        F = 100.0
        ytm = (C + (F - price) / n) / ((F + price) / 2) * 100
        return round(ytm, 3)
    except (ValueError, TypeError, ZeroDivisionError):
        return None


# ─── Related Bonds Discovery ──────────────────────────────────────────────────

def find_related_bonds(BondList, bond_info, max_results=5):
    """Find related bonds by category, era, and coupon rate."""
    bond_id = bond_info['id']
    results = {'same_category': [], 'same_era': [], 'same_coupon': []}
    seen_ids = {bond_id}

    # Same Category L3
    cat = bond_info.get('category_l3', 'N/A')
    if cat != 'N/A':
        mask = (BondList['Category L3'] == cat) & (BondList.index != bond_id)
        matches = BondList[mask].head(max_results)
        for idx, row in matches.iterrows():
            seen_ids.add(idx)
            results['same_category'].append({
                'id': idx,
                'name': row.get("Treasury's Name Of Issue", "Unknown"),
                'first_issue_date': row.get('First Issue Date', 'N/A'),
                'coupon_rate': row.get('Coupon Rate', 'N/A'),
            })

    # Same era (within 5 years)
    issue_date = bond_info.get('first_issue_date')
    if pd.notna(issue_date) and issue_date != 'N/A':
        issue_ts = pd.Timestamp(issue_date)
        date_col = BondList['First Issue Date']
        mask = (
            (date_col >= issue_ts - pd.DateOffset(years=5)) &
            (date_col <= issue_ts + pd.DateOffset(years=5)) &
            (~BondList.index.isin(seen_ids))
        )
        matches = BondList[mask].head(max_results)
        for idx, row in matches.iterrows():
            seen_ids.add(idx)
            results['same_era'].append({
                'id': idx,
                'name': row.get("Treasury's Name Of Issue", "Unknown"),
                'first_issue_date': row.get('First Issue Date', 'N/A'),
                'coupon_rate': row.get('Coupon Rate', 'N/A'),
            })

    # Same coupon rate
    coupon = bond_info.get('coupon_rate')
    if pd.notna(coupon) and coupon != 'N/A':
        mask = (BondList['Coupon Rate'] == coupon) & (~BondList.index.isin(seen_ids))
        matches = BondList[mask].head(max_results)
        for idx, row in matches.iterrows():
            results['same_coupon'].append({
                'id': idx,
                'name': row.get("Treasury's Name Of Issue", "Unknown"),
                'first_issue_date': row.get('First Issue Date', 'N/A'),
                'coupon_rate': row.get('Coupon Rate', 'N/A'),
            })

    return results


# ─── Formatting Helpers ────────────────────────────────────────────────────────

def format_date(val):
    """Format a date value for display."""
    if pd.isna(val) or val == 'N/A':
        return 'N/A'
    if hasattr(val, 'strftime'):
        return val.strftime('%B %d, %Y')
    return str(val)


def format_amount(val):
    """Format a dollar amount for display."""
    if pd.isna(val) or val == 'N/A':
        return 'N/A'
    try:
        val = float(val)
        if val >= 1e9:
            return f"${val/1e9:.2f} billion"
        if val >= 1e6:
            return f"${val/1e6:.2f} million"
        if val >= 1e3:
            return f"${val/1e3:,.0f}"
        return f"${val:,.0f}"
    except (ValueError, TypeError):
        return str(val)


# ─── Notebook Generation (Cell Builders) ───────────────────────────────────────

def build_title_cells(bond_info):
    """Build title and import cells."""
    bond_name = bond_info['name']
    bond_id = bond_info['id']
    return [
        new_markdown_cell(
            f"# Bond Biography: {bond_name}\n\n"
            f"*Generated from the Hall-Payne-Sargent US Federal Bond Database (2,857 issues, 1776-1960)*\n\n"
            f"**Bond ID (L1):** {bond_id}  \n"
            f"**Category:** {bond_info['category_l1']} > {bond_info['category_l2']} > {bond_info['category_l3']}\n\n---"
        ),
        new_code_cell(
            "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n"
            "import matplotlib.patches as mpatches\nimport datetime\nimport warnings\n"
            "warnings.filterwarnings('ignore')\n\n"
            "plt.style.use('seaborn-v0_8-whitegrid')\n"
            "plt.rcParams.update({'figure.figsize': (12, 6), 'font.size': 12,\n"
            "    'axes.titlesize': 14, 'axes.labelsize': 12})\n\n"
            "# Load the bond database\n"
            "store = pd.HDFStore('data/BondDF.h5', mode='r')\n"
            "BondList = store['BondList']\nBondQuant = store['BondQuant']\nBondPrice = store['BondPrice']\nstore.close()\n\n"
            "BondQuant_T = BondQuant.transpose()\nBondPrice_T = BondPrice.transpose()\n\n"
            f"bond_id = {bond_id}\n"
            f"print(f'Loaded data for: {bond_name} (ID: {bond_id})')"
        ),
    ]


def build_overview_cells(bond_info, era_desc, price_stats, quant_lifecycle):
    """Build overview with auto-filled narrative."""
    bond_name = bond_info['name']
    issue_str = format_date(bond_info['first_issue_date'])
    red_str = format_date(bond_info['final_redemption_date'])
    act = bond_info['authorizing_act']
    coupon = bond_info['coupon_rate']
    amount = format_amount(bond_info['authorized_amount'])

    # Build substantive overview paragraph
    para1 = f"The **{bond_name}** was authorized under the {act}."
    if issue_str != 'N/A':
        para1 += f" It was first issued on {issue_str}"
    if coupon != 'N/A':
        para1 += f" with a coupon rate of {coupon}%"
    if amount != 'N/A':
        para1 += f", raising {amount}"
    para1 += "."
    if red_str != 'N/A':
        para1 += f" Final redemption occurred on {red_str}."
    para1 += f" The bond was active during {era_desc}."

    # Build data-driven paragraph
    para2 = ""
    if price_stats:
        para2 = (
            f"\nDuring its lifetime on the secondary market, the bond's average price was "
            f"${price_stats['mean_price']}, ranging from ${price_stats['min_price']} to "
            f"${price_stats['max_price']} (based on {price_stats['n_observations']} monthly observations "
            f"from {price_stats['first_date']} to {price_stats['last_date']})."
        )
    if quant_lifecycle:
        para2 += (
            f" Peak outstanding reached {format_amount(quant_lifecycle['peak_outstanding'])} "
            f"on {quant_lifecycle['peak_date']}."
        )

    enrich = (
        "\n\n<!-- ENRICH: Add 1-2 paragraphs on the political motivations behind this bond's "
        "issuance, the key figures involved, and what makes this bond's story distinctive "
        "in the broader arc of U.S. fiscal history. -->"
    )
    return [new_markdown_cell(f"## Overview\n\n{para1}{para2}{enrich}")]


def build_historical_context_cells(bond_info, overlapping_events):
    """Build historical context with auto-detected event timeline."""
    if not overlapping_events:
        return [new_markdown_cell(
            "## Historical Context\n\n"
            "<!-- ENRICH: Provide historical context for this bond's issuance. What wars, crises, "
            "or infrastructure projects motivated the borrowing? -->"
        )]

    # Build timeline table
    rows = "| Date | Event | Category |\n|------|-------|----------|\n"
    for evt in overlapping_events:
        start = evt['start'][:10]
        end = evt['end'][:10]
        date_str = start if start == end else f"{start} to {end}"
        rows += f"| {date_str} | {evt['name']} | {evt['category'].title()} |\n"

    wars = [e['name'] for e in overlapping_events if e['category'] == 'war']
    crises = [e['name'] for e in overlapping_events if e['category'] == 'crisis']
    legislation = [e['name'] for e in overlapping_events if e['category'] == 'legislation']

    context_notes = ""
    if wars:
        context_notes += f"\nThe bond's lifetime overlapped with: **{', '.join(wars)}**."
    if crises:
        context_notes += f" Financial crises during this period included: **{', '.join(crises)}**."
    if legislation:
        context_notes += f" Key legislation: **{', '.join(legislation[:4])}**."

    enrich_parts = []
    for evt in overlapping_events:
        if evt['category'] in ('war', 'crisis'):
            enrich_parts.append(f"- How did the {evt['name']} affect this bond's price and demand?")

    enrich = "\n\n<!-- ENRICH: Expand on the historical context. Specifically:\n"
    enrich += "\n".join(enrich_parts[:5]) if enrich_parts else "- What was the fiscal/political backdrop for this bond?"
    enrich += "\n-->"

    return [new_markdown_cell(
        f"## Historical Context\n\n"
        f"The following major events occurred during this bond's lifetime:\n\n{rows}"
        f"{context_notes}{enrich}"
    )]


def build_lifecycle_timeline_cells(bond_info, overlapping_events):
    """Build a lifecycle timeline visualization."""
    bond_id = bond_info['id']
    bond_name = bond_info['name']

    dates_code = ""
    date_fields = [
        ('authorizing_act_date', 'Authorization'),
        ('first_issue_date', 'First Issue'),
        ('first_redemption_date', 'First Redemption'),
        ('final_redemption_date', 'Final Redemption'),
    ]
    valid_dates = []
    for field, label in date_fields:
        val = bond_info.get(field)
        if pd.notna(val) and val != 'N/A':
            valid_dates.append((label, str(pd.Timestamp(val).date())))

    if len(valid_dates) < 2:
        return []

    events_for_plot = []
    for evt in overlapping_events[:6]:
        events_for_plot.append((evt['name'], evt['start'][:10], evt['category']))

    code = (
        "# Bond Lifecycle Timeline\n"
        "fig, ax = plt.subplots(figsize=(14, 4))\n\n"
        "# Key dates\n"
        f"dates = {valid_dates}\n"
        f"events = {events_for_plot}\n\n"
        "import matplotlib.dates as mdates\n"
        "from datetime import datetime\n\n"
        "# Plot bond lifetime bar\n"
        "d0 = datetime.strptime(dates[0][1], '%Y-%m-%d')\n"
        "d1 = datetime.strptime(dates[-1][1], '%Y-%m-%d')\n"
        "ax.barh(0, (d1 - d0).days, left=mdates.date2num(d0), height=0.3, \n"
        "        color='#1f77b4', alpha=0.4, label='Bond Lifetime')\n\n"
        "# Mark key dates\n"
        "for label, date_str in dates:\n"
        "    d = datetime.strptime(date_str, '%Y-%m-%d')\n"
        "    ax.plot(mdates.date2num(d), 0, 'D', color='#1f77b4', markersize=10)\n"
        "    ax.annotate(f'{label}\\n{date_str}', (mdates.date2num(d), 0.25),\n"
        "               ha='center', va='bottom', fontsize=8, rotation=30)\n\n"
        "# Mark historical events\n"
        "colors = {'war': '#e74c3c', 'crisis': '#9b59b6', 'legislation': '#2ecc71', 'other': '#95a5a6', 'monetary': '#f39c12'}\n"
        "for name, date_str, cat in events:\n"
        "    d = datetime.strptime(date_str, '%Y-%m-%d')\n"
        "    ax.axvline(mdates.date2num(d), color=colors.get(cat, 'gray'), alpha=0.5, linestyle='--')\n"
        "    ax.annotate(name, (mdates.date2num(d), -0.25), ha='center', va='top',\n"
        "               fontsize=7, rotation=45, color=colors.get(cat, 'gray'))\n\n"
        "ax.set_yticks([])\n"
        "ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))\n"
        f"ax.set_title('{bond_name} — Lifecycle Timeline')\n"
        "ax.set_ylim(-1, 1)\n"
        "plt.tight_layout()\nplt.show()"
    )
    return [new_code_cell(code)]


def build_bond_features_cells(bond_info):
    """Build bond features table and code cell."""
    bond_id = bond_info['id']
    coupon_str = f"{bond_info['coupon_rate']}%" if bond_info['coupon_rate'] != 'N/A' else 'N/A'
    freq_str = f"{bond_info['coupons_per_year']} times/year" if bond_info['coupons_per_year'] != 'N/A' else 'N/A'

    table = (
        f"## Bond Features\n\n"
        f"| Feature | Detail |\n|---------|--------|\n"
        f"| **Name** | {bond_info['name']} |\n"
        f"| **Authorizing Act** | {bond_info['authorizing_act']} |\n"
        f"| **Authorization Date** | {format_date(bond_info['authorizing_act_date'])} |\n"
        f"| **First Issue Date** | {format_date(bond_info['first_issue_date'])} |\n"
        f"| **Term** | {bond_info['term']} |\n"
        f"| **First Redemption** | {format_date(bond_info['first_redemption_date'])} |\n"
        f"| **Final Redemption** | {format_date(bond_info['final_redemption_date'])} |\n"
        f"| **Coupon Rate** | {coupon_str} |\n"
        f"| **Payment Frequency** | {freq_str} |\n"
        f"| **Callable** | {bond_info['callable']} |\n"
        f"| **Payable in Coin** | {bond_info['coin']} |\n"
        f"| **Authorized Amount** | {format_amount(bond_info['authorized_amount'])} |\n"
        f"| **Price Sold** | {bond_info['price_sold']} |\n"
    )

    code = (
        "# Display full bond features from database\n"
        f"row = BondList.loc[{bond_id}]\n"
        "display_cols = [\n"
        "    \"Treasury's Name Of Issue\", 'Authorizing Act', 'Term Of Loan',\n"
        "    'First Issue Date', 'First Redemption Date', 'Final Redemption Date',\n"
        "    'Coupon Rate', 'Coupons Per Year', 'Callable', 'Coin',\n"
        "    'Authorized Amount', 'Price Sold'\n"
        "]\n"
        "print('Bond Features from Database:')\n"
        "print('=' * 55)\n"
        "for col in display_cols:\n"
        "    if col in row.index:\n"
        "        print(f'  {col:<30} {row[col]}')"
    )
    return [new_markdown_cell(table), new_code_cell(code)]


def build_quantity_cells(bond_info, quant_lifecycle, overlapping_events):
    """Build quantity analysis with auto-narrative."""
    bond_id = bond_info['id']
    bond_name = bond_info['name']

    # Narrative
    narrative = "## Bond Quantity Over Time\n\n"
    if quant_lifecycle:
        narrative += (
            f"The bond's outstanding quantity peaked at "
            f"**{format_amount(quant_lifecycle['peak_outstanding'])}** on "
            f"{quant_lifecycle['peak_date']}. Data spans from {quant_lifecycle['first_date']} "
            f"to {quant_lifecycle['last_date']} ({quant_lifecycle['total_months']} monthly observations).\n"
        )
    else:
        narrative += "The chart below shows the outstanding quantity over the bond's lifetime.\n"

    # Build event dict for annotations
    evt_lines = ""
    relevant_events = [e for e in overlapping_events if e['category'] in ('war', 'crisis', 'legislation')][:4]
    if relevant_events:
        safe_names = [e['name'][:25].replace("'", "\\'") for e in relevant_events]
        evt_entries = ", ".join([f"'{e['start'][:10]}': '{safe_names[i]}'" for i, e in enumerate(relevant_events)])
        evt_lines = f"\nevents = {{{evt_entries}}}\nfor date_str, label in events.items():\n    d = pd.Timestamp(date_str)\n    ax.axvline(d, color='gray', alpha=0.4, linestyle='--')\n    ax.text(d, ax.get_ylim()[1]*0.97, label, rotation=90, va='top', ha='right', fontsize=8, alpha=0.7)\n"

    code = (
        "# Bond quantity over time\n"
        "fig, ax = plt.subplots(figsize=(12, 6))\n\n"
        f"for stype in ['Public Holdings', 'Total Outstanding']:\n"
        f"    try:\n"
        f"        s = BondQuant_T.loc[({bond_id}, stype)]\n"
        f"        s = s[s.notna()]\n"
        f"        if len(s) > 0:\n"
        f"            ax.plot(s.index, s.values / 1e6, marker='.', markersize=3, linewidth=1.5, label=stype)\n"
        f"    except KeyError:\n"
        f"        pass\n\n"
        f"ax.set_title('{bond_name} — Outstanding Quantity')\n"
        f"ax.set_xlabel('Date')\nax.set_ylabel('Amount ($ millions)')\n"
        f"ax.legend()\nax.grid(True, alpha=0.3)\n"
        f"{evt_lines}\n"
        f"plt.tight_layout()\nplt.show()"
    )

    enrich = (
        "\n\n<!-- ENRICH: Describe the quantity trends. What drove the issuance pattern? "
        "When and why did redemptions begin? Were bonds refinanced into other instruments? -->"
    )
    return [new_markdown_cell(narrative), new_code_cell(code), new_markdown_cell(f"### Quantity Analysis{enrich}")]


def build_price_cells(bond_info, price_stats, period_stats, significant_events, overlapping_events):
    """Build price analysis with annotations and dual-axis chart."""
    bond_id = bond_info['id']
    bond_name = bond_info['name']
    cells = []

    # Narrative with period statistics
    narrative = "## Secondary Market Prices\n\n"
    if price_stats:
        narrative += (
            f"**Overall Statistics ({price_stats['first_date']} to {price_stats['last_date']}):** "
            f"Mean ${price_stats['mean_price']}, Range ${price_stats['min_price']}–${price_stats['max_price']}, "
            f"Std Dev ${price_stats['std_price']}, {price_stats['n_observations']} observations.\n"
        )
    if period_stats:
        narrative += "\n**By Period:**\n\n| Period | Mean | Std | Min | Max | Obs |\n|--------|------|-----|-----|-----|-----|\n"
        for ps in period_stats:
            narrative += f"| {ps['period']} | ${ps['mean']} | ${ps['std']} | ${ps['min']} | ${ps['max']} | {ps['n_obs']} |\n"
    cells.append(new_markdown_cell(narrative))

    # Annotated price chart
    evt_lines = ""
    relevant_events = [e for e in overlapping_events if e['category'] in ('war', 'crisis')][:4]
    if relevant_events:
        safe_names = [e['name'][:25].replace("'", "\\'") for e in relevant_events]
        evt_entries = ", ".join([f"'{e['start'][:10]}': '{safe_names[i]}'" for i, e in enumerate(relevant_events)])
        evt_lines = f"\nevents = {{{evt_entries}}}\nfor date_str, label in events.items():\n    d = pd.Timestamp(date_str)\n    ax.axvline(d, color='gray', alpha=0.4, linestyle='--')\n    ax.text(d, ax.get_ylim()[1]*0.97, label, rotation=90, va='top', ha='right', fontsize=8, alpha=0.7)\n"

    code_price = (
        "# Annotated price chart\n"
        "fig, ax = plt.subplots(figsize=(12, 6))\n\n"
        f"s = BondPrice_T.loc[({bond_id}, 'Average')]\n"
        "s = pd.to_numeric(s, errors='coerce').dropna()\n\n"
        "if len(s) > 0:\n"
        "    ax.plot(s.index, s.values, marker='.', markersize=3, linewidth=1.5, color='#2ca02c')\n"
        "    ax.axhline(100, color='black', alpha=0.2, linestyle='--', label='Par ($100)')\n"
        f"    ax.set_title('{bond_name} — Secondary Market Price')\n"
        "    ax.set_xlabel('Date')\n    ax.set_ylabel('Price ($)')\n"
        f"    ax.legend()\n    ax.grid(True, alpha=0.3)\n"
        f"{evt_lines}\n"
        "plt.tight_layout()\nplt.show()"
    )
    cells.append(new_code_cell(code_price))

    # Dual-axis chart (price + quantity)
    code_dual = (
        "# Price and Quantity — dual-axis chart\n"
        "fig, ax1 = plt.subplots(figsize=(12, 6))\n\n"
        "# Quantity (left axis)\n"
        f"for stype in ['Public Holdings', 'Total Outstanding']:\n"
        f"    try:\n"
        f"        q = BondQuant_T.loc[({bond_id}, stype)]\n"
        f"        q = q[q.notna()]\n"
        f"        if len(q) > 0:\n"
        f"            ax1.plot(q.index, q.values / 1e6, color='#1f77b4', alpha=0.6, label=f'Quantity ({{stype}})')\n"
        f"            break\n"
        f"    except KeyError:\n        pass\n\n"
        "ax1.set_xlabel('Date')\nax1.set_ylabel('Quantity ($ millions)', color='#1f77b4')\n"
        "ax1.tick_params(axis='y', labelcolor='#1f77b4')\n\n"
        "# Price (right axis)\n"
        "ax2 = ax1.twinx()\n"
        f"p = BondPrice_T.loc[({bond_id}, 'Average')]\n"
        "p = pd.to_numeric(p, errors='coerce').dropna()\n"
        "if len(p) > 0:\n"
        "    ax2.plot(p.index, p.values, color='#2ca02c', marker='.', markersize=2, label='Price')\n"
        "    ax2.set_ylabel('Price ($)', color='#2ca02c')\n"
        "    ax2.tick_params(axis='y', labelcolor='#2ca02c')\n\n"
        f"ax1.set_title('{bond_name} — Price and Quantity')\n"
        "ax1.grid(True, alpha=0.3)\nfig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))\n"
        "plt.tight_layout()\nplt.show()"
    )
    cells.append(new_code_cell(code_dual))

    # Significant events narrative
    if significant_events:
        evt_text = "### Detected Price/Quantity Events\n\n"
        evt_text += "The following significant movements were auto-detected:\n\n"
        evt_text += "| Date | Type | Change | Nearest Historical Event |\n|------|------|--------|-------------------------|\n"
        for evt in significant_events[:10]:
            date_str = evt['date'].strftime('%Y-%m') if hasattr(evt['date'], 'strftime') else str(evt['date'])
            nearest = evt['nearest_event'] or 'None identified'
            evt_text += f"| {date_str} | {evt['type']} | {evt['magnitude']:+.1f}% | {nearest} |\n"
        evt_text += "\n<!-- ENRICH: Explain the causal relationships between these price movements and the historical events listed. -->"
        cells.append(new_markdown_cell(evt_text))
    else:
        cells.append(new_markdown_cell(
            "### Price Trends\n\n"
            "<!-- ENRICH: Analyze the price trends. What drove fluctuations? "
            "How did the bond trade relative to par? -->"
        ))

    return cells


def build_volatility_cells(bond_info, volatility_data):
    """Build volatility analysis section."""
    if not volatility_data:
        return []
    bond_id = bond_info['id']
    bond_name = bond_info['name']

    narrative = (
        f"## Price Volatility\n\n"
        f"**Maximum drawdown:** {volatility_data['max_drawdown_pct']:.1f}% "
        f"(from peak on {volatility_data['max_drawdown_peak']} to trough on {volatility_data['max_drawdown_trough']})\n\n"
        f"**Average monthly return:** {volatility_data['avg_monthly_return']:.3f}%\n\n"
        f"The chart below shows the 12-month rolling standard deviation of prices, "
        f"indicating periods of high and low price stability."
    )

    code = (
        "# Rolling volatility (12-month window)\n"
        f"p = BondPrice_T.loc[({bond_id}, 'Average')]\n"
        "p = pd.to_numeric(p, errors='coerce').dropna()\n\n"
        "if len(p) >= 12:\n"
        "    rolling_std = p.rolling(window=12).std().dropna()\n"
        "    fig, ax = plt.subplots(figsize=(12, 4))\n"
        "    ax.fill_between(rolling_std.index, rolling_std.values, alpha=0.4, color='#e74c3c')\n"
        "    ax.plot(rolling_std.index, rolling_std.values, color='#e74c3c', linewidth=1)\n"
        f"    ax.set_title('{bond_name} — 12-Month Rolling Price Volatility')\n"
        "    ax.set_xlabel('Date')\n    ax.set_ylabel('Std Dev ($)')\n"
        "    ax.grid(True, alpha=0.3)\n    plt.tight_layout()\n    plt.show()\n"
        "else:\n    print('Insufficient data for rolling volatility (need >= 12 observations)')"
    )
    return [new_markdown_cell(narrative), new_code_cell(code)]


def build_ytm_cells(bond_info):
    """Build yield-to-maturity analysis (conditional)."""
    coupon = bond_info.get('coupon_rate')
    final_red = bond_info.get('final_redemption_date')
    if pd.isna(coupon) or coupon == 'N/A' or pd.isna(final_red) or final_red == 'N/A':
        return []

    bond_id = bond_info['id']
    bond_name = bond_info['name']

    narrative = (
        f"## Approximate Yield to Maturity\n\n"
        f"Using the bond's coupon rate ({coupon}%) and remaining years to maturity at each observation, "
        f"the chart below shows an approximate YTM trajectory. Higher YTM indicates lower market confidence "
        f"or higher required returns; lower YTM indicates the opposite."
    )

    code = (
        "# Approximate Yield to Maturity\n"
        f"p = BondPrice_T.loc[({bond_id}, 'Average')]\n"
        "p = pd.to_numeric(p, errors='coerce').dropna()\n\n"
        f"final_redemption = pd.Timestamp('{pd.Timestamp(final_red).date()}')\n"
        f"coupon_rate = {float(coupon)}\n\n"
        "ytm_values = []\nytm_dates = []\n"
        "for date, price in p.items():\n"
        "    years_left = (final_redemption - date).days / 365.25\n"
        "    if years_left > 0 and price > 0:\n"
        "        ytm = (coupon_rate + (100 - price) / years_left) / ((100 + price) / 2) * 100\n"
        "        ytm_values.append(ytm)\n"
        "        ytm_dates.append(date)\n\n"
        "if ytm_values:\n"
        "    fig, ax = plt.subplots(figsize=(12, 5))\n"
        "    ax.plot(ytm_dates, ytm_values, color='#9b59b6', marker='.', markersize=3, linewidth=1.5)\n"
        f"    ax.axhline({float(coupon)}, color='black', alpha=0.2, linestyle='--', label=f'Coupon Rate ({{coupon_rate}}%)')\n"
        f"    ax.set_title('{bond_name} — Approximate Yield to Maturity')\n"
        "    ax.set_xlabel('Date')\n    ax.set_ylabel('YTM (%)')\n"
        "    ax.legend()\n    ax.grid(True, alpha=0.3)\n    plt.tight_layout()\n    plt.show()\n"
        "else:\n    print('Could not compute YTM')"
    )
    return [new_markdown_cell(narrative), new_code_cell(code)]


def build_related_bonds_cells(bond_info, related_bonds, BondPrice_T):
    """Build related bonds comparison."""
    cells = []
    bond_name = bond_info['name']
    bond_id = bond_info['id']

    # Build table
    all_related = []
    for category, bonds in related_bonds.items():
        for b in bonds:
            all_related.append((category, b))

    if not all_related:
        return []

    table = "## Related Bonds\n\n"
    table += "| Relationship | Bond Name | Issue Date | Coupon |\n|-------------|-----------|------------|--------|\n"
    for cat, b in all_related[:12]:
        cat_label = cat.replace('_', ' ').title()
        issue = format_date(b['first_issue_date'])
        coupon = f"{b['coupon_rate']}%" if pd.notna(b.get('coupon_rate')) and b['coupon_rate'] != 'N/A' else 'N/A'
        table += f"| {cat_label} | {b['name'][:45]} | {issue} | {coupon} |\n"
    cells.append(new_markdown_cell(table))

    # Comparative price chart — pick up to 4 related bonds with price data
    compare_ids = []
    compare_names = []
    for cat, b in all_related:
        if len(compare_ids) >= 4:
            break
        try:
            s = BondPrice_T.loc[(b['id'], 'Average')]
            s = pd.to_numeric(s, errors='coerce').dropna()
            if len(s) > 5:
                compare_ids.append(b['id'])
                compare_names.append(b['name'][:30])
        except KeyError:
            continue

    if compare_ids:
        ids_str = str(compare_ids)
        names_str = str(compare_names)
        code = (
            "# Comparative price chart with related bonds\n"
            "fig, ax = plt.subplots(figsize=(12, 6))\n\n"
            "# This bond\n"
            f"p = BondPrice_T.loc[({bond_id}, 'Average')]\n"
            "p = pd.to_numeric(p, errors='coerce').dropna()\n"
            f"if len(p) > 0:\n"
            f"    ax.plot(p.index, p.values, linewidth=2, label='{bond_name[:30]} (this bond)')\n\n"
            "# Related bonds\n"
            f"related_ids = {ids_str}\n"
            f"related_names = {names_str}\n"
            "for rid, rname in zip(related_ids, related_names):\n"
            "    try:\n"
            "        s = BondPrice_T.loc[(rid, 'Average')]\n"
            "        s = pd.to_numeric(s, errors='coerce').dropna()\n"
            "        if len(s) > 0:\n"
            "            ax.plot(s.index, s.values, linewidth=1, alpha=0.7, label=rname)\n"
            "    except KeyError:\n        pass\n\n"
            "ax.axhline(100, color='black', alpha=0.15, linestyle='--')\n"
            f"ax.set_title('Price Comparison — {bond_name[:30]} vs. Related Bonds')\n"
            "ax.set_xlabel('Date')\nax.set_ylabel('Price ($)')\n"
            "ax.legend(fontsize=8, loc='best')\nax.grid(True, alpha=0.3)\n"
            "plt.tight_layout()\nplt.show()"
        )
        cells.append(new_code_cell(code))
        cells.append(new_markdown_cell(
            "<!-- ENRICH: Compare the price behavior of this bond with the related bonds shown above. "
            "What explains any divergences or similarities? -->"
        ))
    return cells


def build_distribution_cells(bond_info):
    """Build issuance and distribution section."""
    price_sold = bond_info.get('price_sold', 'N/A')
    amount = format_amount(bond_info.get('authorized_amount', 'N/A'))

    auto_text = ""
    if price_sold != 'N/A' and pd.notna(price_sold):
        auto_text += f"\nThe bond was originally sold at **{price_sold}** (per $100 face value)."
    if amount != 'N/A':
        auto_text += f" The authorized amount was **{amount}**."

    return [new_markdown_cell(
        f"## Issuance, Distribution, and Redemption\n{auto_text}\n\n"
        "<!-- ENRICH: Describe how the bond was marketed and sold. Consider:\n"
        "- Who were the primary buyers (banks, public, foreign investors)?\n"
        "- What denominations were available?\n"
        "- Were there intermediaries or brokers involved?\n"
        "- How and when was the bond redeemed?\n"
        "- Was there any refinancing into other instruments? -->"
    )]


def build_implications_cells(bond_info, overlapping_events):
    """Build implications section with era-specific prompts."""
    prompts = ["- What precedents did this bond set for U.S. fiscal policy?"]

    wars = [e['name'] for e in overlapping_events if e['category'] == 'war']
    crises = [e['name'] for e in overlapping_events if e['category'] == 'crisis']

    if wars:
        prompts.append(f"- How did this bond contribute to financing the {wars[0]}?")
    if crises:
        prompts.append(f"- How did the {crises[0]} affect this bond and its holders?")
    prompts.append("- What does this bond reveal about the evolution of U.S. government creditworthiness?")
    prompts.append("- Are there interesting anecdotes or tangential stories that bring this bond to life?")

    return [new_markdown_cell(
        "## Implications and Legacy\n\n"
        "<!-- ENRICH: Discuss the broader significance of this bond:\n"
        + "\n".join(prompts) + "\n-->"
    )]


def build_references_cells(bond_info, suggested_refs):
    """Build references section with auto-suggested sources."""
    refs_md = "\n".join([f"- {r}" for r in suggested_refs])
    return [new_markdown_cell(
        f"## References\n\n{refs_md}\n\n"
        "<!-- ENRICH: Add primary sources, archival references, and bond-specific scholarly work. -->\n\n"
        "---\n\n"
        "*Generated by the Bond Biography Agent using the Hall-Payne-Sargent Bond Database.*"
    )]


# ─── Notebook Generation (Orchestrator) ────────────────────────────────────────

def generate_chapter_notebook(bond_info, price_stats, period_stats, volatility_data,
                               significant_events, overlapping_events, era_desc,
                               quant_lifecycle, related_bonds, suggested_refs,
                               has_price, has_quant, BondPrice_T):
    """Assemble the complete notebook from cell builders."""
    nb = new_notebook()
    nb.metadata['kernelspec'] = {
        'display_name': 'Python 3', 'language': 'python', 'name': 'python3'
    }

    # Preamble
    nb.cells.extend(build_title_cells(bond_info))
    nb.cells.extend(build_overview_cells(bond_info, era_desc, price_stats, quant_lifecycle))
    nb.cells.extend(build_historical_context_cells(bond_info, overlapping_events))
    nb.cells.extend(build_lifecycle_timeline_cells(bond_info, overlapping_events))
    nb.cells.extend(build_bond_features_cells(bond_info))

    # Data Analysis
    if has_quant:
        nb.cells.extend(build_quantity_cells(bond_info, quant_lifecycle, overlapping_events))
    if has_price:
        nb.cells.extend(build_price_cells(bond_info, price_stats, period_stats,
                                           significant_events, overlapping_events))
        nb.cells.extend(build_volatility_cells(bond_info, volatility_data))
        nb.cells.extend(build_ytm_cells(bond_info))

    # Context
    nb.cells.extend(build_related_bonds_cells(bond_info, related_bonds, BondPrice_T))
    nb.cells.extend(build_distribution_cells(bond_info))
    nb.cells.extend(build_implications_cells(bond_info, overlapping_events))
    nb.cells.extend(build_references_cells(bond_info, suggested_refs))

    return nb


# ─── Search and Discovery ─────────────────────────────────────────────────────

def search_bonds(BondList, query):
    """Search for bonds by name."""
    mask = BondList["Treasury's Name Of Issue"].str.contains(query, case=False, na=False)
    return BondList[mask][["Treasury's Name Of Issue", "Category L3", "First Issue Date",
                           "Coupon Rate", "Term Of Loan"]].copy()


def list_categories(BondList):
    """List all bond categories with counts."""
    return BondList.groupby(['Category L1', 'Category L2', 'Category L3']).size()


# ─── Main CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Bond Biography Agent (Enhanced) — Generate comprehensive bond biography chapters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --bond-id 20044                    Generate chapter for Louisiana Purchase bonds
  %(prog)s --bond-id 20101                    Generate chapter for Civil War 5-20s
  %(prog)s --search "Liberty"                 Search for bonds by name
  %(prog)s --search "War" --generate-first    Search and auto-generate for first match
  %(prog)s --list-categories                  Show all bond categories
  %(prog)s --interactive                      Interactive bond selection
        """
    )
    parser.add_argument('--bond-id', type=int, help='L1 ID of the bond')
    parser.add_argument('--search', type=str, help='Search bonds by name')
    parser.add_argument('--list-categories', action='store_true', help='List categories')
    parser.add_argument('--generate-first', action='store_true', help='Auto-generate for first search result')
    parser.add_argument('--output', type=str, help='Output filename')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')

    args = parser.parse_args()

    if not any([args.bond_id, args.search, args.list_categories, args.interactive]):
        parser.print_help()
        sys.exit(0)

    print("Loading bond database...")
    BondList, BondPrice_T, BondQuant_T = load_bond_database_h5()
    print(f"Loaded {len(BondList)} bond issues.\n")

    if args.list_categories:
        cats = list_categories(BondList)
        print("Bond Categories:")
        print("=" * 70)
        for (l1, l2, l3), count in cats.items():
            print(f"  {l1} > {l2} > {l3}: {count} bonds")
        return

    # Resolve bond_id
    bond_id = None
    if args.search:
        results = search_bonds(BondList, args.search)
        if len(results) == 0:
            print(f"No bonds found matching '{args.search}'")
            return
        print(f"Found {len(results)} bonds matching '{args.search}':")
        print("=" * 80)
        bond_name_col = "Treasury's Name Of Issue"
        for idx, row in results.iterrows():
            print(f"  L1 ID {idx:>6}: {row[bond_name_col]:<50} ({row.get('First Issue Date', 'N/A')})")
        if args.generate_first:
            bond_id = results.index[0]
            print(f"\nGenerating chapter for first match: {bond_id}")
        else:
            print(f"\nUse --bond-id <ID> to generate a chapter.")
            return
    elif args.bond_id:
        bond_id = args.bond_id
    elif args.interactive:
        print("Interactive Bond Biography Generator")
        print("=" * 40)
        query = input("Search for a bond (or enter L1 ID): ").strip()
        try:
            bond_id = int(query)
        except ValueError:
            results = search_bonds(BondList, query)
            if len(results) == 0:
                print(f"No bonds found matching '{query}'")
                return
            print(f"\nFound {len(results)} matches:")
            bond_name_col = "Treasury's Name Of Issue"
            for i, (idx, row) in enumerate(results.iterrows()):
                print(f"  [{i}] L1 ID {idx}: {row[bond_name_col]}")
            choice = input("\nEnter number to select (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return
            try:
                bond_id = results.index[int(choice)]
            except (ValueError, IndexError):
                print("Invalid selection.")
                return

    # Generate
    bond_info = get_bond_info(BondList, bond_id)
    if bond_info is None:
        print(f"Error: Bond ID {bond_id} not found.")
        sys.exit(1)

    print(f"\nGenerating enhanced biography for: {bond_info['name']}")
    print(f"  Bond ID: {bond_id}")
    print(f"  Category: {bond_info['category_l3']}")
    print(f"  Issued: {format_date(bond_info['first_issue_date'])}")
    print(f"  Coupon: {bond_info['coupon_rate']}%")

    # Get data
    price_series = get_price_data(BondPrice_T, bond_id)
    quant_series = get_quantity_data(BondQuant_T, bond_id)
    has_price = len(price_series) > 0
    has_quant = len(quant_series) > 0

    print(f"  Price data: {'Yes' if has_price else 'No'} ({len(price_series)} observations)")
    print(f"  Quantity data: {'Yes' if has_quant else 'No'} ({len(quant_series)} observations)")

    # Advanced analysis
    price_stats = compute_price_statistics(price_series)
    period_stats = compute_period_statistics(price_series, bond_info) if has_price else []
    volatility_data = compute_volatility_analysis(price_series) if has_price else {}
    significant_events = detect_significant_events(price_series, quant_series)
    quant_lifecycle = compute_quantity_lifecycle(quant_series) if has_quant else {}

    overlapping_events = get_overlapping_events(
        bond_info['first_issue_date'], bond_info['final_redemption_date'])
    era_desc = get_era_description(
        bond_info['first_issue_date'], bond_info['final_redemption_date'])
    related_bonds = find_related_bonds(BondList, bond_info)
    suggested_refs = suggest_references(bond_info)

    n_related = sum(len(v) for v in related_bonds.values())
    print(f"  Historical events overlapping: {len(overlapping_events)}")
    print(f"  Significant price events detected: {len(significant_events)}")
    print(f"  Related bonds found: {n_related}")
    print(f"  Suggested references: {len(suggested_refs)}")

    # Generate notebook
    nb = generate_chapter_notebook(
        bond_info, price_stats, period_stats, volatility_data,
        significant_events, overlapping_events, era_desc,
        quant_lifecycle, related_bonds, suggested_refs,
        has_price, has_quant, BondPrice_T
    )

    # Save
    if args.output:
        output_path = args.output
    else:
        safe_name = bond_info['name'].replace(' ', '_').replace('.', '').replace("'", '')
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_')
        output_path = f"chapter_{bond_id}_{safe_name}.ipynb"

    output_full = Path(__file__).parent / output_path
    with open(output_full, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print(f"\n{'='*60}")
    print(f"  Chapter saved to: {output_full}")
    print(f"  Total cells: {len(nb.cells)}")
    print(f"  Sections marked <!-- ENRICH --> need researcher input.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
