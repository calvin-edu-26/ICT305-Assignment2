import streamlit as st

from heuristic1.loaders.owid import load as load_owid
from heuristic2.loaders.ndgain import load as load_ndgain

# ── DATA LOADING ──────────────────────────────────────────────────────────────
owid_data = load_owid()
ndgain_data = load_ndgain()

# ── COMPUTED KPIs ─────────────────────────────────────────────────────────────

def get_top10_emissions_share(year: int) -> float:
    """Calvin's KPI — top 10 emitters' share of global CO₂."""
    snapshot = owid_data[owid_data["year"] == year]
    return round(snapshot.nlargest(10, "co2")["share_global_co2"].sum(), 1)

def get_most_vulnerable(year: int):
    """Ruben's KPI — most vulnerable nation by ND-GAIN score."""
    snapshot = ndgain_data[ndgain_data["year"] == year]
    return snapshot.sort_values("vulnerability", ascending=False).iloc[0]


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
        label="🏭 Top 10 Emitters' Share",
        value=f"{share}%",
        help="Share of global CO₂ emissions from the top 10 emitting nations."
    )

with kpi2:
    # Ruben — Climate Vulnerability
    most_vuln = get_most_vulnerable(selected_year)
    st.metric(
        label="⚠️ Most Vulnerable Nation",
        value=most_vuln["Name"],
        delta=f"Score: {most_vuln['vulnerability']:.2f}",
        help="Country with the highest ND-GAIN vulnerability score."
    )

with kpi3:
    # Lam — Extreme Weather
    # TODO: Replace with computed metric from Lam's dataset
    st.metric(
        label="🌪️ Disaster Events",
        value="—",
        help="Lam's metric — to be added."
    )

with kpi4:
    # Lucas — Sea Level Rise
    # TODO: Replace with computed metric from Lucas's dataset
    st.metric(
        label="🌊 Sea Level Rise",
        value="—",
        help="Lucas's metric — to be added."
    )

with kpi5:
    # Nengjie — Climate Finance
    # TODO: Replace with computed metric from Nengjie's dataset
    st.metric(
        label="💰 Finance Gap",
        value="—",
        help="Nengjie's metric — to be added."
    )

st.divider()

# ── OVERVIEW CHART ─────────────────────────────────────────────────────────────
# Per brief: high-level trend summarising overall behaviour.
# To be decided collectively once all sub-heuristic charts are complete.

st.subheader("Global Overview")
st.info("📍 Group-level overview chart — to be confirmed once all sub-heuristics are complete.")