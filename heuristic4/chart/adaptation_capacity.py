import numpy as np
import pandas as pd
import plotly.express as px
from heuristic4.data.config import RISK_COLORS
from heuristic4.chart.style import clean_fig

def chart(df):

    plot_df = df.dropna(subset=["annual_co2"]).copy()
    plot_df = plot_df[plot_df["annual_co2"] > 0]

    plot_df["co2_size"] = np.sqrt(plot_df["annual_co2"])
    plot_df["co2_size"] = plot_df["co2_size"].clip(
        upper=plot_df["co2_size"].quantile(0.97)
    )

    fig = px.scatter(
        plot_df,
        x="gdp_per_capita",
        y="popcount_exposure",
        size="co2_size",
        size_max=28,
        color="risk_zone",
        hover_name="country",
        log_x=True,
        log_y=True,
        title="Population Exposure Compared with Economic Capacity (GDP per Capita)",
        labels={
            "gdp_per_capita": "GDP per capita",
            "popcount_exposure": "Population exposed",
            "co2_size": "Annual CO₂ emissions",
            "risk_zone": "Risk zone"
        },
        color_discrete_map=RISK_COLORS,
        hover_data={
            "annual_co2": ":,.0f",
            "population_density": ":,.2f",
            "co2_per_person_proxy": ":,.4f",
            "co2_size": False
        }
    )

    fig.update_traces(
        marker=dict(opacity=0.72, line=dict(width=0.7, color="white"))
    )

    return clean_fig(fig, height=720)
