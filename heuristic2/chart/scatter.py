import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def chart(data: pd.DataFrame, selected_year: int, selected_subregions: list, selected_country: str):
    """
    Builds a scatter plot of vulnerability score vs CO₂ per capita.

    Parameters
    ----------
    data : pd.DataFrame
        Full merged dataset from heuristic2/loaders/ndgain.py
    selected_year : int
        Year selected via sidebar slider
    selected_subregions : list of str
        Sub-regions selected via sidebar multiselect.
        Empty list means all sub-regions shown.
    selected_country : str
        Country name to highlight. "None" means no highlight.

    Returns
    -------
    plotly.graph_objects.Figure
    """

    # ── PERCENTILE-BASED COLOUR RANGE ─────────────────────────────────────────
    # Matches choropleth colour scale for visual consistency across both charts.
    vmin = data["vulnerability"].quantile(0.05)
    vmax = data["vulnerability"].quantile(0.95)

    # ── FILTER BY YEAR ────────────────────────────────────────────────────────
    snapshot = data[data["year"] == selected_year].copy()

    # ── RESOLVE COUNTRY HIGHLIGHT BEFORE SUB-REGION FILTER ───────────────────
    # Must be extracted before sub-region filtering so the selected country
    # is always highlighted even if its region is filtered out.
    df_highlight = None
    if selected_country and selected_country != "None":
        df_highlight = snapshot[snapshot["Name"] == selected_country].copy()

    # ── FILTER BY SUB-REGION ──────────────────────────────────────────────────
    if selected_subregions:
        snapshot = snapshot[snapshot["subregion"].isin(selected_subregions)]

    # ── DROP MISSING VALUES ───────────────────────────────────────────────────
    snapshot = snapshot.dropna(subset=["co2_per_capita", "vulnerability"])

    # ── BUILD SCATTER PLOT ────────────────────────────────────────────────────
    fig = px.scatter(
        snapshot,
        x="co2_per_capita",
        y="vulnerability",
        color="vulnerability",
        color_continuous_scale=[
            [0.0, "#FFFFB2"],
            [0.5, "#FD8D3C"],
            [1.0, "#BD0026"],
        ],
        range_color=[vmin, vmax],
        hover_name="Name",
        hover_data={
            "vulnerability": ":.3f",
            "co2_per_capita": ":.2f",
            "subregion": True,
            "year": False,
        },
        labels={
            "co2_per_capita": "CO₂ per Capita (tonnes)",
            "vulnerability": "Vulnerability Score",
            "subregion": "Sub-Region",
        },
        title=f"Climate Vulnerability vs CO₂ Emissions per Capita ({selected_year})",
        opacity=0.8,
    )

    # ── QUADRANT REFERENCE LINES ──────────────────────────────────────────────
    # Median lines divide the plot into four analytical quadrants.
    # Top-left quadrant (high vulnerability, low emissions) is the injustice zone
    # that directly supports the Big Idea narrative.
    median_co2 = snapshot["co2_per_capita"].median()
    median_vuln = snapshot["vulnerability"].median()

    fig.add_vline(
        x=median_co2,
        line_dash="dash",
        line_color="grey",
        line_width=1,
        annotation_text=f"Median CO₂: {median_co2:.1f}t",
        annotation_position="top right",
        annotation_font_size=11,
        annotation_font_color="grey",
    )

    fig.add_hline(
        y=median_vuln,
        line_dash="dash",
        line_color="grey",
        line_width=1,
        annotation_text=f"Median Vulnerability: {median_vuln:.2f}",
        annotation_position="bottom right",
        annotation_font_size=11,
        annotation_font_color="grey",
    )

    # Top-left quadrant label — injustice zone
    fig.add_annotation(
        x=0, y=1,
        xref="paper", yref="paper",
        text="⚠️ High Vulnerability<br>Low Emissions",
        showarrow=False,
        font=dict(size=11, color="#BD0026"),
        align="left",
        xanchor="left",
        yanchor="top",
        bgcolor="rgba(255,255,255,0.6)",
        bordercolor="#BD0026",
        borderwidth=1,
    )

    # ── COUNTRY HIGHLIGHT ─────────────────────────────────────────────────────
    if df_highlight is not None and not df_highlight.empty:
        df_highlight = df_highlight.dropna(subset=["co2_per_capita", "vulnerability"])

        if not df_highlight.empty:
            fig.add_trace(
                go.Scatter(
                    x=df_highlight["co2_per_capita"],
                    y=df_highlight["vulnerability"],
                    mode="markers+text",
                    marker=dict(
                        size=16,
                        color="#1a1a1a",
                        symbol="circle-open",
                        line=dict(width=2.5, color="#1a1a1a"),
                    ),
                    text=df_highlight["Name"],
                    textposition="top center",
                    textfont=dict(size=12, color="#1a1a1a"),
                    name=selected_country,
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

    # ── LAYOUT REFINEMENTS ────────────────────────────────────────────────────
    fig.update_layout(
        xaxis=dict(
            title="CO₂ per Capita (tonnes)",
            showgrid=True,
            gridcolor="rgba(200,200,200,0.3)",
            zeroline=False,
        ),
        yaxis=dict(
            title="Vulnerability Score (0–1)",
            range=[0, 1],
            showgrid=True,
            gridcolor="rgba(200,200,200,0.3)",
            zeroline=False,
        ),
        coloraxis_showscale=False,
        margin=dict(l=40, r=20, t=50, b=40),
        title_font_size=16,
        title_x=0.5,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    fig.update_traces(marker=dict(size=8), selector=dict(mode="markers"))

    return fig