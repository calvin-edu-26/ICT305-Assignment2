import pandas as pd
import plotly.express as px
import streamlit as st


def render_global_context(world_bank: pd.DataFrame) -> None:
    st.subheader("World Bank Global Context")
    indicators = sorted(world_bank["indicator"].dropna().unique())
    selected = st.selectbox("Global context indicator", indicators, index=0)
    view = world_bank[world_bank["indicator"].eq(selected)].sort_values("year")
    st.plotly_chart(
        px.line(
            view,
            x="year",
            y="value",
            markers=True,
            labels={"year": "Year", "value": selected},
            title=f"Global trend: {selected}",
        ),
        use_container_width=True,
    )
