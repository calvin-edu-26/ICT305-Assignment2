import pandas as pd
import plotly.express as px
import streamlit as st

from components.utils import compact_money, pct, usd_millions


def render_overview(filtered: pd.DataFrame) -> None:
    total_climate = usd_millions(filtered["climate_usd_thousand"])
    total_adaptation = usd_millions(filtered["adaptation_usd_thousand"])
    total_mitigation = usd_millions(filtered["mitigation_usd_thousand"])
    adapt_share = filtered["adaptation_usd_thousand"].sum() / filtered["climate_usd_thousand"].sum()
    recipient_count = filtered["recipient"].nunique()

    st.subheader("Overview / Executive Summary")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Climate finance committed", compact_money(total_climate))
    kpi2.metric("Adaptation finance", compact_money(total_adaptation), pct(adapt_share))
    kpi3.metric("Mitigation finance", compact_money(total_mitigation))
    kpi4.metric("Recipient countries / groups", f"{recipient_count:,}")

    yearly = (
        filtered.groupby("year", as_index=False)[
            ["adaptation_usd_thousand", "mitigation_usd_thousand", "climate_usd_thousand"]
        ]
        .sum()
        .assign(
            adaptation_usd_million=lambda d: d["adaptation_usd_thousand"] / 1000,
            mitigation_usd_million=lambda d: d["mitigation_usd_thousand"] / 1000,
        )
    )
    yearly_long = yearly.melt(
        id_vars="year",
        value_vars=["adaptation_usd_million", "mitigation_usd_million"],
        var_name="finance_type",
        value_name="usd_million",
    )
    yearly_long["finance_type"] = yearly_long["finance_type"].map(
        {"adaptation_usd_million": "Adaptation", "mitigation_usd_million": "Mitigation"}
    )
    st.plotly_chart(
        px.line(
            yearly_long,
            x="year",
            y="usd_million",
            color="finance_type",
            markers=True,
            labels={"year": "Year", "usd_million": "Commitment, 2024 USD millions", "finance_type": "Finance type"},
            title="Adaptation vs mitigation over time",
        ),
        use_container_width=True,
    )

