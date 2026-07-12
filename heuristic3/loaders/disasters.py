"""
heuristic3/loaders/disasters.py
Loads and cleans the 4 CSVs in heuristic3/data/ for the "Extreme Weather &
Economic Damage" dashboard (see heuristic3/page.py).

Exposes a single function, load_data(), which returns the four DataFrames
consumed by heuristic3/page.py and heuristic3/chart/*.py:

    co2_df, deaths_df, damage_df, events_df = load_data()

Column contracts (what the chart modules expect):
    co2_df    : one row per country-year. Needs `year`, `country`,
                `co2_per_capita`, `gdp_per_capita`, `income_group`.
                (raw co2.csv only has `gdp` + `population`, so
                gdp_per_capita is derived here.)
    deaths_df : raw deaths.csv (`Entity`, `Year`, per-disaster-type death
                columns, `All disasters`) plus an `income_group` column.
    damage_df : raw damage_gdp.csv (same shape as deaths.csv, values are
                % of GDP) plus an `income_group` column.
    events_df : raw events.csv columns are `Entity` (actually holds the
                disaster type, e.g. "All disasters", "Flood", ...),
                `Year`, `Disasters`. Renamed here to `disaster_type` and
                `n_disasters` to match what the chart modules expect.
"""

import pandas as pd
import streamlit as st

from heuristic3.constants import INCOME_GROUPS

DATA_DIR = "heuristic3/data"


@st.cache_data
def load_data():
    """
    Reads and cleans the 4 source CSVs for Heuristic 3.

    Cached with @st.cache_data so repeated calls across sections of
    page.py (and the Overview page's KPI call) are cheap after the first,
    cold read.

    Returns
    -------
    tuple(co2_df, deaths_df, damage_df, events_df) : pd.DataFrame x4
    """
    # ── CO2 / GDP / population (country-year) ──────────────────────────
    co2_df = pd.read_csv(f"{DATA_DIR}/co2.csv")
    co2_df["gdp_per_capita"] = co2_df["gdp"] / co2_df["population"]
    co2_df["income_group"] = co2_df["country"].map(INCOME_GROUPS)

    # ── Deaths by disaster type (country-year) ─────────────────────────
    deaths_df = pd.read_csv(f"{DATA_DIR}/deaths.csv")
    deaths_df["income_group"] = deaths_df["Entity"].map(INCOME_GROUPS)

    # ── Economic damage, % of GDP, by disaster type (country-year) ─────
    damage_df = pd.read_csv(f"{DATA_DIR}/damage_gdp.csv")
    damage_df["income_group"] = damage_df["Entity"].map(INCOME_GROUPS)

    # ── Global disaster event counts by type (Year x type) ─────────────
    events_df = pd.read_csv(f"{DATA_DIR}/events.csv")
    events_df = events_df.rename(
        columns={"Entity": "disaster_type", "Disasters": "n_disasters"}
    )

    return co2_df, deaths_df, damage_df, events_df
