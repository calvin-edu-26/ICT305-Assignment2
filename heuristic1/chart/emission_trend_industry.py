import pandas as pd
import plotly.express as px

INDUSTRY_COLS = {
    "coal_co2": "Coal",
    "oil_co2": "Oil",
    "gas_co2": "Gas",
    "cement_co2": "Cement",
    "flaring_co2": "Flaring",
    "other_industry_co2": "Other",
    "land_use_change_co2": "Land-Use Change",
}

def chart(data: pd.DataFrame, years: range):
    snapshot = data[data["year"].between(years.start, years.stop)]
    annual = snapshot.groupby("year")[list(INDUSTRY_COLS.keys())].sum().reset_index()
    industry = annual.melt(id_vars="year", var_name="industry", value_name="co2")
    industry["industry"] = industry["industry"].map(INDUSTRY_COLS)

    fig = px.line(
        industry,
        x="year",
        y="co2",
        color="industry",
    )

    return fig