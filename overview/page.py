import streamlit as st

from heuristic1.loaders.owid import load as load_owid
from heuristic2.loaders.ndgain import load as load_ndgain
from heuristic3.loaders.disasters import load_data as load_disasters
from heuristic4.loaders.sea_level import load as load_sea_level
from heuristic5.loaders.data_loader import load_provider_finance_data
from overview.chart import chart as build_heatmap

# ── DATA LOADING ──────────────────────────────────────────────────────────────
owid_data = load_owid()
ndgain_data = load_ndgain()
_, _, _, events_df = load_disasters()
sea_level_data = load_sea_level()
finance_data = load_provider_finance_data()

CLIMATE_COL = "climate_usd_thousand"

# ── COMPUTED KPIs ─────────────────────────────────────────────────────────────
# Each KPI is fixed at the most recent year available in its respective dataset.
# Year labels are shown inline in each metric label for transparency.

def get_top10_emissions_share() -> tuple:
    """Calvin's KPI - top 10 emitters' share of global CO₂ with delta vs previous year."""
    owid_countries = owid_data[owid_data["iso_code"].notna() & (owid_data["iso_code"].str.len() == 3)]
    latest_year = int(owid_countries[owid_countries["co2"].notna()]["year"].max())
    prev_year = latest_year - 1

    def compute_share(year):
        snapshot = owid_countries[owid_countries["year"] == year].dropna(subset=["co2"])
        total = snapshot["co2"].sum()
        top10 = snapshot.nlargest(10, "co2")["co2"].sum()
        return (top10 / total * 100) if total > 0 else 0

    share_latest = compute_share(latest_year)
    share_prev = compute_share(prev_year)
    delta = round(share_latest - share_prev, 2)
    return f"{share_latest:.1f}%", f"{'+' if delta >= 0 else ''}{delta:.2f}% vs {prev_year}", latest_year


def get_most_vulnerable() -> tuple:
    """Ruben's KPI - most vulnerable nation in 2024 with actual vulnerability score."""
    snapshot_2024 = ndgain_data[ndgain_data["year"] == 2024]
    most_vuln = snapshot_2024.sort_values("vulnerability", ascending=False).iloc[0]
    return most_vuln, 2024


def get_disaster_events_kpi() -> tuple:
    """Lam's KPI - total global disaster events in the most recent year. Capped at 2024."""
    all_disasters = events_df[
        (events_df["disaster_type"] == "All disasters") &
        (events_df["Year"] <= 2024)
    ]
    latest_year = int(all_disasters["Year"].max())
    prev_year = latest_year - 1
    total_latest = int(all_disasters[all_disasters["Year"] == latest_year]["n_disasters"].sum())
    total_prev = int(all_disasters[all_disasters["Year"] == prev_year]["n_disasters"].sum())
    delta = total_latest - total_prev
    return (
        f"{total_latest:,}",
        f"{'+' if delta >= 0 else ''}{delta:,} vs {prev_year}",
        latest_year
    )


def get_sea_level_kpi() -> tuple:
    """Lucas's KPI - most recent observed sea level anomaly in mm. Capped at 2024."""
    historical = sea_level_data[
        (sea_level_data["scenario"] == "Historical") &
        (sea_level_data["year"] <= 2024)
    ].dropna(subset=["sea_level_mm"])
    latest = historical.sort_values("year").iloc[-1]
    prev = historical.sort_values("year").iloc[-2]
    delta = latest["sea_level_mm"] - prev["sea_level_mm"]
    return (
        f"{latest['sea_level_mm']:.1f} mm",
        f"{'+' if delta >= 0 else ''}{delta:.1f} mm vs {int(prev['year'])}",
        int(latest["year"])
    )


def get_climate_finance_kpi() -> tuple:
    """Nengjie's KPI - total climate finance in most recent year."""
    latest_year = int(finance_data["year"].max())
    prev_year = latest_year - 1
    total_latest = finance_data[finance_data["year"] == latest_year][CLIMATE_COL].sum() / 1e6
    total_prev = finance_data[finance_data["year"] == prev_year][CLIMATE_COL].sum() / 1e6
    delta = total_latest - total_prev
    return (
        f"${total_latest:.1f}B",
        f"{'+' if delta >= 0 else ''}{delta:.1f}B vs {prev_year}",
        latest_year
    )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(layout="wide")


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

st.subheader("Key Indicators at a Glance")
st.caption(
    "Each indicator reflects the most recent year available in its respective dataset."
)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    emissions_value, emissions_delta, emissions_year = get_top10_emissions_share()
    st.metric(
        label=f"🏭 Top 10 Emitters' Share ({emissions_year})",
        value=emissions_value,
        delta=emissions_delta,
        delta_color="inverse",
        help=(
            "The combined share of global CO₂ emissions from the top 10 emitting nations. "
            "A higher share indicates greater emissions concentration among a small group of countries. "
            "Delta shows the change vs the previous year A red delta indicates worsening concentration."
        )
    )

with kpi2:
    most_vuln, vuln_year = get_most_vulnerable()
    st.metric(
        label=f"⚠️ Most Vulnerable Nation ({vuln_year})",
        value=most_vuln["Name"],
        delta=f"Score: {most_vuln['vulnerability']:.3f} / 1.000",
        delta_color="off",
        help=(
            "The country with the highest ND-GAIN vulnerability score in the most recent year. "
            "The ND-GAIN score ranges from 0 (least vulnerable) to 1 (most vulnerable), "
            "measuring exposure, sensitivity, and adaptive capacity across food, water, health, "
            "ecosystem, habitat, and infrastructure sectors."
        )
    )

with kpi3:
    disaster_value, disaster_delta, disaster_year = get_disaster_events_kpi()
    st.metric(
        label=f"🌪️ Disaster Events ({disaster_year})",
        value=disaster_value,
        delta=disaster_delta,
        delta_color="inverse",
        help=(
            "Total number of natural disaster events recorded globally in the most recent year. "
            "Includes floods, storms, droughts, earthquakes, wildfires, and extreme temperatures. "
            "Delta shows the change vs the previous year A red delta indicates worsening conditions."
        )
    )

with kpi4:
    sea_value, sea_delta, sea_year = get_sea_level_kpi()
    st.metric(
        label=f"🌊 Sea Level Anomaly ({sea_year})",
        value=sea_value,
        delta=sea_delta,
        delta_color="inverse",
        help=(
            "Global mean sea level anomaly measured in millimetres (mm) relative to a historical baseline. "
            "A rising sea level directly threatens low-lying coastal nations and small island states. "
            "Delta shows the year-on-year change A red delta indicates worsening conditions."
        )
    )

with kpi5:
    finance_value, finance_delta, finance_year = get_climate_finance_kpi()
    st.metric(
        label=f"💰 Climate Finance ({finance_year})",
        value=finance_value,
        delta=finance_delta,
        help=(
            "Total climate-related development finance committed globally in the most recent year, "
            "measured in USD billions. Includes both adaptation and mitigation finance from donor nations. "
            "Delta shows the change vs the previous year A green delta indicates more support being committed."
        )
    )

st.divider()

st.subheader("Global Overview - Climate Injustice at a Glance")
st.caption(
    "Top 40 most vulnerable nations ranked by vulnerability score. "
    "All metrics normalised to 0-1 using 95th percentile scaling to prevent "
    "outliers from distorting the colour distribution. "
    "Disaster Damage % GDP reflects average annual damage across all available years. "
    "Darker cells indicate lower scores; brighter cells indicate higher scores."
)
st.plotly_chart(build_heatmap(top_n=40), use_container_width=True)

with st.container(border=True):
    st.markdown("**What to Look For**")
    st.markdown(
        "The injustice pattern is visible across the rows. The most vulnerable "
        "nations (**Mauritania**, **Somalia**, **Chad**, **Yemen**, and **Sudan**) "
        "appear bright in the **Vulnerability** and **Displacement Pressure** "
        "columns, confirming severe climate exposure and high displacement risk. "
        "Yet the same nations appear consistently dark in the **CO2 per Capita** "
        "column, confirming they bear minimal responsibility for the crisis. "
        "The **Disaster Damage % GDP** column reveals that nations like **Chad**, "
        "**Yemen**, **Tonga**, **Vanuatu**, and **Liberia** suffer the greatest "
        "economic losses from extreme weather relative to their GDP, despite "
        "emitting far below the global average. "
        "The **Finance Received per Capita** column highlights a further disparity: "
        "small island states such as **Solomon Islands**, **Tonga**, **Vanuatu**, "
        "and **Kiribati** receive relatively higher per-capita finance due to their "
        "small populations, while larger but equally vulnerable nations like "
        "**Somalia**, **Chad**, and **Sudan** remain significantly underserved. "
        "Navigate to each sub-heuristic tab in the sidebar to explore these "
        "dimensions in depth."
    )