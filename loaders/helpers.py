import pandas as pd
from heuristic4.data.config import COUNTRY_RENAMES, SCENARIO_LABELS

def clean_country_name(name):

    if pd.isna(name):
        return name

    name = str(name).strip()
    return COUNTRY_RENAMES.get(name, name)

def scenario_name(code):

    return SCENARIO_LABELS.get(str(code), str(code))

def latest_year_value(df, id_cols):

    year_cols = [col for col in df.columns if str(col).isdigit()]

    long_df = df.melt(
        id_vars=id_cols,
        value_vars=year_cols,
        var_name="year",
        value_name="value"
    )

    long_df["year"] = pd.to_numeric(long_df["year"], errors="coerce")
    long_df["value"] = pd.to_numeric(long_df["value"], errors="coerce")

    return (
        long_df
        .dropna(subset=["value"])
        .sort_values("year")
        .groupby(id_cols, as_index=False)
        .tail(1)
    )

def classify_risk(row, median_pressure, median_gdp):


    high_pressure = row["displacement_pressure"] >= median_pressure
    high_gdp = row["gdp_per_capita"] >= median_gdp

    if high_pressure and not high_gdp:
        return "Critical Risk"

    if high_pressure and high_gdp:
        return "High Exposure, Higher Capacity"

    if not high_pressure and not high_gdp:
        return "Emerging Risk"

    return "Lower Risk"
