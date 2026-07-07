import math

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def provider_summary(filtered: pd.DataFrame) -> pd.DataFrame:
    return (
        filtered.groupby("provider", as_index=False)[
            ["adaptation_usd_thousand", "mitigation_usd_thousand", "climate_usd_thousand"]
        ]
        .sum()
        .assign(
            adaptation_usd_million=lambda d: d["adaptation_usd_thousand"] / 1000,
            mitigation_usd_million=lambda d: d["mitigation_usd_thousand"] / 1000,
            climate_usd_million=lambda d: d["climate_usd_thousand"] / 1000,
            adaptation_share=lambda d: np.where(
                d["climate_usd_thousand"] > 0,
                d["adaptation_usd_thousand"] / d["climate_usd_thousand"],
                0,
            ),
        )
        .sort_values("climate_usd_million", ascending=False)
    )


def region_summary(filtered: pd.DataFrame) -> pd.DataFrame:
    return (
        filtered.groupby("region", as_index=False)[
            ["adaptation_usd_thousand", "mitigation_usd_thousand", "climate_usd_thousand"]
        ]
        .sum()
        .assign(
            adaptation_usd_million=lambda d: d["adaptation_usd_thousand"] / 1000,
            mitigation_usd_million=lambda d: d["mitigation_usd_thousand"] / 1000,
            climate_usd_million=lambda d: d["climate_usd_thousand"] / 1000,
            adaptation_share=lambda d: np.where(
                d["climate_usd_thousand"] > 0,
                d["adaptation_usd_thousand"] / d["climate_usd_thousand"],
                0,
            ),
        )
    )


def recipient_summary(filtered: pd.DataFrame) -> pd.DataFrame:
    return (
        filtered.groupby(["recipient", "region"], as_index=False)[
            ["adaptation_usd_thousand", "mitigation_usd_thousand", "climate_usd_thousand"]
        ]
        .sum()
        .assign(
            adaptation_usd_million=lambda d: d["adaptation_usd_thousand"] / 1000,
            mitigation_usd_million=lambda d: d["mitigation_usd_thousand"] / 1000,
            climate_usd_million=lambda d: d["climate_usd_thousand"] / 1000,
            adaptation_share=lambda d: np.where(
                d["climate_usd_thousand"] > 0,
                d["adaptation_usd_thousand"] / d["climate_usd_thousand"],
                0,
            ),
        )
    )


def render_exploration(filtered: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    st.subheader("Exploratory Analysis")
    left, right = st.columns(2)

    providers = provider_summary(filtered)
    regions = region_summary(filtered)
    recipients = recipient_summary(filtered)

    with left:
        st.plotly_chart(
            px.bar(
                providers.head(15),
                x="climate_usd_million",
                y="provider",
                color="adaptation_share",
                orientation="h",
                labels={
                    "provider": "Provider",
                    "climate_usd_million": "Climate finance, 2024 USD millions",
                    "adaptation_share": "Adaptation share",
                },
                title="Provider commitments and adaptation share",
                color_continuous_scale="Tealgrn",
            ).update_layout(yaxis={"categoryorder": "total ascending"}),
            use_container_width=True,
        )

    with right:
        st.plotly_chart(
            px.treemap(
                regions,
                path=["region"],
                values="climate_usd_million",
                color="adaptation_share",
                color_continuous_scale="RdYlGn",
                labels={"climate_usd_million": "Climate finance, 2024 USD millions", "adaptation_share": "Adaptation share"},
                title="Where does filtered climate finance go?",
            ),
            use_container_width=True,
        )

    scatter_data = recipients[recipients["climate_usd_million"] > 0].copy()
    x_limit = float(scatter_data["mitigation_usd_million"].max()) if not scatter_data.empty else 0.0
    x_limit = float(max(1.0, math.ceil(x_limit / 1000) * 1000))
    x_step = max(1.0, round(x_limit / 100))
    scatter_chart = st.empty()
    mitigation_range = st.slider(
        "Mitigation finance range (2024 USD millions)",
        min_value=0.0,
        max_value=x_limit,
        value=(0.0, x_limit),
        step=float(x_step),
    )
    scatter_view = scatter_data[
        scatter_data["mitigation_usd_million"].between(mitigation_range[0], mitigation_range[1])
    ].copy()

    scatter_chart.plotly_chart(
        px.scatter(
            scatter_view,
            x="mitigation_usd_million",
            y="adaptation_usd_million",
            size="climate_usd_million",
            color="region",
            hover_name="recipient",
            labels={
                "mitigation_usd_million": "Mitigation finance, 2024 USD millions",
                "adaptation_usd_million": "Adaptation finance, 2024 USD millions",
                "climate_usd_million": "Total climate finance",
            },
            title="Recipient adaptation vs mitigation",
        )
        .update_xaxes(range=[mitigation_range[0], mitigation_range[1]], rangeslider_visible=False)
        .update_layout(height=620),
        use_container_width=True,
    )

    return providers, regions, recipients

