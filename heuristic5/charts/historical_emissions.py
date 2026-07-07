import pandas as pd
import plotly.express as px
import streamlit as st


def render_historical_emissions(historical_emissions: pd.DataFrame) -> None:
    st.subheader("Historical Emissions Context")
    view = historical_emissions[
        historical_emissions["Gas"].astype(str).str.contains("CO2|CO", case=False, na=False)
        & historical_emissions["Sector"].astype(str).str.contains("Total", case=False, na=False)
    ].copy()
    if view.empty:
        view = historical_emissions.copy()
    latest_year = view["year"].max()
    latest = (
        view[view["year"].eq(latest_year)]
        .groupby("Country", as_index=False)["value"]
        .sum()
        .sort_values("value", ascending=False)
        .head(15)
    )
    st.plotly_chart(
        px.bar(
            latest,
            x="value",
            y="Country",
            orientation="h",
            labels={"value": "Latest available emissions value", "Country": "Country"},
            title=f"Top historical emissions records in {int(latest_year)}",
        ).update_layout(yaxis={"categoryorder": "total ascending"}),
        use_container_width=True,
    )
