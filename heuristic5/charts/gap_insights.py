import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from components.utils import compact_money, pct


def render_gap_insights(
    providers: pd.DataFrame,
    regions: pd.DataFrame,
    recipients: pd.DataFrame,
    emissions: pd.DataFrame,
    vulnerability: pd.DataFrame,
    filtered: pd.DataFrame,
) -> None:
    st.subheader("Insight Highlights")

    latest_emissions_year = int(emissions.dropna(subset=["co2"])["year"].max())
    latest_emissions = emissions[(emissions["year"] == latest_emissions_year) & emissions["co2"].notna()]
    provider_emissions = latest_emissions.rename(columns={"country": "provider"})[
        ["provider", "co2", "co2_per_capita", "population", "gdp"]
    ]
    provider_gap = providers.merge(provider_emissions, on="provider", how="left")
    provider_gap["adaptation_per_mtco2"] = np.where(
        provider_gap["co2"] > 0,
        provider_gap["adaptation_usd_million"] / provider_gap["co2"],
        np.nan,
    )

    gap_left, gap_right = st.columns(2)
    with gap_left:
        st.plotly_chart(
            px.scatter(
                provider_gap.dropna(subset=["co2"]),
                x="co2",
                y="adaptation_usd_million",
                size="climate_usd_million",
                color="adaptation_share",
                hover_name="provider",
                labels={
                    "co2": f"CO2 emissions in {latest_emissions_year}, million tonnes",
                    "adaptation_usd_million": "Adaptation finance, 2024 USD millions",
                    "climate_usd_million": "Total climate finance",
                    "adaptation_share": "Adaptation share",
                },
                title="Emitter adaptation support gap",
                color_continuous_scale="RdYlGn",
            ),
            use_container_width=True,
        )

    with gap_right:
        vulnerability_view = vulnerability.dropna(subset=["iso_code", "vulnerability", "funding_per_capita"])
        st.plotly_chart(
            px.choropleth(
                vulnerability_view,
                locations="iso_code",
                color="funding_per_capita",
                hover_name="country",
                hover_data={"vulnerability": ":.2f", "funding_per_capita": ":.2f", "iso_code": False},
                color_continuous_scale="YlGnBu",
                labels={"funding_per_capita": "Funding per capita, USD"},
                title="Vulnerable-country funding per capita",
            ),
            use_container_width=True,
        )

    ranked_gap = provider_gap.sort_values("adaptation_per_mtco2", ascending=True).dropna(subset=["adaptation_per_mtco2"])
    low_adaptation = providers.sort_values("adaptation_share").head(3)
    top_regions = regions.sort_values("adaptation_usd_million", ascending=False).head(3)
    insight_cols = st.columns(3)
    insight_cols[0].info(
        f"Lowest adaptation-per-emissions provider: **{ranked_gap.iloc[0]['provider']}** "
        f"at {compact_money(ranked_gap.iloc[0]['adaptation_per_mtco2'])} per MtCO2."
        if not ranked_gap.empty
        else "Provider emissions matching is unavailable for the current selection."
    )
    insight_cols[1].info(
        "Lowest adaptation shares: "
        + ", ".join(f"{row.provider} ({pct(row.adaptation_share)})" for row in low_adaptation.itertuples())
    )
    insight_cols[2].info(
        "Largest adaptation recipient regions: "
        + ", ".join(f"{row.region} ({compact_money(row.adaptation_usd_million)})" for row in top_regions.itertuples())
    )

    focus_metric = st.radio(
        "Gap lens",
        ["Adaptation delivery", "Mitigation balance", "Vulnerability targeting"],
        index=0,
        horizontal=True,
    )

    if focus_metric == "Vulnerability targeting":
        vuln_region = (
            vulnerability.groupby("region", as_index=False)[["vulnerability", "funding_per_capita"]]
            .median()
            .dropna()
            .sort_values("vulnerability", ascending=False)
        )
        st.plotly_chart(
            px.bar(
                vuln_region,
                x="vulnerability",
                y="region",
                color="funding_per_capita",
                orientation="h",
                labels={"vulnerability": "Median vulnerability score", "region": "Region", "funding_per_capita": "Median funding per capita"},
                title="Vulnerability vs funding per capita",
                color_continuous_scale="Blues",
            ).update_layout(yaxis={"categoryorder": "total ascending"}),
            use_container_width=True,
        )
    elif focus_metric == "Mitigation balance":
        st.plotly_chart(
            px.violin(
                recipients[recipients["climate_usd_million"] > 0],
                x="region",
                y="adaptation_share",
                box=True,
                points=False,
                labels={"region": "Recipient region", "adaptation_share": "Adaptation share"},
                title="Distribution of adaptation share by recipient region",
            ),
            use_container_width=True,
        )
    else:
        sector_summary = (
            filtered.groupby("sector", as_index=False)[["adaptation_usd_thousand", "climate_usd_thousand"]]
            .sum()
            .assign(
                adaptation_usd_million=lambda d: d["adaptation_usd_thousand"] / 1000,
                adaptation_share=lambda d: np.where(
                    d["climate_usd_thousand"] > 0,
                    d["adaptation_usd_thousand"] / d["climate_usd_thousand"],
                    0,
                ),
            )
            .sort_values("adaptation_usd_million", ascending=False)
            .head(12)
        )
        st.plotly_chart(
            px.bar(
                sector_summary,
                x="adaptation_usd_million",
                y="sector",
                color="adaptation_share",
                orientation="h",
                labels={
                    "adaptation_usd_million": "Adaptation finance, 2024 USD millions",
                    "sector": "Sector",
                    "adaptation_share": "Adaptation share",
                },
                title="Which sectors receive adaptation finance?",
                color_continuous_scale="Greens",
            ).update_layout(yaxis={"categoryorder": "total ascending"}),
            use_container_width=True,
        )


