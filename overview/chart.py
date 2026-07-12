"""
overview/chart.py
-----------------
Builds the synthesis heatmap for the Overview page.

Shows the top 40 most vulnerable countries across 5 dimensions:
    1. CO₂ per Capita       (Calvin)  — who caused it
    2. Vulnerability Score  (Ruben)   — who is exposed
    3. Economic Damage %GDP (Lam)     — who is suffering
    4. Displacement Pressure(Lucas)   — who faces displacement
    5. Finance per Capita   (Nengjie) — who is getting help

All metrics are min-max normalised to 0–1 for comparability.
Countries are sorted by vulnerability score (descending).
"""

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from heuristic1.loaders.owid import load as load_owid
from heuristic2.loaders.ndgain import load as load_ndgain
from heuristic2.constants import NAME_OVERRIDES
from heuristic4.loaders.country_dataset import load as load_country_dataset
from heuristic5.loaders.data_loader import load_recipient_finance_data

CLIMATE_COL = "climate_usd_thousand"


@st.cache_data(show_spinner=False)
def _build_merged() -> pd.DataFrame:
    """
    Merges all 5 sub-heuristic metrics into a single country-level DataFrame.
    Cached so the expensive merge only runs once per session.
    """

    # ── CALVIN — CO₂ per capita ───────────────────────────────────────────────
    owid = load_owid()
    owid = owid[owid["iso_code"].notna() & (owid["iso_code"].str.len() == 3)]
    latest_co2 = (
        owid.dropna(subset=["co2_per_capita"])
        .sort_values("year")
        .groupby("iso_code", as_index=False)
        .last()[["iso_code", "country", "co2_per_capita", "population"]]
    )

    # ── RUBEN — Vulnerability score 2024 ─────────────────────────────────────
    ndgain = load_ndgain()
    vuln_2024 = (
        ndgain[ndgain["year"] == 2024][["ISO3", "Name", "vulnerability"]]
        .rename(columns={"ISO3": "iso_code"})
    )

    # ── LAM — Average annual economic damage % GDP ────────────────────────────
    # Average across all available years is used instead of latest year,
    # since disaster damage is sporadic — latest year may be zero even for
    # highly disaster-prone nations.
    dmg = pd.read_csv("heuristic3/data/damage_gdp.csv")
    dmg = dmg.dropna(subset=["All disasters"])
    avg_dmg = (
        dmg[dmg["All disasters"] > 0]
        .groupby("Code", as_index=False)["All disasters"]
        .mean()
        .rename(columns={"Code": "iso_code", "All disasters": "damage_pct_gdp"})
    )

    # ── LUCAS — Displacement pressure ─────────────────────────────────────────
    country_df = load_country_dataset()
    displacement = country_df[["country_code", "displacement_pressure"]].rename(
        columns={"country_code": "iso_code"}
    )

    # ── NENGJIE — Climate finance received per capita ─────────────────────────
    rp = load_recipient_finance_data()
    finance = (
        rp.groupby("recipient")[CLIMATE_COL]
        .sum()
        .reset_index()
        .rename(columns={"recipient": "country", CLIMATE_COL: "finance_usd_thousand"})
    )

    # Map recipient country names to ISO3 using OWID name lookup
    name_to_iso = (
        owid[["country", "iso_code"]]
        .drop_duplicates()
        .set_index("country")["iso_code"]
        .to_dict()
    )
    finance["iso_code"] = finance["country"].map(name_to_iso)
    finance = finance.dropna(subset=["iso_code"])
    finance = finance.merge(
        latest_co2[["iso_code", "population"]], on="iso_code", how="left"
    )
    finance["finance_per_capita"] = (
        finance["finance_usd_thousand"] * 1000
        / finance["population"].replace(0, np.nan)
    )
    finance = finance[["iso_code", "finance_per_capita"]]

    # ── MERGE ALL ─────────────────────────────────────────────────────────────
    df = (
        vuln_2024
        .merge(latest_co2[["iso_code", "co2_per_capita"]], on="iso_code", how="left")
        .merge(avg_dmg, on="iso_code", how="left")
        .merge(displacement, on="iso_code", how="left")
        .merge(finance, on="iso_code", how="left")
    )

    # Fill missing values with 0
    # damage_pct_gdp = 0 means no recorded disaster damage
    # finance_per_capita = 0 means no recorded climate finance received
    # displacement_pressure = 0 means no recorded displacement exposure
    df["damage_pct_gdp"] = df["damage_pct_gdp"].fillna(0)
    df["finance_per_capita"] = df["finance_per_capita"].fillna(0)
    df["displacement_pressure"] = df["displacement_pressure"].fillna(0)
    df = df.dropna(subset=["vulnerability", "co2_per_capita"])

    return df


def _normalise(df: pd.DataFrame, col: str, percentile: float = 0.95) -> pd.Series:
    """
    Percentile-based normalisation to 0–1 range.
    Values above the given percentile are capped to prevent outliers
    from compressing the rest of the distribution toward zero.
    """
    min_val = df[col].min()
    max_val = df[col].quantile(percentile)
    if max_val == min_val:
        return pd.Series(0.5, index=df.index)
    return ((df[col] - min_val) / (max_val - min_val)).clip(0, 1)


def chart(top_n: int = 40):
    """
    Builds the synthesis heatmap for the Overview page.

    Parameters
    ----------
    top_n : int
        Number of most vulnerable countries to show. Default 40.

    Returns
    -------
    plotly.graph_objects.Figure
    """

    df = _build_merged()

    # ── SELECT TOP N MOST VULNERABLE COUNTRIES ────────────────────────────────
    top = df.nlargest(top_n, "vulnerability").copy()
    top["Name"] = top["Name"].replace(NAME_OVERRIDES)

    # ── NORMALISE ALL METRICS TO 0–1 ─────────────────────────────────────────
    # Normalisation is computed across the FULL dataset so rankings are
    # meaningful relative to all 189 countries, not just the top 40.
    metrics = {
        "CO₂ per Capita": "co2_per_capita",
        "Vulnerability": "vulnerability",
        "Disaster Damage % GDP": "damage_pct_gdp",
        "Displacement Pressure": "displacement_pressure",
        "Finance Received per Capita": "finance_per_capita",
    }

    heatmap_data = pd.DataFrame(index=top["Name"])

    for label, col in metrics.items():
        heatmap_data[label] = _normalise(df, col).loc[top.index].values

    # Sort countries by vulnerability (highest at top)
    heatmap_data = heatmap_data.sort_values("Vulnerability", ascending=False)

    # ── BUILD HEATMAP ─────────────────────────────────────────────────────────
    fig = px.imshow(
        heatmap_data,
        color_continuous_scale=[
            [0.0, "#1a1a2e"],   # Dark — low score
            [0.5, "#e94560"],   # Mid — moderate score
            [1.0, "#f5f5f5"],   # Light — high score
        ],
        zmin=0,
        zmax=1,
        aspect="auto",
        title=f"Climate Injustice at a Glance — Top {top_n} Most Vulnerable Nations",
        labels={"color": "Normalised Score (0–1)"},
    )

    # ── HIGHLIGHT TOP 5 MOST VULNERABLE NATIONS ──────────────────────────────
    # Yellow border drawn around the top 5 rows to immediately draw
    # the policymaker's eye to the most critical cases.
    fig.add_shape(
        type="rect",
        x0=-0.5,
        x1=len(metrics) - 0.5,
        y0=-0.5,
        y1=4.5,
        line=dict(color="#FFD700", width=3),
        fillcolor="rgba(0,0,0,0)",
    )

    fig.add_annotation(
        x=len(metrics) - 0.5,
        y=2,
        xref="x",
        yref="y",
        text="⚠️ Top 5<br>Most Vulnerable",
        showarrow=False,
        font=dict(size=11, color="#FFD700"),
        xanchor="left",
        yanchor="middle",
        xshift=8,
    )

    fig.update_layout(
        xaxis=dict(
            title="",
            tickfont=dict(size=12),
            side="bottom",
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=11),
            autorange="reversed",
        ),
        coloraxis_colorbar=dict(
            title="Score<br>(0–1)",
            tickvals=[0, 0.5, 1],
            ticktext=["Low", "Mid", "High"],
        ),
        margin=dict(l=10, r=10, t=50, b=20),
        title_font_size=15,
        height=800,
    )

    return fig