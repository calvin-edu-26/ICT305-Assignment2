import pandas as pd
import plotly.express as px

# ── COUNTRY NAME CLEANING ─────────────────────────────────────────────────────
# Exact strings as they appear in the ND-GAIN dataset.
# Truncated or verbose names replaced with clean display labels.
NAME_OVERRIDES = {
    "Congo, the Democratic Republic o": "DR Congo",
    "Micronesia, Federated States of": "Micronesia",
    "Sao Tome and Principe": "São Tomé & Príncipe",
    "Bolivia, Plurinational State of": "Bolivia",
    "Tanzania, United Republic of": "Tanzania",
    "Iran, Islamic Republic of": "Iran",
    "Korea, Republic of": "South Korea",
    "Korea, Democratic People's Repub": "North Korea",
    "Lao People's Democratic Republic": "Laos",
    "Moldova, Republic of": "Moldova",
    "Venezuela, Bolivarian Republic o": "Venezuela",
    "Syrian Arab Republic": "Syria",
    "Libyan Arab Jamahiriya": "Libya",
    "Saint Vincent and the Grenadines": "St. Vincent & Grenadines",
    "Saint Kitts and Nevis": "St. Kitts & Nevis",
}


def chart(data: pd.DataFrame, selected_year: int):
    """
    Builds an annotated horizontal bar chart showing the top 15 most
    vulnerable, lowest-emitting nations for a selected year.

    Selection logic:
        1. Filter to countries at or below the median CO₂ per capita
           (the low-emitting half of the world)
        2. Rank those countries by vulnerability score (descending)
        3. Take the top 15

    Parameters
    ----------
    data : pd.DataFrame
        Full merged dataset from heuristic2/loaders/ndgain.py
    selected_year : int
        Year selected via sidebar slider — chart updates in real time

    Returns
    -------
    plotly.graph_objects.Figure
    """

    # ── FILTER BY YEAR ────────────────────────────────────────────────────────
    snapshot = data[data["year"] == selected_year].copy()
    snapshot = snapshot.dropna(subset=["co2_per_capita", "vulnerability"])

    # ── CLEAN COUNTRY NAMES ───────────────────────────────────────────────────
    snapshot["display_name"] = snapshot["Name"].replace(NAME_OVERRIDES)

    # ── FILTER TO LOW EMITTERS ────────────────────────────────────────────────
    median_co2 = snapshot["co2_per_capita"].median()
    low_emitters = snapshot[snapshot["co2_per_capita"] <= median_co2]

    # ── SELECT TOP 15 BY VULNERABILITY ───────────────────────────────────────
    top15 = low_emitters.nlargest(15, "vulnerability").copy()

    # ── BUILD BAR CHART ───────────────────────────────────────────────────────
    fig = px.bar(
        top15,
        x="vulnerability",
        y="display_name",
        orientation="h",
        color="vulnerability",
        color_continuous_scale=[
            [0.0, "#FFFFB2"],
            [0.5, "#FD8D3C"],
            [1.0, "#BD0026"],
        ],
        range_color=[
            data["vulnerability"].quantile(0.05),
            data["vulnerability"].quantile(0.95),
        ],
        hover_name="Name",
        hover_data={
            "display_name": False,
            "vulnerability": ":.3f",
            "co2_per_capita": ":.2f",
            "subregion": True,
        },
        labels={
            "vulnerability": "Vulnerability Score",
            "display_name": "",
            "co2_per_capita": "CO₂ per Capita (tonnes)",
            "subregion": "Sub-Region",
        },
        title=(
            f"Top 15 Most Vulnerable, Lowest-Emitting Nations ({selected_year})<br>"
            f"<sup>Filtered to countries below median CO₂ per capita ({median_co2:.2f}t)</sup>"
        ),
    )

    # ── GLOBAL MEDIAN VULNERABILITY LINE ──────────────────────────────────────
    # White dashed line contrasts clearly against dark red bars.
    # Thicker line weight ensures it reads above the axis gridlines.
    global_median_vuln = snapshot["vulnerability"].median()

    fig.add_vline(
        x=global_median_vuln,
        line_dash="dash",
        line_color="#FFFFFF",
        line_width=2,
        annotation_text=f"Global Median: {global_median_vuln:.2f}",
        annotation_position="top right",
        annotation_font_size=12,
        annotation_font_color="#FFFFFF",
    )

    # ── LAYOUT REFINEMENTS ────────────────────────────────────────────────────
    fig.update_layout(
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=13),
        ),
        xaxis=dict(
            title="Vulnerability Score",
            range=[0, 1],
            showgrid=True,
            gridcolor="rgba(200,200,200,0.3)",
        ),
        coloraxis_showscale=False,
        margin=dict(l=10, r=20, t=70, b=40),
        title_font_size=15,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=500,
    )

    return fig