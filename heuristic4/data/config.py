from pathlib import Path

# All Heuristic 4 datasets belong in heuristic4/data/.
DATA_DIR = Path(__file__).resolve().parent

FILES = {
    "co2": DATA_DIR / "annual-co2-emissions-per-country.csv",
    "gdp": DATA_DIR / "GDPperCapita.csv",
    "population": DATA_DIR / "Population.csv",
    "density": DATA_DIR / "pop-x1_timeseries_pov550,popcount,popdensity_timeseries_annual_2000-2000,2010-2100_mean_historical_gpw-v4_rev11_mean.xlsx",
    "sea_level": DATA_DIR / "sealevel_global_explorer_data_global.xlsx",
}

RISK_COLORS = {
    "Critical Risk": "#DC2626",
    "High Exposure, Higher Capacity": "#F97316",
    "Emerging Risk": "#2563EB",
    "Lower Risk": "#16A34A",
}

SCENARIO_LABELS = {
    "Historical": "Historical observations",
    "ssp126": "SSP1-2.6: Strong climate action",
    "ssp245": "SSP2-4.5: Moderate pathway",
    "ssp585": "SSP5-8.5: Very high emissions",
}

SCENARIO_COLORS = {
    "Historical observations": "#64748B",
    "SSP1-2.6: Strong climate action": "#16A34A",
    "SSP2-4.5: Moderate pathway": "#2563EB",
    "SSP5-8.5: Very high emissions": "#DC2626",
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
    "Syrian Arab Republic": "Syria",
}
