import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def render_recipient_finance(recipient_finance: pd.DataFrame, year_range: tuple[int, int], selected_regions: list[str]) -> None:
    st.subheader("Recipient Perspective Finance")
    if recipient_finance.empty:
        st.info(
            "CRDF-RP_all_years_2001-2024.csv is related to this project, but it is not currently in the heuristic5 folder. "
            "Place it there to enable this recipient-perspective chart."
        )
        return
    view = recipient_finance[
        recipient_finance["year"].between(year_range[0], year_range[1])
        & recipient_finance["region"].isin(selected_regions)
    ].copy()
    if view.empty:
        st.info("No recipient-perspective finance records match the current filters.")
        return

    top_recipients = (
        view.groupby(["recipient", "region"], as_index=False)[
            ["adaptation_usd_thousand", "mitigation_usd_thousand", "climate_usd_thousand"]
        ]
        .sum()
        .assign(
            adaptation_usd_million=lambda d: d["adaptation_usd_thousand"] / 1000,
            climate_usd_million=lambda d: d["climate_usd_thousand"] / 1000,
            adaptation_share=lambda d: np.where(
                d["climate_usd_thousand"] > 0,
                d["adaptation_usd_thousand"] / d["climate_usd_thousand"],
                0,
            ),
        )
        .sort_values("climate_usd_million", ascending=False)
        .head(20)
    )

    st.plotly_chart(
        px.bar(
            top_recipients,
            x="climate_usd_million",
            y="recipient",
            color="adaptation_share",
            orientation="h",
            labels={
                "recipient": "Recipient",
                "climate_usd_million": "Climate finance, 2024 USD millions",
                "adaptation_share": "Adaptation share",
            },
            title="Top recipients from CRDF recipient perspective",
            color_continuous_scale="YlGn",
        ).update_layout(yaxis={"categoryorder": "total ascending"}),
        use_container_width=True,
    )
