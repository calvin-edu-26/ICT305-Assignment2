import pandas as pd
import plotly.express as px
import plotly.colors as pc

def chart(data: pd.DataFrame, year: int, top: int):
    snapshot = data[data["year"] == year]

    top_countries = snapshot.sort_values("co2_including_luc", ascending=False).head(top)

    fig = px.bar(
        top_countries,
        x="co2_including_luc",
        y="country",
        labels={"co2": "CO₂ (million tonnes)", "country": ""}
    )

    fig.update_layout(yaxis=dict(autorange="reversed"))

    return fig
