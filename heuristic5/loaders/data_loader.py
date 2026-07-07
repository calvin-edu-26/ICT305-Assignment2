from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"

PROVIDER_FINANCE_FILE = DATA_DIR / "CRDF-PP_compact.csv"
RECIPIENT_FINANCE_FILE = DATA_DIR / "CRDF-RP_compact.csv"
VULNERABILITY_FILE = DATA_DIR / "Climate_vulnerability_climate_finance_ODA_and_protracted_crisis.csv"
OWID_EMISSIONS_FILE = DATA_DIR / "owid-co2-data.csv"
OECD_DAC_COMPILED_FILE = DATA_DIR / "OECD_DAC_Climate_Finance_Data" / "oecd_dac_climate_finance_2009_2019_compiled.csv"
WORLD_BANK_FILE = DATA_DIR / "API_WLD_DS2_en_csv_v2_4871" / "API_WLD_DS2_en_csv_v2_4871.csv"
CLIMATE_INDICATORS_FILE = DATA_DIR / "climate_change_converted_csv" / "climate_change_excel_4_6_mb__Data.csv"
COUNTRY_TEMPERATURE_FILE = DATA_DIR / "climate_change_converted_csv" / "historical_data_excel_380_kb__Country_temperatureCRU.csv"
HISTORICAL_EMISSIONS_FILE = DATA_DIR / "historical_emissions.csv"

ADAPTATION_COL = "Adaptation-related development finance (includes overlap) - Commitment - 2024 USD thousand"
MITIGATION_COL = "Mitigation-related development finance (includes overlap) - Commitment - 2024 USD thousand"
CLIMATE_COL = "Climate-related development finance - Commitment - 2024 USD thousand"


def _finance_frame(path: Path) -> pd.DataFrame:
    optional_cols = [
        "Recipient Income Group (OECD Classification)",
        "Sector Name",
        "Financial Instrument",
    ]
    required_cols = [
        "Year",
        "Provider Name",
        "Recipient Name",
        "Recipient Region",
        ADAPTATION_COL,
        MITIGATION_COL,
        CLIMATE_COL,
    ]

    if path.suffix.lower() == ".csv":
        available_cols = list(pd.read_csv(path, nrows=0).columns)
        usecols = required_cols + [col for col in optional_cols if col in available_cols]
        df = pd.read_csv(path, usecols=usecols)
    else:
        df = pd.read_excel(path, sheet_name="All", usecols=required_cols + optional_cols)

    df = df.rename(
        columns={
            "Provider Name": "provider",
            "Recipient Name": "recipient",
            "Recipient Region": "region",
            "Recipient Income Group (OECD Classification)": "income_group",
            "Sector Name": "sector",
            "Financial Instrument": "instrument",
            ADAPTATION_COL: "adaptation_usd_thousand",
            MITIGATION_COL: "mitigation_usd_thousand",
            CLIMATE_COL: "climate_usd_thousand",
        }
    )
    for col in ["income_group", "sector", "instrument"]:
        if col not in df.columns:
            df[col] = "Unspecified"
    for col in ["adaptation_usd_thousand", "mitigation_usd_thousand", "climate_usd_thousand"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df["year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df = df.drop(columns=["Year"]).dropna(subset=["year"])
    df["year"] = df["year"].astype(int)
    for col in ["region", "income_group", "sector", "instrument"]:
        df[col] = df[col].fillna("Unspecified")
    df["adaptation_share"] = np.where(
        df["climate_usd_thousand"] > 0,
        df["adaptation_usd_thousand"] / df["climate_usd_thousand"],
        0,
    )
    return df

@st.cache_data(show_spinner=False)
def load_provider_finance_data() -> pd.DataFrame:
    return _finance_frame(PROVIDER_FINANCE_FILE)


@st.cache_data(show_spinner=False)
def load_recipient_finance_data() -> pd.DataFrame:
    if not RECIPIENT_FINANCE_FILE.exists():
        return pd.DataFrame(
            columns=[
                "provider",
                "recipient",
                "region",
                "income_group",
                "sector",
                "instrument",
                "adaptation_usd_thousand",
                "mitigation_usd_thousand",
                "climate_usd_thousand",
                "year",
                "adaptation_share",
            ]
        )
    return _finance_frame(RECIPIENT_FINANCE_FILE)


@st.cache_data(show_spinner=False)
def load_vulnerability_data() -> pd.DataFrame:
    df = pd.read_excel(VULNERABILITY_FILE, sheet_name="Dataset")
    df = df.rename(
        columns={
            "Country": "country",
            "ISO3": "iso_code",
            "Adaptation ": "adaptation_total",
            "Mitigation": "mitigation_total",
            "Total Funding": "total_funding",
            "Vulnerability": "vulnerability",
            "Region": "region",
            "ODA": "oda",
            "Funding per capita (US$)": "funding_per_capita",
        }
    )
    for col in ["adaptation_total", "mitigation_total", "total_funding", "vulnerability", "oda", "funding_per_capita"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["region"] = df["region"].fillna("Unspecified")
    return df


@st.cache_data(show_spinner=False)
def load_owid_emissions_data() -> pd.DataFrame:
    usecols = ["country", "iso_code", "year", "co2", "co2_per_capita", "population", "gdp"]
    df = pd.read_csv(OWID_EMISSIONS_FILE, usecols=usecols)
    df = df[df["iso_code"].notna() & (df["iso_code"].str.len() == 3)]
    for col in ["co2", "co2_per_capita", "year", "population", "gdp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["year"])


@st.cache_data(show_spinner=False)
def load_oecd_dac_compiled_data() -> pd.DataFrame:
    df = pd.read_csv(OECD_DAC_COMPILED_FILE)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["climate_targeted_total_usd_millions_2019"] = pd.to_numeric(
        df["climate_targeted_total_usd_millions_2019"], errors="coerce"
    )
    return df.dropna(subset=["year"])


@st.cache_data(show_spinner=False)
def load_world_bank_context_data() -> pd.DataFrame:
    df = pd.read_csv(WORLD_BANK_FILE, skiprows=4)
    keep = {
        "SP.POP.TOTL": "Population, total",
        "NY.GDP.PCAP.CD": "GDP per capita, current USD",
        "EG.USE.PCAP.KG.OE": "Energy use per capita",
        "EG.FEC.RNEW.ZS": "Renewable energy consumption",
        "DC.DAC.TOTL.CD": "Net bilateral aid flows from DAC donors",
    }
    df = df[df["Indicator Code"].isin(keep)].copy()
    year_cols = [c for c in df.columns if c.isdigit()]
    long = df.melt(
        id_vars=["Indicator Code", "Indicator Name"],
        value_vars=year_cols,
        var_name="year",
        value_name="value",
    )
    long["year"] = pd.to_numeric(long["year"], errors="coerce")
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    long["indicator"] = long["Indicator Code"].map(keep)
    return long.dropna(subset=["year", "value"])


@st.cache_data(show_spinner=False)
def load_country_temperature_data() -> pd.DataFrame:
    df = pd.read_csv(COUNTRY_TEMPERATURE_FILE)
    df = df.rename(columns={"ISO_3DIGIT": "iso_code", "Annual_temp": "annual_temp"})
    df["annual_temp"] = pd.to_numeric(df["annual_temp"], errors="coerce")
    return df.dropna(subset=["annual_temp"])


@st.cache_data(show_spinner=False)
def load_climate_indicator_data() -> pd.DataFrame:
    df = pd.read_csv(CLIMATE_INDICATORS_FILE, na_values=[".."])
    useful = [
        "AG.LND.EL5M.ZS",
        "EN.ATM.CO2E.PC",
        "EN.ATM.METH.KT.CE",
        "ER.H2O.FWTL.ZS",
        "EG.ELC.RNEW.ZS",
    ]
    df = df[df["Series code"].isin(useful)].copy()
    year_cols = [c for c in df.columns if c.isdigit()]
    long = df.melt(
        id_vars=["Country code", "Country name", "Series code", "Series name"],
        value_vars=year_cols,
        var_name="year",
        value_name="value",
    )
    long["year"] = pd.to_numeric(long["year"], errors="coerce")
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    return long.dropna(subset=["year", "value"])


@st.cache_data(show_spinner=False)
def load_historical_emissions_data() -> pd.DataFrame:
    df = pd.read_csv(HISTORICAL_EMISSIONS_FILE)
    year_cols = [c for c in df.columns if c.isdigit()]
    long = df.melt(
        id_vars=["ISO", "Country", "Data source", "Sector", "Gas", "Unit"],
        value_vars=year_cols,
        var_name="year",
        value_name="value",
    )
    long["year"] = pd.to_numeric(long["year"], errors="coerce")
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    return long.dropna(subset=["year", "value"])



