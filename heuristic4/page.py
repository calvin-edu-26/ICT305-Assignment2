import streamlit as st

from heuristic4.chart.population_pressure import chart as chart_population_pressure
from heuristic4.chart.density_map import chart as chart_density_map
from heuristic4.chart.sea_level import chart as chart_sea_level
from heuristic4.chart.adaptation_capacity import chart as chart_adaptation_capacity
from heuristic4.chart.risk_matrix import chart as chart_risk_matrix
from heuristic4.components.style import load_css
from heuristic4.components.story import (
    story_header, insight_box, risk_zone_legend, decision_support_box,
)
from heuristic4.components.recommendation import render as recommendation_box
from heuristic4.data.config import RISK_COLORS
from heuristic4.loaders.country_dataset import load as build_country_dataset
from heuristic4.loaders.sea_level import load as load_sea_level
from heuristic4.loaders.helpers import scenario_name

def sidebar_filters(country_df, sea_level_df):
    st.sidebar.header("Dashboard Filters")

    top_n = st.sidebar.slider(
        "Countries shown in ranking charts",
        min_value=5,
        max_value=30,
        value=15,
        step=5
    )

    selected_risk_zones = st.sidebar.multiselect(
        "Risk zones shown",
        options=list(RISK_COLORS.keys()),
        default=list(RISK_COLORS.keys())
    )

    scenario_list = sorted(sea_level_df["scenario"].dropna().unique())

    default_scenarios = [
        s for s in ["ssp126", "ssp245", "ssp585"]
        if s in scenario_list
    ]

    selected_scenarios = st.sidebar.multiselect(
        "Sea level projection scenarios",
        scenario_list,
        default=default_scenarios,
        format_func=scenario_name
    )

    selected_countries = st.sidebar.multiselect(
        "Countries shown in table",
        sorted(country_df["country"].dropna().unique())
    )

    filtered_df = country_df[
        country_df["risk_zone"].isin(selected_risk_zones)
    ].copy()

    return filtered_df, top_n, selected_scenarios, selected_countries

def render_header():

    st.markdown("""
<div class="hero">
<h1>Do countries that contribute less to climate change suffer more from its impacts?</h1>
<p>Exploring the unequal burden of climate change across countries</p>
</div>
""", unsafe_allow_html=True)

    with st.expander("How to use this dashboard"):
        st.write("""
        1. Use the sidebar filters to adjust countries, risk zones, and sea-level scenarios.
        2. Start with Chart 1 to identify countries under the most displacement pressure.
        3. Use Chart 2 to see where population concentration is located.
        4. Use Chart 3 to understand how sea-level rise may grow over time.
        5. Use Chart 4 to compare exposure, economic capacity, and CO₂ responsibility.
        6. Use Chart 5 to identify which countries may need support most urgently.
        """)

def render_overview(df):

    st.markdown("## Dashboard Overview")

    critical_count = (df["risk_zone"] == "Critical Risk").sum()

    highest_country = (
        df.sort_values("displacement_pressure", ascending=False).iloc[0]["country"]
        if len(df) > 0
        else "No data"
    )

    avg_exposure = df["popcount_exposure"].mean() if len(df) > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Countries analysed", f"{len(df):,}")
    col2.metric("Critical Risk countries", f"{critical_count:,}")
    col3.metric("Highest pressure country", highest_country)
    col4.metric("Average population exposed", f"{avg_exposure:,.0f}")

    st.divider()

def render_tab_1(df, top_n):

    story_header(
        "①",
        "Who is under pressure?",
        """
        This chart ranks countries with the highest displacement pressure based on exposed population and density.<br><br>
        Displacement pressure estimates how difficult and severe population displacement could become if environmental impacts force people to move.<br><br>
        <b>Displacement Pressure Index = log(1 + Population Exposed) × log(1 + Population Density)</b>
        """
    )

    st.plotly_chart(
        chart_population_pressure(df, top_n),
        use_container_width=True,
        theme="streamlit"
    )

    risk_zone_legend()

    insight_box(
        [
            "South Asian countries dominate the highest displacement pressure rankings.",
            "Bangladesh and India show the greatest pressure due to large exposed populations and dense settlement patterns.",
            "Critical Risk countries combine high displacement pressure with relatively lower economic capacity."
        ],
        "Displacement pressure is not determined by population size alone. Countries become more vulnerable when large numbers of people are concentrated in limited space, making relocation and adaptation more difficult during climate-related events such as sea level rise."
    )

    recommendation_box([
        "Prioritise climate adaptation funding for countries with the highest displacement pressure.",
        "Invest in resilient housing, coastal protection, and emergency shelters in densely populated coastal regions.",
        "Develop long-term relocation and land-use planning for communities most vulnerable to sea-level rise.",
        "Strengthen disaster preparedness and early warning systems in high-risk countries."
    ])

def render_tab_2(df):

    story_header(
        "②",
        "Where is the pressure located?",
        "This chart shows where populations are geographically concentrated and uses population density as an indicator of displacement pressure."
    )

    st.plotly_chart(
        chart_density_map(df),
        use_container_width=True,
        theme="streamlit"
    )

    insight_box(
        [
            "Population concentration is strongest across South Asia, East Asia, and parts of Europe.",
            "Regions with higher density may experience stronger displacement impacts when environmental hazards occur.",
            "Countries with lower density generally have more spatial flexibility for adaptation."
        ],
        "Population density is used as an indicator of displacement pressure because environmental disruption affects more people when populations are geographically concentrated. Dense urban and coastal regions may therefore experience larger social and infrastructure impacts."
    )

    recommendation_box([
        "Focus adaptation programmes in densely populated coastal regions where relocation is more difficult.",
        "Improve evacuation planning and disaster response for areas with large exposed populations.",
        "Encourage sustainable urban planning that reduces future climate vulnerability.",
        "Prioritise infrastructure upgrades in regions where population concentration increases climate risk."
    ])

def render_tab_3(sea_level_df, selected_scenarios):

    story_header(
        "③",
        "How will the threat grow over time?",
        "This chart shows how global sea level has changed in the past and how it may continue to rise in the future under different climate scenarios."
    )

    st.plotly_chart(
        chart_sea_level(sea_level_df, selected_scenarios),
        use_container_width=True,
        theme="streamlit"
    )

    insight_box(
        [
            "Sea level rises under all future climate scenarios.",
            "Strong climate action slows long-term growth but does not fully stop it.",
            "High-emission pathways produce substantially larger increases over time.",
            "The widening gap between scenarios suggests delayed climate action increases long-term adaptation costs."
        ],
        "The divergence between scenarios becomes larger after today's period, showing that current decisions strongly influence future outcomes. Even moderate mitigation significantly reduces long-term displacement pressure compared with worst-case pathways."
    )

    recommendation_box([
        "Accelerate emissions reduction to minimise long-term sea-level rise.",
        "Increase investment in coastal adaptation before projected impacts become more severe.",
        "Incorporate future climate scenarios into national infrastructure and urban planning.",
        "Expand long-term monitoring to support evidence-based adaptation strategies."
    ])

def render_tab_4(df):

    story_header(
        "④",
        "Can countries afford to adapt?",
        "This chart compares population exposure with GDP per capita while bubble size reflects responsibility through annual CO₂ emissions."
    )

    st.plotly_chart(
        chart_adaptation_capacity(df),
        use_container_width=True,
        theme="streamlit"
    )

    st.caption(
        "Note: Countries without available CO₂ values are excluded from this chart only. "
        "CO₂ bubble sizes use square-root scaling and are capped at the 97th percentile for readability."
    )

    insight_box(
        [
            "Countries with lower GDP per capita tend to face greater difficulty responding to population exposure.",
            "Larger bubbles indicate countries with higher annual CO₂ emissions.",
            "Several highly exposed countries are not necessarily the largest contributors to emissions."
        ],
        "This chart highlights a climate equity challenge: countries experiencing the greatest displacement exposure are often not the countries most responsible for emissions. Economic capacity influences how effectively countries can invest in protection, relocation, and long-term climate resilience."
    )

    recommendation_box([
        "Direct international climate finance towards highly exposed countries with limited economic capacity.",
        "Strengthen adaptation funding alongside emissions reduction efforts.",
        "Encourage technology transfer and capacity-building programmes for vulnerable developing nations.",
        "Support climate-resilient infrastructure where exposure is high but financial resources are limited."
    ])

def render_tab_5(df):

    story_header(
        "⑤",
        "Who needs help the most?",
        "This chart combines displacement pressure and economic capacity into a vulnerability matrix to identify countries needing the most support."
    )

    st.plotly_chart(
        chart_risk_matrix(df),
        use_container_width=True,
        theme="streamlit"
    )

    insight_box(
        [
            "Countries in the Critical Zone face both high displacement pressure and lower economic capacity.",
            "Prepared But Exposed countries face strong pressure but possess greater ability to adapt.",
            "Lower Risk countries generally combine lower pressure with stronger resilience."
        ],
        "This matrix identifies where support may be most urgently needed. Countries in the Critical Zone experience both elevated displacement pressure and lower economic readiness, suggesting that climate impacts are shaped not only by exposure but also by unequal adaptive capacity.",
        "Countries most in need of support are often not those most responsible for emissions — reinforcing the unequal burden of climate change."
    )

    recommendation_box([
        "Prioritise Critical Risk countries for immediate adaptation funding and international assistance.",
        "Allocate resources based on both displacement pressure and adaptive capacity rather than emissions alone.",
        "Use the risk categories to guide climate investment, humanitarian planning, and resilience programmes.",
        "Regularly reassess risk classifications as new climate and socioeconomic data become available."
    ])

    decision_support_box()

def render_tab_6(df, selected_countries):

    story_header(
        "⑥",
        "Country-level Dataset",
        "Use this table to inspect the indicators behind the dashboard."
    )

    if selected_countries:
        table_df = df[df["country"].isin(selected_countries)]
    else:
        table_df = df.sort_values(
            "displacement_pressure",
            ascending=False
        ).head(30)

    display_cols = [
        "country",
        "country_code",
        "popcount_exposure",
        "population_density",
        "displacement_pressure",
        "gdp_per_capita",
        "annual_co2",
        "co2_per_person_proxy",
        "risk_zone"
    ]

    st.dataframe(table_df[display_cols], use_container_width=True)

    st.download_button(
        "Download filtered dataset",
        table_df[display_cols].to_csv(index=False),
        "climate_dashboard_filtered_data.csv",
        "text/csv"
    )

def render_climate_dashboard():

    load_css()

    country_df = build_country_dataset()
    sea_level_df = load_sea_level()

    filtered_df, top_n, selected_scenarios, selected_countries = sidebar_filters(
        country_df,
        sea_level_df
    )

    render_header()
    render_overview(filtered_df)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "① Population Exposure",
        "② Global Density Map",
        "③ Sea Level Trend",
        "④ Adaptation Capacity",
        "⑤ Risk Matrix",
        "⑥ Data Table"
    ])

    with tab1:
        render_tab_1(filtered_df, top_n)

    with tab2:
        render_tab_2(filtered_df)

    with tab3:
        render_tab_3(sea_level_df, selected_scenarios)

    with tab4:
        render_tab_4(filtered_df)

    with tab5:
        render_tab_5(filtered_df)

    with tab6:
        render_tab_6(filtered_df, selected_countries)

    st.markdown("""
<div class="footer">
Data sources: World Bank, Sea Level Explorer, Our World in Data.
</div>
""", unsafe_allow_html=True)

# Streamlit executes this file directly through st.Page().
st.set_page_config(page_title="Sea Level Rise & Displacement", layout="wide")
render_climate_dashboard()

st.divider()
_, next_col = st.columns([15, 2])
with next_col:
    st.page_link("heuristic5/page.py", label="Next: Climate Finance →")