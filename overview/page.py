import streamlit as st

from heuristic1.loaders.owid import load as load_owid
from heuristic2.loaders.ndgain import load as load_ndgain
from heuristic5.loaders.data_loader import load_provider_finance_data

# ── DATA LOADING ──────────────────────────────────────────────────────────────
owid_data = load_owid()
ndgain_data = load_ndgain()
finance_data = load_provider_finance_data()

CLIMATE_COL = "climate_usd_thousand"

# ── COMPUTED KPIs ─────────────────────────────────────────────────────────────

def get_top10_emissions_share(year: int) -> float:
    """Calvin's KPI — top 10 emitters' share of global CO₂."""
    snapshot = owid_data[owid_data["year"] == year]
    return round(snapshot.nlargest(10, "co2")["share_global_co2"].sum(), 1)

def get_most_vulnerable(year: int):
    """Ruben's KPI — most vulnerable nation by ND-GAIN score."""
    snapshot = ndgain_data[ndgain_data["year"] == year]
    return snapshot.sort_values("vulnerability", ascending=False).iloc[0]

def get_climate_finance_kpi() -> tuple:
    """
    Nengjie's KPI — total climate finance committed in 2023 (most recent
    complete year) with delta vs 2022.
    Returns (value_str, delta_str)
    """
    total_2023 = finance_data[finance_data["year"] == 2023][CLIMATE_COL].sum() / 1e6
    total_2022 = finance_data[finance_data["year"] == 2022][CLIMATE_COL].sum() / 1e6
    delta = total_2023 - total_2022
    return f"${total_2023:.1f}B", f"{'+' if delta >= 0 else ''}{delta:.1f}B vs 2022"


# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION & SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(layout="wide")

with st.sidebar:
    st.header("Filters")

    selected_year = st.selectbox(
        "Year",
        options=list(range(2018, 1994, -1)),
        index=0,
        help="Select a year to update KPI indicators."
    )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE LAYOUT
# ═════════════════════════════════════════════════════════════════════════════

st.title("Climate Injustice Dashboard")
st.markdown(
    """
    > **"The nations least responsible for climate change are bearing its greatest consequences."**

    This dashboard presents evidence across five interconnected dimensions of climate 
    injustice, designed to support strategic decision-making by international climate 
    organisations such as the **UN** and **IPCC**.
    """
)

st.divider()

# ── KPI METRICS ───────────────────────────────────────────────────────────────
# Per brief: high-level snapshot of the most important indicators.
# One KPI per sub-heuristic. Responsive to the year selector.

st.subheader(f"Key Indicators at a Glance ({selected_year})")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    # Calvin — Carbon Emissions
    share = get_top10_emissions_share(selected_year)
    st.metric(
        label="Top 10 Emitters' Share",
        value=f"{share}%",
        help="Share of global CO₂ emissions from the top 10 emitting nations."
    )

with kpi2:
    # Ruben — Climate Vulnerability
    most_vuln = get_most_vulnerable(selected_year)
    st.metric(
        label="Most Vulnerable Nation",
        value=most_vuln["Name"],
        delta=f"Score: {most_vuln['vulnerability']:.2f}",
        help="Country with the highest ND-GAIN vulnerability score."
    )

with kpi3:
    # Lam — Extreme Weather
    # TODO: Replace with computed metric from Lam's dataset
    st.metric(
        label="Disaster Events",
        value="—",
        help="Lam's metric — to be added."
    )

with kpi4:
    # Lucas — Sea Level Rise
    # TODO: Replace with computed metric from Lucas's dataset
    st.metric(
        label="Sea Level Rise",
        value="—",
        help="Lucas's metric — to be added."
    )

with kpi5:
    # Nengjie — Climate Finance
    # Fixed at 2023 — most recent complete year in Nengjie's dataset.
    # Independent of year selector (finance data runs 2013–2024, not 1995–2018).
    finance_value, finance_delta = get_climate_finance_kpi()
    st.metric(
        label="Climate Finance (2023)",
        value=finance_value,
        delta=finance_delta,
        help="Total climate-related development finance committed globally in 2023."
    )

st.divider()

# ── OVERVIEW CHART ─────────────────────────────────────────────────────────────
# Per brief: high-level trend summarising overall behaviour.
# To be decided collectively once all sub-heuristic charts are complete.

st.subheader("Global Overview")
st.info("Group-level overview chart — to be confirmed once all sub-heuristics are complete.")