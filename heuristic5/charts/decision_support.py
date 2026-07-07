import pandas as pd
import streamlit as st


def render_decision_support(providers: pd.DataFrame) -> None:
    st.subheader("Decision Support")
    st.write(
        "Use the filters to test whether a provider group is prioritising adaptation in the countries and regions most exposed to climate harm. "
        "A stakeholder can use this dashboard to decide where to request stronger adaptation commitments, which providers need follow-up, "
        "and whether finance is moving toward vulnerable recipients or remaining concentrated in mitigation-heavy portfolios."
    )

    decision_table = providers[
        ["provider", "climate_usd_million", "adaptation_usd_million", "mitigation_usd_million", "adaptation_share"]
    ].copy()
    decision_table["climate_usd_million"] = decision_table["climate_usd_million"].round(2)
    decision_table["adaptation_usd_million"] = decision_table["adaptation_usd_million"].round(2)
    decision_table["mitigation_usd_million"] = decision_table["mitigation_usd_million"].round(2)
    decision_table["adaptation_share"] = (decision_table["adaptation_share"] * 100).round(1)
    decision_table = decision_table.rename(
        columns={
            "provider": "Provider",
            "climate_usd_million": "Climate finance (USD m)",
            "adaptation_usd_million": "Adaptation (USD m)",
            "mitigation_usd_million": "Mitigation (USD m)",
            "adaptation_share": "Adaptation share (%)",
        }
    )
    st.dataframe(decision_table, use_container_width=True, hide_index=True)
