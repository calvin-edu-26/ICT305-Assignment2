import streamlit as st

from heuristic1.loaders import country_geojson, owid
from heuristic1.chart import global_nation_co2_emission

st.set_page_config(layout="wide")

with st.sidebar:
    st.header("Filters")

    selected_year = st.selectbox(
        "Year",
        options=list(range(2024, 2009, -1)), # TODO: Change to actual year range base on data
        index=0
    )

st.plotly_chart(
    global_nation_co2_emission.chart(owid.load(), country_geojson.load(), selected_year),
    use_container_width=True,
)