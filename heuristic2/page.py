import streamlit as st

from heuristic2.loaders import ndgain
from heuristic2.chart import choropleth, scatter, bar_chart
from heuristic2.components import insight, recommendation
from heuristic2.components.recommendation import Recommendation

# ── DATA LOADING ──────────────────────────────────────────────────────────────
data = ndgain.load()

# ── DATA SOURCE REFERENCES ────────────────────────────────────────────────────
NDGAIN_REF = "Source: ND-GAIN Country Index — Notre Dame Global Adaptation Initiative via Kaggle (1995–2018)"
OWID_REF = "Source: Our World in Data — CO₂ and Greenhouse Gas Emissions dataset (owid-co2-data.csv)"


# ── DYNAMIC INSIGHT HELPER ────────────────────────────────────────────────────
def get_threshold(year: int) -> str:
    """
    Returns the threshold period for the selected year.
    Two meaningful shifts identified from data validation:
        - Pre-2010  : Niger leads, Micronesia in top 3
        - 2010+     : Somalia leads, Chad replaces Micronesia
    """
    return "pre_2010" if year < 2010 else "from_2010"


# ═════════════════════════════════════════════════════════════════════════════
# SECTION FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def exploratory_analysis_section():
    """
    Core interactive section — choropleth map and scatter plot.
    Both charts respond simultaneously to all three sidebar controls.
    Per brief: enables comparison, pattern identification, anomaly detection.
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
    Annotated bar chart showing top 15 most vulnerable, lowest-emitting nations.
    Dynamic insight text changes based on two data-validated threshold periods:
        - Pre-2010  : Niger leads, Micronesia in top 3
        - 2010+     : Somalia leads, Chad enters top 3
    Per brief: evidence-based insights derived from the dataset.
    """
    st.header("Insight Highlights")

    st.subheader("Top 15 Most Vulnerable, Lowest-Emitting Nations")
    st.caption(
        "Countries ranked by vulnerability score among those at or below "
        "the global median CO₂ per capita. These nations contribute least "
        "to climate change yet face its greatest consequences."
    )

    st.plotly_chart(
        bar_chart.chart(data, selected_year),
        use_container_width=True
    )
    st.caption(f"{NDGAIN_REF} | {OWID_REF}")

    # ── DYNAMIC INSIGHT TEXT ──────────────────────────────────────────────────
    threshold = get_threshold(selected_year)

    if threshold == "pre_2010":
        insight.render(
            f"In **{selected_year}**, **Niger** ranks as the most vulnerable "
            "low-emitting nation, with a vulnerability score consistently above 0.69 "
            "despite contributing less than 0.06 tonnes of CO₂ per capita — "
            "well below the global median. **Micronesia** appears in the top 3, "
            "highlighting how small island states face existential climate risks "
            "despite near-zero emissions. Sub-Saharan Africa dominates the list, "
            "with the top 15 averaging a vulnerability score of 0.619 — "
            "significantly above the global median."
        )
    else:
        insight.render(
            f"In **{selected_year}**, **Somalia** has overtaken Niger as the most "
            "vulnerable low-emitting nation, reflecting a worsening of its climate "
            "exposure and adaptive capacity. **Chad** has entered the top 3, "
            "displacing Micronesia. Notably, **Bangladesh**, **Maldives**, "
            "**Vanuatu**, and **Burkina Faso** have dropped out of the top 15 "
            "since 1995 — suggesting marginal relative improvement — while "
            "**DR Congo**, **Uganda**, **Eritrea**, and **São Tomé & Príncipe** "
            "have newly entered, signalling a worsening of their relative position. "
            "The global median CO₂ per capita has risen to over 2.6 tonnes, "
            "yet these nations remain far below 0.5 tonnes."
        )


def decision_support_section():
    """
    Translates analytical findings into actionable guidance for UN/IPCC policymakers.
    Per brief: explains how stakeholders interact with the dashboard, what decisions
    it supports, and what actions the data recommends.

    Structure (per brief, three required elements):
        1. How to use the dashboard       — static
        2. Decisions the dashboard supports — static
        3. Recommended actions            — dynamic (threshold-based)
    """
    st.header("Decision Support")

    # ── 1. HOW TO USE THE DASHBOARD ──────────────────────────────────────────
    with st.container(border=True):
        st.markdown("**How to Use This Dashboard**")
        st.markdown(
            "Use the **Year slider** in the sidebar to track how climate vulnerability "
            "has shifted across nations from 1995 to 2018. Apply the **Sub-Region filter** "
            "to focus on specific parts of the world. Use **Highlight Country** on the "
            "scatter plot to assess a specific nation's position relative to global peers. "
            "Cross-reference the choropleth map, scatter plot, and bar chart together — "
            "each view illuminates a different dimension of the same injustice."
        )

    st.divider()

    # ── 2. DECISIONS THIS DASHBOARD SUPPORTS ─────────────────────────────────
    with st.container(border=True):
        st.markdown("**Decisions This Dashboard Supports**")
        st.markdown(
            "This dashboard is designed to support the following strategic decisions "
            "by international climate organisations such as the **UN** and **IPCC**:"
        )
        st.markdown(
            "- **Prioritisation of adaptation funding** — identifying which nations "
            "require urgent support based on vulnerability relative to emissions\n"
            "- **Regional intervention planning** — determining which sub-regions "
            "face systemic vulnerability and require coordinated policy responses\n"
            "- **Progress monitoring** — tracking whether the vulnerability gap between "
            "high-emitting and low-emitting nations is narrowing or widening over time\n"
            "- **Accountability assessment** — evaluating whether the nations most "
            "responsible for emissions are taking sufficient action to protect those "
            "bearing the greatest consequences"
        )

    st.divider()

    # ── 3. DYNAMIC RECOMMENDED ACTIONS ───────────────────────────────────────
    threshold = get_threshold(selected_year)

    if threshold == "pre_2010":
        recommendation.render([
            Recommendation(
                audience="UN Climate Adaptation Fund",
                recommendations=[
                    "Prioritise adaptation finance to Sub-Saharan African nations — "
                    "particularly Niger, Somalia, Chad, and Mali — which consistently "
                    "rank as most vulnerable despite negligible emissions.",
                    "Establish dedicated small island state programmes for nations "
                    "like Micronesia and Solomon Islands, which face existential "
                    "climate threats despite contributing less than 1.6 tonnes CO₂ "
                    "per capita.",
                ]
            ),
            Recommendation(
                audience="IPCC Working Group II",
                recommendations=[
                    "Prioritise regional vulnerability assessments for West and "
                    "Central Africa, where multiple nations simultaneously rank in "
                    "the top 15 most vulnerable low-emitting countries.",
                    "Investigate why Bangladesh and Maldives rank highly in this "
                    "period — both face acute climate exposure that warrants targeted "
                    "research into adaptation pathways.",
                ]
            ),
        ])
    else:
        recommendation.render([
            Recommendation(
                audience="UN Climate Adaptation Fund",
                recommendations=[
                    "Urgently reassess Somalia's adaptation funding — its rise to "
                    "the top vulnerability rank since 2010 signals a deteriorating "
                    "situation requiring immediate international support.",
                    "Investigate the newly entered nations — DR Congo, Uganda, "
                    "Eritrea, and São Tomé & Príncipe — to determine whether their "
                    "entry into the top 15 reflects worsening climate exposure or "
                    "declining adaptive capacity, and respond accordingly.",
                ]
            ),
            Recommendation(
                audience="IPCC Working Group II",
                recommendations=[
                    "Document the relative improvement of Bangladesh, Maldives, "
                    "Vanuatu, and Burkina Faso as potential case studies in "
                    "successful adaptation, and identify which policies drove "
                    "their vulnerability reduction.",
                    "Assess the widening gap between the global median CO₂ per "
                    "capita (now above 2.6 tonnes) and the emissions of the top 15 "
                    "most vulnerable nations (below 0.5 tonnes) as evidence for "
                    "strengthening the Loss and Damage framework under the UNFCCC.",
                ]
            ),
        ])


# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION & SIDEBAR
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