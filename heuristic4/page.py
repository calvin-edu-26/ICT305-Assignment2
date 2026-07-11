import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path

# ============================================================
# CONFIGURATION
# Stores: Dataset file paths, Colour palettes, Scenario labels and Country name replacements
# ============================================================

DATA_DIR = Path(__file__).parent / "Datasets"

FILES = {
    "co2": DATA_DIR / "annual-co2-emissions-per-country.csv",
    "gdp": DATA_DIR / "GDPperCapita.csv",
    "population": DATA_DIR / "Population.csv",
    "density": DATA_DIR / "pop-x1_timeseries_pov550,popcount,popdensity_timeseries_annual_2000-2000,2010-2100_mean_historical_gpw-v4_rev11_mean.xlsx",
    "sea_level": DATA_DIR / "sealevel_global_explorer_data_global.xlsx"
}

RISK_COLORS = {
    "Critical Risk": "#DC2626",
    "High Exposure, Higher Capacity": "#F97316",
    "Emerging Risk": "#2563EB",
    "Lower Risk": "#16A34A"
}

SCENARIO_LABELS = {
    "Historical": "Historical observations",
    "ssp126": "SSP1-2.6: Strong climate action",
    "ssp245": "SSP2-4.5: Moderate pathway",
    "ssp585": "SSP5-8.5: Very high emissions"
}

SCENARIO_COLORS = {
    "Historical observations": "#111827",
    "SSP1-2.6: Strong climate action": "#16A34A",
    "SSP2-4.5: Moderate pathway": "#2563EB",
    "SSP5-8.5: Very high emissions": "#DC2626"
}

COUNTRY_RENAMES = {
    "United States of America": "United States",
    "Russian Federation": "Russia",
    "Viet Nam": "Vietnam",
    "Korea, Rep.": "South Korea",
    "Korea, Dem. People's Rep.": "North Korea",
    "Iran, Islamic Rep.": "Iran",
    "Egypt, Arab Rep.": "Egypt",
    "Congo, Dem. Rep.": "Democratic Republic of Congo",
    "Congo, Rep.": "Congo",
    "Bahamas, The": "Bahamas",
    "Gambia, The": "Gambia",
    "Yemen, Rep.": "Yemen",
    "Venezuela, RB": "Venezuela",
    "Lao PDR": "Laos",
    "Syrian Arab Republic": "Syria"
}

# ============================================================
# STYLING
# Controls the overall look of the dashboard: Header design, Story cards, Tabs and Footer
# ============================================================

def load_css():
    st.markdown("""
<style>
/* =========================================================
   GENERAL PAGE SPACING
   ========================================================= */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* =========================================================
   HERO HEADER
   Keeps its own dark-blue design in both themes.
   ========================================================= */

.hero {
    padding: 30px;
    border-radius: 22px;
    background: linear-gradient(90deg, #082032, #0F4C75);
    color: #ffffff;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 8px;
    color: #ffffff;
}

.hero p {
    font-size: 18px;
    color: #dbeafe;
}


/* =========================================================
   STORY, INSIGHT AND RECOMMENDATION CARDS
   Uses Streamlit theme variables so light and dark modes work.
   ========================================================= */

.section-card,
.story-box {
    padding: 22px;
    border-radius: 18px;
    border: 1px solid rgba(128, 128, 128, 0.30);
    margin: 18px 0;

    background-color: var(--secondary-background-color);
    color: var(--text-color);
}


/* Headings inside cards */
.section-card h1,
.section-card h2,
.section-card h3,
.section-card h4,
.story-box h1,
.story-box h2,
.story-box h3,
.story-box h4 {
    color: var(--text-color) !important;
    margin-top: 0;
}


/* Paragraphs and list items inside cards */
.section-card p,
.section-card li,
.story-box p,
.story-box li {
    color: var(--text-color) !important;
    font-size: 15px;
    line-height: 1.7;
}


/* Bold text must also follow the active theme */
.section-card b,
.section-card strong,
.story-box b,
.story-box strong {
    color: var(--text-color) !important;
}


/* Improve list spacing */
.story-box ul,
.section-card ul {
    margin-top: 10px;
    margin-bottom: 12px;
    padding-left: 24px;
}

.story-box li,
.section-card li {
    margin-bottom: 7px;
}


/* =========================================================
   TABS
   ========================================================= */

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background-color: var(--secondary-background-color);
    padding: 12px;
    border-radius: 18px;
    margin-bottom: 20px;
}

.stTabs [data-baseweb="tab"] {
    height: 55px;
    padding: 12px 20px;
    border-radius: 14px;

    background-color: var(--background-color);
    border: 1px solid rgba(128, 128, 128, 0.30);
    font-weight: 700;
    color: var(--text-color);
}

.stTabs [aria-selected="true"] {
    background-color: #0F4C75 !important;
    color: #ffffff !important;
    border: 1px solid #0F4C75 !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    padding: 20px;
    text-align: center;
    color: var(--text-color);
    opacity: 0.75;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SMALL UI COMPONENTS
# Reusable functions for HTML code.
# ============================================================

# Creates the explanation card above each chart.
def story_header(number, title, subtitle):

    st.markdown(f"""
<div class="section-card">
<h3>{number} {title}</h3>
<p>{subtitle}</p>
</div>
""", unsafe_allow_html=True)

# Creates a reusable insights and analysis box.
def insight_box(insights, analysis, conclusion=None):

    bullets = "".join(
        f"<li>{item}</li>"
        for item in insights
    )

    conclusion_html = ""

    if conclusion:
        conclusion_html = f"""
<h3 style="margin-top:22px;">Key Takeaway</h3>
<p style="font-size:20px;font-weight:700;color:var(--text-color);line-height:1.5;">
{conclusion}
</p>
"""

    st.markdown(
        f"""
<div class="story-box">
<h3>🔍 Insights</h3>

<ul>
{bullets}
</ul>

<h3>📊 Analysis</h3>

<p>{analysis}</p>

{conclusion_html}
</div>
""",
        unsafe_allow_html=True
    )

def recommendation_box(recommendations):

    bullets = "".join(
        f"<li>{item}</li>"
        for item in recommendations
    )

    st.markdown(
        f"""
<div class="story-box">
<h3>💡 Recommendations</h3>

<ul>
{bullets}
</ul>
</div>
""",
        unsafe_allow_html=True
    )

# Explains the risk zone colours used in Chart 1.
def risk_zone_legend():

    st.markdown("""
<div class="story-box">
<h3>Understanding the Risk Zones</h3>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:20px;">

<div style="display:flex;align-items:flex-start;gap:12px;">
<div style="width:18px;height:18px;background:#DC2626;border-radius:4px;margin-top:3px;flex-shrink:0;"></div>
<div>
<b style="color:var(--text-color);">Critical Risk</b>
<p style="margin:6px 0 0 0;color:var(--text-color);opacity:0.85;">
High displacement pressure combined with lower economic capacity.
These countries need urgent adaptation support.
</p>
</div>
</div>

<div style="display:flex;align-items:flex-start;gap:12px;">
<div style="width:18px;height:18px;background:#F97316;border-radius:4px;margin-top:3px;flex-shrink:0;"></div>
<div>
<b style="color:var(--text-color);">High Exposure, Higher Capacity</b>
<p style="margin:6px 0 0 0;color:var(--text-color);opacity:0.85;">
High exposure but stronger economic ability to invest in adaptation and resilience.
</p>
</div>
</div>

</div>
</div>
""", unsafe_allow_html=True)

# Explains how stakeholders should use the dashboard.
def decision_support_box():

    st.markdown("""
<div class="story-box">
<h3>Decision Support</h3>
<p>
This dashboard helps decision-makers identify where climate adaptation support should be prioritised.
</p>

<ul>
<li><b>Governments:</b> plan relocation, coastal protection, and adaptation funding.</li>
<li><b>NGOs:</b> identify countries needing urgent humanitarian or resilience support.</li>
<li><b>International climate agencies:</b> compare exposure, responsibility, and adaptive capacity.</li>
<li><b>Policymakers:</b> prioritise countries where high displacement pressure overlaps with lower economic readiness.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ============================================================
# DATA CLEANING HELPERS
# Functions to clean names, reshape datasets, and classify risk.
# ============================================================

# Standardises country names so datasets can merge correctly.
def clean_country_name(name):

    if pd.isna(name):
        return name

    name = str(name).strip()
    return COUNTRY_RENAMES.get(name, name)

# Converts technical scenario codes into readable labels.
def scenario_name(code):

    return SCENARIO_LABELS.get(str(code), str(code))

# This converts World Bank datasets year columns into rows and keeps the latest value.
def latest_year_value(df, id_cols):

    year_cols = [col for col in df.columns if str(col).isdigit()]

    long_df = df.melt(
        id_vars=id_cols,
        value_vars=year_cols,
        var_name="year",
        value_name="value"
    )

    long_df["year"] = pd.to_numeric(long_df["year"], errors="coerce")
    long_df["value"] = pd.to_numeric(long_df["value"], errors="coerce")

    return (
        long_df
        .dropna(subset=["value"])
        .sort_values("year")
        .groupby(id_cols, as_index=False)
        .tail(1)
    )

#     Classifies countries into four risk zones using displacement pressure and GDP per capita as adaptation capacity
def classify_risk(row, median_pressure, median_gdp):


    high_pressure = row["displacement_pressure"] >= median_pressure
    high_gdp = row["gdp_per_capita"] >= median_gdp

    if high_pressure and not high_gdp:
        return "Critical Risk"

    if high_pressure and high_gdp:
        return "High Exposure, Higher Capacity"

    if not high_pressure and not high_gdp:
        return "Emerging Risk"

    return "Lower Risk"

# ============================================================
# DATA LOADERS
# Each function loads one dataset only.
# @st.cache_data makes the dashboard faster after first load.
# ============================================================

# Loads latest annual CO₂ emissions by country.
@st.cache_data
def load_co2():

    co2 = pd.read_csv(FILES["co2"]).rename(columns={
        "Entity": "country",
        "Code": "country_code",
        "Year": "year",
        "Annual CO₂ emissions": "annual_co2"
    })

    co2["country"] = co2["country"].apply(clean_country_name)
    co2["annual_co2"] = pd.to_numeric(co2["annual_co2"], errors="coerce")

    return (
        co2
        .dropna(subset=["country_code"])
        .sort_values("year")
        .groupby(["country", "country_code"], as_index=False)
        .tail(1)
        [["country", "country_code", "annual_co2"]]
    )

# Loads World Bank CSV files and keeps the latest available value.
@st.cache_data
def load_world_bank_csv(file_path, value_name):

    df = pd.read_csv(file_path, skiprows=4)

    latest = latest_year_value(
        df,
        ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
    )

    latest = latest.rename(columns={
        "Country Name": "country",
        "Country Code": "country_code",
        "value": value_name
    })

    latest["country"] = latest["country"].apply(clean_country_name)

    return latest[["country", "country_code", value_name]]

#     Loads population exposure and density from the Excel dataset.
@st.cache_data
def load_population_density():

    workbook = pd.ExcelFile(FILES["density"])

    pop_sheet = next(s for s in workbook.sheet_names if "popcount" in s.lower())
    density_sheet = next(s for s in workbook.sheet_names if "popdensity" in s.lower())

    pop = pd.read_excel(FILES["density"], sheet_name=pop_sheet)
    density = pd.read_excel(FILES["density"], sheet_name=density_sheet)

    pop_value_col = [c for c in pop.columns if c not in ["code", "name"]][0]
    density_value_col = [c for c in density.columns if c not in ["code", "name"]][0]

    pop = pop.rename(columns={
        "code": "country_code",
        "name": "country",
        pop_value_col: "popcount_exposure"
    })

    density = density.rename(columns={
        "code": "country_code",
        "name": "country",
        density_value_col: "population_density"
    })

    output = pop[["country_code", "country", "popcount_exposure"]].merge(
        density[["country_code", "population_density"]],
        on="country_code",
        how="inner"
    )

    output["country"] = output["country"].apply(clean_country_name)
    output["popcount_exposure"] = pd.to_numeric(output["popcount_exposure"], errors="coerce")
    output["population_density"] = pd.to_numeric(output["population_density"], errors="coerce")

    return output

# Loads historical and projected global sea-level change.
@st.cache_data
def load_sea_level():

    observed = pd.read_excel(
        FILES["sea_level"],
        sheet_name="Observations-Extrapolation"
    ).rename(columns={
        "Year": "year",
        "Observation Extrapolation 50th": "sea_level_mm"
    })

    observed = observed[["year", "sea_level_mm"]].copy()
    observed["scenario"] = "Historical"
    observed["scenario_label"] = "Historical observations"

    future = pd.read_excel(FILES["sea_level"], sheet_name="Future-Total")

    if "quantile" in future.columns:
        future = future[future["quantile"] == 50]

    year_cols = [col for col in future.columns if str(col).isdigit()]

    future = future.melt(
        id_vars=["scenario"],
        value_vars=year_cols,
        var_name="year",
        value_name="sea_level_mm"
    )

    future["scenario_label"] = future["scenario"].apply(scenario_name)

    output = pd.concat([observed, future], ignore_index=True)

    output["year"] = pd.to_numeric(output["year"], errors="coerce")
    output["sea_level_mm"] = pd.to_numeric(output["sea_level_mm"], errors="coerce")

    return output.dropna(subset=["year", "sea_level_mm"])

# ============================================================
# DATASET BUILDER
# Combines all country-level datasets into one dataframe.
# ============================================================

@st.cache_data
def build_country_dataset():
    co2 = load_co2()
    gdp = load_world_bank_csv(FILES["gdp"], "gdp_per_capita")
    population = load_world_bank_csv(FILES["population"], "population_total")
    exposure = load_population_density()

    df = (
        exposure
        .merge(gdp[["country_code", "gdp_per_capita"]], on="country_code", how="left")
        .merge(population[["country_code", "population_total"]], on="country_code", how="left")
        .merge(co2[["country_code", "annual_co2"]], on="country_code", how="left")
    )

    df = df.dropna(subset=[
        "popcount_exposure",
        "population_density",
        "gdp_per_capita"
    ])

    df = df[
        (df["popcount_exposure"] > 0)
        & (df["population_density"] > 0)
        & (df["gdp_per_capita"] > 0)
    ].copy()

    # Custom index used to estimate displacement pressure.
    df["displacement_pressure"] = (
        np.log1p(df["popcount_exposure"])
        * np.log1p(df["population_density"])
    )

    # CO₂ per person proxy adds a responsibility comparison.
    df["co2_per_person_proxy"] = (
        df["annual_co2"] / df["population_total"].replace(0, pd.NA)
    )

    median_pressure = df["displacement_pressure"].median()
    median_gdp = df["gdp_per_capita"].median()

    df["risk_zone"] = df.apply(
        lambda row: classify_risk(row, median_pressure, median_gdp),
        axis=1
    )

    return df

# ============================================================
# KPI FUNCTION
# Used by the Overview page to display Heuristic 4's KPI.
# ============================================================

@st.cache_data
def get_critical_risk_count():
    """
    Returns the total number of countries classified
    as Critical Risk.
    """

    country_df = build_country_dataset()

    return int(
        (country_df["risk_zone"] == "Critical Risk").sum()
    )

# ============================================================
# CHART STYLE HELPER
# Applies consistent layout to every Plotly chart.
# ============================================================

def clean_fig(fig, height=650):
    """
    Applies a consistent Plotly style that automatically
    adapts to Streamlit Light and Dark mode.
    """

    fig.update_layout(

        # Use Plotly's default template instead of white
        template="plotly",

        height=height,

        # Transparent backgrounds
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=60
        ),

        font=dict(size=14),

        title=dict(
            font=dict(size=20)
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0
        )
    )

    fig.update_xaxes(
        showgrid=True,
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        zeroline=False
    )

    return fig

# ============================================================
# CHART FUNCTIONS
# Each function creates one chart and returns a Plotly figure.
# ============================================================

# Chart 1: ranks countries by displacement pressure.
def chart_population_pressure(df, top_n):

    plot_df = (
        df
        .query("population_total > 1000000")
        .sort_values("displacement_pressure", ascending=False)
        .head(top_n)
        .sort_values("displacement_pressure")
    )

    fig = px.bar(
        plot_df,
        x="displacement_pressure",
        y="country",
        orientation="h",
        color="risk_zone",
        title="Countries with Highest Displacement Pressure",
        labels={
            "displacement_pressure": "Displacement pressure index",
            "country": "Country",
            "risk_zone": "Risk zone"
        },
        color_discrete_map=RISK_COLORS,
        hover_data={
            "popcount_exposure": ":,.0f",
            "population_density": ":,.2f",
            "gdp_per_capita": ":,.0f",
            "annual_co2": ":,.0f"
        }
    )

    fig = clean_fig(fig, height=560)
    fig.update_layout(legend=dict(orientation="v", y=1, x=1.02))

    return fig

# Chart 2: shows global population density distribution.
def chart_density_map(df):

    plot_df = df.copy()
    plot_df["density_display"] = np.log1p(plot_df["population_density"])

    fig = px.choropleth(
        plot_df,
        locations="country_code",
        color="density_display",
        hover_name="country",
        title="Global Population Density Map",
        color_continuous_scale=[
            [0, "#F8FAFC"],
            [0.2, "#FDE68A"],
            [0.5, "#FB923C"],
            [1, "#DC2626"]
        ],
        labels={"density_display": "Population Density"},
        hover_data={
            "population_density": ":,.2f",
            "popcount_exposure": ":,.0f",
            "gdp_per_capita": ":,.2f",
            "annual_co2": ":,.0f",
            "country_code": False,
            "density_display": False
        }
    )

    fig.update_geos(
        projection_type="natural earth",
        showcountries=True,
        countrycolor="#64748b",
        showcoastlines=True,
        coastlinecolor="#64748b",
        showframe=False,
        bgcolor="rgba(0,0,0,0)"
    )

    return clean_fig(fig, height=760)

# Chart 3: shows historical and projected sea-level rise.
def chart_sea_level(sea_level_df, selected_scenarios):

    plot_df = sea_level_df[
        (sea_level_df["scenario"] == "Historical")
        | (sea_level_df["scenario"].isin(selected_scenarios))
    ].copy()

    plot_df = (
        plot_df
        .groupby(["year", "scenario_label"], as_index=False)["sea_level_mm"]
        .mean()
        .sort_values(["scenario_label", "year"])
    )

    fig = px.line(
        plot_df,
        x="year",
        y="sea_level_mm",
        color="scenario_label",
        color_discrete_map=SCENARIO_COLORS,
        title="Observed and Projected Global Mean Sea Level Change",
        labels={
            "year": "Year",
            "sea_level_mm": "Sea level change (mm)",
            "scenario_label": ""
        }
    )

    for trace in fig.data:
        trace.line.width = 6 if "Historical" in trace.name else 4

    fig.add_vline(x=2025, line_dash="dot", line_color="#475569")

    fig.add_annotation(
        x=2025,
        y=1.05,
        yref="paper",
        text="Today",
        showarrow=False,
        font=dict(size=14, color="#0f172a")
    )

    fig = clean_fig(fig, height=550)

    fig.update_layout(
        legend=dict(orientation="h", y=1.18, x=0, title_text=""),
        margin=dict(t=150, b=60, l=40, r=40),
        hovermode="x unified"
    )

    return fig

# Chart 4: compares exposure, GDP, and CO₂ emissions.
def chart_adaptation_capacity(df):

    plot_df = df.dropna(subset=["annual_co2"]).copy()
    plot_df = plot_df[plot_df["annual_co2"] > 0]

    plot_df["co2_size"] = np.sqrt(plot_df["annual_co2"])
    plot_df["co2_size"] = plot_df["co2_size"].clip(
        upper=plot_df["co2_size"].quantile(0.97)
    )

    fig = px.scatter(
        plot_df,
        x="gdp_per_capita",
        y="popcount_exposure",
        size="co2_size",
        size_max=28,
        color="risk_zone",
        hover_name="country",
        log_x=True,
        log_y=True,
        title="Population Exposure Compared with Economic Capacity (GDP per Capita)",
        labels={
            "gdp_per_capita": "GDP per capita",
            "popcount_exposure": "Population exposed",
            "co2_size": "Annual CO₂ emissions",
            "risk_zone": "Risk zone"
        },
        color_discrete_map=RISK_COLORS,
        hover_data={
            "annual_co2": ":,.0f",
            "population_density": ":,.2f",
            "co2_per_person_proxy": ":,.4f",
            "co2_size": False
        }
    )

    fig.update_traces(
        marker=dict(opacity=0.72, line=dict(width=0.7, color="white"))
    )

    return clean_fig(fig, height=720)

# Chart 5: combines pressure and capacity into a decision matrix.
def chart_risk_matrix(df):

    plot_df = df.copy()

    plot_df["pressure_display"] = plot_df["displacement_pressure"].clip(
        upper=plot_df["displacement_pressure"].quantile(0.95)
    )

    plot_df["gdp_display"] = plot_df["gdp_per_capita"].clip(
        upper=plot_df["gdp_per_capita"].quantile(0.90)
    )

    plot_df["population_display"] = plot_df["popcount_exposure"].clip(
        upper=plot_df["popcount_exposure"].quantile(0.95)
    )

    plot_df["log_gdp"] = np.log1p(plot_df["gdp_display"])

    median_pressure = plot_df["pressure_display"].median()
    median_gdp = plot_df["log_gdp"].median()

    fig = px.scatter(
        plot_df,
        x="pressure_display",
        y="log_gdp",
        size="population_display",
        color="risk_zone",
        hover_name="country",
        title="Country Displacement Vulnerability Matrix",
        labels={
            "pressure_display": "Higher → More displacement pressure",
            "log_gdp": "Higher → Greater economic capacity",
            "population_display": "Population exposed",
            "risk_zone": "Risk zone"
        },
        color_discrete_map=RISK_COLORS,
        hover_data={
            "population_density": ":,.2f",
            "gdp_per_capita": ":,.2f",
            "popcount_exposure": ":,.0f",
            "annual_co2": ":,.0f",
            "co2_per_person_proxy": ":,.4f",
            "pressure_display": False,
            "log_gdp": False,
            "population_display": False
        }
    )

    fig.add_vline(
        x=median_pressure,
        line_dash="dash",
        line_color="#334155",
        annotation_text="Median Displacement Pressure",
        annotation_position="top left"
    )

    fig.add_hline(
        y=median_gdp,
        line_dash="dash",
        line_color="#334155",
        annotation_text="Median Economic Capacity",
        annotation_position="bottom right"
    )

    fig.update_traces(marker=dict(opacity=0.8))

    return clean_fig(fig, height=760)

# ============================================================
# SIDEBAR FILTERS
# Creates user controls and returns filtered data.
# ============================================================

def sidebar_filters(country_df, sea_level_df):
    st.sidebar.header("Dashboard Filters")

    top_n = st.sidebar.slider(
        "Countries shown in ranking charts",
        min_value=5,
        max_value=30,
        value=15,
        step=5
    )

    selected_risk_zones = st.sidebar.multiselect(
        "Risk zones shown",
        options=list(RISK_COLORS.keys()),
        default=list(RISK_COLORS.keys())
    )

    scenario_list = sorted(sea_level_df["scenario"].dropna().unique())

    default_scenarios = [
        s for s in ["ssp126", "ssp245", "ssp585"]
        if s in scenario_list
    ]

    selected_scenarios = st.sidebar.multiselect(
        "Sea level projection scenarios",
        scenario_list,
        default=default_scenarios,
        format_func=scenario_name
    )

    selected_countries = st.sidebar.multiselect(
        "Countries shown in table",
        sorted(country_df["country"].dropna().unique())
    )

    filtered_df = country_df[
        country_df["risk_zone"].isin(selected_risk_zones)
    ].copy()

    return filtered_df, top_n, selected_scenarios, selected_countries

# ============================================================
# PAGE SECTIONS
# Each render function controls one dashboard section or tab.
# ============================================================

# Renders dashboard title and usage instructions.
def render_header():

    st.markdown("""
<div class="hero">
<h1>Do countries that contribute less to climate change suffer more from its impacts?</h1>
<p>Exploring the unequal burden of climate change across countries</p>
</div>
""", unsafe_allow_html=True)

    with st.expander("How to use this dashboard"):
        st.write("""
        1. Use the sidebar filters to adjust countries, risk zones, and sea-level scenarios.
        2. Start with Chart 1 to identify countries under the most displacement pressure.
        3. Use Chart 2 to see where population concentration is located.
        4. Use Chart 3 to understand how sea-level rise may grow over time.
        5. Use Chart 4 to compare exposure, economic capacity, and CO₂ responsibility.
        6. Use Chart 5 to identify which countries may need support most urgently.
        """)

# Renders KPI cards required for the executive summary.
def render_overview(df):

    st.markdown("## Dashboard Overview")

    critical_count = (df["risk_zone"] == "Critical Risk").sum()

    highest_country = (
        df.sort_values("displacement_pressure", ascending=False).iloc[0]["country"]
        if len(df) > 0
        else "No data"
    )

    avg_exposure = df["popcount_exposure"].mean() if len(df) > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Countries analysed", f"{len(df):,}")
    col2.metric("Critical Risk countries", f"{critical_count:,}")
    col3.metric("Highest pressure country", highest_country)
    col4.metric("Average population exposed", f"{avg_exposure:,.0f}")

    st.divider()

# Renders Chart 1 and its supporting insight explanation.
def render_tab_1(df, top_n):

    story_header(
        "①",
        "Who is under pressure?",
        """
        This chart ranks countries with the highest displacement pressure based on exposed population and density.<br><br>
        Displacement pressure estimates how difficult and severe population displacement could become if environmental impacts force people to move.<br><br>
        <b>Displacement Pressure Index = log(1 + Population Exposed) × log(1 + Population Density)</b>
        """
    )

    st.plotly_chart(
        chart_population_pressure(df, top_n),
        use_container_width=True,
        theme="streamlit"
    )

    risk_zone_legend()

    insight_box(
        [
            "South Asian countries dominate the highest displacement pressure rankings.",
            "Bangladesh and India show the greatest pressure due to large exposed populations and dense settlement patterns.",
            "Critical Risk countries combine high displacement pressure with relatively lower economic capacity."
        ],
        "Displacement pressure is not determined by population size alone. Countries become more vulnerable when large numbers of people are concentrated in limited space, making relocation and adaptation more difficult during climate-related events such as sea level rise."
    )

    recommendation_box([
        "Prioritise climate adaptation funding for countries with the highest displacement pressure.",
        "Invest in resilient housing, coastal protection, and emergency shelters in densely populated coastal regions.",
        "Develop long-term relocation and land-use planning for communities most vulnerable to sea-level rise.",
        "Strengthen disaster preparedness and early warning systems in high-risk countries."
    ])

# Renders Chart 2 and explains geographic concentration.
def render_tab_2(df):

    story_header(
        "②",
        "Where is the pressure located?",
        "This chart shows where populations are geographically concentrated and uses population density as an indicator of displacement pressure."
    )

    st.plotly_chart(
        chart_density_map(df),
        use_container_width=True,
        theme="streamlit"
    )

    insight_box(
        [
            "Population concentration is strongest across South Asia, East Asia, and parts of Europe.",
            "Regions with higher density may experience stronger displacement impacts when environmental hazards occur.",
            "Countries with lower density generally have more spatial flexibility for adaptation."
        ],
        "Population density is used as an indicator of displacement pressure because environmental disruption affects more people when populations are geographically concentrated. Dense urban and coastal regions may therefore experience larger social and infrastructure impacts."
    )

    recommendation_box([
        "Focus adaptation programmes in densely populated coastal regions where relocation is more difficult.",
        "Improve evacuation planning and disaster response for areas with large exposed populations.",
        "Encourage sustainable urban planning that reduces future climate vulnerability.",
        "Prioritise infrastructure upgrades in regions where population concentration increases climate risk."
    ])

# Renders Chart 3 and explains future sea-level trends.
def render_tab_3(sea_level_df, selected_scenarios):

    story_header(
        "③",
        "How will the threat grow over time?",
        "This chart shows how global sea level has changed in the past and how it may continue to rise in the future under different climate scenarios."
    )

    st.plotly_chart(
        chart_sea_level(sea_level_df, selected_scenarios),
        use_container_width=True,
        theme="streamlit"
    )

    insight_box(
        [
            "Sea level rises under all future climate scenarios.",
            "Strong climate action slows long-term growth but does not fully stop it.",
            "High-emission pathways produce substantially larger increases over time.",
            "The widening gap between scenarios suggests delayed climate action increases long-term adaptation costs."
        ],
        "The divergence between scenarios becomes larger after today's period, showing that current decisions strongly influence future outcomes. Even moderate mitigation significantly reduces long-term displacement pressure compared with worst-case pathways."
    )

    recommendation_box([
        "Accelerate emissions reduction to minimise long-term sea-level rise.",
        "Increase investment in coastal adaptation before projected impacts become more severe.",
        "Incorporate future climate scenarios into national infrastructure and urban planning.",
        "Expand long-term monitoring to support evidence-based adaptation strategies."
    ])

# Renders Chart 4 and explains affordability/adaptation capacity.
def render_tab_4(df):

    story_header(
        "④",
        "Can countries afford to adapt?",
        "This chart compares population exposure with GDP per capita while bubble size reflects responsibility through annual CO₂ emissions."
    )

    st.plotly_chart(
        chart_adaptation_capacity(df),
        use_container_width=True,
        theme="streamlit"
    )

    st.caption(
        "Note: Countries without available CO₂ values are excluded from this chart only. "
        "CO₂ bubble sizes use square-root scaling and are capped at the 97th percentile for readability."
    )

    insight_box(
        [
            "Countries with lower GDP per capita tend to face greater difficulty responding to population exposure.",
            "Larger bubbles indicate countries with higher annual CO₂ emissions.",
            "Several highly exposed countries are not necessarily the largest contributors to emissions."
        ],
        "This chart highlights a climate equity challenge: countries experiencing the greatest displacement exposure are often not the countries most responsible for emissions. Economic capacity influences how effectively countries can invest in protection, relocation, and long-term climate resilience."
    )

    recommendation_box([
        "Direct international climate finance towards highly exposed countries with limited economic capacity.",
        "Strengthen adaptation funding alongside emissions reduction efforts.",
        "Encourage technology transfer and capacity-building programmes for vulnerable developing nations.",
        "Support climate-resilient infrastructure where exposure is high but financial resources are limited."
    ])

# Renders Chart 5 and decision-support guidance.
def render_tab_5(df):

    story_header(
        "⑤",
        "Who needs help the most?",
        "This chart combines displacement pressure and economic capacity into a vulnerability matrix to identify countries needing the most support."
    )

    st.plotly_chart(
        chart_risk_matrix(df),
        use_container_width=True,
        theme="streamlit"
    )

    insight_box(
        [
            "Countries in the Critical Zone face both high displacement pressure and lower economic capacity.",
            "Prepared But Exposed countries face strong pressure but possess greater ability to adapt.",
            "Lower Risk countries generally combine lower pressure with stronger resilience."
        ],
        "This matrix identifies where support may be most urgently needed. Countries in the Critical Zone experience both elevated displacement pressure and lower economic readiness, suggesting that climate impacts are shaped not only by exposure but also by unequal adaptive capacity.",
        "Countries most in need of support are often not those most responsible for emissions — reinforcing the unequal burden of climate change."
    )

    recommendation_box([
        "Prioritise Critical Risk countries for immediate adaptation funding and international assistance.",
        "Allocate resources based on both displacement pressure and adaptive capacity rather than emissions alone.",
        "Use the risk categories to guide climate investment, humanitarian planning, and resilience programmes.",
        "Regularly reassess risk classifications as new climate and socioeconomic data become available."
    ])

    decision_support_box()

# Renders data table and download option.
def render_tab_6(df, selected_countries):

    story_header(
        "⑥",
        "Country-level Dataset",
        "Use this table to inspect the indicators behind the dashboard."
    )

    if selected_countries:
        table_df = df[df["country"].isin(selected_countries)]
    else:
        table_df = df.sort_values(
            "displacement_pressure",
            ascending=False
        ).head(30)

    display_cols = [
        "country",
        "country_code",
        "popcount_exposure",
        "population_density",
        "displacement_pressure",
        "gdp_per_capita",
        "annual_co2",
        "co2_per_person_proxy",
        "risk_zone"
    ]

    st.dataframe(table_df[display_cols], use_container_width=True)

    st.download_button(
        "Download filtered dataset",
        table_df[display_cols].to_csv(index=False),
        "climate_dashboard_filtered_data.csv",
        "text/csv"
    )

# ============================================================
# MAIN DASHBOARD FUNCTION
# ============================================================

# Main function that runs the whole dashboard.
def render_climate_dashboard():

    load_css()

    country_df = build_country_dataset()
    sea_level_df = load_sea_level()

    filtered_df, top_n, selected_scenarios, selected_countries = sidebar_filters(
        country_df,
        sea_level_df
    )

    render_header()
    render_overview(filtered_df)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "① Population Exposure",
        "② Global Density Map",
        "③ Sea Level Trend",
        "④ Adaptation Capacity",
        "⑤ Risk Matrix",
        "⑥ Data Table"
    ])

    with tab1:
        render_tab_1(filtered_df, top_n)

    with tab2:
        render_tab_2(filtered_df)

    with tab3:
        render_tab_3(sea_level_df, selected_scenarios)

    with tab4:
        render_tab_4(filtered_df)

    with tab5:
        render_tab_5(filtered_df)

    with tab6:
        render_tab_6(filtered_df, selected_countries)

    st.markdown("""
<div class="footer">
Data sources: World Bank, Sea Level Explorer, Our World in Data.
</div>
""", unsafe_allow_html=True)

# ============================================================
# STANDALONE RUNNER
# ============================================================

if __name__ == "__main__":
    st.set_page_config(
        page_title="Climate Change Impact Dashboard",
        layout="wide"
    )

    render_climate_dashboard()
