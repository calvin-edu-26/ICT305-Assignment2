import streamlit as st

from heuristic1.loaders import country_geojson, owid, edgar
from heuristic1.chart import global_nation_co2_emission, top_emission_nation, global_emission_trend, emission_trend_industry, top_emission_nation_income_group, bottom_emission_nation_per_capita, top_emission_nation_per_capita, top_emission_nation_sector
from heuristic1.components import insight, recommendation
from heuristic1.components.recommendation import Recommendation

# Data Source
owid_data = owid.load()
edgar_data = edgar.load()

# Data Source Reference
OWID_REF = "Source: Our World in Data — CO₂ and Greenhouse Gas Emissions dataset (owid-co2-data.csv)"
EDGAR_REF = "Source: IEA-EDGAR CO₂ (EDGAR_2025_GHG) — European Commission Joint Research Centre & IEA, September 2025"

# Section
def overview_section():
    st.header("Carbon Emissions by Nations")
    map, top = st.columns([3, 1])

    with map:
        selected_percentile = st.selectbox(
            "Percentile:",
            options=["95", "100"],
            index=0,
            width=100
        )

        st.caption("Color scale capped at 95th percentile to show distribution. Hover for exact values.")
        
        st.plotly_chart(
            global_nation_co2_emission.chart(
                    owid_data, 
                    country_geojson.load(), 
                    selected_year, 
                    float(selected_percentile)
                ), 
                use_container_width=True,
        )

    with top:
        top_number = 5
        st.subheader(f"Top {top_number} Countries by CO₂ Emissions")

        st.plotly_chart(
            top_emission_nation.chart(owid_data, selected_year, top_number)
        )

    st.caption(OWID_REF)

    insight.render([
        "Top **5** emission nations accounted to over **57%**: **China (28%)**, **United States (11.7%)**, **India (7.49%)**, **Russia (5.07%)**, **Brazil (4.87%)**.",
        "**4** out of **5** top emitters are major global oil-and-gas producers: **United States**, **Russia**, **China**, **Brazil**.",
        "**4** out of **5** top emitters are heavy on rapid industrialization and manufacturing: **Brazil**, **Russia**, **India**, **China**"
    ])

    recommendation.render([
        Recommendation("Ministries of Industry, Energy, and Trade", [
            "Implement strict, legal binding energy-efficiency standards targeting heavy manufacturing to reduce carbon footprint.",
            "Enforce zero-tolerance policies on methane venting and flaring towards oil-and-gas producers.",
            "Reduce financial subsidies for domestic oul and gas exploration, reallocate budgets into domestic renewable energy development.",
        ]),
        Recommendation("Upper Management of Oil and Gas Companies", [
            "Replace diesel-powered drilling rigs, pumps, and field equipment with fully electrified systems powered by renewable energy in phase to reduce carbon footprint on extraction operations.",
            "Deploy carbon capture systems at natural gas processing plants and refineries to mitigate carbon emissions.",
        ]),
        Recommendation("Multilateral Development Banks", [
            "Offer blended finance and partial credit guarantees to private investors funding industrial decarbonization projects.",
            "Cease underwriting, debt financing, and equity investments in new fossil fuel extraction, processing, or fossil-based power generation."
        ])
    ])

def global_emission_trend_section():
    st.header(f"Global Emission Trend ({start_year}-{end_year})")

    st.plotly_chart(
        global_emission_trend.chart(
            owid_data,
            range(start_year, end_year),
        )
    )

    st.caption(OWID_REF)

    recommendation.render([
        Recommendation("UN Loss and Damage Fund Adminstrators", [
            "Acknowlege that steep climb from 1950 to 2000 led to inevitable sea-level rise; prioritize funds for immediate coastal retreat and foritification in vulnerable regions.",
            "Impose steeper levy on high emission nations.",
        ]),
        Recommendation("Civil Infrastructure Planners", [
            "Implement strict zoning laws preventing new infrastructure in hazard zones with high emission.",
            "Build adaptive infrastructures to scale alongside future environmental risks; progressive expansion design to cater long-term needs of expected sea-level rise."
        ]),
    ])

def top_emission_nations_then_now_section():
    top_n = 20
    st.header(f"Top {top_n} Carbon Emission Nations - Then VS Now")

    then, now = st.columns(2, vertical_alignment="top")
    
    with then:
        st.subheader(f"{start_year}")
        st.plotly_chart(
            top_emission_nation_income_group.chart(owid_data, start_year, top_n)
                .update_layout(height=max(400, top_n * 28))
        )
        
    with now:
        st.subheader(f"{selected_year}")
        st.plotly_chart(
            top_emission_nation_income_group.chart(owid_data, selected_year, top_n)
                .update_layout(height=max(400, top_n * 28))    
        )

    st.caption(OWID_REF)

    insight.render([
        "In 1900, United States led carbon emission at roughly 2,100 Mt annually. By 2024, China took over and maxes at over 10,000 Mt. Top emission increased by more than **5x** over a century.",
        "Western industrial powers emitted the most in 1900. By 2024, top emission shifted to the manufacturing powerhouses in Asia - **China**, **India**, **Indonesia**, **Thailand**.",
    ])
    recommendation.render([
        Recommendation("Ministry of Environment", [
            "Mandate annual carbon footprint reduction plan and emission review enforced by law.",
            "Advocate decarbonization, strictly enfore global green trade standards and penalize high-emitting imports financially with taxes and levies.",
            "Finance clean energy patents to high emitting developing nations like **India** and **Vietnam** to expedite transition towards green energy.",
        ]),
        Recommendation("Ministry of Environment", [
            "Deploy real-time geospatial monitoring to instantly identify, penalize and shut down illegal logging and mining activities.",
            "Form a unified economic body to collectively dictate global climate finance terms to the top industrial superpowers.",
        ]),
    ])

def top_n_bottom_emission_nations_section():
    n = 20
    st.header(f"Top VS Bottom {n} Carbon Emission Nations")

    top, bottom = st.columns(2, vertical_alignment="top")

    with top:
        st.plotly_chart(
            top_emission_nation_per_capita.chart(owid_data, selected_year, n)
                .update_layout(height=max(400, n * 28)),
            use_container_width=True
        )

    with bottom:
        st.plotly_chart(
            bottom_emission_nation_per_capita.chart(owid_data, selected_year, n)
                .update_layout(height=max(400, n * 28)),
        )

    st.caption(OWID_REF)

    insight.render([
        "While countries like **China** and the **US** are the top emitters by raw numbers, top 20 list of per capita emission is heavily dominated by small, weathly petro-states - **Qatar**, **Brunei**, **Kuwait**, **Saudi Arabia**.",
        "Qatar, top emitter per capita contributed a staggering **40t** per person a year, which is almost **8x** of global average of **5t**.",
    ])

def top_emission_nation_sector_section():
    n = 20
    st.plotly_chart(
        top_emission_nation_sector.chart(edgar_data, selected_year, n)
            .update_layout(height=max(400, n * 28))
    )

    st.caption(EDGAR_REF)

# Layout
st.set_page_config(layout="wide")
with st.sidebar:
    st.header("Filters")

    selected_year = st.selectbox(
        "Year",
        # TODO: Change to actual year range base on data
        options=list(range(2024, 2009, -1)),
        index=0
    )

    start_year, end_year = st.slider(
        "Year range",
        # TODO: Change to actual year range base on data
        1900,
        2024,
        (1900, 2024)
    )

overview_section()
global_emission_trend_section()
top_emission_nations_then_now_section()
top_n_bottom_emission_nations_section()
top_emission_nation_sector_section()
