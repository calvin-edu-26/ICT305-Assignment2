import pandas as pd
import plotly.express as px

# ── COUNTRY NAME CLEANING ─────────────────────────────────────────────────────
# Some ND-GAIN country names are too long or truncated for clean chart display.
NAME_OVERRIDES = {
    "Congo, the Democratic Republic of the": "DR Congo",
    "Micronesia, Federated States of": "Micronesia",
    "Sao Tome and Principe": "São Tomé & Príncipe",
    "Solomon Islands": "Solomon Islands",
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

    This directly answers the core analytical question:
    "Which nations are most vulnerable relative to how little they emit?"

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
    # Countries at or below the median CO₂ per capita are classified as
    # low emitters — this is the population of interest for the Big Idea.
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

    # ── MEDIAN VULNERABILITY ANNOTATION ──────────────────────────────────────
    # Reference line showing where the global median vulnerability sits
    # relative to these 15 countries — reinforces how far above average they are.
    global_median_vuln = snapshot["vulnerability"].median()

    fig.add_vline(
        x=global_median_vuln,
        line_dash="dash",
        line_color="grey",
        line_width=1,
        annotation_text=f"Global Median: {global_median_vuln:.2f}",
        annotation_position="top right",
        annotation_font_size=11,
        annotation_font_color="grey",
    )

    # ── LAYOUT REFINEMENTS ────────────────────────────────────────────────────
    fig.update_layout(
        yaxis=dict(
            autorange="reversed",              # Highest vulnerability at top
            tickfont=dict(size=13),
        ),
        xaxis=dict(
            title="Vulnerability Score",
            range=[0, 1],                      # Fixed range for year-to-year comparison
            showgrid=True,
            gridcolor="rgba(200,200,200,0.3)",
        ),
        coloraxis_showscale=False,             # Colour bar shown on choropleth already
        margin=dict(l=10, r=20, t=70, b=40),
        title_font_size=15,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=500,
    )

    return fig