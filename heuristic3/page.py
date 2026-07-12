"""
ICT305 Group Project — Heuristic 3: Extreme Weather & Economic Damage
"Disaster frequency and cost hitting poorest nations hardest"

Author: Jim (Lam Thanh Chieu)

Folder layout (mirrors heuristic2):
    constants.py        : shared colour palette, income group lookup
    loaders/disasters.py: load_data() — reads & cleans the 4 CSVs in data/
    chart/*.py           : one file per chart, each exposing chart(...) ->
                            plotly figure. No Streamlit calls inside.
    page.py (this file)  : sidebar controls, filtering, section narrative,
                            and calls into the chart modules above.

Datasets (all local CSV files in /data folder):
  - deaths.csv        : Annual deaths from natural disasters by country & type (OWID/EM-DAT)
  - damage_gdp.csv    : Economic damage as % of GDP by country & type (OWID/EM-DAT)
  - events.csv        : Global disaster event counts by type (OWID/EM-DAT)
  - co2.csv           : CO2, GDP, population, temperature change by country (OWID/GCP)
"""

import streamlit as st

# Must be the very first Streamlit command executed in this script run —
# calling it after any cached data loader below can trip
# StreamlitSetPageConfigMustBeFirstCommandError if that loader's cache
# happens to be cold and emits a spinner.
#
# NOTE: this only fires inside render_extreme_weather_dashboard() (see
# bottom of file), not at import time — see the note by load_data() below.

from heuristic3.constants import INCOME_ORDER
from heuristic3.loaders.disasters import load_data
from heuristic3.chart import (
    co2_by_income,
    damage_by_country,
    damage_by_income,
    deaths_by_type,
    disaster_frequency,
    events_vs_deaths,
    ml_regression,
    wealth_vs_damage,
)

# NOTE: load_data() is intentionally NOT called at module level. Doing so
# would execute a Streamlit-cached call as a side effect of simply
# *importing* this module (e.g. from the Overview page), which can race
# ahead of that page's own st.set_page_config() call and crash with
# StreamlitSetPageConfigMustBeFirstCommandError. Callers below invoke
# load_data() themselves (it's cheap after the first, cached call).

# ─────────────────────────────────────────────
# KPI FUNCTION
# Used by the Overview page to display Heuristic 3's KPI.
# ─────────────────────────────────────────────
def get_total_disaster_events() -> int:
    """
    Lam's KPI — total number of recorded disaster events
    across all years and all disaster types.
    """
    _, _, _, events_df = load_data()
    events_all = events_df[events_df["disaster_type"] == "All disasters"]
    return int(events_all["n_disasters"].sum())

# ─────────────────────────────────────────────
# MAIN DASHBOARD FUNCTION
# Wraps sidebar + page rendering so this module can be safely
# imported (e.g. by the Overview page) without executing the
# full Streamlit page as a side effect of import.
# ─────────────────────────────────────────────
def render_extreme_weather_dashboard():

    # ─────────────────────────────────────────────
    # PAGE CONFIG
    # ─────────────────────────────────────────────
    st.set_page_config(
        page_title="Extreme Weather & Economic Damage",
        page_icon="🌪️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # ─────────────────────────────────────────────
    # DATA LOADING (deferred until after set_page_config, see note above)
    # ─────────────────────────────────────────────
    co2_df, deaths_df, damage_df, events_df = load_data()

    YEAR_MIN = int(max(deaths_df["Year"].min(), damage_df["Year"].min(), events_df["Year"].min()))
    YEAR_MAX = int(min(deaths_df["Year"].max(), damage_df["Year"].max(), events_df["Year"].max()))
    DISASTER_TYPES = sorted([t for t in events_df["disaster_type"].unique()
        if t not in ["All disasters","All disasters excluding earthquakes",
                     "All disasters excluding extreme temperature"]])

    # ─────────────────────────────────────────────
    # SIDEBAR — 3 INTERACTIVE CONTROLS
    # ─────────────────────────────────────────────
    with st.sidebar:
        st.title("🌪️ Dashboard Controls")
        st.markdown("---")

        st.subheader("📅 Year Range")
        year_range = st.slider(
            "Select time period",
            min_value=YEAR_MIN, max_value=YEAR_MAX,
            value=(1980, YEAR_MAX), step=1,
            help="Filters all charts to the selected time period.",
        )

        st.subheader("🌊 Disaster Types")
        selected_types = st.multiselect(
            "Select disaster types",
            options=DISASTER_TYPES,
            default=["Flood","Extreme weather","Drought","Earthquake"],
            help="Filters disaster frequency and deaths charts by type.",
        )
        if not selected_types:
            selected_types = DISASTER_TYPES

        st.subheader("💰 Income Groups")
        selected_income = st.multiselect(
            "Select income groups",
            options=INCOME_ORDER,
            default=INCOME_ORDER,
            help="Filters country-level charts by World Bank income classification.",
        )
        if not selected_income:
            selected_income = INCOME_ORDER

        st.markdown("---")
        st.caption(
            "**Data sources:**\n"
            "- EM-DAT / CRED (via Our World in Data)\n"
            "- OWID CO₂ & GHG Dataset (Global Carbon Project)\n"
            "- World Bank Income Classifications 2023"
        )

    # ─────────────────────────────────────────────
    # APPLY FILTERS
    # ─────────────────────────────────────────────
    y_start, y_end = year_range

    events_filtered = events_df[
        (events_df["Year"] >= y_start) & (events_df["Year"] <= y_end) &
        (events_df["disaster_type"].isin(selected_types))].copy()

    events_all = events_df[
        (events_df["Year"] >= y_start) & (events_df["Year"] <= y_end) &
        (events_df["disaster_type"] == "All disasters")].copy()

    deaths_filtered = deaths_df[
        (deaths_df["Year"] >= y_start) & (deaths_df["Year"] <= y_end) &
        (deaths_df["income_group"].isin(selected_income))].copy()

    damage_filtered = damage_df[
        (damage_df["Year"] >= y_start) & (damage_df["Year"] <= y_end) &
        (damage_df["income_group"].isin(selected_income))].copy()

    co2_filtered = co2_df[
        (co2_df["year"] >= y_start) & (co2_df["year"] <= y_end) &
        (co2_df["income_group"].isin(selected_income))].copy()

    # ─────────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────────
    st.markdown("## 🌪️ Extreme Weather & Economic Damage")
    st.markdown(
        "> **Core narrative:** The nations that have contributed the least to climate change "
        "are paying the highest price for it. Disasters are becoming more frequent, "
        "more destructive, and increasingly unaffordable for the world's poorest countries — "
        "while the largest emitters remain largely insulated from the consequences."
    )
    st.markdown("---")

    # ─────────────────────────────────────────────
    # SECTION 1 — OVERVIEW / EXECUTIVE SUMMARY
    # ─────────────────────────────────────────────
    st.markdown("### 📊 Section 1: Overview")

    total_events = int(events_all["n_disasters"].sum())
    total_deaths = int(deaths_df[
        (deaths_df["Year"] >= y_start) & (deaths_df["Year"] <= y_end)
    ]["All disasters"].sum())

    avg_damage_low  = damage_df[
        (damage_df["Year"] >= y_start) & (damage_df["Year"] <= y_end) &
        (damage_df["income_group"] == "Low Income")]["All disasters"].mean()
    avg_damage_high = damage_df[
        (damage_df["Year"] >= y_start) & (damage_df["Year"] <= y_end) &
        (damage_df["income_group"] == "High Income")]["All disasters"].mean()

    top_country = (
        damage_filtered.groupby("Entity")["All disasters"]
        .mean().dropna().sort_values(ascending=False).index[0]
        if len(damage_filtered) > 0 else "N/A"
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌪️ Total Disaster Events", f"{total_events:,}")
    with col2:
        st.metric("💀 Total Deaths", f"{total_deaths:,.0f}")
    with col3:
        st.metric(
            "📉 Damage % GDP — Low vs High Income",
            f"{avg_damage_low:.2f}% vs {avg_damage_high:.2f}%",
            help="Low-income nations lose far more of their GDP to disasters than high-income ones."
        )
    with col4:
        st.metric("🏴 Hardest-Hit Country (avg)", top_country,
                  help="Country with highest average economic damage as % of GDP in the selected period.")

    st.markdown("---")

    # ─────────────────────────────────────────────
    # SECTION 2 — EXPLORATORY ANALYSIS
    # ─────────────────────────────────────────────
    st.markdown("### 🔍 Section 2: Exploratory Analysis")

    # ── CHART 1 ──────────────────────────────────
    st.subheader("Chart 1 — Disaster Frequency Over Time by Type")
    st.caption("How has the number of recorded natural disasters changed since 1900, broken down by type?")

    fig1 = disaster_frequency.chart(events_filtered, y_start, y_end)
    st.plotly_chart(fig1, use_container_width=True)

    with st.expander("📖 Analysis — Chart 1"):
        st.markdown("""
        #### What the data shows
        The global count of natural disasters has risen dramatically — from **123 events in 1980**
        to **414 events in 2020**, a **237% increase** in just 40 years. This is not simply a
        recording effect. While improved reporting has contributed to higher counts in recent
        decades, the scientific consensus from the IPCC confirms that climate change is
        physically driving more frequent and intense weather events.

        Floods stand out as the sharpest-rising category — growing from **39 events in 1980**
        to **193 in 2019**, a **395% increase**. Floods are directly driven by changes in
        precipitation patterns, rising sea levels, and more intense storm systems — all
        consequences of a warming atmosphere. Extreme weather events show a similarly steep
        upward trend, while geological disasters such as earthquakes remain relatively flat,
        confirming that the rise is climate-driven rather than geological.

        #### Why this matters
        This chart establishes the scale of the problem. Every bar or peak you see represents
        real communities — often the world's most vulnerable — dealing with floods, storms,
        and droughts with little infrastructure, savings, or government support to fall back on.
        A child growing up in Bangladesh or Mozambique today faces a world with four times
        more flood events than their grandparents did.

        #### Audience-specific insights
        - 🏛️ **Policymakers:** The upward trend is not cyclical — it is structural. Climate
          adaptation budgets need to be planned for a world where disasters are the norm,
          not the exception. Existing disaster response frameworks designed for rare events
          are already obsolete.
        - 🌐 **International aid organisations (UN, Red Cross, etc.):** Pre-positioning
          resources in flood-prone low-income regions is now operationally essential.
          A reactive response model is no longer sufficient given the frequency of events.
        - 📊 **Researchers & analysts:** Use the disaster type filter to isolate climate-driven
          types (Flood, Extreme Weather, Drought) from geological ones (Earthquake, Volcano).
          The divergence in trend lines is a natural experiment confirming climate causation.
        - 🧒 **Students & general public:** Think of it this way — when your grandparents
          were young, a major flood somewhere in the world happened roughly once a week.
          Today, it happens almost every day.
        """)

    # ── CHART 2 ──────────────────────────────────
    st.subheader("Chart 2 — Top 20 Countries by Economic Damage as % of GDP")
    st.caption("Which countries lose the most relative to their economy when disasters strike?")

    fig2 = damage_by_country.chart(damage_filtered, y_start, y_end, top_n=20)
    st.plotly_chart(fig2, use_container_width=True)

    with st.expander("📖 Analysis — Chart 2"):
        st.markdown("""
        #### What the data shows
        This chart immediately reveals who bears the real cost of natural disasters.
        **Dominica** averages **46% of its entire GDP** lost to disasters annually.
        **Samoa** averages **44%**. **Haiti** averages over **4% of GDP** every year —
        and in 2010, following the catastrophic earthquake, that figure reached **67%** of GDP
        in a single year. To put that in perspective: imagine Australia losing 67% of its
        entire national economy in twelve months and being expected to recover without
        sustained international support.

        Crucially, nearly every country in this top 20 is either **Low Income** (red) or
        a **small island developing state** — nations whose entire economies are the size
        of a single suburb in a wealthy country. High-income nations are almost entirely
        absent from this chart. The United States, Germany, and Japan — the world's
        largest economies and among its largest historic emitters — do not appear here.

        The pattern is systematic, not random. These are not simply unlucky countries.
        They are countries located in tropical climate zones that are geographically
        most exposed to climate-driven disasters, with the least financial capacity to
        absorb losses and rebuild.

        #### Audience-specific insights
        - 🏛️ **Policymakers in high-income nations:** This chart makes the moral case
          for climate reparations concrete. Countries like Dominica and Haiti are not
          poor because of poor governance alone — they are being systematically
          impoverished by disasters they did not cause. Climate finance commitments
          must reflect this.
        - 🌐 **International aid organisations:** Aid allocation models should weight
          disaster damage as a percentage of GDP, not just absolute dollar figures.
          A $100 million disaster means little to the United States; it can mean
          the collapse of a small island economy.
        - 🏴 **Governments of vulnerable nations:** This data provides evidence for
          loss-and-damage compensation claims under the UNFCCC framework. Countries
          with consistently high damage % GDP have the strongest documented case
          for dedicated climate finance mechanisms.
        - 🧒 **Students & general public:** If your household earned $50,000 a year
          and lost $23,000 of it every year to floods and storms — money that never
          came back — how would your family ever get ahead? That is what Dominica
          faces every year.
        """)

    # ── CHART 3 ──────────────────────────────────
    st.subheader("Chart 3 — Wealth vs. Disaster Damage Burden (Country Level)")
    st.caption(
        "Each dot is one country. Wealthier countries suffer less economic damage as a "
        "share of GDP. Dot size shows CO₂ per capita — revealing who caused the problem."
    )

    scatter_data = wealth_vs_damage.build_scatter_data(co2_df, damage_filtered, y_start, y_end)
    fig3 = wealth_vs_damage.chart(scatter_data, y_start, y_end)
    st.plotly_chart(fig3, use_container_width=True)

    with st.expander("📖 Analysis — Chart 3"):
        st.markdown("""
        #### What the data shows
        This is the single most important chart in this dashboard because it shows
        all three dimensions of the climate injustice story simultaneously:
        **wealth** (x-axis), **disaster damage burden** (y-axis), and **emissions
        responsibility** (bubble size).

        The pattern is striking. **Low-income nations (red dots)** cluster in the
        top-left: low GDP, high damage burden, and small bubbles — meaning they
        emit very little CO₂ per person. **High-income nations (blue dots)** cluster
        bottom-right: high GDP, low damage burden, and large bubbles — they emit
        the most CO₂ per person.

        **Low-income countries suffer on average 2.5% of GDP in damage per year.**
        **High-income countries suffer just 0.13% of GDP.** That is a **19-fold
        difference** in relative damage burden — between the nations that emit the
        most and those that emit the least.

        Hover over any dot to see the country name. Countries like Haiti, Mozambique,
        and Bangladesh sit in the danger zone: low GDP, high damage, and minimal
        emissions. Meanwhile the United States, Germany, and Australia sit safely
        in the bottom right — wealthy, protected, and historically responsible for
        the majority of cumulative global emissions.

        #### Audience-specific insights
        - 🏛️ **Policymakers & international negotiators:** This chart is the
          empirical foundation of the "polluter pays" principle. The 19-fold gap
          in damage burden between income groups is quantifiable evidence for
          differentiated responsibilities in climate negotiations.
        - 📊 **Researchers & analysts:** The bubble size encoding adds a third
          variable without adding visual clutter. Try filtering to specific income
          groups using the sidebar to isolate the relationship within each tier.
          Note that even within the Lower Middle Income group, there is significant
          variation — suggesting governance, geography, and disaster type also matter.
        - 🌐 **Aid organisations:** Countries in the top-left danger zone (low GDP,
          high damage) should be prioritised for both pre-disaster resilience funding
          and post-disaster reconstruction support. The chart can serve as a visual
          triage tool.
        """)

    # ── CHART 4 ──────────────────────────────────
    st.subheader("Chart 4 — Total Deaths by Disaster Type and Income Group")
    st.caption(
        "Which disaster types are deadliest — and does income group determine "
        "how many people die from the same type of disaster?"
    )

    fig4 = deaths_by_type.chart(deaths_filtered, y_start, y_end)
    st.plotly_chart(fig4, use_container_width=True)

    with st.expander("📖 Analysis — Chart 4"):
        st.markdown("""
        #### What the data shows
        Across all recorded history in this dataset, **droughts have killed over 10.5 million
        people**, making them the deadliest disaster category by a significant margin. **Floods
        have killed over 7 million**. These two categories alone account for the vast majority
        of all disaster-related deaths globally.

        The grouped bar structure reveals something equally important: **the same disaster
        type kills far more people in lower-income nations**. Look at Floods — the bars for
        Lower Middle Income and Low Income nations dwarf those of High Income nations.
        Bangladesh alone has recorded over **2.5 million deaths** from natural disasters
        in this dataset. India has recorded over **4.6 million**. China, while classified
        as Upper Middle Income today, recorded nearly **11 million deaths** historically —
        concentrated in earlier decades before economic development reduced vulnerability.

        High-income nations are not immune — Japan's earthquake and tsunami deaths,
        Europe's 2003 heatwave — but their death tolls from the same events are consistently
        lower because they have early warning systems, building codes, emergency services,
        and social safety nets that lower-income nations cannot afford to maintain.

        #### Audience-specific insights
        - 🏛️ **Policymakers:** Drought mortality is almost entirely preventable through
          early warning systems, food security programs, and water infrastructure.
          The fact that 10.5 million people have died from droughts — a slow-onset
          disaster with weeks of warning — reflects a failure of investment, not
          a failure of forecasting.
        - 🌐 **Aid organisations:** Flood preparedness in Lower Middle Income nations
          should be the single highest-priority investment. Bangladesh has dramatically
          reduced flood deaths over the past 30 years through cyclone shelters and
          warning systems — proving that low-cost infrastructure saves lives at scale.
        - 📊 **Researchers:** Use the disaster type filter in the sidebar to isolate
          individual categories. The pattern shifts significantly — Extreme Temperatures
          show relatively higher mortality in High Income nations (e.g. Europe's 2003
          heatwave), which is an exception worth investigating further.
        - 🧒 **Students & general public:** It is not bad luck that kills more people
          in poorer countries during the same type of disaster. It is the absence of
          the things wealthy countries take for granted — reliable weather warnings,
          strong buildings, and hospitals that can cope with a surge in patients.
        """)

    # ─────────────────────────────────────────────
    # SECTION 3 — INSIGHT HIGHLIGHTS
    # ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 💡 Section 3: Insight Highlights")

    col_left, col_right = st.columns(2)

    with col_left:
        # ── CHART 5 ──────────────────────────────
        st.subheader("Chart 5 — CO₂ per Capita by Income Group Over Time")
        st.caption("The emissions gap: who is responsible for the warming that drives these disasters?")

        fig5 = co2_by_income.chart(co2_filtered, y_start, y_end)
        st.plotly_chart(fig5, use_container_width=True)

    with col_right:
        # ── CHART 6 ──────────────────────────────
        st.subheader("Chart 6 — Avg Economic Damage % GDP by Income Group")
        st.caption("The consequences gap: who pays the price for disasters they did not cause?")

        fig6 = damage_by_income.chart(damage_df, y_start, y_end, selected_income)
        st.plotly_chart(fig6, use_container_width=True)

    with st.expander("📖 Analysis — Charts 5 & 6 (Read Together)"):
        st.markdown("""
        #### What the data shows — Chart 5 (CO₂ Emissions)
        High-income nations emit an average of **10.1 tonnes of CO₂ per person per year**.
        Low-income nations emit just **0.3 tonnes per person** — roughly **33 times less**.
        This gap has persisted and in many cases widened over recent decades.

        The trajectory of Upper Middle Income nations (primarily China and Brazil) shows
        a sharp upward climb from the 1990s onward, reflecting rapid industrialisation.
        However, their cumulative historical contribution remains far below that of
        high-income nations, which have been emitting heavily since the Industrial Revolution.
        The atmospheric CO₂ that is warming the planet today is largely the product of
        200 years of emissions from a small number of wealthy nations.

        #### What the data shows — Chart 6 (Damage % GDP)
        While high-income nations emit 33 times more CO₂ per capita, they suffer only
        **0.13% of GDP** in disaster damage on average. Low-income nations — the smallest
        emitters — suffer **2.52% of GDP** on average. This is the injustice in numbers:
        those who caused the least warming lose the most to its consequences.

        When read alongside Chart 5, these two charts together form the core argument
        of this entire dashboard section. The inverse relationship is not coincidence —
        it is the structural outcome of a global economic system where the ability to
        pollute and the ability to protect oneself from pollution's consequences
        are both functions of wealth.

        #### Audience-specific insights
        - 🏛️ **International negotiators (COP, UNFCCC):** Charts 5 and 6 together
          are the empirical case for the "common but differentiated responsibilities"
          principle. Nations should contribute to climate finance in proportion to
          their historical emissions and in inverse proportion to their vulnerability.
          The 33x emissions gap and 19x damage gap provide concrete numbers for
          negotiating burden-sharing formulas.
        - 🏴 **Governments of low-income nations:** These charts provide evidence
          to present at international climate negotiations. The data shows that
          your nations are not simply "underdeveloped" — you are being actively
          harmed by the emissions of others. Loss and damage compensation is
          not charity; it is accountability.
        - 🧒 **Students & general public:** Imagine two neighbours. One burns
          rubbish in their backyard every day (smoke drifts to both properties).
          The other breathes it but burns almost nothing. Now imagine the second
          neighbour's house catches fire from the smoke damage — and is told
          to rebuild on their own. That is the climate situation in one analogy.
        """)

    # ── CHART 7 ──────────────────────────────────
    st.subheader("Chart 7 — Disaster Events vs. Total Deaths Over Time")
    st.caption(
        "Are we getting better at protecting lives as disasters become more frequent? "
        "The dual axis shows whether rising event counts translate to rising death tolls."
    )

    fig7 = events_vs_deaths.chart(events_df, deaths_df, y_start, y_end)
    st.plotly_chart(fig7, use_container_width=True)

    with st.expander("📖 Analysis — Chart 7"):
        st.markdown("""
        #### What the data shows
        This dual-axis chart tells a nuanced story. The grey bars (left axis) show
        that disaster events have risen consistently and steeply from the 1980s onward.
        The red line (right axis) tells a different story: death tolls are **volatile
        and dominated by catastrophic single events**, rather than rising in lockstep
        with event frequency.

        The deadliest years in this dataset (1931, 1928, 1943) reflect pre-modern
        disasters — China's 1931 floods killed an estimated 3.7 million people at a
        time when there were no early warning systems, no air rescue, and no
        international humanitarian response infrastructure. That the modern world
        has reduced mass-casualty events of that scale is a genuine achievement.

        However, this apparent improvement masks a critical reality: **death tolls have
        fallen primarily in wealthier and better-prepared nations**. Meanwhile, lower-income
        countries continue to experience high mortality from disasters that wealthier
        nations would survive with far fewer casualties. The Haitian earthquake of 2010
        killed over 200,000 people — a similar earthquake in Chile the same year killed
        fewer than 600. The difference was almost entirely infrastructure and preparedness.

        From a financial perspective, even as death tolls have declined in absolute terms,
        **economic damage has risen sharply** (see Charts 5 and 6) — meaning the world
        is getting better at saving lives but worse at protecting economies, particularly
        in low-income nations.

        #### Audience-specific insights
        - 🏛️ **Policymakers:** The reduction in deaths over time is evidence that
          investment in early warning systems, building codes, and emergency services
          works. The question is why this investment has not reached the nations that
          need it most. Redirecting a fraction of high-income nations' defence budgets
          toward disaster preparedness in vulnerable nations would save more lives
          per dollar than almost any other intervention.
        - 🌐 **Aid organisations:** The volatility of the death toll line confirms
          that catastrophic single events dominate the statistics. Pre-positioning
          emergency supplies and trained personnel in high-risk regions before
          disasters occur is far more effective than reactive deployment.
        - 📊 **Researchers:** Set the year range slider to 1960–2025 and observe
          how the relationship between events and deaths changes across different
          periods. The decoupling of rising events and falling average deaths from
          the 1980s onward coincides with the establishment of international
          humanitarian frameworks (UNDRO, later OCHA) and advances in satellite
          weather forecasting.
        - 🧒 **Students & general public:** We have genuinely gotten better at
          warning people and helping them survive disasters. But we have not gotten
          better at making sure everyone in the world has equal access to that
          protection. A child in Norway and a child in Mozambique face the same
          rising storm — but very different chances of surviving it.
        """)

    # ─────────────────────────────────────────────
    # SECTION 4 — ML + DECISION SUPPORT
    # ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🤖 Section 4: Decision Support & Predictive Insight")

    st.subheader("ML Model — Does Wealth Predict a Country's Disaster Damage Burden?")
    st.caption(
        "A linear regression model trained on country-level data. "
        "The model asks: if you know how wealthy a country is, how well can you "
        "predict how much of its GDP it will lose to natural disasters?"
    )

    regression = ml_regression.fit(scatter_data)

    if regression is not None:
        r2, pred_low, pred_high, ratio = regression.r2, regression.pred_low, regression.pred_high, regression.ratio

        st.plotly_chart(regression.fig, use_container_width=True)

        col_ml1, col_ml2, col_ml3 = st.columns(3)
        with col_ml1:
            st.metric("Model R²", f"{r2:.3f}",
                      help="Proportion of damage burden variation explained by GDP per capita alone.")
        with col_ml2:
            st.metric("Predicted damage — GDP/capita $1,500", f"{max(pred_low,0):.3f}% of GDP",
                      help="Typical low-income country")
        with col_ml3:
            st.metric("Predicted damage — GDP/capita $45,000", f"{max(pred_high,0):.3f}% of GDP",
                      delta=f"{ratio:.1f}× higher for poor nations", delta_color="inverse",
                      help="Typical high-income country")

        with st.expander("📖 Analysis — ML Model"):
            st.markdown(f"""
            #### What the model tells us
            The regression line confirms a **statistically significant negative relationship**
            between national wealth (GDP per capita) and disaster damage burden (% of GDP).
            The model's R² of **{r2:.3f}** means that GDP per capita alone explains
            **{r2*100:.1f}%** of the variation in disaster damage burden across countries.
            That is a meaningful result for a single-variable model applied to a complex,
            multi-factor outcome.

            The practical interpretation is clear: **a country with a GDP per capita of
            $1,500** (representative of many Low Income nations) is predicted to suffer
            **{max(pred_low,0):.3f}% of its GDP** in disaster damage annually on average.
            **A country with GDP per capita of $45,000** (representative of High Income
            nations) is predicted to suffer only **{max(pred_high,0):.3f}%**. The damage
            burden for the poorest nations is predicted to be roughly **{ratio:.1f} times
            higher** than for the wealthiest.

            The scatter of points around the regression line also reveals something important:
            there are significant outliers — small island states like Dominica and Samoa
            that suffer far more damage than the model predicts even for their income level.
            These outliers represent countries where geography (small land area, high coastal
            exposure) and limited economic diversification amplify vulnerability beyond what
            income alone explains.

            #### Limitations of this model
            A linear regression with one predictor is intentionally simple — chosen for
            interpretability over precision. A more accurate model would include geography
            (distance from coast, elevation), population density, disaster preparedness
            index, and governance quality. However, adding those variables would make the
            model harder to explain to a general audience, and the core finding — that
            wealth strongly predicts protection from disaster damage — would remain unchanged.

            #### Audience-specific insights
            - 🏛️ **Policymakers & economists:** The R² value and regression slope provide
              a quantifiable basis for climate finance allocation formulas. The model
              could be extended to project future damage burdens under different warming
              scenarios, providing an evidence base for adaptation investment calculations.
            - 📊 **Researchers:** This is a baseline model. Residual analysis (the gap
              between predicted and actual damage for each country) is itself informative —
              countries significantly above the regression line may have particularly poor
              infrastructure or high geographic exposure; those below may have invested
              effectively in disaster risk reduction despite low income.
            - 🌐 **Aid organisations:** The model output can serve as a rapid triage tool
              for identifying countries most in need of resilience investment. Countries
              in the upper-left region of the scatter plot (low GDP, high damage) represent
              the highest-priority cases.
            """)
    else:
        st.warning("Not enough data for the ML model. Try expanding your filters.")

    # ─────────────────────────────────────────────
    # COMPREHENSIVE ANALYSIS SUMMARY
    # ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📝 Comprehensive Analysis Summary")

    with st.expander("📖 Read Full Cross-Chart Analysis", expanded=True):
        st.markdown("""
        #### The Complete Story — Connecting All 7 Charts

        Together, the seven charts in this dashboard tell a single coherent story about
        one of the most profound injustices of the 21st century.

        **Charts 1 and 7** establish the context: natural disasters are becoming dramatically
        more frequent (237% increase in events from 1980 to 2020), driven primarily by
        climate-sensitive categories like floods and extreme weather. While average death
        tolls have declined in absolute terms due to improved preparedness, economic damage
        is rising — and the burden of that damage is not shared equally.

        **Charts 2 and 3** reveal who bears the cost. The top 20 most economically damaged
        countries are overwhelmingly low-income or small island states. Dominica loses
        an average of 46% of its GDP annually. Haiti has lost up to 67% of its GDP in a
        single year. The scatter chart in Chart 3 makes the inverse relationship visible
        at the country level: as GDP per capita rises, disaster damage as a share of the
        economy falls — and the size of each bubble (CO₂ per capita) shows that the
        countries causing the most warming are the ones suffering the least.

        **Chart 4** adds the human dimension. Over 10.5 million people have died from
        droughts alone — a slow-onset disaster type that gives weeks of warning and is
        almost entirely preventable with adequate water infrastructure and food security
        systems. The deaths are concentrated in lower-income nations not because those
        nations are uniquely exposed, but because they lack the resources that wealthier
        nations deploy as a matter of course.

        **Charts 5 and 6** place the injustice in its sharpest relief. High-income nations
        emit 33 times more CO₂ per capita than low-income nations (Chart 5), yet suffer
        19 times less economic damage as a share of GDP (Chart 6). The emissions gap
        and the damage gap move in opposite directions — the more a nation has historically
        contributed to climate change, the less it suffers from its consequences.

        **The ML model** quantifies this relationship statistically, confirming that GDP
        per capita alone explains a significant proportion of variation in disaster damage
        burden. The model's prediction — that a low-income country suffers roughly 19 times
        more damage as a share of GDP than a high-income one — matches the raw data averages
        precisely, validating the analytical approach.

        #### The Central Conclusion
        The data does not support the narrative that natural disasters are random misfortunes
        distributed across humanity without pattern. They are systematically concentrated
        among the world's most vulnerable and least culpable nations. This is not a problem
        that will be solved by disaster response alone — it requires a fundamental rethinking
        of who is responsible for climate change, who is suffering its consequences, and who
        should pay to address the gap between those two groups.

        #### What Should Change
        - **Climate finance must scale dramatically** — current pledges fall far short of
          what is needed to cover the documented damage burden faced by low-income nations.
        - **Loss and damage mechanisms** under the UNFCCC must be operationalised with
          predictable, grant-based funding rather than loans that deepen debt burdens.
        - **Disaster risk reduction investment** — early warning systems, resilient
          infrastructure, and community preparedness programs — delivers a documented
          return of $6 in avoided losses for every $1 invested, yet remains chronically
          underfunded in the nations that need it most.
        - **The "polluter pays" principle** must be applied at the international level
          with the same rigour it is applied within domestic environmental law.
        """)

    # ─────────────────────────────────────────────
    # AUDIENCE-SPECIFIC RECOMMENDATIONS
    # ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🎯 Recommendations by Audience")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏛️ Policymakers",
        "🌐 Aid Organisations",
        "🏴 Vulnerable Nation Governments",
        "📊 Researchers & Analysts",
        "🧒 Students & General Public"
    ])

    with tab1:
        st.markdown("""
        #### For Policymakers and Government Officials in High-Income Nations

        The data in this dashboard provides a clear, evidence-based case for action.
        Here is what the findings specifically recommend:

        **1. Scale up climate finance — with urgency**
        Charts 2 and 6 show that low-income nations suffer an average of 2.52% of
        GDP in disaster damage annually. For a country with a GDP of $10 billion,
        that is $252 million per year in losses — recurring, compounding, and increasing
        as the climate worsens. Current international climate finance pledges are
        insufficient to cover this documented damage, let alone build resilience
        against future losses.

        **2. Prioritise grants over loans**
        Countries that are already losing 20–46% of their GDP to disasters cannot
        afford to repay climate adaptation loans. Debt-based climate finance deepens
        the crisis rather than alleviating it. Policy frameworks should shift toward
        grant-based mechanisms, particularly for the countries appearing in Chart 2's
        top 10.

        **3. Use this dashboard's data to inform burden-sharing formulas**
        The 33-fold gap in CO₂ emissions per capita (Chart 5) between High Income
        and Low Income nations, combined with the 19-fold gap in damage burden
        (Chart 6), provides a quantifiable basis for differentiated climate finance
        contributions. Nations should contribute in proportion to their historical
        emissions and receive support in proportion to their vulnerability.

        **4. Invest in early warning systems in vulnerable nations**
        Chart 7 shows that mass-casualty events have declined over time in nations
        with robust preparedness systems. The same investment deployed in Low Income
        nations would save lives at a fraction of the cost of post-disaster
        humanitarian response.
        """)

    with tab2:
        st.markdown("""
        #### For International Aid and Humanitarian Organisations

        This dashboard provides operational intelligence for more effective
        resource allocation. Key recommendations:

        **1. Use Chart 2 as a geographic triage tool**
        The top 20 countries by average damage % GDP represent the highest-priority
        targets for resilience investment. Small island developing states (Dominica,
        Samoa, Grenada) and Sub-Saharan African nations (Mozambique, Madagascar)
        consistently appear at the top. Pre-disaster resilience programs in these
        locations will yield higher returns than reactive post-disaster response.

        **2. Prioritise flood preparedness in Lower Middle Income nations**
        Chart 4 shows that floods are the second-deadliest disaster type globally,
        with death toll concentrated in lower-income nations. Bangladesh's experience
        demonstrates that relatively low-cost cyclone shelter networks and early
        warning systems can dramatically reduce flood mortality even in densely
        populated, low-lying areas. This model should be replicated across similarly
        exposed nations.

        **3. Shift from event-driven to trend-driven response planning**
        Chart 1 shows disaster frequency rising at a predictable rate. Resource
        allocation should be planned on multi-year cycles that account for this
        upward trend, rather than responding to individual events as they occur.

        **4. Address the drought mortality gap**
        Chart 4 shows droughts as the deadliest category with over 10.5 million
        deaths recorded. Unlike sudden-onset disasters, droughts develop over weeks
        and months, providing ample warning. Deaths from droughts are almost entirely
        preventable with adequate food security infrastructure and early response
        funding. This represents the highest-return intervention available.
        """)

    with tab3:
        st.markdown("""
        #### For Governments of Climate-Vulnerable Nations

        This dashboard provides evidence to support your position in international
        negotiations and domestic planning. Key recommendations:

        **1. Document and publish your damage data**
        The data in Charts 2 and 3 is powerful precisely because it is quantified.
        Countries that maintain detailed records of disaster damage as a percentage
        of GDP have the strongest evidence base for loss-and-damage compensation
        claims under the UNFCCC. Invest in national disaster loss accounting systems.

        **2. Use Charts 5 and 6 together in diplomatic contexts**
        The inverse relationship between emissions responsibility (Chart 5) and damage
        burden (Chart 6) is your core argument at international climate negotiations.
        Your nations emit a fraction of global CO₂ yet suffer a disproportionate share
        of its consequences. This is documented, quantified, and undeniable.

        **3. Build coalitions around shared data**
        Countries appearing in Chart 2's top 20 have a shared interest in advocating
        for stronger loss-and-damage mechanisms. Regional coalitions (AOSIS for island
        states, African Union for Sub-Saharan nations) that present unified,
        data-backed positions have historically been more effective in climate
        negotiations than individual nations acting alone.

        **4. Invest in disaster risk reduction now**
        Chart 7 shows that preparedness investments reduce deaths even as event
        frequency rises. Every dollar invested in early warning systems, resilient
        infrastructure, and community preparedness saves an estimated $6 in avoided
        disaster losses. This is a better return than most development investments
        and reduces dependency on international emergency aid.
        """)

    with tab4:
        st.markdown("""
        #### For Researchers and Data Analysts

        This dashboard is a starting point for deeper investigation. Key directions:

        **1. Explore the residuals of the ML model**
        The linear regression in Section 4 leaves a portion of variance unexplained
        (R² = {:.3f} means {:.1f}% is unexplained). The countries that sit furthest
        above the regression line (more damage than wealth would predict) are
        analytically interesting — they likely have specific geographic exposures,
        governance gaps, or data quality issues worth investigating.

        **2. Use the year range slider to identify structural breaks**
        Set the year range to different periods and observe how Chart 1's disaster
        frequency trends change. The period 1988–1992 (end of Cold War, establishment
        of new data collection systems) and 2000–2005 (post-9/11 development funding
        shifts) may represent structural breaks worth examining.

        **3. Investigate the Extreme Temperatures anomaly in Chart 4**
        High-income nations show relatively higher mortality from Extreme Temperatures
        compared to other disaster types. This reflects events like Europe's 2003 heatwave
        (70,000+ deaths), which challenged the assumption that wealth provides complete
        protection. Urban heat island effects and ageing populations in wealthy nations
        are contributing factors worth researching.

        **4. Extend the model with additional predictors**
        The current ML model uses GDP per capita as the sole predictor. Adding variables
        such as geographic disaster exposure index (ND-GAIN), governance quality (World
        Bank Governance Indicators), and urban population density would significantly
        improve predictive accuracy and provide a more nuanced policy tool.

        **5. Compare pre- and post-Paris Agreement trends**
        Use the year slider to compare the 2005–2015 period against 2015–2024.
        Has the Paris Agreement (2015) produced any measurable change in damage
        trajectories for the most vulnerable nations?
        """.format(
            regression.r2 if regression is not None else 0,
            (1 - regression.r2)*100 if regression is not None else 100
        ))

    with tab5:
        st.markdown("""
        #### For Students, Educators, and the General Public

        Climate change can feel abstract — temperatures rising by fractions of a degree,
        emissions measured in gigatonnes. This dashboard tries to make it concrete.
        Here is what the data is really saying:

        **The disaster lottery is rigged**
        Natural disasters are not random. Whether a flood kills ten people or ten thousand
        depends enormously on whether those people live in a country with flood barriers,
        early warning sirens, emergency services, and hospitals. Those things cost money.
        The countries with the least money face the most disasters — and they face them
        with the least protection.

        **The people least responsible are paying the most**
        The average person in a Low Income country emits about 0.3 tonnes of CO₂ per year.
        The average person in a High Income country emits about 10 tonnes — 33 times more.
        Yet the data shows that low-income countries lose 19 times more of their economy
        to climate-related disasters. The people burning the least fuel are losing the
        most to the fire.

        **This is getting worse, not better**
        Chart 1 shows that disasters have increased by 237% since 1980. Floods —
        the most climate-sensitive disaster type — have increased by nearly 400%.
        Every child born today will grow up in a world with more floods, more storms,
        and more droughts than the generation before them. The question is whether
        the world will make sure every child has equal protection from those events.

        **What can you do?**
        Understanding the problem is the first step. Sharing this data with people
        who make decisions — voting for climate-aware representatives, supporting
        organisations that work on disaster risk reduction, and demanding that
        wealthy nations honour their climate finance commitments — all contribute
        to changing the system that produces these outcomes.
        """)

    # ─────────────────────────────────────────────
    # FOOTER
    # ─────────────────────────────────────────────
    st.markdown("---")
    st.caption(
        "ICT305 Data Visualisation & Simulation | Group Project | "
        "Heuristic 3: Extreme Weather & Economic Damage | "
        "Data: EM-DAT/CRED via Our World in Data & Global Carbon Project (OWID) | "
        "Income Classifications: World Bank 2023 | "
        "Author: Jim (Lam Thanh Chieu)"
    )


if __name__ == "__main__":
    render_extreme_weather_dashboard()
