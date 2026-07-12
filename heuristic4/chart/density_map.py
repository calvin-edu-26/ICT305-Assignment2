import numpy as np
import pandas as pd
import plotly.express as px
from heuristic4.chart.style import clean_fig

def chart(df):

    plot_df = df.copy()
    plot_df["density_display"] = np.log1p(plot_df["population_density"])

    fig = px.choropleth(
        plot_df,
        locations="country_code",
        color="density_display",
        hover_name="country",
        title="Global Population Density Map",
        color_continuous_scale=[
            [0, "#F8FAFC"],
            [0.2, "#FDE68A"],
            [0.5, "#FB923C"],
            [1, "#DC2626"]
        ],
        labels={"density_display": "Population Density"},
        hover_data={
            "population_density": ":,.2f",
            "popcount_exposure": ":,.0f",
            "gdp_per_capita": ":,.2f",
            "annual_co2": ":,.0f",
            "country_code": False,
            "density_display": False
        }
    )

    fig.update_geos(
        projection_type="natural earth",
        showcountries=True,
        countrycolor="#64748b",
        showcoastlines=True,
        coastlinecolor="#64748b",
        showframe=False,
        bgcolor="rgba(0,0,0,0)"
    )

    return clean_fig(fig, height=760)
