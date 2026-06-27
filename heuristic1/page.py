import streamlit as st

from heuristic1.loaders import country_geojson, owid, edgar
from heuristic1.chart import global_nation_co2_emission, top_emission_nation, emission_trend_industry, top_emission_nation_income_group, bottom_emission_nation_per_capita, top_emission_nation_per_capita, top_emission_nation_sector

st.set_page_config(layout="wide")


def overview_section():
    map, top = st.columns([3, 1])

    with map:
        st.plotly_chart(
            global_nation_co2_emission.chart(
                owid.load(), country_geojson.load(), selected_year),
            use_container_width=True,
        )

    with top:
        top_number = 5
        st.subheader(f"Top {top_number} Countries by CO₂ Emissions")

        st.plotly_chart(
            top_emission_nation.chart(owid.load(), selected_year, top_number)
        )


def top_emission_nations_then_now():
    then, now = st.columns(2, vertical_alignment="top")
    top_n = 20

    with then:
        st.plotly_chart(top_emission_nation_income_group.chart(
            owid.load(), start_year, top_n))

    with now:
        st.plotly_chart(top_emission_nation_income_group.chart(
            owid.load(), selected_year, top_n))


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

st.title("Carbon Emissions by Nations")
overview_section()
st.subheader(
    f"Global CO₂ Emissions Trend by Industry ({start_year}–{end_year})")
st.plotly_chart(emission_trend_industry.chart(
    owid.load(), range(start_year, end_year)))
top_emission_nations_then_now()
top_n_bottom_emission_nations_section()
top_emission_nation_sector_section()
