import streamlit as st

from heuristic2.loaders import ndgain
from heuristic2.chart import choropleth, scatter
from heuristic2.components import insight, recommendation
from heuristic2.components.recommendation import Recommendation

# ── DATA LOADING ──────────────────────────────────────────────────────────────
data = ndgain.load()

# ── DATA SOURCE REFERENCES ────────────────────────────────────────────────────
NDGAIN_REF = "Source: ND-GAIN Country Index — Notre Dame Global Adaptation Initiative via Kaggle (1995–2018)"
OWID_REF = "Source: Our World in Data — CO₂ and Greenhouse Gas Emissions dataset (owid-co2-data.csv)"


# ═════════════════════════════════════════════════════════════════════════════
# SECTION FUNCTIONS
# Per brief: Exploratory Analysis, Insight Highlights, Decision Support.
# Variables (selected_year, selected_subregions, selected_country) are
# defined in the sidebar block below and referenced here at call time.
# ═════════════════════════════════════════════════════════════════════════════

def exploratory_analysis_section():
    """
    Core interactive section — choropleth map and scatter plot.
    Both charts respond simultaneously to all three sidebar controls.
    Per brief: enables comparison, pattern identification, and anomaly detection.
    """
    st.header("Exploratory Analysis")

    # ── CHOROPLETH MAP ─────────────────────────────────────────────────────────
    st.subheader("Vulnerability by Country")
    st.caption(
        "Colour intensity reflects climate vulnerability score. "
        "Scale is percentile-adjusted (5th–95th) to maximise visual contrast. "
        "Darker red indicates higher vulnerability. "
        "Hover over any country for details."
    )

    st.plotly_chart(
        choropleth.chart(data, selected_year, selected_subregions),
        use_container_width=True
    )

    st.caption(NDGAIN_REF)
    st.divider()

    # ── SCATTER PLOT ───────────────────────────────────────────────────────────
    st.subheader("Vulnerability vs Emissions per Country")
    st.caption(
        "Each dot represents one country. "
        "Countries in the top-left quadrant have high vulnerability "
        "but low emissions — the clearest cases of climate injustice. "
        "Use the sidebar controls to filter by year, region, or highlight "
        "a specific country."
    )

    st.plotly_chart(
        scatter.chart(data, selected_year, selected_subregions, selected_country),
        use_container_width=True
    )

    st.caption(f"{NDGAIN_REF} | {OWID_REF}")


def insight_highlights_section():
    """
    Annotated findings derived from the data.
    Per brief: highlights trends, patterns, and anomalies of significance.
    """
    st.header("Insight Highlights")

    # TODO: Add annotated bar chart (top 15 most vulnerable, lowest-emitting nations)
    st.info("Bar Chart here.")


def decision_support_section():
    """
    Translates analytical findings into actionable guidance for UN/IPCC policymakers.
    Per brief: explains how stakeholders should use the dashboard and what decisions
    it is designed to support.
    """
    st.header("Decision Support")

    # TODO: Add insight callout and recommendations
    st.info("Decision support incoming~")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION & SIDEBAR
# Sidebar controls are defined here and referenced by section functions above.
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(layout="wide")

with st.sidebar:
    st.header("Filters")

    selected_year = st.slider(
        "📅 Year",
        min_value=1995,
        max_value=2018,
        value=2018,
        step=1,
        help="Slide to explore how vulnerability has shifted over time (1995–2018)."
    )

    all_subregions = sorted(data["subregion"].unique().tolist())
    selected_subregions = st.multiselect(
        "🌐 Sub-Region",
        options=all_subregions,
        default=[],
        placeholder="All regions shown by default",
        help="Select one or more UN sub-regions to filter both charts simultaneously."
    )

    all_countries = sorted(data["Name"].unique().tolist())
    selected_country = st.selectbox(
        "🔍 Highlight Country",
        options=["None"] + all_countries,
        index=0,
        help="Select a country to highlight its position on the scatter plot."
    )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE LAYOUT
# ═════════════════════════════════════════════════════════════════════════════

st.title("Climate Vulnerability & Exposure")
st.markdown(
    """
    **Sub-heuristic:** Which nations are most vulnerable to climate change 
    relative to how little they have contributed to emissions?

    > *"The nations least responsible for climate change are bearing its greatest consequences."*
    """
)

st.divider()

exploratory_analysis_section()

st.divider()

insight_highlights_section()

st.divider()

decision_support_section()