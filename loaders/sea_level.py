import pandas as pd
import streamlit as st
from heuristic4.data.config import FILES
from heuristic4.loaders.helpers import scenario_name

@st.cache_data
def load():

    observed = pd.read_excel(
        FILES["sea_level"],
        sheet_name="Observations-Extrapolation"
    ).rename(columns={
        "Year": "year",
        "Observation Extrapolation 50th": "sea_level_mm"
    })

    observed = observed[["year", "sea_level_mm"]].copy()
    observed["scenario"] = "Historical"
    observed["scenario_label"] = "Historical observations"

    future = pd.read_excel(FILES["sea_level"], sheet_name="Future-Total")

    if "quantile" in future.columns:
        future = future[future["quantile"] == 50]

    year_cols = [col for col in future.columns if str(col).isdigit()]

    future = future.melt(
        id_vars=["scenario"],
        value_vars=year_cols,
        var_name="year",
        value_name="sea_level_mm"
    )

    future["scenario_label"] = future["scenario"].apply(scenario_name)

    output = pd.concat([observed, future], ignore_index=True)

    output["year"] = pd.to_numeric(output["year"], errors="coerce")
    output["sea_level_mm"] = pd.to_numeric(output["sea_level_mm"], errors="coerce")

    return output.dropna(subset=["year", "sea_level_mm"])
