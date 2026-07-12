import pandas as pd
import plotly.express as px
import streamlit as st

def chart(data: pd.DataFrame, year: int, top_n: int):
    snapshot = data[data["year"] == year]

    top = snapshot.sort_values("co2_including_luc_per_capita", ascending=False).head(top_n)
    mean = snapshot["co2_including_luc_per_capita"].mean()

    fig = px.bar(
        top,
        x="co2_including_luc_per_capita",
        y="country",
        labels={"co2_including_luc_per_capita": "Annual CO₂ Emission (Mt) Per Capita", "country": ""}
    )

    fig.add_vline(
        x=mean,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {mean:.1f}t",
        annotation_font_color=st.get_option("theme.primaryColor")
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed", tickfont=dict(size=16))
    )

    return fig
