from pathlib import Path
import pandas as pd
import streamlit as st
from heuristic4.loaders.helpers import clean_country_name, latest_year_value

@st.cache_data
def load(file_path, value_name):

    df = pd.read_csv(file_path, skiprows=4)

    latest = latest_year_value(
        df,
        ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
    )

    latest = latest.rename(columns={
        "Country Name": "country",
        "Country Code": "country_code",
        "value": value_name
    })

    latest["country"] = latest["country"].apply(clean_country_name)

    return latest[["country", "country_code", value_name]]
