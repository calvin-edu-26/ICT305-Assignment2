import pandas as pd
import streamlit as st

# ── UN SUB-REGION MAPPING ─────────────────────────────────────────────────────
# Maps ISO3 country codes to UN M49 sub-regions.
# Source: United Nations Statistics Division (M49 standard).
UN_SUBREGION_MAP = {
    # Northern Africa
    "DZA": "Northern Africa", "EGY": "Northern Africa", "LBY": "Northern Africa",
    "MAR": "Northern Africa", "SDN": "Northern Africa", "TUN": "Northern Africa",
    "ESH": "Northern Africa",

    # Sub-Saharan Africa
    "AGO": "Sub-Saharan Africa", "BEN": "Sub-Saharan Africa", "BWA": "Sub-Saharan Africa",
    "BFA": "Sub-Saharan Africa", "BDI": "Sub-Saharan Africa", "CPV": "Sub-Saharan Africa",
    "CMR": "Sub-Saharan Africa", "CAF": "Sub-Saharan Africa", "TCD": "Sub-Saharan Africa",
    "COM": "Sub-Saharan Africa", "COD": "Sub-Saharan Africa", "COG": "Sub-Saharan Africa",
    "CIV": "Sub-Saharan Africa", "DJI": "Sub-Saharan Africa", "GNQ": "Sub-Saharan Africa",
    "ERI": "Sub-Saharan Africa", "SWZ": "Sub-Saharan Africa", "ETH": "Sub-Saharan Africa",
    "GAB": "Sub-Saharan Africa", "GMB": "Sub-Saharan Africa", "GHA": "Sub-Saharan Africa",
    "GIN": "Sub-Saharan Africa", "GNB": "Sub-Saharan Africa", "KEN": "Sub-Saharan Africa",
    "LSO": "Sub-Saharan Africa", "LBR": "Sub-Saharan Africa", "MDG": "Sub-Saharan Africa",
    "MWI": "Sub-Saharan Africa", "MLI": "Sub-Saharan Africa", "MRT": "Sub-Saharan Africa",
    "MUS": "Sub-Saharan Africa", "MOZ": "Sub-Saharan Africa", "NAM": "Sub-Saharan Africa",
    "NER": "Sub-Saharan Africa", "NGA": "Sub-Saharan Africa", "RWA": "Sub-Saharan Africa",
    "STP": "Sub-Saharan Africa", "SEN": "Sub-Saharan Africa", "SLE": "Sub-Saharan Africa",
    "SOM": "Sub-Saharan Africa", "ZAF": "Sub-Saharan Africa", "SSD": "Sub-Saharan Africa",
    "TZA": "Sub-Saharan Africa", "TGO": "Sub-Saharan Africa", "UGA": "Sub-Saharan Africa",
    "ZMB": "Sub-Saharan Africa", "ZWE": "Sub-Saharan Africa", "SYC": "Sub-Saharan Africa",
    "MDV": "Sub-Saharan Africa",

    # Northern America
    "CAN": "Northern America", "USA": "Northern America", "BMU": "Northern America",
    "GRL": "Northern America", "SPM": "Northern America",

    # Latin America & the Caribbean
    "ARG": "Latin America & Caribbean", "BOL": "Latin America & Caribbean",
    "BRA": "Latin America & Caribbean", "CHL": "Latin America & Caribbean",
    "COL": "Latin America & Caribbean", "ECU": "Latin America & Caribbean",
    "GUY": "Latin America & Caribbean", "PRY": "Latin America & Caribbean",
    "PER": "Latin America & Caribbean", "SUR": "Latin America & Caribbean",
    "URY": "Latin America & Caribbean", "VEN": "Latin America & Caribbean",
    "BLZ": "Latin America & Caribbean", "CRI": "Latin America & Caribbean",
    "SLV": "Latin America & Caribbean", "GTM": "Latin America & Caribbean",
    "HND": "Latin America & Caribbean", "MEX": "Latin America & Caribbean",
    "NIC": "Latin America & Caribbean", "PAN": "Latin America & Caribbean",
    "ATG": "Latin America & Caribbean", "BHS": "Latin America & Caribbean",
    "BRB": "Latin America & Caribbean", "CUB": "Latin America & Caribbean",
    "DOM": "Latin America & Caribbean", "GRD": "Latin America & Caribbean",
    "HTI": "Latin America & Caribbean", "JAM": "Latin America & Caribbean",
    "KNA": "Latin America & Caribbean", "LCA": "Latin America & Caribbean",
    "VCT": "Latin America & Caribbean", "TTO": "Latin America & Caribbean",
    "DMA": "Latin America & Caribbean",

    # Central Asia
    "KAZ": "Central Asia", "KGZ": "Central Asia", "TJK": "Central Asia",
    "TKM": "Central Asia", "UZB": "Central Asia",

    # Eastern Asia
    "CHN": "Eastern Asia", "JPN": "Eastern Asia", "MNG": "Eastern Asia",
    "PRK": "Eastern Asia", "KOR": "Eastern Asia", "TWN": "Eastern Asia",
    "HKG": "Eastern Asia", "MAC": "Eastern Asia",

    # South-eastern Asia
    "BRN": "South-eastern Asia", "KHM": "South-eastern Asia", "IDN": "South-eastern Asia",
    "LAO": "South-eastern Asia", "MYS": "South-eastern Asia", "MMR": "South-eastern Asia",
    "PHL": "South-eastern Asia", "SGP": "South-eastern Asia", "THA": "South-eastern Asia",
    "TLS": "South-eastern Asia", "VNM": "South-eastern Asia",

    # Southern Asia
    "AFG": "Southern Asia", "BGD": "Southern Asia", "BTN": "Southern Asia",
    "IND": "Southern Asia", "IRN": "Southern Asia", "NPL": "Southern Asia",
    "PAK": "Southern Asia", "LKA": "Southern Asia",

    # Western Asia
    "ARM": "Western Asia", "AZE": "Western Asia", "BHR": "Western Asia",
    "CYP": "Western Asia", "GEO": "Western Asia", "IRQ": "Western Asia",
    "ISR": "Western Asia", "JOR": "Western Asia", "KWT": "Western Asia",
    "LBN": "Western Asia", "OMN": "Western Asia", "PSE": "Western Asia",
    "QAT": "Western Asia", "SAU": "Western Asia", "SYR": "Western Asia",
    "TUR": "Western Asia", "ARE": "Western Asia", "YEM": "Western Asia",

    # Eastern Europe
    "BLR": "Eastern Europe", "BGR": "Eastern Europe", "CZE": "Eastern Europe",
    "HUN": "Eastern Europe", "POL": "Eastern Europe", "MDA": "Eastern Europe",
    "ROU": "Eastern Europe", "RUS": "Eastern Europe", "SVK": "Eastern Europe",
    "UKR": "Eastern Europe",

    # Northern Europe
    "DNK": "Northern Europe", "EST": "Northern Europe", "FIN": "Northern Europe",
    "ISL": "Northern Europe", "IRL": "Northern Europe", "LVA": "Northern Europe",
    "LTU": "Northern Europe", "NOR": "Northern Europe", "SWE": "Northern Europe",
    "GBR": "Northern Europe",

    # Southern Europe
    "ALB": "Southern Europe", "AND": "Southern Europe", "BIH": "Southern Europe",
    "HRV": "Southern Europe", "GRC": "Southern Europe", "ITA": "Southern Europe",
    "MLT": "Southern Europe", "MNE": "Southern Europe", "MKD": "Southern Europe",
    "PRT": "Southern Europe", "SMR": "Southern Europe", "SRB": "Southern Europe",
    "SVN": "Southern Europe", "ESP": "Southern Europe",

    # Western Europe
    "AUT": "Western Europe", "BEL": "Western Europe", "FRA": "Western Europe",
    "DEU": "Western Europe", "LIE": "Western Europe", "LUX": "Western Europe",
    "MCO": "Western Europe", "NLD": "Western Europe", "CHE": "Western Europe",

    # Oceania
    "AUS": "Oceania", "FJI": "Oceania", "KIR": "Oceania", "MHL": "Oceania",
    "FSM": "Oceania", "NRU": "Oceania", "NZL": "Oceania", "PLW": "Oceania",
    "PNG": "Oceania", "WSM": "Oceania", "SLB": "Oceania", "TON": "Oceania",
    "TUV": "Oceania", "VUT": "Oceania",
}

# ── ND-GAIN FILES ─────────────────────────────────────────────────────────────
# All 6 ND-GAIN indicator CSV files expected in heuristic2/data/
NDGAIN_FILES = [
    "vulnerability",
    "exposure",
    "sensitivity",
    "capacity",
    "readiness",
    "gain",
]

@st.cache_data
def load() -> pd.DataFrame:
    """
    Loads, merges, and returns the full ND-GAIN + OWID dataset.

    Steps:
        1. Load all 6 ND-GAIN CSVs from heuristic2/data/, melt to long format
        2. Merge all 6 into a single DataFrame on ISO3 + year
        3. Load OWID from heuristic1/data/ (shared dataset, no duplication)
        4. Filter OWID to 1995-2018 and relevant columns
        5. Merge ND-GAIN with OWID on ISO3 + year
        6. Drop countries with missing CO₂ data (Monaco, San Marino)
        7. Add UN sub-region labels

    Returns
    -------
    pd.DataFrame with columns:
        ISO3, Name, year, vulnerability, exposure, sensitivity,
        capacity, readiness, gain, co2_per_capita, co2,
        share_global_co2, population, gdp, subregion
    """

    # ── STEP 1 & 2: LOAD AND MERGE ND-GAIN FILES ─────────────────────────────
    merged = None
    for name in NDGAIN_FILES:
        df = pd.read_csv(f"heuristic2/data/{name}.csv")

        df_long = df.melt(
            id_vars=["ISO3", "Name"],
            var_name="year",
            value_name=name
        )
        df_long["year"] = df_long["year"].astype(int)

        if merged is None:
            merged = df_long
        else:
            merged = merged.merge(df_long, on=["ISO3", "Name", "year"])

    # ── STEP 3 & 4: LOAD AND FILTER OWID ─────────────────────────────────────
    # Referenced from heuristic1/data/ to avoid duplication.
    owid = pd.read_csv(
        "heuristic1/data/owid-co2-data.csv",
        usecols=[
            "iso_code", "country", "year",
            "co2_per_capita", "co2",
            "share_global_co2", "population", "gdp"
        ]
    )

    owid = owid[
        (owid["year"] >= 1995) &
        (owid["year"] <= 2024)
    ].copy()

    owid = owid.rename(columns={"iso_code": "ISO3"})

    # ── STEP 5: MERGE ND-GAIN WITH OWID ──────────────────────────────────────
    df = merged.merge(owid, on=["ISO3", "year"], how="left")

    # ── STEP 6: DROP COUNTRIES WITH MISSING CO₂ DATA ─────────────────────────
    # Monaco and San Marino have no OWID emissions data.
    df = df.dropna(subset=["co2_per_capita"])

    # ── STEP 7: ADD UN SUB-REGION LABELS ─────────────────────────────────────
    df["subregion"] = df["ISO3"].map(UN_SUBREGION_MAP)
    df["subregion"] = df["subregion"].fillna("Other")

    df = df.sort_values(["ISO3", "year"]).reset_index(drop=True)

    return df