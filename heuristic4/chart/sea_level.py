import pandas as pd
import plotly.express as px
from heuristic4.data.config import SCENARIO_COLORS
from heuristic4.chart.style import clean_fig

def chart(sea_level_df, selected_scenarios):

    plot_df = sea_level_df[
        (sea_level_df["scenario"] == "Historical")
        | (sea_level_df["scenario"].isin(selected_scenarios))
    ].copy()

    plot_df = (
        plot_df
        .groupby(["year", "scenario_label"], as_index=False)["sea_level_mm"]
        .mean()
        .sort_values(["scenario_label", "year"])
    )

    fig = px.line(
        plot_df,
        x="year",
        y="sea_level_mm",
        color="scenario_label",
        color_discrete_map=SCENARIO_COLORS,
        title="Observed and Projected Global Mean Sea Level Change",
        labels={
            "year": "Year",
            "sea_level_mm": "Sea level change (mm)",
            "scenario_label": ""
        }
    )

    for trace in fig.data:
        trace.line.width = 6 if "Historical" in trace.name else 4

    fig.add_vline(x=2025, line_dash="dot", line_color="#475569")

    fig.add_annotation(
        x=2025,
        y=1.05,
        yref="paper",
        text="Today",
        showarrow=False,
        font=dict(size=14, color="#0f172a")
    )

    fig = clean_fig(fig, height=550)

    fig.update_layout(
        legend=dict(orientation="h", y=1.18, x=0, title_text=""),
        margin=dict(t=150, b=60, l=40, r=40),
        hovermode="x unified"
    )

    return fig
