import streamlit as st

# ═════════════════════════════════════════════════════════════════════════════
# DATA REFERENCES PAGE
# Lists all datasets used across all sub-heuristics with full citations,
# source links and download links where available.
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(layout="wide")

st.title("Data References")
st.markdown(
    "All datasets used in this dashboard are publicly available and sourced "
    "from recognised international organisations. Used strictly for academic "
    "purposes in accordance with each dataset's respective license."
)

st.divider()

# ── CARBON EMISSIONS (CALVIN) ─────────────────────────────────────────────────
st.subheader("Carbon Emissions by Nation")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
| Dataset | Source | Years Covered |
|---|---|---|
| Our World in Data CO₂ and Greenhouse Gas Emissions | Our World in Data / Global Carbon Project | 1750–2024 |
| IEA-EDGAR CO₂ Emissions by Country | European Commission Joint Research Centre & IEA | 1970–2024 |
""")
with col2:
    st.link_button("Download OWID CO₂", "https://github.com/owid/co2-data", use_container_width=True)
    st.link_button("Download IEA-EDGAR", "https://edgar.jrc.ec.europa.eu/dataset_ghg80", use_container_width=True)

st.divider()

# ── CLIMATE VULNERABILITY (RUBEN) ─────────────────────────────────────────────
st.subheader("Climate Vulnerability & Exposure")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
| Dataset | Source | Years Covered |
|---|---|---|
| ND-GAIN Country Index | Notre Dame Global Adaptation Initiative (ND-GAIN) | 1995–2024 |
| Our World in Data CO₂ and Greenhouse Gas Emissions | Our World in Data / Global Carbon Project | 1995–2024 |
""")
with col2:
    st.link_button("Download ND-GAIN", "https://gain-new.crc.nd.edu/", use_container_width=True)
    st.link_button("Download OWID CO₂", "https://github.com/owid/co2-data", use_container_width=True)

st.divider()

# ── EXTREME WEATHER (LAM) ─────────────────────────────────────────────────────
st.subheader("Extreme Weather & Economic Damage")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
| Dataset | Source | Years Covered |
|---|---|---|
| Annual Deaths from Natural Disasters | EM-DAT / CRED, UCLouvain via Our World in Data | 1900–2025 |
| Economic Damage as % of GDP from Natural Disasters | EM-DAT / CRED, UCLouvain via Our World in Data | 1960–2024 |
| Number of Natural Disaster Events | EM-DAT / CRED, UCLouvain via Our World in Data | 1900–2025 |
| CO₂ and Greenhouse Gas Emissions | Our World in Data / Global Carbon Project | 1750–2024 |
| World Bank Income Classifications | World Bank Country and Lending Groups | Latest available |
""")
with col2:
    st.link_button("Download EM-DAT via OWID", "https://ourworldindata.org/natural-disasters", use_container_width=True)
    st.link_button("Download OWID CO₂", "https://github.com/owid/co2-data", use_container_width=True)
    st.link_button("Download World Bank Income", "https://datahelpdesk.worldbank.org/knowledgebase/articles/906519", use_container_width=True)

st.divider()

# ── SEA LEVEL RISE (LUCAS) ────────────────────────────────────────────────────
st.subheader("Sea Level Rise & Displacement")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
| Dataset | Source | Years Covered |
|---|---|---|
| GDP per Capita | Our World in Data / World Bank | 1960–2024 |
| CO₂ Emissions | Our World in Data / World Bank | 1750–2024 |
| Coastal Population Exposure | Climate Change Knowledge Portal / World Bank | 2000–2007 |
| Population Density | Climate Change Knowledge Portal / World Bank | 2000–2007 |
| Sea Level Rise Projections | NASA Sea Level Projection Tool | 2020–2150 |
""")
with col2:
    st.link_button("Download GDP per Capita", "https://data.worldbank.org/indicator/NY.GDP.PCAP.CD", use_container_width=True)
    st.link_button("Download CO₂ Emissions", "https://github.com/owid/co2-data", use_container_width=True)
    st.link_button("Download Coastal Exposure", "https://climateknowledgeportal.worldbank.org/", use_container_width=True)
    st.link_button("Download Sea Level Data", "https://sealevel.nasa.gov/ipcc-ar6-sea-level-projection-tool", use_container_width=True)

st.divider()

# ── CLIMATE FINANCE (NENGJIE) ─────────────────────────────────────────────────
st.subheader("Climate Finance Gap")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
| Dataset | Source | Years Covered |
|---|---|---|
| OECD Climate-Related Development Finance - Provider Perspective | OECD | 2013–2024 |
| OECD Climate-Related Development Finance - Recipient Perspective | OECD | 2001–2024 |
| Climate Vulnerability, ODA and Climate Finance | Development Initiatives | Latest available |
| Our World in Data CO₂ | Our World in Data / Global Carbon Project | 1750–2024 |
| OECD DAC Adaptation and Mitigation Finance | OECD DAC | 2009–2019 |
| World Bank Climate Change Indicators | Climate Change Knowledge Portal / World Bank | 1990–2008 |
| World Development Indicators | World Bank | Latest available |
| Historical Greenhouse Gas Emissions | Climate Watch / World Resources Institute | 1990–2023 |
""")
with col2:
    st.link_button("Download OECD Climate Finance", "https://www.oecd.org/en/topics/climate-related-development-finance.html", use_container_width=True)
    st.link_button("Download Dev Initiatives Data", "https://devinit.org/", use_container_width=True)
    st.link_button("Download OWID CO₂", "https://github.com/owid/co2-data", use_container_width=True)
    st.link_button("Download World Bank WDI", "https://databank.worldbank.org/source/world-development-indicators", use_container_width=True)
    st.link_button("Download Historical GHG", "https://www.climatewatchdata.org/ghg-emissions", use_container_width=True)

st.divider()

st.caption(
    "All data has been used strictly for academic purposes in accordance "
    "with each dataset's respective license. "
    "Download links direct to the original data source pages."
)
