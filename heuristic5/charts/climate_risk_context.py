import pandas as pd
import plotly.express as px
import streamlit as st


def render_climate_risk_context(
    country_temperature: pd.DataFrame,
    climate_indicators: pd.DataFrame,
    vulnerability: pd.DataFrame,
) -> None:
    st.subheader("Climate Risk Context")
    left, right = st.columns(2)

    temp_view = country_temperature.merge(
        vulnerability[["iso_code", "country", "region", "vulnerability", "funding_per_capita"]],
        on="iso_code",
        how="inner",
    ).dropna(subset=["annual_temp", "vulnerability"])

    with left:
        st.plotly_chart(
            px.scatter(
                temp_view,
                x="annual_temp",
                y="vulnerability",
                color="region",
                size="funding_per_capita",
                hover_name="country",
                labels={
                    "annual_temp": "Historical annual temperature",
                    "vulnerability": "Vulnerability score",
                    "funding_per_capita": "Funding per capita, USD",
                },
                title="Temperature, vulnerability and funding",
            ),
            use_container_width=True,
        )

    indicator_view = climate_indicators[
        climate_indicators["Series name"].str.contains("CO2|renewable|below 5m", case=False, na=False)
    ].copy()
    latest_year = indicator_view.groupby(["Country code", "Series code"])["year"].transform("max")
    latest = indicator_view[indicator_view["year"].eq(latest_year)].dropna(subset=["value"])
    land_risk = latest[latest["Series code"].eq("AG.LND.EL5M.ZS")].sort_values("value", ascending=False).head(15)

    with right:
        st.plotly_chart(
            px.bar(
                land_risk,
                x="value",
                y="Country name",
                orientation="h",
                labels={"value": "Land area below 5m (% of land area)", "Country name": "Country"},
                title="Countries exposed to low-elevation land risk",
            ).update_layout(yaxis={"categoryorder": "total ascending"}),
            use_container_width=True,
        )
