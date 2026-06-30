import streamlit as st

from heuristic1.loaders import country_geojson, owid, edgar
from heuristic1.chart import global_nation_co2_emission, top_emission_nation, emission_trend_industry, top_emission_nation_income_group, bottom_emission_nation_per_capita, top_emission_nation_per_capita, top_emission_nation_sector
from heuristic1.components import insight, recommendation
from heuristic1.components.recommendation import Recommendation

st.set_page_config(layout="wide")


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
                    owid.load(), 
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
            top_emission_nation.chart(owid.load(), selected_year, top_number)
        )


def top_emission_nations_then_now():
    top_n = 20
    st.header(f"Top {top_n} Carbon Emission Nations - Then VS Now")

    then, now = st.columns(2, vertical_alignment="top")
    
    with then:
        st.subheader(f"{start_year}")
        st.plotly_chart(
            top_emission_nation_income_group.chart(owid.load(), start_year, top_n)
                .update_layout(height=max(400, top_n * 28))
        )
        
        insight.render("Just the top 20 countries generate the majority of global CO₂. Pressure on these governments — especially the wealthiest among them — offers the fastest path to meaningful cuts.")
        recommendation.render([
            Recommendation("National Policymakers", ["Develop sector-specific legislation — a carbon price alone is insufficient; targeted regulations on buildings, transport, and agriculture are needed alongside it."])
        ])

    with now:
        st.subheader(f"{selected_year}")
        st.plotly_chart(
            top_emission_nation_income_group.chart(owid.load(), selected_year, top_n)
                .update_layout(height=max(400, top_n * 28))    
        )


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

def top_n_bottom_emission_nations_section():
    top, bottom = st.columns(2, vertical_alignment="top")
    n = 20

    with top:
        st.plotly_chart(
            top_emission_nation_per_capita.chart(owid.load(), selected_year, n)
                .update_layout(height=max(400, n * 28)),
            use_container_width=True
        )

    with bottom:
        st.plotly_chart(
            bottom_emission_nation_per_capita.chart(owid.load(), selected_year, n)
                .update_layout(height=max(400, n * 28)),
        )

def top_emission_nation_sector_section():
    n = 20
    st.plotly_chart(
        top_emission_nation_sector.chart(edgar.load(), selected_year, n)
            .update_layout(height=max(400, n * 28))
    )

overview_section()
st.subheader(
    f"Global CO₂ Emissions Trend by Industry ({start_year}–{end_year})")
st.plotly_chart(emission_trend_industry.chart(
    owid.load(), range(start_year, end_year)))
top_emission_nations_then_now()
top_n_bottom_emission_nations_section()
top_emission_nation_sector_section()
