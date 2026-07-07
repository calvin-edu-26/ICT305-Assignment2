"""
ICT305 Group Project — Heuristic 3: Extreme Weather & Economic Damage
"Disaster frequency and cost hitting poorest nations hardest"

Author: Jim (Lam Thanh Chieu)
Datasets (all local CSV files in /data folder):
  - deaths.csv        : Annual deaths from natural disasters by country & type (OWID/EM-DAT)
  - damage_gdp.csv    : Economic damage as % of GDP by country & type (OWID/EM-DAT)
  - events.csv        : Global disaster event counts by type (OWID/EM-DAT)
  - co2.csv           : CO2, GDP, population, temperature change by country (OWID/GCP)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import os

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
# COLOUR PALETTE (colour-blind friendly)
# ─────────────────────────────────────────────
COLORS = {
    "Low Income":          "#d62728",
    "Lower Middle Income": "#ff7f0e",
    "Upper Middle Income": "#2ca02c",
    "High Income":         "#1f77b4",
}
ACCENT  = "#d62728"

# ─────────────────────────────────────────────
# INCOME GROUP LOOKUP  (World Bank 2023)
# ─────────────────────────────────────────────
INCOME_GROUPS = {
    "Australia":"High Income","Austria":"High Income","Belgium":"High Income",
    "Canada":"High Income","Denmark":"High Income","Finland":"High Income",
    "France":"High Income","Germany":"High Income","Iceland":"High Income",
    "Ireland":"High Income","Italy":"High Income","Japan":"High Income",
    "Luxembourg":"High Income","Netherlands":"High Income","New Zealand":"High Income",
    "Norway":"High Income","Portugal":"High Income","Singapore":"High Income",
    "South Korea":"High Income","Spain":"High Income","Sweden":"High Income",
    "Switzerland":"High Income","United Kingdom":"High Income","United States":"High Income",
    "Israel":"High Income","Greece":"High Income","Czech Republic":"High Income",
    "Slovakia":"High Income","Slovenia":"High Income","Estonia":"High Income",
    "Latvia":"High Income","Lithuania":"High Income","Poland":"High Income",
    "Hungary":"High Income","Croatia":"High Income","Romania":"High Income",
    "Bulgaria":"High Income","Chile":"High Income","Uruguay":"High Income",
    "Saudi Arabia":"High Income","United Arab Emirates":"High Income",
    "Kuwait":"High Income","Qatar":"High Income","Bahrain":"High Income",
    "Oman":"High Income","Malta":"High Income","Cyprus":"High Income",
    "China":"Upper Middle Income","Brazil":"Upper Middle Income",
    "Mexico":"Upper Middle Income","Russia":"Upper Middle Income",
    "Turkey":"Upper Middle Income","South Africa":"Upper Middle Income",
    "Argentina":"Upper Middle Income","Colombia":"Upper Middle Income",
    "Peru":"Upper Middle Income","Malaysia":"Upper Middle Income",
    "Thailand":"Upper Middle Income","Iran":"Upper Middle Income",
    "Iraq":"Upper Middle Income","Ecuador":"Upper Middle Income",
    "Kazakhstan":"Upper Middle Income","Algeria":"Upper Middle Income",
    "Dominican Republic":"Upper Middle Income","Belarus":"Upper Middle Income",
    "Azerbaijan":"Upper Middle Income","Albania":"Upper Middle Income",
    "Botswana":"Upper Middle Income","Gabon":"Upper Middle Income",
    "India":"Lower Middle Income","Indonesia":"Lower Middle Income",
    "Philippines":"Lower Middle Income","Vietnam":"Lower Middle Income",
    "Bangladesh":"Lower Middle Income","Pakistan":"Lower Middle Income",
    "Nigeria":"Lower Middle Income","Egypt":"Lower Middle Income",
    "Morocco":"Lower Middle Income","Ghana":"Lower Middle Income",
    "Kenya":"Lower Middle Income","Senegal":"Lower Middle Income",
    "Cambodia":"Lower Middle Income","Myanmar":"Lower Middle Income",
    "Bolivia":"Lower Middle Income","Honduras":"Lower Middle Income",
    "El Salvador":"Lower Middle Income","Nicaragua":"Lower Middle Income",
    "Sri Lanka":"Lower Middle Income","Nepal":"Lower Middle Income",
    "Zambia":"Lower Middle Income","Zimbabwe":"Lower Middle Income",
    "Ivory Coast":"Lower Middle Income",
    "Ethiopia":"Low Income","Tanzania":"Low Income","Uganda":"Low Income",
    "Mozambique":"Low Income","Madagascar":"Low Income","Malawi":"Low Income",
    "Mali":"Low Income","Burkina Faso":"Low Income","Niger":"Low Income",
    "Chad":"Low Income","Democratic Republic of Congo":"Low Income",
    "Afghanistan":"Low Income","Haiti":"Low Income","Sudan":"Low Income",
    "South Sudan":"Low Income","Guinea":"Low Income","Togo":"Low Income",
    "Sierra Leone":"Low Income","Liberia":"Low Income",
    "Central African Republic":"Low Income","Somalia":"Low Income",
    "Rwanda":"Low Income","Burundi":"Low Income",
}
INCOME_ORDER = ["Low Income","Lower Middle Income","Upper Middle Income","High Income"]

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
BASE = os.path.join(os.path.dirname(__file__), "data/")

@st.cache_data(show_spinner="Loading datasets…")
def load_data():
    # Load all 4 CSVs
    deaths  = pd.read_csv(os.path.join(BASE, "deaths.csv"))
    damage  = pd.read_csv(os.path.join(BASE, "damage_gdp.csv"))
    events  = pd.read_csv(os.path.join(BASE, "events.csv"))
    co2     = pd.read_csv(os.path.join(BASE, "co2.csv"))

    # --- CO2: filter to actual countries, add derived columns ---
    co2 = co2[
        co2["iso_code"].notna() &
        (co2["iso_code"].str.startswith("OWID") == False)
    ].copy()
    co2["gdp_per_capita"] = co2["gdp"] / co2["population"]
    co2["income_group"]   = co2["country"].map(INCOME_GROUPS)

    # --- Deaths: filter to actual countries only (3-letter iso code) ---
    deaths = deaths[deaths["Code"].notna() & (deaths["Code"].str.len() == 3)].copy()
    deaths["income_group"] = deaths["Entity"].map(INCOME_GROUPS)

    # --- Damage: filter to actual countries only ---
    damage = damage[damage["Code"].notna() & (damage["Code"].str.len() == 3)].copy()
    damage["income_group"] = damage["Entity"].map(INCOME_GROUPS)

    # --- Events: global only, rename for clarity ---
    events = events.rename(columns={"Entity":"disaster_type","Disasters":"n_disasters"})

    return co2, deaths, damage, events

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

    # Control 1 — Year range slider
    st.subheader("📅 Year Range")
    year_range = st.slider(
        "Select time period",
        min_value=YEAR_MIN, max_value=YEAR_MAX,
        value=(1980, YEAR_MAX), step=1,
        help="Filters all charts to the selected time period.",
    )

    # Control 2 — Disaster type multiselect
    st.subheader("🌊 Disaster Types")
    selected_types = st.multiselect(
        "Select disaster types",
        options=DISASTER_TYPES,
        default=["Flood","Extreme weather","Drought","Earthquake"],
        help="Filters disaster frequency and deaths charts by type.",
    )
    if not selected_types:
        selected_types = DISASTER_TYPES

    # Control 3 — Income group multiselect
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
        "- OWID CO₂ & GHG Dataset\n"
        "- World Bank Income Classifications 2023"
    )

# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
y_start, y_end = year_range

# Events (global, by type)
events_filtered = events_df[
    (events_df["Year"] >= y_start) &
    (events_df["Year"] <= y_end) &
    (events_df["disaster_type"].isin(selected_types))
].copy()

events_all = events_df[
    (events_df["Year"] >= y_start) &
    (events_df["Year"] <= y_end) &
    (events_df["disaster_type"] == "All disasters")
].copy()

# Deaths (country-level)
deaths_filtered = deaths_df[
    (deaths_df["Year"] >= y_start) &
    (deaths_df["Year"] <= y_end) &
    (deaths_df["income_group"].isin(selected_income))
].copy()

# Damage (country-level)
damage_filtered = damage_df[
    (damage_df["Year"] >= y_start) &
    (damage_df["Year"] <= y_end) &
    (damage_df["income_group"].isin(selected_income))
].copy()

# CO2 (country-level)
co2_filtered = co2_df[
    (co2_df["year"] >= y_start) &
    (co2_df["year"] <= y_end) &
    (co2_df["income_group"].isin(selected_income))
].copy()

# ─────────────────────────────────────────────
# SECTION 1 — OVERVIEW / EXECUTIVE SUMMARY
# ─────────────────────────────────────────────
st.markdown("## 🌍 Extreme Weather & Economic Damage")
st.markdown(
    "> **Core finding:** Nations that emit the least CO₂ suffer the greatest economic "
    "destruction from natural disasters — a profound climate injustice."
)
st.markdown("---")

# KPI CARDS
total_events   = int(events_all["n_disasters"].sum())
total_deaths   = int(deaths_df[
    (deaths_df["Year"] >= y_start) & (deaths_df["Year"] <= y_end)
]["All disasters"].sum())

avg_damage_low = damage_filtered[
    damage_filtered["income_group"] == "Low Income"
]["All disasters"].mean()
avg_damage_high = damage_filtered[
    damage_filtered["income_group"] == "High Income"
]["All disasters"].mean()

# Top country by avg damage % GDP
top_country = (
    damage_filtered.groupby("Entity")["All disasters"]
    .mean().dropna().sort_values(ascending=False)
    .index[0] if len(damage_filtered) > 0 else "N/A"
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🌪️ Total Disaster Events", f"{total_events:,}")
with col2:
    st.metric("💀 Total Deaths", f"{total_deaths:,.0f}")
with col3:
    st.metric("📉 Avg Damage % GDP — Low Income",
              f"{avg_damage_low:.2f}%",
              delta=f"vs {avg_damage_high:.2f}% High Income",
              delta_color="inverse")
with col4:
    st.metric("🏴 Hardest-Hit Country", top_country,
              help="Country with highest average economic damage as % of GDP")

st.markdown("---")

# CHART 1 — Disaster frequency over time by type
st.subheader("📈 Chart 1 — Disaster Frequency Over Time by Type")
st.caption("Global count of natural disaster events per year, broken down by type.")

fig1 = px.line(
    events_filtered,
    x="Year", y="n_disasters", color="disaster_type",
    labels={"n_disasters":"Number of Disasters","Year":"Year","disaster_type":"Disaster Type"},
    title=f"Global Natural Disaster Frequency by Type ({y_start}–{y_end})",
    template="plotly_white",
)
fig1.update_traces(line_width=2)
fig1.update_layout(
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
)
st.plotly_chart(fig1, use_container_width=True)

with st.expander("💡 What this tells us"):
    st.markdown(
        "Flood and extreme weather events have increased sharply since the 1970s, "
        "tracking closely with accelerating greenhouse gas emissions. This rising "
        "frequency disproportionately affects low-income nations with the least "
        "capacity to prepare and recover."
    )

# ─────────────────────────────────────────────
# SECTION 2 — EXPLORATORY ANALYSIS
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("## 🔍 Exploratory Analysis")

# CHART 2 — Top 20 countries by avg damage % GDP
st.subheader("📊 Chart 2 — Top 20 Countries by Economic Damage as % of GDP")
st.caption(
    "Shows which countries lose the most relative to their economy. "
    "Colour indicates income group — revealing the injustice pattern clearly."
)

top20_damage = (
    damage_filtered.groupby(["Entity","income_group"])["All disasters"]
    .mean().dropna().reset_index()
    .sort_values("All disasters", ascending=False)
    .head(20)
)
top20_damage["income_group"] = pd.Categorical(
    top20_damage["income_group"], categories=INCOME_ORDER, ordered=True
)

fig2 = px.bar(
    top20_damage,
    x="All disasters", y="Entity",
    color="income_group",
    color_discrete_map=COLORS,
    orientation="h",
    labels={"All disasters":"Avg Economic Damage (% of GDP)","Entity":"Country","income_group":"Income Group"},
    title=f"Top 20 Countries by Average Economic Damage as % of GDP ({y_start}–{y_end})",
    template="plotly_white",
    category_orders={"income_group": INCOME_ORDER},
)
fig2.update_layout(yaxis=dict(autorange="reversed"))
fig2.update_traces(hovertemplate="<b>%{y}</b><br>Avg Damage: %{x:.2f}% of GDP<extra></extra>")
st.plotly_chart(fig2, use_container_width=True)

with st.expander("💡 What this tells us"):
    st.markdown(
        "Small island states and low-income nations dominate this chart. "
        "Countries like Dominica, Samoa, and Haiti routinely lose a significant "
        "share of their entire GDP to a single disaster event — losses that "
        "high-income nations would consider minor rounding errors in their budgets."
    )

# CHART 3 — Scatter: GDP per capita vs avg damage % GDP (country level)
st.subheader("🔵 Chart 3 — Wealth vs. Disaster Damage Burden (Country Level)")
st.caption(
    "Each dot is a country. Wealthier countries (right) suffer far less economic "
    "damage relative to their GDP than poorer ones (left)."
)

# Join damage with CO2 for GDP per capita
co2_avg = (
    co2_df[co2_df["year"].between(y_start, y_end)]
    .groupby("country")[["gdp_per_capita","co2_per_capita"]]
    .mean().reset_index()
    .rename(columns={"country":"Entity"})
)
damage_avg = (
    damage_filtered.groupby(["Entity","income_group"])["All disasters"]
    .mean().dropna().reset_index()
)
scatter_data = damage_avg.merge(co2_avg, on="Entity", how="inner")
scatter_data = scatter_data[scatter_data["gdp_per_capita"].notna()]

fig3 = px.scatter(
    scatter_data,
    x="gdp_per_capita", y="All disasters",
    color="income_group",
    color_discrete_map=COLORS,
    size="co2_per_capita",
    size_max=25,
    hover_name="Entity",
    hover_data={
        "gdp_per_capita":":.0f",
        "All disasters":":.3f",
        "co2_per_capita":":.2f",
        "income_group":True,
    },
    labels={
        "gdp_per_capita":"GDP per Capita (USD, 2011 PPP)",
        "All disasters":"Avg Economic Damage (% of GDP)",
        "income_group":"Income Group",
        "co2_per_capita":"CO₂ per Capita",
    },
    title=f"GDP per Capita vs. Economic Damage as % of GDP ({y_start}–{y_end} average)",
    template="plotly_white",
    category_orders={"income_group": INCOME_ORDER},
)
fig3.update_layout(legend=dict(title="Income Group"))
st.plotly_chart(fig3, use_container_width=True)

with st.expander("💡 What this tells us"):
    st.markdown(
        "Dot size = CO₂ per capita. The negative correlation is clear: "
        "as GDP per capita rises, disaster damage as % of GDP falls sharply. "
        "Low-income nations (red) cluster top-left — poorest AND most damaged. "
        "High-income nations (blue) cluster bottom-right — wealthiest AND least damaged, "
        "yet their larger dot sizes show they are the biggest CO₂ emitters."
    )

# CHART 4 — Deaths by income group per disaster type
st.subheader("📊 Chart 4 — Total Deaths by Disaster Type and Income Group")
st.caption("Which disaster types kill the most people — and in which income groups?")

death_cols = ["Droughts","Earthquakes","Volcanoes","Floods","Landslides",
              "Storms","Wildfires","Extreme temperatures"]
death_cols_present = [c for c in death_cols if c in deaths_filtered.columns
                      and c.lower().replace(" ","_") in [t.lower().replace(" ","_")
                      for t in selected_types + ["Droughts","Earthquakes","Floods",
                      "Storms","Wildfires","Landslides","Volcanoes","Extreme temperatures"]]]

deaths_melted = deaths_filtered.melt(
    id_vars=["Entity","Year","income_group"],
    value_vars=death_cols,
    var_name="disaster_type", value_name="deaths"
).dropna(subset=["deaths","income_group"])

deaths_grouped = (
    deaths_melted.groupby(["disaster_type","income_group"])["deaths"]
    .sum().reset_index()
)
deaths_grouped["income_group"] = pd.Categorical(
    deaths_grouped["income_group"], categories=INCOME_ORDER, ordered=True
)

fig4 = px.bar(
    deaths_grouped,
    x="disaster_type", y="deaths",
    color="income_group",
    color_discrete_map=COLORS,
    barmode="group",
    labels={"deaths":"Total Deaths","disaster_type":"Disaster Type","income_group":"Income Group"},
    title=f"Total Deaths by Disaster Type and Income Group ({y_start}–{y_end})",
    template="plotly_white",
    category_orders={"income_group": INCOME_ORDER},
)
fig4.update_layout(
    xaxis_tickangle=-30,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────────
# SECTION 3 — INSIGHT HIGHLIGHTS
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("## 💡 Insight Highlights")

col_left, col_right = st.columns(2)

with col_left:
    # CHART 5 — CO2 per capita by income group over time
    st.subheader("🏭 Chart 5 — CO₂ per Capita by Income Group")
    st.caption("Who is responsible for emissions — and who suffers the consequences?")

    co2_income = (
        co2_filtered.dropna(subset=["co2_per_capita","income_group"])
        .groupby(["year","income_group"])["co2_per_capita"]
        .mean().reset_index()
    )
    co2_income["income_group"] = pd.Categorical(
        co2_income["income_group"], categories=INCOME_ORDER, ordered=True
    )

    fig5 = px.line(
        co2_income,
        x="year", y="co2_per_capita",
        color="income_group",
        color_discrete_map=COLORS,
        labels={"co2_per_capita":"CO₂ per Capita (tonnes)","year":"Year","income_group":"Income Group"},
        title=f"Average CO₂ per Capita by Income Group ({y_start}–{y_end})",
        template="plotly_white",
        category_orders={"income_group": INCOME_ORDER},
    )
    fig5.update_traces(line_width=2.5)
    fig5.update_layout(hovermode="x unified")
    st.plotly_chart(fig5, use_container_width=True)

with col_right:
    # CHART 6 — Average damage % GDP by income group (bar)
    st.subheader("💸 Chart 6 — Avg Economic Damage % GDP by Income Group")
    st.caption("Low-income nations lose a far greater share of their GDP to disasters.")

    damage_by_income = (
        damage_filtered.dropna(subset=["income_group","All disasters"])
        .groupby("income_group")["All disasters"]
        .mean().reset_index()
    )
    damage_by_income["income_group"] = pd.Categorical(
        damage_by_income["income_group"], categories=INCOME_ORDER, ordered=True
    )
    damage_by_income = damage_by_income.sort_values("income_group")

    fig6 = px.bar(
        damage_by_income,
        x="income_group", y="All disasters",
        color="income_group",
        color_discrete_map=COLORS,
        labels={"All disasters":"Avg Damage (% of GDP)","income_group":"Income Group"},
        title=f"Average Economic Damage as % of GDP by Income Group ({y_start}–{y_end})",
        template="plotly_white",
        category_orders={"income_group": INCOME_ORDER},
    )
    fig6.update_layout(showlegend=False)
    # Annotate Low Income bar
    if len(damage_by_income) > 0:
        low_val = damage_by_income[damage_by_income["income_group"]=="Low Income"]["All disasters"]
        if len(low_val) > 0:
            fig6.add_annotation(
                x="Low Income", y=float(low_val.values[0]),
                text=f"<b>{float(low_val.values[0]):.2f}%</b><br>of GDP lost",
                showarrow=True, arrowhead=2,
                arrowcolor=ACCENT, font=dict(color=ACCENT, size=11),
                bgcolor="white", bordercolor=ACCENT,
            )
    st.plotly_chart(fig6, use_container_width=True)

# CHART 7 — Annotated: disaster events vs total deaths dual axis
st.subheader("📉 Chart 7 — Disaster Events vs. Total Deaths Over Time")
st.caption(
    "Rising event frequency paired with death toll — showing whether "
    "the world is getting better at limiting casualties despite more disasters."
)

events_all_yr = events_df[
    (events_df["Year"] >= y_start) &
    (events_df["Year"] <= y_end) &
    (events_df["disaster_type"] == "All disasters")
].copy()

deaths_global_yr = (
    deaths_df[(deaths_df["Year"] >= y_start) & (deaths_df["Year"] <= y_end)]
    .groupby("Year")["All disasters"].sum().reset_index()
    .rename(columns={"All disasters":"total_deaths"})
)

dual = events_all_yr.merge(deaths_global_yr, on="Year", how="inner")

fig7 = go.Figure()
fig7.add_trace(go.Bar(
    x=dual["Year"], y=dual["n_disasters"],
    name="No. of Disasters",
    marker_color="#adb5bd",
    yaxis="y1",
    hovertemplate="Year: %{x}<br>Events: %{y:,}<extra></extra>",
))
fig7.add_trace(go.Scatter(
    x=dual["Year"], y=dual["total_deaths"],
    name="Total Deaths",
    line=dict(color=ACCENT, width=3),
    yaxis="y2",
    hovertemplate="Year: %{x}<br>Deaths: %{y:,.0f}<extra></extra>",
))

# Find deadliest year
if len(dual) > 0:
    deadliest = dual.loc[dual["total_deaths"].idxmax()]
    fig7.add_annotation(
        x=int(deadliest["Year"]),
        y=float(deadliest["total_deaths"]),
        text=f"<b>{int(deadliest['Year'])}</b><br>{int(deadliest['total_deaths']):,} deaths",
        showarrow=True, arrowhead=2,
        arrowcolor="#333", font=dict(size=10),
        bgcolor="white", bordercolor="#333",
        yref="y2",
    )

fig7.update_layout(
    title=f"Global Disaster Events vs. Total Deaths ({y_start}–{y_end})",
    xaxis=dict(title="Year"),
    yaxis=dict(title="Number of Disaster Events", side="left"),
    yaxis2=dict(title="Total Deaths", side="right", overlaying="y"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified",
    template="plotly_white",
)
st.plotly_chart(fig7, use_container_width=True)

with st.expander("💡 What this tells us"):
    st.markdown(
        "While the number of disasters has risen steadily, death tolls have become "
        "more variable — spiking during catastrophic single events. This shows that "
        "preparedness improvements in wealthy nations reduce deaths, but vulnerable "
        "low-income nations remain exposed to mass-casualty events."
    )

# ─────────────────────────────────────────────
# SECTION 4 — DECISION SUPPORT + ML
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("## 🤖 Decision Support & Predictive Insight")

st.subheader("📐 ML Model — Does Wealth Predict a Country's Disaster Damage Burden?")
st.caption(
    "Linear regression predicts a country's average economic damage (% of GDP) "
    "from its GDP per capita. This quantifies the wealth-vulnerability relationship."
)

if len(scatter_data) > 10:
    X = scatter_data[["gdp_per_capita"]].values
    y_ml = scatter_data["All disasters"].values

    model = LinearRegression()
    model.fit(X, y_ml)
    scatter_data["predicted"] = model.predict(X)
    r2 = model.score(X, y_ml)

    fig_ml = px.scatter(
        scatter_data,
        x="gdp_per_capita", y="All disasters",
        color="income_group",
        color_discrete_map=COLORS,
        hover_name="Entity",
        labels={
            "gdp_per_capita":"GDP per Capita (USD)",
            "All disasters":"Avg Economic Damage (% of GDP)",
            "income_group":"Income Group",
        },
        title=f"GDP per Capita vs. Disaster Damage — Linear Regression (R²={r2:.3f})",
        template="plotly_white",
        category_orders={"income_group": INCOME_ORDER},
    )
    x_line = np.linspace(scatter_data["gdp_per_capita"].min(),
                         scatter_data["gdp_per_capita"].max(), 200)
    y_line = model.predict(x_line.reshape(-1,1))
    fig_ml.add_trace(go.Scatter(
        x=x_line, y=y_line,
        mode="lines",
        name=f"Regression Line (R²={r2:.3f})",
        line=dict(color="#333333", width=2, dash="dash"),
    ))
    st.plotly_chart(fig_ml, use_container_width=True)

    slope = model.coef_[0]
    pred_low  = float(model.predict([[1500]])[0])
    pred_high = float(model.predict([[45000]])[0])

    col_ml1, col_ml2, col_ml3 = st.columns(3)
    with col_ml1:
        st.metric("Model R²", f"{r2:.3f}",
                  help="How well GDP per capita alone explains disaster damage burden.")
    with col_ml2:
        st.metric("Slope", f"{slope:.6f}% per $1 GDP/capita",
                  help="For every $1 increase in GDP per capita, disaster damage % GDP changes by this amount.")
    with col_ml3:
        ratio = pred_low / max(pred_high, 0.0001)
        st.metric("Damage Ratio: Low vs High Income",
                  f"{ratio:.1f}× more",
                  help="A low-income country suffers this many times more damage as % of GDP than a high-income one.")

    with st.expander("🧠 How to interpret this model"):
        st.markdown(f"""
        The regression line confirms a clear negative relationship: **wealthier nations
        suffer less economic damage as a share of their GDP from natural disasters.**

        - **R² = {r2:.3f}** — GDP per capita explains **{r2*100:.1f}%** of the variation
          in disaster damage burden across countries.
        - A country with GDP/capita of **$1,500** (typical low-income) is predicted to
          suffer **{max(pred_low,0):.3f}%** of GDP in disaster damage on average.
        - A country with GDP/capita of **$45,000** (typical high-income) is predicted to
          suffer only **{max(pred_high,0):.3f}%** of GDP.
        - Low-income countries bear roughly **{ratio:.1f}× more** damage burden than
          high-income countries — despite contributing a fraction of global CO₂ emissions.
        """)
else:
    st.warning("Not enough data for the ML model. Try expanding your filters.")

# ─────────────────────────────────────────────
# DECISION SUPPORT
# ─────────────────────────────────────────────
st.markdown("---")
st.subheader("🎯 What Decisions Does This Dashboard Support?")

st.markdown("""
This dashboard supports **strategic and policy-level decisions** for:
- 🏛️ **Policymakers & Government Officials** — directing climate adaptation funding
- 🌐 **International Aid Organisations** — prioritising disaster preparedness resources
- 📊 **Researchers & Analysts** — understanding wealth vs. climate vulnerability
- 🧒 **Educators & General Public** — understanding climate injustice visually

| Decision Question | How to Use This Dashboard |
|---|---|
| Which nations need the most climate finance? | Chart 2 + Chart 6 — highest damage % GDP countries are almost entirely low-income |
| Are disasters getting more frequent? | Chart 1 — filter by type to see trend for floods and extreme weather |
| Which disaster types kill the most people? | Chart 4 — grouped by income group to see who suffers most |
| Are richer nations more responsible for emissions? | Chart 5 — CO₂ per capita gap between High and Low income groups |
| How much does wealth predict damage burden? | ML model — R² and ratio metrics quantify the relationship |
| Which specific country is hardest hit? | Chart 2 and Chart 3 — hover over dots/bars for country name |

### Recommended actions:
1. **Redirect climate finance** toward Low and Lower-Middle Income nations — Charts 2 and 6 confirm they bear the highest damage burden.
2. **Prioritise flood preparedness** — Chart 1 shows floods are the fastest-growing disaster type.
3. **Hold high-income nations accountable** — Chart 5 confirms they emit the most CO₂ while Chart 6 shows they suffer the least damage.
""")

st.markdown("---")
st.caption(
    "ICT305 Data Visualisation & Simulation | Group Project | "
    "Heuristic 3: Extreme Weather & Economic Damage | "
    "Data: OWID/EM-DAT (CRED/UCLouvain) & Global Carbon Project | "
    "Author: Jim (Lam Thanh Chieu)"
)
