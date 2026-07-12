import numpy as np
import pandas as pd
import streamlit as st
from heuristic4.data.config import FILES
from heuristic4.loaders.co2 import load as load_co2
from heuristic4.loaders.world_bank import load as load_world_bank
from heuristic4.loaders.population_density import load as load_population_density
from heuristic4.loaders.helpers import classify_risk

@st.cache_data
def load():
    co2 = load_co2()
    gdp = load_world_bank(FILES["gdp"], "gdp_per_capita")
    population = load_world_bank(FILES["population"], "population_total")
    exposure = load_population_density()

    df = (
        exposure
        .merge(gdp[["country_code", "gdp_per_capita"]], on="country_code", how="left")
        .merge(population[["country_code", "population_total"]], on="country_code", how="left")
        .merge(co2[["country_code", "annual_co2"]], on="country_code", how="left")
    )

    df = df.dropna(subset=[
        "popcount_exposure",
        "population_density",
        "gdp_per_capita"
    ])

    df = df[
        (df["popcount_exposure"] > 0)
        & (df["population_density"] > 0)
        & (df["gdp_per_capita"] > 0)
    ].copy()

    # Custom index used to estimate displacement pressure.
    df["displacement_pressure"] = (
        np.log1p(df["popcount_exposure"])
        * np.log1p(df["population_density"])
    )

    # CO₂ per person proxy adds a responsibility comparison.
    df["co2_per_person_proxy"] = (
        df["annual_co2"] / df["population_total"].replace(0, pd.NA)
    )

    median_pressure = df["displacement_pressure"].median()
    median_gdp = df["gdp_per_capita"].median()

    df["risk_zone"] = df.apply(
        lambda row: classify_risk(row, median_pressure, median_gdp),
        axis=1
    )

    return df

def get_critical_risk_count():
    """
    Returns the total number of countries classified
    as Critical Risk.
    """

    country_df = load()

    return int(
        (country_df["risk_zone"] == "Critical Risk").sum()
    )
