import pandas as pd
import streamlit as st
from heuristic4.data.config import FILES
from heuristic4.loaders.helpers import clean_country_name

@st.cache_data
def load():

    co2 = pd.read_csv(FILES["co2"]).rename(columns={
        "Entity": "country",
        "Code": "country_code",
        "Year": "year",
        "Annual CO₂ emissions": "annual_co2"
    })

    co2["country"] = co2["country"].apply(clean_country_name)
    co2["annual_co2"] = pd.to_numeric(co2["annual_co2"], errors="coerce")

    return (
        co2
        .dropna(subset=["country_code"])
        .sort_values("year")
        .groupby(["country", "country_code"], as_index=False)
        .tail(1)
        [["country", "country_code", "annual_co2"]]
    )
