import numpy as np
import pandas as pd
import plotly.express as px
from heuristic4.data.config import RISK_COLORS
from heuristic4.chart.style import clean_fig

def chart(df):

    plot_df = df.copy()

    plot_df["pressure_display"] = plot_df["displacement_pressure"].clip(
        upper=plot_df["displacement_pressure"].quantile(0.95)
    )

    plot_df["gdp_display"] = plot_df["gdp_per_capita"].clip(
        upper=plot_df["gdp_per_capita"].quantile(0.90)
    )

    plot_df["population_display"] = plot_df["popcount_exposure"].clip(
        upper=plot_df["popcount_exposure"].quantile(0.95)
    )

    plot_df["log_gdp"] = np.log1p(plot_df["gdp_display"])

    median_pressure = plot_df["pressure_display"].median()
    median_gdp = plot_df["log_gdp"].median()

    fig = px.scatter(
        plot_df,
        x="pressure_display",
        y="log_gdp",
        size="population_display",
        color="risk_zone",
        hover_name="country",
        title="Country Displacement Vulnerability Matrix",
        labels={
            "pressure_display": "Higher → More displacement pressure",
            "log_gdp": "Higher → Greater economic capacity",
            "population_display": "Population exposed",
            "risk_zone": "Risk zone"
        },
        color_discrete_map=RISK_COLORS,
        hover_data={
            "population_density": ":,.2f",
            "gdp_per_capita": ":,.2f",
            "popcount_exposure": ":,.0f",
            "annual_co2": ":,.0f",
            "co2_per_person_proxy": ":,.4f",
            "pressure_display": False,
            "log_gdp": False,
            "population_display": False
        }
    )

    fig.add_vline(
        x=median_pressure,
        line_dash="dash",
        line_color="#334155",
        annotation_text="Median Displacement Pressure",
        annotation_position="top left"
    )

    fig.add_hline(
        y=median_gdp,
        line_dash="dash",
        line_color="#334155",
        annotation_text="Median Economic Capacity",
        annotation_position="bottom right"
    )

    fig.update_traces(marker=dict(opacity=0.8))

    return clean_fig(fig, height=760)
