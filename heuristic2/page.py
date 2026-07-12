import streamlit as st

from heuristic2.loaders import ndgain
from heuristic2.chart import choropleth, scatter, bar_chart
from heuristic2.components import insight, recommendation
from heuristic2.components.recommendation import DecisionCard

# ── DATA LOADING ──────────────────────────────────────────────────────────────
data = ndgain.load()

# ── DATA SOURCE REFERENCES ────────────────────────────────────────────────────
NDGAIN_REF = "Source: ND-GAIN Country Index — Notre Dame Global Adaptation Initiative (1995–2024)"
OWID_REF = "Source: Our World in Data — CO₂ and Greenhouse Gas Emissions dataset (owid-co2-data.csv)"


# ── DYNAMIC INSIGHT HELPER ────────────────────────────────────────────────────
def get_threshold(year: int) -> str:
    """
    Returns the threshold period for the selected year.
    Two meaningful shifts identified from data validation (1995–2024):
        - Pre-2022  : Somalia consistently leads as most vulnerable low-emitting nation
        - 2022+     : Mauritania emerges as new leader, overtaking Somalia
    """
    return "pre_2022" if year < 2022 else "from_2022"


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

    # ── SCATTER PLOT INLINE TOGGLES ───────────────────────────────────────────
    # Placed directly above the chart so changes are immediately visible.
    tog_col1, tog_col2, tog_col3 = st.columns(3)

    with tog_col1:
        all_countries = sorted(data["Name"].unique().tolist())
        selected_country = st.selectbox(
            "🔍 Highlight Country",
            options=["None"] + all_countries,
            index=0,
            help="Select a country to highlight its position on the scatter plot."
        )

    with tog_col2:
        color_mode = st.radio(
            "Colour By",
            options=["Vulnerability Score", "Sub-Region"],
            index=0,
            horizontal=True,
            help="Switch between colouring dots by vulnerability score or by UN sub-region."
        )

    with tog_col3:
        show_medians = st.toggle(
            "Show Median Guide Lines",
            value=True,
            help="Toggle the median CO₂ and vulnerability reference lines on or off."
        )

    st.plotly_chart(
        scatter.chart(
            data,
            selected_year,
            selected_subregions,
            selected_country,
            show_medians=show_medians,
            color_mode="vulnerability" if color_mode == "Vulnerability Score" else "subregion",
        ),
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

    if threshold == "pre_2022":
        insight.render(
            f"In **{selected_year}**, **Somalia** ranks as the most vulnerable "
            "low-emitting nation, a position it has held consistently since 1995. "
            "Despite contributing less than **0.07 tonnes of CO₂ per capita** — "
            "far below the global median — Somalia's vulnerability score remains "
            "above 0.63. **Guinea-Bissau** and **Eritrea** feature persistently in "
            "the top 3, reflecting deep structural vulnerability across the Horn "
            "of Africa and West Africa. Sub-Saharan Africa dominates the list, "
            "with the top 15 averaging a vulnerability score above 0.62 — "
            "significantly above the global median."
        )
    else:
        insight.render(
            f"In **{selected_year}**, **Mauritania** has emerged as the most "
            "vulnerable low-emitting nation, overtaking Somalia for the first time "
            "in the dataset's history. With a vulnerability score of **0.655** and "
            "CO₂ per capita of just **1.01 tonnes**, Mauritania exemplifies the "
            "core injustice — high climate exposure with minimal emissions "
            "responsibility. **Somalia** and **Chad** remain in the top 3. "
            "Notably, **Malawi**, **Mali**, and **Niger** have dropped out of the "
            "top 15 since 1995, while **Burundi**, **Sierra Leone**, and **Tonga** "
            "have newly entered — signalling shifting vulnerability patterns across "
            "Sub-Saharan Africa and the Pacific. The global median CO₂ per capita "
            "has risen to **2.88 tonnes**, while these 15 nations average below "
            "**0.5 tonnes**."
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

    # ── 1. DECISIONS THIS DASHBOARD SUPPORTS ─────────────────────────────────
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

    # ── DYNAMIC RECOMMENDED ACTIONS ───────────────────────────────────────────
    # 2x2 grid — one card per strategic decision identified above.
    # Content switches at the 2022 threshold based on validated data shifts.
    st.markdown("**Recommended Actions**")
    threshold = get_threshold(selected_year)

    if threshold == "pre_2022":
        recommendation.render([
            DecisionCard(
                decision="Prioritisation of Adaptation Funding",
                action=(
                    "Direct adaptation finance urgently to **Somalia**, **Chad**, "
                    "**Guinea-Bissau**, and **Eritrea** — consistently the most "
                    "vulnerable low-emitting nations across this period. Somalia "
                    "contributes less than **0.07 tonnes CO₂ per capita** yet "
                    "maintains the highest vulnerability score in the dataset. "
                    "Funding must reflect this disproportionate burden."
                )
            ),
            DecisionCard(
                decision="Regional Intervention Planning",
                action=(
                    "Coordinate a regional response across **Sub-Saharan Africa** "
                    "and the **Horn of Africa**, where multiple nations simultaneously "
                    "rank in the top 15 most vulnerable low-emitting countries. "
                    "A nation-by-nation approach is insufficient — systemic regional "
                    "vulnerability requires coordinated policy and funding mechanisms."
                )
            ),
            DecisionCard(
                decision="Progress Monitoring",
                action=(
                    "Establish baseline vulnerability metrics for **Solomon Islands**, "
                    "**Micronesia**, and **Rwanda** — small island and landlocked "
                    "nations appearing persistently in the top 15. Track whether "
                    "adaptation interventions are reducing their vulnerability "
                    "relative to global peers over time."
                )
            ),
            DecisionCard(
                decision="Accountability Assessment",
                action=(
                    "High-emitting nations must demonstrate measurable action to "
                    "reduce vulnerability of low-emitting nations they "
                    "disproportionately affect. The concentration of top-15 "
                    "vulnerability in Sub-Saharan Africa — a region responsible "
                    "for under 2% of global emissions — must be formally documented "
                    "in UNFCCC accountability frameworks."
                )
            ),
        ])
    else:
        recommendation.render([
            DecisionCard(
                decision="Prioritisation of Adaptation Funding",
                action=(
                    "Urgently direct resources to **Mauritania** — the newly emerged "
                    "most vulnerable low-emitting nation as of 2022, with a "
                    "vulnerability score of 0.655 and CO₂ per capita of just 1.01 "
                    "tonnes. Reassess **Somalia** and **Chad** funding — both remain "
                    "in the top 3 and require sustained long-term support."
                )
            ),
            DecisionCard(
                decision="Regional Intervention Planning",
                action=(
                    "The emergence of **Mauritania** at the top of the vulnerability "
                    "rankings signals that West Africa now requires equal prioritisation "
                    "alongside the Horn of Africa. Newly entered nations — **Burundi**, "
                    "**Sierra Leone**, and **Tonga** — indicate expanding vulnerability "
                    "across Central Africa and the Pacific requiring coordinated "
                    "regional responses."
                )
            ),
            DecisionCard(
                decision="Progress Monitoring",
                action=(
                    "Document **Malawi**, **Mali**, and **Niger** — all dropped out "
                    "of the top 15 since 1995 — as adaptation case studies. Identify "
                    "which policies and investments drove their relative vulnerability "
                    "reduction and apply these lessons to currently worsening nations. "
                    "Track Mauritania's trajectory closely as a new critical risk country."
                )
            ),
            DecisionCard(
                decision="Accountability Assessment",
                action=(
                    "The global median CO₂ per capita has reached **2.88 tonnes** "
                    "by 2024, while the top 15 most vulnerable nations remain below "
                    "**0.5 tonnes**. This widening gap must strengthen the "
                    "**Loss and Damage framework** under the UNFCCC — holding "
                    "high-emitting nations formally accountable for consequences "
                    "borne by those least responsible."
                )
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
        max_value=2024,
        value=2024,
        step=1,
        help="Slide to explore how vulnerability has shifted over time (1995–2024)."
    )

    all_subregions = sorted(data["subregion"].unique().tolist())
    selected_subregions = st.multiselect(
        "🌐 Sub-Region",
        options=all_subregions,
        default=[],
        placeholder="All regions shown by default",
        help="Select one or more UN sub-regions to filter both charts simultaneously."
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

# ── HOW TO USE THIS DASHBOARD ─────────────────────────────────────────────────
# Placed before Exploratory Analysis so users are oriented before exploring.
# Per course materials (Topic 3): introduce context before presenting data.
with st.container(border=True):
    st.markdown("**How to Use This Dashboard**")
    st.markdown(
        "Use the **Year slider** in the sidebar to track how climate vulnerability "
        "has shifted across nations from 1995 to 2024. Apply the **Sub-Region filter** "
        "to focus on specific parts of the world. Use the **Highlight Country** "
        "selector above the scatter plot to assess a specific nation's position "
        "relative to global peers. Toggle the **Median Guide Lines** on or off, and "
        "switch between **Vulnerability Score** and **Sub-Region** colouring to explore "
        "different dimensions of the data. Cross-reference the choropleth map, scatter "
        "plot, and bar chart together — each view illuminates a different dimension "
        "of the same injustice."
    )

st.divider()

exploratory_analysis_section()

st.divider()

insight_highlights_section()

st.divider()

decision_support_section()