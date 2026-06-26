import streamlit as st

from heuristic1.loaders import country_geojson, owid
from heuristic1.chart import global_nation_co2_emission, top_emission_nation, emission_trend_industry

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

st.title("Carbon Emissions by Nations")
overview_section()
st.subheader(f"Global CO₂ Emissions Trend by Industry ({start_year}–{end_year})")
st.plotly_chart(emission_trend_industry.chart(owid.load(), range(start_year, end_year)))
