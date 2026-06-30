import pandas as pd
import plotly.express as px

def chart(data: pd.DataFrame, year_range: range):
    snapshot = data[data["year"].between(year_range.start, year_range.stop)]
    groupby_year = snapshot.groupby("year")["co2_including_luc"].sum().reset_index()

    fig = px.line(
        groupby_year,
        x="year",
        y="co2_including_luc",
        labels={"co2_including_luc": "Annual CO₂ Emission (Mt)", "year": "Year"}
    )

    fig.update_traces(fill="tozeroy")

    return fig