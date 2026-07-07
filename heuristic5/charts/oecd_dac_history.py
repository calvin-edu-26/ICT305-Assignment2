import pandas as pd
import plotly.express as px
import streamlit as st


def render_oecd_dac_history(oecd_dac: pd.DataFrame) -> None:
    st.subheader("OECD DAC Historical Finance Context")
    view = oecd_dac[oecd_dac["donor"] != "DAC members, Total"].copy()
    yearly = (
        view.groupby(["year", "objective"], as_index=False)["climate_targeted_total_usd_millions_2019"]
        .sum()
        .dropna()
    )
    st.plotly_chart(
        px.area(
            yearly,
            x="year",
            y="climate_targeted_total_usd_millions_2019",
            color="objective",
            labels={
                "year": "Year",
                "climate_targeted_total_usd_millions_2019": "Climate-targeted finance, 2019 USD millions",
                "objective": "Objective",
            },
            title="Earlier OECD DAC adaptation and mitigation finance",
        ),
        use_container_width=True,
    )
