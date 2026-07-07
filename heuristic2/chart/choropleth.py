import pandas as pd
import plotly.express as px


def chart(data: pd.DataFrame, selected_year: int, selected_subregions: list):
    """
    Builds a choropleth map of climate vulnerability scores.

    Parameters
    ----------
    data : pd.DataFrame
        Full merged dataset from heuristic2/loaders/ndgain.py
    selected_year : int
        Year selected via sidebar slider
    selected_subregions : list of str
        Sub-regions selected via sidebar multiselect.
        Empty list means all sub-regions shown.

    Returns
    -------
    plotly.graph_objects.Figure
    """

    # ── PERCENTILE-BASED COLOUR RANGE ─────────────────────────────────────────
    # Computed from the full dataset before any filtering so the colour
    # scale stays consistent as the year slider changes.
    # 5th–95th percentile maximises contrast across the meaningful range
    # of vulnerability scores without distortion from outliers.
    vmin = data["vulnerability"].quantile(0.05)
    vmax = data["vulnerability"].quantile(0.95)

    # ── FILTER BY YEAR ────────────────────────────────────────────────────────
    snapshot = data[data["year"] == selected_year].copy()

    # ── FILTER BY SUB-REGION ──────────────────────────────────────────────────
    if selected_subregions:
        snapshot = snapshot[snapshot["subregion"].isin(selected_subregions)]

    # ── BUILD CHOROPLETH ──────────────────────────────────────────────────────
    fig = px.choropleth(
        snapshot,
        locations="ISO3",
        color="vulnerability",
        hover_name="Name",
        hover_data={
            "ISO3": False,
            "subregion": True,
            "vulnerability": ":.3f",
            "co2_per_capita": ":.2f",
        },
        color_continuous_scale=[
            [0.0, "#FFFFB2"],
            [0.5, "#FD8D3C"],
            [1.0, "#BD0026"],
        ],
        range_color=[vmin, vmax],
        labels={
            "vulnerability": "Vulnerability Score",
            "co2_per_capita": "CO₂ per Capita (tonnes)",
            "subregion": "Sub-Region",
        },
        title=f"Global Climate Vulnerability Score ({selected_year})",
    )

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="lightgrey",
            projection_type="equirectangular",
            bgcolor="rgba(0,0,0,0)",
        ),
        dragmode=False,
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=50, b=0),
        title_font_size=16,
    )

    return fig