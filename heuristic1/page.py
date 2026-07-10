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
        Recommendation("Ministries of Foreign Affaris & Climate Trade Negotiators (High-Emitting Nations)", [
            "**Establish \"Green Trade Channels\"**: Partner with high-emitting countries as collaborative effort to expedite border processing targetting clean technologies, increasing accessibility and affordability of those equipments.",
            "**Tie International Aid to Clean Energy**: Structure agreements to fund solar or wind power rather than coal-dependent projects for financial aid and infrastructure loans to developing countries.",
            "**Implement Graduated Import Fees**: Introduce border fees on raw industrial imports (like cement or metal) that involves carbon-emitting production cycle, encourage transition towards green energy.",
        ]),
        Recommendation("Global Carbon Standard & Certification Boards", [
            "**Redefine Product Footprint Baselines**: Create strict, localized criteria for certifying carbon-neutral products.",
            "**Standardize Supply Chain Ledgers**: Deploy transparent digital tracking tools for international trade, forcing companies to declare the total emissions embedded in goods imported from the top 5 heavy emitters.",
            "**Publish Transparent Multi-Scale Data Dashboards**: Build public data platforms that show both absolute emissions and capped statistical views, preventing high-emitting entities from hiding behind misleading visual scales.",
        ]),
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
        Recommendation("Ministries of Finance", [
            "**Launch 10-Year Phased Subsidy Shifting**: Create step-by-step plan to slowly reduce tax breaks for fossil fuel drilling, ensuring those funds are reallocated for domestic battery storage grids development.",
            "**Enact Carbon Fees**: Introduce gradually increasing fee on industrial carbon output, giving businesses a clear, multi-year timeline to update their equipment.",
            "**Incentivize Long-Term Corporate Investments**: Offer corporate tax credits to buinesses that invest their private capital in renewal energy projects.",
        ]),
        Recommendation("Energy Quantitative Analysts", [
            "**Discount Short-Term Anomalies**: Train predictie market alhorithms to ignore brief, crisis-driven economic contractions, preventing false optimism on natural emissions drops.",
            "**Model Extreme Deployment Targets**: Publish clear, data-backed reports tracking the exact volume of renewable enerfy capacity required annually to maintain current emission level.",
            "**Provide Transparent Metric Transitions**: Present enerfy market data explicitly linking annual fuel consumption rates directly to the long-term, compounding atmospheric build-up."
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
        Recommendation("Multilateral Development Banks", [
            "**De-Risk Private Renewable Investment**: Use public development funds to absorb the first layer of financial loss on clean energy projects in emerging markets, making it appealing for private investors to fund solar arrays.",
            "**Provide Lower-Interest Loans for Green Projects**: Offer competitive, below-market interest rates for public infrastructure projects that substitue carbon-heavy alternatives."
        ]),
        Recommendation("Ministries of Industry & Investment Promotion - Emerging Countries", [
            "**Enact Green Foreign Direct Investment (FDI) Rules**: Require internaltional corporations expanding factories in the country to build dedicated solar or wind systems to power their new facilities.",
            "**Subsidize Factory Electrification**: Provide state-backed tax credits for domestic factories that replace old fossil-fuel boilers with high-temperature electric heat pumps.",
            "**Establish Low-Carbon Industrial Parks**: Zone new manufacturing zones with shared, pre-installed green infrastructure, such as centralized waste-heat recovery systems and solar microgrids.",
            "**Mandate Digital Energy Tracking**: Require all mid-sized and large factories to use automated software to track power waste and keep their energy consumption stable as production scales."
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

    recommendation.render([
        Recommendation("Ministries of Housing and Urban Planning (High Per-Capita Countries)", [
            "**Update Building Codes for Climate Reality**: Mandate that new residential and commercial buildings feature thick insulation, double-paned windows, and smart heating/cooling systems.",
            "**Introduce Tiered Utility Pricing**: Implement a progressive billing systems for electricity and water where baseline usage is highly affordable, but excessive household luxury consumption is taxed at higher rates.",
            "**Fund Energy-Efficiency Home Rebates**: Provide simple, upfront cash-back incentives for middle-income houseowners who replace old fossil-gas furnaces with modern electric heat pumps.",
            "**Require Solar Integration on Large Roofs**: Mandate all new massive commercial buildings install rooftop solar panels to power cooling equipments."
        ]),
        Recommendation("UN Loss & Damage Administrators", [
            "**Apportion Funding Metrics via Cumulative Per-Capita History**: Calculate mandatory donor country contributions based on duration the nation has operated above the global per-capita average.",
            "**Finance Micro-Farming Climate Resilience**: Fund local programs that provide drought-resistant seeds and solar-powered water pumps directly to smallholder farmers in vulnerable zones.",
        ]),
    ])

def top_emission_nation_sector_section():
    n = 20
    st.header(f"Top {n} Emitting Nations: Annual CO₂ Emissions by Sector")

    st.plotly_chart(
        top_emission_nation_sector.chart(edgar_data, selected_year, n)
            .update_layout(height=max(400, n * 28))
    )

    st.caption(EDGAR_REF)

    insight.render([
        "The chart reveals that one-size-fits-all approach to tackle global decarbonization will fail as structural makeup of emissions varies between top emitting nations.",
        "**China** & **India** were heavy on power industry and manufacturing combusion.",
        "**United States** has significant power sector and massive road transportation footprint.",
    ])

    recommendation.render([
        Recommendation("City Planners", [
            "**Electrify city-owned vehicles**: Swap out public transit buses, garbage trucks, and government vehicles with electric-powered version.",
            "**Create dedicated bus lanes**: Designate special lanes for public buses to improve travel time, incentivize commuters to take public transport.",
            "**Plan Self-Sustainable Neighbourhood**: Structure suburbs with staple amenities like groceries, schools, and clinics within walking distance, reducing car dependence.",
            "**Plant urban tree canopies**: Plant trees along city streets to naturally cool down neighbourhoods, reducing needs of air-condition cooling.",
        ]),
        Recommendation("Fleet Operations Managers & Corporate Logistic Directors", [
            "**Deploy Route Optimization Software**: Mandate the use of GPS-based routing systems to systematically avoid redundant miles, cutting diesel usage.",
            "**Shift Freight to Electrified Rail**: Cooperate with rail authorities to move heavy cargo containers off long-distance highways onto electric train networks.",
            "**Enforce Weekly Tire Checks**: Implement mandatory, systematic tire inflation checks across all fleet vehicles, ensuring tires are properly inflated to optimize fuel efficiency.",
        ]),
    ])

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
