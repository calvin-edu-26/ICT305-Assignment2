from pathlib import Path
import sys

import streamlit as st

HEURISTIC_DIR = Path(__file__).resolve().parent
if str(HEURISTIC_DIR) not in sys.path:
    sys.path.insert(0, str(HEURISTIC_DIR))

from charts.climate_risk_context import render_climate_risk_context
from charts.decision_support import render_decision_support
from charts.finance_exploration import render_exploration
from charts.gap_insights import render_gap_insights
from charts.global_context import render_global_context
from charts.historical_emissions import render_historical_emissions
from charts.oecd_dac_history import render_oecd_dac_history
from charts.overview import render_overview
from charts.recipient_finance import render_recipient_finance
from loaders.data_loader import (
    load_climate_indicator_data,
    load_country_temperature_data,
    load_historical_emissions_data,
    load_oecd_dac_compiled_data,
    load_owid_emissions_data,
    load_provider_finance_data,
    load_recipient_finance_data,
    load_vulnerability_data,
    load_world_bank_context_data,
)


st.set_page_config(
    page_title="Heuristic 5 | Climate Finance Gap",
    page_icon="",
    layout="wide",
)


try:
    provider_finance = load_provider_finance_data()
except ImportError as exc:
    st.error(
        "This dashboard needs Excel-reading support because some supplied files are workbooks "
        "even though they use .csv or .xls names. Install the missing reader and rerun Streamlit."
    )
    st.exception(exc)
    st.stop()


st.title("Heuristic 5: Climate Finance Gap")
st.caption("A decision-support dashboard for checking whether major providers are delivering enough adaptation finance to vulnerable recipients.")

st.info(
    "Recommended flow: start with the main finance gap, then check recipient-side delivery, then use risk and global context to support your explanation."
)

with st.expander("How to use this dashboard", expanded=False):
    st.write(
        "1. Choose the dashboard section from the sidebar.\n"
        "2. Filter years, provider countries, and recipient regions.\n"
        "3. Use the main dashboard to compare adaptation finance, mitigation finance, and provider responsibility.\n"
        "4. Use the context sections only when you need supporting evidence for climate risk or global trends."
    )

with st.sidebar:
    st.header("Dashboard Flow")
    section = st.radio(
        "Dashboard section",
        [
            "Main Finance Gap",
            "Recipient Finance",
            "Risk & Global Context",
            "Data Sources",
        ],
        index=0,
    )

    st.header("Filters")
    min_year, max_year = int(provider_finance["year"].min()), int(provider_finance["year"].max())
    year_range = st.slider("Commitment year range", min_year, max_year, (max(min_year, 2018), max_year))

    default_providers = [
        provider
        for provider in ["United States", "Germany", "Japan", "France", "United Kingdom", "Canada", "Italy", "Australia"]
        if provider in set(provider_finance["provider"])
    ]
    selected_providers = st.multiselect(
        "Provider countries",
        sorted(provider_finance["provider"].dropna().unique()),
        default=default_providers or sorted(provider_finance["provider"].dropna().unique())[:8],
    )

    selected_regions = st.multiselect(
        "Recipient regions",
        sorted(provider_finance["region"].dropna().unique()),
        default=sorted(provider_finance["region"].dropna().unique()),
    )


    st.divider()



filtered = provider_finance[
    provider_finance["year"].between(year_range[0], year_range[1])
    & provider_finance["provider"].isin(selected_providers)
    & provider_finance["region"].isin(selected_regions)
].copy()

if filtered.empty:
    st.warning("No records match the selected filters. Adjust the year, provider, or region controls.")
    st.stop()

if section == "Main Finance Gap":
    vulnerability = load_vulnerability_data()
    owid_emissions = load_owid_emissions_data()
    st.subheader("Step 1: Main Finance Gap")
    st.write("Use this section to identify whether selected providers are directing enough climate finance toward adaptation.")
    render_overview(filtered)
    providers, regions, recipients = render_exploration(filtered)
    render_gap_insights(
        providers=providers,
        regions=regions,
        recipients=recipients,
        emissions=owid_emissions,
        vulnerability=vulnerability,
        filtered=filtered,
    )
    render_decision_support(providers)

elif section == "Recipient Finance":
    recipient_finance = load_recipient_finance_data()
    oecd_dac_history = load_oecd_dac_compiled_data()
    st.subheader("Step 2: Recipient Finance")
    st.write("Use this section to check which recipients receive climate finance and how earlier OECD DAC adaptation and mitigation finance changed over time.")
    render_recipient_finance(recipient_finance, year_range, selected_regions)
    render_oecd_dac_history(oecd_dac_history)

elif section == "Risk & Global Context":
    vulnerability = load_vulnerability_data()
    world_bank_context = load_world_bank_context_data()
    country_temperature = load_country_temperature_data()
    climate_indicators = load_climate_indicator_data()
    historical_emissions = load_historical_emissions_data()
    st.subheader("Step 3: Risk & Global Context")
    st.write("Use this section when you need supporting evidence about climate exposure, global development trends, and historical emissions.")
    render_climate_risk_context(country_temperature, climate_indicators, vulnerability)
    render_global_context(world_bank_context)
    render_historical_emissions(historical_emissions)

else:
    st.subheader("Data References")
    st.write(
        "Datasets used by Heuristic 5 and the dashboard sections they support."
    )
    st.dataframe(
        [
            {
                "Sub-heuristic": "Heuristic 5 - Climate Finance Gap",
                "Member": "Huang Neng Jie",
                "Dataset": "CRDF-PP_compact.csv",
                "Source": "OECD climate-related development finance - provider perspective",
                "Years Covered": "2013-2024",
            },
            {
                "Sub-heuristic": "Heuristic 5 - Climate Finance Gap",
                "Member": "Huang Neng Jie",
                "Dataset": "CRDF-RP_compact.csv",
                "Source": "OECD climate-related development finance - recipient perspective",
                "Years Covered": "2001-2024",
            },
            {
                "Sub-heuristic": "Heuristic 5 - Climate Finance Gap",
                "Member": "Huang Neng Jie",
                "Dataset": "Climate_vulnerability_climate_finance_ODA_and_protracted_crisis.csv",
                "Source": "Development Initiatives vulnerability, ODA, and climate finance dataset",
                "Years Covered": "Latest available dataset values",
            },
            {
                "Sub-heuristic": "Heuristic 5 - Climate Finance Gap",
                "Member": "Huang Neng Jie",
                "Dataset": "owid-co2-data.csv",
                "Source": "Our World in Data CO2 and greenhouse gas emissions",
                "Years Covered": "1750-2024",
            },
            {
                "Sub-heuristic": "Heuristic 5 - Climate Finance Gap",
                "Member": "Huang Neng Jie",
                "Dataset": "OECD_DAC_Climate_Finance_Data/oecd_dac_climate_finance_2009_2019_compiled.csv",
                "Source": "OECD DAC adaptation and mitigation finance compiled data",
                "Years Covered": "2009-2019",
            },
            {
                "Sub-heuristic": "Heuristic 5 - Climate Finance Gap",
                "Member": "Huang Neng Jie",
                "Dataset": "climate_change_converted_csv/*.csv",
                "Source": "World Bank Climate Change Knowledge Portal converted CSV files",
                "Years Covered": "1990-2008",
            },
            {
                "Sub-heuristic": "Heuristic 5 - Climate Finance Gap",
                "Member": "Huang Neng Jie",
                "Dataset": "API_WLD_DS2_en_csv_v2_4871/API_WLD_DS2_en_csv_v2_4871.csv",
                "Source": "World Bank World Development Indicators",
                "Years Covered": "Available World Bank indicator years",
            },
            {
                "Sub-heuristic": "Heuristic 5 - Climate Finance Gap",
                "Member": "Huang Neng Jie",
                "Dataset": "historical_emissions.csv",
                "Source": "Historical greenhouse gas emissions dataset",
                "Years Covered": "1990-2023",
            },
        ],
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    "Data sources include OECD climate-related development finance, Development Initiatives vulnerability data, "
    "Our World in Data emissions, converted World Bank climate data, World Development Indicators, and historical emissions data."
)







