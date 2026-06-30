import pandas as pd
import plotly.express as px
import plotly.colors as pc


def chart(data: pd.DataFrame, year: int, top: int):
    snapshot = data[data["year"] == year]

    sorted = snapshot.sort_values("co2_including_luc", ascending=False)
    top_countries = sorted.head(top)
    other_total = sorted.iloc[top:]["co2_including_luc"].sum()

    chart_data = pd.concat([
        top_countries,
        pd.DataFrame([{"country": "Other", "co2_including_luc": other_total}])
    ])

    fig = px.pie(
        chart_data,
        names="country",
        values="co2_including_luc",
        color="country",
        color_discrete_map={"Other": "lightgray"},
    )

    fig.update_traces(
        textinfo="label+percent",
    )

    return fig
