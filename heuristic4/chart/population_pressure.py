import pandas as pd
import plotly.express as px
from heuristic4.data.config import RISK_COLORS
from heuristic4.chart.style import clean_fig

def chart(df, top_n):

    plot_df = (
        df
        .query("population_total > 1000000")
        .sort_values("displacement_pressure", ascending=False)
        .head(top_n)
        .sort_values("displacement_pressure")
    )

    fig = px.bar(
        plot_df,
        x="displacement_pressure",
        y="country",
        orientation="h",
        color="risk_zone",
        title="Countries with Highest Displacement Pressure",
        labels={
            "displacement_pressure": "Displacement pressure index",
            "country": "Country",
            "risk_zone": "Risk zone"
        },
        color_discrete_map=RISK_COLORS,
        hover_data={
            "popcount_exposure": ":,.0f",
            "population_density": ":,.2f",
            "gdp_per_capita": ":,.0f",
            "annual_co2": ":,.0f"
        }
    )

    fig = clean_fig(fig, height=560)
    fig.update_layout(legend=dict(orientation="v", y=1, x=1.02))

    return fig
