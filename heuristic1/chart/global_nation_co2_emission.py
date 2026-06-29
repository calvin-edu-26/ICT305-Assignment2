import pandas as pd
import plotly.express as px

def chart(data: pd.DataFrame, geojson, year: int, percentile: float):
    snapshot = data[data["year"] == year]
    snapshot_percentile = snapshot["co2_including_luc"].quantile(percentile / 100)

    fig = px.choropleth_map(
        snapshot,
        geojson=geojson,
        locations="iso_code",
        featureidkey="properties.ISO_A3_EH",
        color="co2_including_luc",
        hover_name="country",
        color_continuous_scale="YlOrRd",
        range_color=(0, snapshot_percentile),
        zoom=1,
        center={"lat": 20, "lon": 0},
        labels={"co2_including_luc": "Annual CO₂ emission (Mt)"},
        height=700
    )

    return fig
