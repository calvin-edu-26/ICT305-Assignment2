import pandas as pd
import streamlit as st

NON_COUNTRY_VALUES = ["Africa", "Africa (GCP)", "Asia", "Asia (GCP)", "Asia (excl. China and India)", "Central America (GCP)", "Europe", "Europe (GCP)", "Europe (excl. EU-27)", "Europe (excl. EU-28)", "European Union (27)", "European Union (28)", "High-income countries", "International aviation", "Kuwaiti Oil Fires", "Least developed countries (Jones et al.)", "Low-income countries", "Lower-middle-income countries", "Middle East (GCP)", "Non-OECD (GCP)", "North America", "North America (excl. USA)", "OECD (GCP)", "OECD (Jones et al.)", "Oceania", "Oceania (GCP)", "South America", "South America (GCP)", "Upper-middle-income countries", "World"]

@st.cache_data
def load() -> pd.DataFrame:
    df = pd.read_csv("heuristic1/data/owid-co2-data.csv")
    df = df[-df["country"].isin(NON_COUNTRY_VALUES)]
    return df