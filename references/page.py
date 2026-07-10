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
| Sea Level Rise & Displacement | Lucas | Sea Level Rise Projections | World Bank Climate Change Knowledge Portal | Historical + SSP projections to 2150 |
| Sea Level Rise & Displacement | Lucas | Coastal Population Exposure | Climate Central – Sea Level Explorer | Current estimates |
| Sea Level Rise & Displacement | Lucas | GDP per Capita & CO₂ Emissions | Our World in Data / World Bank | Latest available |
""")

st.divider()

# ── PENDING DATASETS ──────────────────────────────────────────────────────────
st.subheader("Pending Confirmation")

st.markdown("""
| Sub-heuristic | Member | Status |
|---|---|---|
| Extreme Weather & Economic Damage | Lam | To be confirmed |
| Sea Level Rise & Displacement | Lucas | To be confirmed |
| Climate Finance Gap | Nengjie | To be confirmed |
""")

st.divider()

st.caption(
    "This page will be updated as each member confirms their dataset. "
)
