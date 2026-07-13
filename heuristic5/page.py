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
from components import insight, recommendation
from components.recommendation import Recommendation
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


# Data Source
try:
    provider_finance = load_provider_finance_data()
except ImportError as exc:
    st.error(
        "This dashboard needs Excel-reading support because some supplied files are workbooks "
        "even though they use .csv or .xls names. Install the missing reader and rerun Streamlit."
    )
    st.exception(exc)
    st.stop()


# Data Source Reference
OECD_PROVIDER_REF = (
    "Source: OECD climate-related development finance - provider perspective "
    "(CRDF-PP_compact.csv)"
)
OECD_RECIPIENT_REF = (
    "Source: OECD climate-related development finance - recipient perspective "
    "(CRDF-RP_compact.csv)"
)
VULNERABILITY_REF = (
    "Source: Development Initiatives vulnerability, ODA, and climate finance dataset "
    "(Climate_vulnerability_climate_finance_ODA_and_protracted_crisis.csv)"
)
OWID_REF = "Source: Our World in Data - CO2 and greenhouse gas emissions (owid-co2-data.csv)"
OECD_DAC_REF = (
    "Source: OECD DAC adaptation and mitigation finance compiled data "
    "(oecd_dac_climate_finance_2009_2019_compiled.csv)"
)
WORLD_BANK_REF = (
    "Source: World Bank Climate Change Knowledge Portal and World Development Indicators"
)
HISTORICAL_EMISSIONS_REF = "Source: Historical greenhouse gas emissions dataset (historical_emissions.csv)"


def filter_provider_finance():
    filtered_data = provider_finance[
        provider_finance["year"].between(year_range[0], year_range[1])
        & provider_finance["provider"].isin(selected_providers)
        & provider_finance["region"].isin(selected_regions)
    ].copy()

    if filtered_data.empty:
        st.warning("No records match the selected filters. Adjust the year, provider, or region controls.")
        st.stop()

    return filtered_data


def render_analysis_notes(label: str, insights: list[str], recommendations: list[Recommendation]):
    with st.expander(label, expanded=False):
        insight.render(insights)
        recommendation.render(recommendations)


# Section
def overview_section(filtered_data):
    st.header("Climate Finance Gap")
    st.caption(
        "A decision-support dashboard for checking whether major providers are delivering enough "
        "adaptation finance to vulnerable recipients."
    )

    render_overview(filtered_data)
    st.caption(OECD_PROVIDER_REF)

    render_analysis_notes(
        "📖 Analysis — Chart 1: What this shows / What you can do",
        [
            "Climate finance should not be judged only by total committed dollars; the key equity question is whether enough money is reaching adaptation needs.",
            "A high mitigation total can still leave climate-vulnerable countries under-supported when adaptation finance remains a smaller share of commitments.",
            "The selected year range and provider filters allow stakeholders to test whether major donors are improving their adaptation commitment over time.",
        ],
        [
            Recommendation("UN Climate Finance Negotiators", [
                "Use adaptation share as a headline accountability measure alongside total climate finance.",
                "Request provider-level reporting that separates adaptation, mitigation, and overlapping climate finance commitments.",
                "Prioritise follow-up with providers whose total climate finance is high but adaptation share remains low.",
            ]),
            Recommendation("Climate Finance Analysts", [
                "Compare finance trends over multiple years instead of relying on a single commitment year.",
                "Track whether adaptation finance grows in vulnerable regions rather than only in easier-to-fund mitigation projects.",
            ]),
        ],
    )


def provider_and_region_section(filtered_data):
    st.header("Provider Commitments and Recipient Regions")

    providers, regions, recipients = render_exploration(filtered_data)
    st.caption(OECD_PROVIDER_REF)

    render_analysis_notes(
        "📖 Analysis — Chart 2: What this shows / What you can do",
        [
            "Provider totals reveal who is committing the largest amount of climate finance, while adaptation share shows whether that finance is aligned with climate resilience.",
            "Regional allocation exposes whether finance is concentrated in a few recipient regions or distributed toward places with larger adaptation needs.",
            "Recipient-level adaptation versus mitigation patterns help identify countries receiving climate finance that may not match their resilience priorities.",
        ],
        [
            Recommendation("Development Finance Institutions", [
                "Set minimum adaptation-share benchmarks for portfolios that serve highly exposed regions.",
                "Review recipient regions with high climate risk but comparatively low adaptation finance commitments.",
                "Use recipient-level scatter patterns to find countries where mitigation-heavy support should be balanced with resilience funding.",
            ]),
            Recommendation("Recipient Governments", [
                "Use the provider and region comparison to identify which donors are most likely to support adaptation programmes.",
                "Frame funding requests around concrete adaptation gaps rather than broad climate finance needs.",
            ]),
        ],
    )

    return providers, regions, recipients


def finance_gap_section(filtered_data, providers, regions, recipients):
    st.header("Emitter Responsibility and Adaptation Gap")

    vulnerability = load_vulnerability_data()
    owid_emissions = load_owid_emissions_data()
    render_gap_insights(
        providers=providers,
        regions=regions,
        recipients=recipients,
        emissions=owid_emissions,
        vulnerability=vulnerability,
        filtered=filtered_data,
    )
    st.caption(f"{OWID_REF} | {VULNERABILITY_REF} | {OECD_PROVIDER_REF}")

    render_analysis_notes(
        "📖 Analysis — Chart 3: What this shows / What you can do",
        [
            "The emissions comparison links provider responsibility to adaptation support, showing whether large emitters are contributing proportionally to resilience finance.",
            "Funding-per-capita patterns can reveal vulnerable countries that receive limited support even when climate exposure is high.",
            "Sector-level adaptation finance shows whether commitments are aimed at practical resilience needs such as water, agriculture, disaster risk, and infrastructure.",
        ],
        [
            Recommendation("Loss and Damage Fund Administrators", [
                "Use emissions responsibility and adaptation delivery together when prioritising provider follow-up.",
                "Flag high-emitting providers with low adaptation-per-emissions support for stronger contribution discussions.",
                "Direct new funding windows toward vulnerable countries with low funding per capita.",
            ]),
            Recommendation("National Climate Planning Teams", [
                "Connect adaptation funding requests to measurable vulnerability indicators.",
                "Separate urgent resilience sectors from mitigation projects when preparing donor proposals.",
            ]),
        ],
    )


def decision_support_section(providers):
    st.header("Decision Support")

    render_decision_support(providers)
    st.caption(OECD_PROVIDER_REF)

    render_analysis_notes(
        "📖 Analysis — Chart 4: What this shows / What you can do",
        [
            "The decision table turns the dashboard into a provider comparison tool for identifying strong and weak adaptation performers.",
            "Providers with large total finance but low adaptation share are priority cases for policy dialogue.",
        ],
        [
            Recommendation("Policy Advisors", [
                "Rank providers by adaptation share before preparing negotiation briefs.",
                "Use the table to identify which providers require evidence-based follow-up on adaptation commitments.",
            ]),
            Recommendation("Programme Managers", [
                "Use provider-level totals to shortlist likely partners for adaptation-focused projects.",
                "Pair financial scale with adaptation share so large but mitigation-heavy providers are not mistaken for resilience leaders.",
            ]),
        ],
    )


def recipient_finance_section():
    st.header("Recipient Finance and Historical OECD DAC Trends")

    recipient_finance = load_recipient_finance_data()
    oecd_dac_history = load_oecd_dac_compiled_data()
    render_recipient_finance(recipient_finance, year_range, selected_regions)
    render_oecd_dac_history(oecd_dac_history)
    st.caption(f"{OECD_RECIPIENT_REF} | {OECD_DAC_REF}")

    render_analysis_notes(
        "📖 Analysis — Chart 5: What this shows / What you can do",
        [
            "Recipient-side data checks whether committed finance is visible from the perspective of the countries and regions receiving support.",
            "Historical OECD DAC trends provide context for whether adaptation has been catching up with mitigation over time.",
            "A recipient view helps avoid judging climate finance only from donor announcements.",
        ],
        [
            Recommendation("Recipient Country Ministries", [
                "Compare provider-perspective and recipient-perspective finance before relying on headline donor totals.",
                "Use historical DAC trends to argue for sustained adaptation support, not one-year increases.",
            ]),
            Recommendation("International NGOs", [
                "Monitor whether finance reaches countries facing repeated climate shocks.",
                "Use recipient evidence to support advocacy for transparent climate finance delivery.",
            ]),
        ],
    )


def risk_and_global_context_section():
    st.header("Climate Risk and Global Context")

    vulnerability = load_vulnerability_data()
    world_bank_context = load_world_bank_context_data()
    country_temperature = load_country_temperature_data()
    climate_indicators = load_climate_indicator_data()
    historical_emissions = load_historical_emissions_data()

    render_climate_risk_context(country_temperature, climate_indicators, vulnerability)
    render_global_context(world_bank_context)
    render_historical_emissions(historical_emissions)
    st.caption(f"{VULNERABILITY_REF} | {WORLD_BANK_REF} | {HISTORICAL_EMISSIONS_REF}")

    render_analysis_notes(
        "📖 Analysis — Chart 6: What this shows / What you can do",
        [
            "Climate risk context explains why adaptation finance is an equity issue rather than only a budget issue.",
            "World Bank and historical emissions indicators connect current finance decisions to wider development capacity and long-term responsibility.",
            "Combining finance, risk, and emissions evidence supports stronger recommendations than a finance-only view.",
        ],
        [
            Recommendation("UN and IPCC Working Groups", [
                "Use risk indicators to justify adaptation finance targets for highly exposed countries.",
                "Combine development capacity with historical responsibility when discussing fair provider contributions.",
                "Treat climate finance as part of climate justice evidence, not only as aid accounting.",
            ]),
            Recommendation("Research Teams", [
                "Use global context indicators to explain why similar finance totals can have different effects across regions.",
                "Document where historical emitters and current finance providers diverge.",
            ]),
        ],
    )


def data_references_section():
    st.header("Data References")
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


# Layout
st.set_page_config(layout="wide")
with st.sidebar:
    st.header("Filters")

    min_year, max_year = int(provider_finance["year"].min()), int(provider_finance["year"].max())
    year_range = st.slider(
        "Commitment year range",
        min_year,
        max_year,
        (max(min_year, 2018), max_year),
    )

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


filtered = filter_provider_finance()

overview_section(filtered)
providers_view, regions_view, recipients_view = provider_and_region_section(filtered)
finance_gap_section(filtered, providers_view, regions_view, recipients_view)
decision_support_section(providers_view)
recipient_finance_section()
risk_and_global_context_section()
