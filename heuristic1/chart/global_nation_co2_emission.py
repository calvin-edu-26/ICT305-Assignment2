import pandas as pd
import plotly.express as px

def chart(data: pd.DataFrame, geojson, year: int):
    snapshot = data[data["year"] == year]
    p95 = snapshot["co2_including_luc"].quantile(0.95)

    fig = px.choropleth_map(
        snapshot,
        geojson=geojson,
        locations="iso_code",
        featureidkey="properties.ISO_A3_EH",
        color="co2_including_luc",
        hover_name="country",
        color_continuous_scale="YlOrRd",
        range_color=(0, p95),
        zoom=1,
        center={"lat": 20, "lon": 0},
        height=700
    )

    return fig
