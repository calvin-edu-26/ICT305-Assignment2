import pandas as pd
import streamlit as st
from heuristic4.data.config import FILES
from heuristic4.loaders.helpers import clean_country_name

@st.cache_data
def load():

    workbook = pd.ExcelFile(FILES["density"])

    pop_sheet = next(s for s in workbook.sheet_names if "popcount" in s.lower())
    density_sheet = next(s for s in workbook.sheet_names if "popdensity" in s.lower())

    pop = pd.read_excel(FILES["density"], sheet_name=pop_sheet)
    density = pd.read_excel(FILES["density"], sheet_name=density_sheet)

    pop_value_col = [c for c in pop.columns if c not in ["code", "name"]][0]
    density_value_col = [c for c in density.columns if c not in ["code", "name"]][0]

    pop = pop.rename(columns={
        "code": "country_code",
        "name": "country",
        pop_value_col: "popcount_exposure"
    })

    density = density.rename(columns={
        "code": "country_code",
        "name": "country",
        density_value_col: "population_density"
    })

    output = pop[["country_code", "country", "popcount_exposure"]].merge(
        density[["country_code", "population_density"]],
        on="country_code",
        how="inner"
    )

    output["country"] = output["country"].apply(clean_country_name)
    output["popcount_exposure"] = pd.to_numeric(output["popcount_exposure"], errors="coerce")
    output["population_density"] = pd.to_numeric(output["population_density"], errors="coerce")

    return output
