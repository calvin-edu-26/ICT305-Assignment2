import time
import streamlit as st

from heuristic2.loaders import ndgain
from heuristic2.chart import choropleth, scatter, bar_chart
from heuristic2.components import insight, recommendation
from heuristic2.components.recommendation import DecisionCard

# ── SESSION STATE INITIALISATION ──────────────────────────────────────────────
# Used to manage the play/pause animation state across Streamlit reruns.
if "playing" not in st.session_state:
    st.session_state.playing = False
if "anim_year" not in st.session_state:
    st.session_state.anim_year = 2024
if "scatter_show_medians" not in st.session_state:
    st.session_state.scatter_show_medians = True
if "scatter_color_mode" not in st.session_state:
    st.session_state.scatter_color_mode = "Vulnerability Score"
if "scatter_country" not in st.session_state:
    st.session_state.scatter_country = "None"

# ── DATA LOADING ──────────────────────────────────────────────────────────────
data = ndgain.load()

# ── DATA SOURCE REFERENCES ────────────────────────────────────────────────────
NDGAIN_REF = "Source: ND-GAIN Country Index — Notre Dame Global Adaptation Initiative (1995–2024)"
OWID_REF = "Source: Our World in Data — CO₂ and Greenhouse Gas Emissions dataset (owid-co2-data.csv)"


# ── DYNAMIC INSIGHT HELPER ────────────────────────────────────────────────────
def get_threshold(year: int) -> str:
    """
    Returns the threshold period for the selected year.
    Two meaningful shifts identified from data validation (1995-2024):
        - Pre-2022  : Somalia consistently leads as most vulnerable low-emitting nation
        - 2022+     : Mauritania emerges as new leader, overtaking Somalia
    """
    return "pre_2022" if year < 2022 else "from_2022"


# ═════════════════════════════════════════════════════════════════════════════
# SECTION FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def exploratory_analysis_section():
    st.header("Exploratory Analysis")
    st.markdown(
        "Explore how climate vulnerability and CO2 emissions relate across "
        "nations over time. Use the sidebar controls to filter by year, "
        "sub-region, or animate through the full time range."
    )

    # ── CHOROPLETH MAP ─────────────────────────────────────────────────────────
    st.subheader("Vulnerability by Country")
    st.caption(
        "Colour intensity reflects the ND-GAIN climate vulnerability score (0-1). "
        "Scale is percentile-adjusted (5th-95th) to maximise visual contrast. "
        "Darker red indicates higher vulnerability. Hover over any country for details."
    )

    st.plotly_chart(
        choropleth.chart(data, selected_year, selected_subregions),
        use_container_width=True
    )

    with st.container(border=True):
        st.markdown("**What this chart shows**")
        st.markdown(
            "A global map of climate vulnerability scores for the selected year. "
            "Countries shaded in darker red face the highest climate risks across "
            "food, water, health, ecosystems, human habitat, and infrastructure. "
            "Sub-Saharan Africa and South Asia consistently emerge as the most "
            "vulnerable regions."
        )
        st.markdown("**How to use it**")
        st.markdown(
            "- Use the **Year slider** to track how vulnerability has shifted globally over time.\n"
            "- Use the **Sub-Region filter** to isolate specific parts of the world.\n"
            "- Use the **Play button** to animate the map from 1995 to 2024 and observe long-term trends.\n"
            "- Hover over any country to see its exact vulnerability score and CO2 per capita."
        )

    st.divider()

    # ── SCATTER PLOT CONTROLS ─────────────────────────────────────────────────
    st.subheader("Vulnerability vs Emissions per Country")
    st.caption(
        "Each dot represents one country. Countries in the top-left quadrant "
        "have high vulnerability but low emissions — the clearest cases of "
        "climate injustice. Use the controls below to explore different dimensions."
    )

    tog_col1, tog_col2, tog_col3 = st.columns(3)
    with tog_col1:
        color_mode_options = ["Vulnerability Score", "Sub-Region"]
        show_medians = st.toggle(
            "Show Median Guide Lines",
            value=st.session_state.scatter_show_medians,
            help=(
                "Draws horizontal and vertical lines at the global median "
                "vulnerability score and CO2 per capita. Divides the chart "
                "into four quadrants for easier interpretation."
            )
        )
        st.session_state.scatter_show_medians = show_medians

    with tog_col2:
        color_mode = st.radio(
            "Colour By",
            options=color_mode_options,
            index=color_mode_options.index(st.session_state.scatter_color_mode),
            horizontal=True,
            help=(
                "Vulnerability Score: colours each country by its vulnerability "
                "score using the same yellow-to-red scale as the map above. "
                "Sub-Region: assigns a fixed colour to each UN sub-region "
                "to reveal regional clustering patterns."
            )
        )
        st.session_state.scatter_color_mode = color_mode

    with tog_col3:
        all_countries = sorted(data["Name"].unique().tolist())
        country_options = ["None"] + all_countries
        selected_country = st.selectbox(
            "Highlight Country",
            options=country_options,
            index=country_options.index(st.session_state.scatter_country) if st.session_state.scatter_country in country_options else 0,
            help=(
                "Select a specific country to highlight its position on the "
                "scatter plot with a white circle marker. Useful for tracking "
                "a country of interest relative to global peers."
            )
        )
        st.session_state.scatter_country = selected_country

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

    with st.container(border=True):
        st.markdown("**What this chart shows**")
        st.markdown(
            "Each country is plotted by its CO2 emissions per capita (X-axis) "
            "against its climate vulnerability score (Y-axis). The closer a "
            "country is to the top-left corner, the greater the injustice it "
            "faces: high vulnerability, low emissions responsibility. "
            "The median guide lines divide the chart into four quadrants, "
            "with the top-left being the primary zone of climate injustice."
        )
        st.markdown("**How to use it**")
        st.markdown(
            "- Use the **Year slider** or **Play button** to animate the scatter "
            "plot and observe how the vulnerability-emissions relationship has "
            "shifted from 1995 to 2024.\n"
            "- Toggle **Show Median Guide Lines** to show or hide the quadrant dividers.\n"
            "- Switch **Colour By** to Sub-Region to identify regional clustering patterns.\n"
            "- Use **Highlight Country** to track a specific nation's position "
            "relative to global peers across different years."
        )


def insight_highlights_section():
    st.header("Insight Highlights")
    st.markdown(
        "The chart below ranks the 15 nations that are simultaneously among "
        "the lowest CO2 emitters and the most vulnerable to climate change. "
        "These nations represent the clearest cases of climate injustice."
    )

    st.subheader("Top 15 Most Vulnerable, Lowest-Emitting Nations")
    st.caption(
        "Countries ranked by vulnerability score among those at or below "
        "the global median CO2 per capita. Bars are coloured by UN sub-region. "
        "The white dashed line shows the global median vulnerability score."
    )

    st.plotly_chart(
        bar_chart.chart(data, selected_year),
        use_container_width=True
    )
    st.caption(f"{NDGAIN_REF} | {OWID_REF}")

    with st.container(border=True):
        st.markdown("**What this chart shows**")
        st.markdown(
            "A ranked horizontal bar chart of the 15 nations with the highest "
            "vulnerability scores among low-emitting countries (those at or "
            "below the global median CO2 per capita). Bar colours represent "
            "UN sub-regions, making it easy to see which regions dominate "
            "the list. The white dashed line marks the global median vulnerability "
            "score, showing how far above average these nations sit."
        )
        st.markdown("**How to use it**")
        st.markdown(
            "- Use the **Year slider** to see how the ranking changes over time "
            "and which nations enter or leave the top 15.\n"
            "- Note the **bar colours** to identify sub-regional patterns — "
            "Sub-Saharan Africa consistently dominates the list.\n"
            "- Compare bar lengths against the **white dashed median line** to "
            "gauge how far above the global average these nations sit.\n"
            "- Hover over any bar to see the exact vulnerability score and "
            "CO2 per capita for that country."
        )

    # ── DYNAMIC INSIGHT TEXT ──────────────────────────────────────────────────
    threshold = get_threshold(selected_year)

    if threshold == "pre_2022":
        insight.render(
            f"In **{selected_year}**, **Somalia** leads as the most vulnerable "
            "low-emitting nation with a vulnerability score above 0.63, despite "
            "contributing less than **0.07 tonnes CO2 per capita**. "
            "**Guinea-Bissau** consistently ranks second, while the third position "
            "rotates among **Mauritania**, **Rwanda**, **Micronesia**, and **Eritrea** "
            "across different years. Sub-Saharan Africa and small island states "
            "dominate the list, with the top 15 averaging a vulnerability score "
            "above **0.62**, significantly above the global median of approximately 0.47."
        )
    else:
        insight.render(
            f"In **{selected_year}**, **Mauritania** has overtaken Somalia as the "
            "most vulnerable low-emitting nation, with a vulnerability score of "
            "**0.655** and CO2 per capita of just **1.01 tonnes**. "
            "**Sudan** has risen to second place, a new entrant in the top 3, "
            "while **Somalia** falls to third. **Chad**, **Eritrea**, **Yemen**, "
            "**Solomon Islands**, and **Guinea-Bissau** remain consistent fixtures "
            "in the top 15. The global median CO2 per capita has risen to "
            "**2.88 tonnes** by 2024, while the top 15 nations average below "
            "**0.5 tonnes**, a widening gap that defines the core climate injustice."
        )


def decision_support_section():
    st.header("Decision Support")
    st.markdown(
        "This section translates the analytical findings from the charts above "
        "into actionable guidance for international climate organisations "
        "such as the **United Nations (UN)** and the "
        "**Intergovernmental Panel on Climate Change (IPCC)**."
    )

    

    # ── DECISIONS THIS DASHBOARD SUPPORTS ────────────────────────────────────
    with st.container(border=True):
        st.markdown("**Decisions This Dashboard Supports**")
        st.markdown(
            "This dashboard is designed to support the following strategic decisions "
            "by international climate organisations such as the **UN** and **IPCC**:"
        )
        st.markdown(
            "- **Prioritisation of adaptation funding**: identifying which nations "
            "require urgent support based on vulnerability relative to emissions.\n"
            "- **Regional intervention planning**: determining which sub-regions "
            "face systemic vulnerability and require coordinated policy responses.\n"
            "- **Progress monitoring**: tracking whether the vulnerability gap between "
            "high-emitting and low-emitting nations is narrowing or widening over time.\n"
            "- **Accountability assessment**: evaluating whether the nations most "
            "responsible for emissions are taking sufficient action to protect those "
            "bearing the greatest consequences."
        )

    st.divider()

    # ── DYNAMIC RECOMMENDED ACTIONS ───────────────────────────────────────────
    st.markdown("**Recommended Actions**")
    threshold = get_threshold(selected_year)

    if threshold == "pre_2022":
        recommendation.render([
            DecisionCard(
                decision="Prioritisation of Adaptation Funding",
                action=(
                    "Direct adaptation finance urgently to **Somalia**, **Chad**, "
                    "**Guinea-Bissau**, and **Eritrea**, consistently the most "
                    "vulnerable low-emitting nations across this period. Somalia "
                    "contributes less than **0.07 tonnes CO2 per capita** yet "
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
                    "A nation-by-nation approach is insufficient: systemic regional "
                    "vulnerability requires coordinated policy and funding mechanisms."
                )
            ),
            DecisionCard(
                decision="Progress Monitoring",
                action=(
                    "Establish baseline vulnerability metrics for **Solomon Islands**, "
                    "**Micronesia**, and **Rwanda**, small island and landlocked "
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
                    "vulnerability in Sub-Saharan Africa, a region responsible "
                    "for under 2% of global emissions, must be formally documented "
                    "in UNFCCC accountability frameworks."
                )
            ),
        ])
    else:
        recommendation.render([
            DecisionCard(
                decision="Prioritisation of Adaptation Funding",
                action=(
                    "Urgently direct resources to **Mauritania**, the newly emerged "
                    "most vulnerable low-emitting nation as of 2022, with a "
                    "vulnerability score of 0.655 and CO2 per capita of just 1.01 "
                    "tonnes. Reassess **Somalia** and **Chad** funding: both remain "
                    "in the top 3 and require sustained long-term support."
                )
            ),
            DecisionCard(
                decision="Regional Intervention Planning",
                action=(
                    "The emergence of **Mauritania** at the top of the vulnerability "
                    "rankings signals that West Africa now requires equal prioritisation "
                    "alongside the Horn of Africa. Newly entered nations, **Burundi**, "
                    "**Sierra Leone**, and **Tonga**, indicate expanding vulnerability "
                    "across Central Africa and the Pacific requiring coordinated "
                    "regional responses."
                )
            ),
            DecisionCard(
                decision="Progress Monitoring",
                action=(
                    "Document **Malawi**, **Mali**, and **Niger**, all dropped out "
                    "of the top 15 since 1995, as adaptation case studies. Identify "
                    "which policies and investments drove their relative vulnerability "
                    "reduction and apply these lessons to currently worsening nations. "
                    "Track Mauritania's trajectory closely as a new critical risk country."
                )
            ),
            DecisionCard(
                decision="Accountability Assessment",
                action=(
                    "The global median CO2 per capita has reached **2.88 tonnes** "
                    "by 2024, while the top 15 most vulnerable nations remain below "
                    "**0.5 tonnes**. This widening gap must strengthen the "
                    "Loss and Damage framework under the UNFCCC, holding "
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

    # ── YEAR SLIDER ───────────────────────────────────────────────────────────
    # Disabled during animation so the slider reflects the current animated year.
    if st.session_state.playing:
        selected_year = st.session_state.anim_year
        st.slider(
            "📅 Year",
            min_value=1995,
            max_value=2024,
            value=selected_year,
            step=1,
            disabled=True,
            help="Slider is disabled during animation. Press Pause to regain manual control."
        )
    else:
        selected_year = st.slider(
            "Year",
            min_value=1995,
            max_value=2024,
            value=st.session_state.anim_year,
            step=1,
            help="Slide to explore how vulnerability has shifted over time (1995-2024)."
        )
        st.session_state.anim_year = selected_year

    # ── PLAY / PAUSE BUTTON ───────────────────────────────────────────────────
    play_col, speed_col = st.columns([1, 1])
    with play_col:
        play_label = "⏸ Pause" if st.session_state.playing else "▶ Play"
        if st.button(play_label, use_container_width=True):
            st.session_state.playing = not st.session_state.playing
            if st.session_state.playing and st.session_state.anim_year >= 2024:
                st.session_state.anim_year = 1995
            st.rerun()
    with speed_col:
        speed = st.selectbox(
            "Speed",
            options=["Slow", "Normal", "Fast"],
            index=1,
            label_visibility="collapsed",
            help="Controls the animation speed."
        )

    speed_map = {"Slow": 1.0, "Normal": 0.5, "Fast": 0.2}

    # ── SUB-REGION FILTER ─────────────────────────────────────────────────────
    all_subregions = sorted(data["subregion"].unique().tolist())
    selected_subregions = st.multiselect(
        "Sub-Region",
        options=all_subregions,
        default=[],
        placeholder="All regions shown by default",
        help=(
            "Filter both charts to show only countries within the selected "
            "UN sub-regions. Select multiple regions to compare them."
        )
    )

    # ── GLOSSARY ──────────────────────────────────────────────────────────────
    st.divider()
    with st.expander("Glossary"):
        st.caption("**CO₂** — Carbon Dioxide. A greenhouse gas produced by burning fossil fuels, deforestation, and industrial processes. The primary driver of human-caused climate change.")
        st.caption("**GDP** — Gross Domestic Product. The total monetary value of all goods and services produced in a country in a given year. Used here to contextualise the economic scale of climate damage.")
        st.caption("**GHG** — Greenhouse Gas. Gases that trap heat in the atmosphere, including CO₂, methane (CH₄), and nitrous oxide (N₂O).")
        st.caption("**IPCC** — Intergovernmental Panel on Climate Change. A United Nations body that assesses the science related to climate change and its impacts.")
        st.caption("**ND-GAIN** — Notre Dame Global Adaptation Initiative. A research index measuring a country's vulnerability to climate change and its readiness to adapt, scored from 0 (least vulnerable) to 1 (most vulnerable).")
        st.caption("**UN** — United Nations. An international organisation founded in 1945 to promote peace, security, and cooperation among nations.")
        st.caption("**UNFCCC** — United Nations Framework Convention on Climate Change. An international treaty providing the framework for global climate action, including the Paris Agreement and the Loss and Damage framework.")
        st.caption("**Per Capita** — Per person. Used to normalise metrics by population size, enabling fair comparisons between countries of different sizes.")
        st.caption("**Sub-Region** — A geographic grouping of countries based on the United Nations M49 standard (e.g., Sub-Saharan Africa, South-eastern Asia, Oceania).")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE LAYOUT
# ═════════════════════════════════════════════════════════════════════════════

st.title("Climate Vulnerability & Exposure")
st.markdown(
    """
    **Which nations are most vulnerable to climate change 
    relative to how little they have contributed to emissions?**

    > *"The nations least responsible for climate change are bearing its greatest consequences."*
    """
)

st.divider()

# ── HOW TO USE THIS DASHBOARD ─────────────────────────────────────────────────
with st.container(border=True):
    with st.expander("**How to Use This Dashboard**"):
        st.markdown("Use the **Year slider** in the sidebar to track how climate vulnerability has shifted across nations from 1995 to 2024.")
        st.markdown("Press **Play** to animate through all years automatically.")
        st.markdown("Apply the **Sub-Region filter** to focus on specific parts of the world.")
        st.markdown("Use the **Highlight Country** selector above the scatter plot to assess a specific nation's position relative to global peers.")
        st.markdown("Toggle the **Median Guide Lines** on or off, and switch between **Vulnerability Score** and **Sub-Region** colouring to explore different dimensions of the data.")
        st.markdown("Expand the **Glossary** in the sidebar for definitions of all acronyms used throughout this page.")
    

st.divider()

exploratory_analysis_section()

st.divider()

insight_highlights_section()

st.divider()

decision_support_section()

st.divider()
_, next_col = st.columns([11, 2])
with next_col:
    st.page_link("heuristic3/page.py", label="Next: Extreme Weather →")


# ═════════════════════════════════════════════════════════════════════════════
# ANIMATION LOOP
# Must be at the end of the script so charts render before the next rerun.
# ═════════════════════════════════════════════════════════════════════════════

if st.session_state.playing:
    time.sleep(speed_map[speed])
    if st.session_state.anim_year < 2024:
        st.session_state.anim_year += 1
        st.rerun()
    else:
        st.session_state.playing = False
        st.rerun()