import streamlit as st

# ═════════════════════════════════════════════════════════════════════════════
# DATA REFERENCES PAGE
# Lists all datasets used across all sub-heuristics with full citations.
# Updated as each member confirms their dataset.
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(layout="wide")

st.title("Data References")
st.markdown(
    "All datasets used in this dashboard are publicly available and sourced "
    "from recognised international organisations. Used strictly for academic "
    "purposes in accordance with each dataset's respective license."
)

st.divider()

# ── CONFIRMED DATASETS ────────────────────────────────────────────────────────
st.subheader("Confirmed Datasets")

st.markdown("""
| Sub-heuristic | Member | Dataset | Source | Years Covered |
|---|---|---|---|---|
| Carbon Emissions | Calvin | Our World in Data CO₂ | Our World in Data / Global Carbon Project | 1750–2024 |
| Carbon Emissions | Calvin | IEA-EDGAR CO₂ | European Commission Joint Research Centre & IEA | 1970–2024 |
| Climate Vulnerability | Ruben | ND-GAIN Country Index | Notre Dame Global Adaptation Initiative (ND-GAIN) | 1995–2018 |
| Climate Vulnerability | Ruben | Our World in Data CO₂ | Our World in Data / Global Carbon Project | 1995–2018 |
| Sea Level Rise & Displacement | Lucas | GDP per Capita | Our World in Data / World Bank | 1960-2024 |
| Sea Level Rise & Displacement | Lucas | CO₂ Emissions | Our World in Data / World Bank | 1750-2024 |
| Sea Level Rise & Displacement | Lucas | Coastal Population Exposure | Climate Change Knowledge Portal / World Bank | 2000-2007 |
| Sea Level Rise & Displacement | Lucas | Population Density | Climate Change Knowledge Portal / World Bank | 2000-2007 |
| Sea Level Rise & Displacement | Lucas | Sea Level Rise Projections | NASA Sea Level Projection Tool | 2020-2150 |
| Climate Finance Gap | Nengjie | OECD Climate-Related Development Finance - Provider Perspective | OECD | 2013-2024 |
| Climate Finance Gap | Nengjie | OECD Climate-Related Development Finance - Recipient Perspective | OECD | 2001-2024 |
| Climate Finance Gap | Nengjie | Climate Vulnerability, ODA and Climate Finance | Development Initiatives | Latest available |
| Climate Finance Gap | Nengjie | Our World in Data CO₂ | Our World in Data / Global Carbon Project | 1750-2024 |
| Climate Finance Gap | Nengjie | OECD DAC Adaptation and Mitigation Finance | OECD DAC | 2009-2019 |
| Climate Finance Gap | Nengjie | World Bank Climate Change Indicators | Climate Change Knowledge Portal / World Bank | 1990-2008 |
| Climate Finance Gap | Nengjie | World Development Indicators | World Bank | Available World Bank indicator years |
| Climate Finance Gap | Nengjie | Historical Greenhouse Gas Emissions | Historical greenhouse gas emissions dataset | 1990-2023 |
| Extreme Weather & Economic Damage | Lam | Annual Deaths from Natural Disasters | EM-DAT / CRED, UCLouvain — via Our World in Data | 1900–2025 |
| Extreme Weather & Economic Damage | Lam | Economic Damage as % of GDP from Natural Disasters | EM-DAT / CRED, UCLouvain — via Our World in Data | 1960–2024 |
| Extreme Weather & Economic Damage | Lam | Number of Natural Disaster Events | EM-DAT / CRED, UCLouvain — via Our World in Data | 1900–2025 |
| Extreme Weather & Economic Damage | Lam | CO₂ and Greenhouse Gas Emissions | Our World in Data / Global Carbon Project | 1750–2024 |
| Extreme Weather & Economic Damage | Lam | World Bank Income Classifications | World Bank Country and Lending Groups | Latest available |
""")

st.divider()

st.divider()

st.caption(
    "This page will be updated as each member confirms their dataset. "
)
