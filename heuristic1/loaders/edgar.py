import pandas as pd
from streamlit import cache_data

NON_COUNTRY_CODES = {"AIR", "SEA"}

IPCC_TO_EDGAR_SECTOR = {
    "1.A.1.a": "Power industry",
    "1.A.1.bc": "Oil refineries & transformation",
    "1.A.2": "Manufacturing combustion",
    "1.A.3.a": "Civil aviation",
    "1.A.3.b_noRES": "Road transportation",
    "1.A.3.c": "Railways",
    "1.A.3.d": "Shipping",
    "1.A.3.e": "Other transport",
    "1.A.4": "Energy for buildings",
    "1.B.1": "Fuel exploitation (coal)",
    "1.B.2": "Oil and natural gas",
    "2.A.1": "Cement production",
    "2.A.2": "Lime production",
    "2.A.3": "Glass production",
    "2.B": "Chemical processes",
    "2.C": "Metal industry",
    "2.D": "Solvents use",
    "3.C.2": "Liming",
    "3.C.3": "Urea application",
    "4.C": "Waste incineration",
    "5.B": "Fossil fuel fires",
}

@cache_data
def load() -> pd.DataFrame:
    df = pd.read_excel(
        "heuristic1/data/IEA_EDGAR_CO2_1970_2024.xlsx", 
        sheet_name="IPCC 2006",
        skiprows=9
    )

    df["sector"] = df["ipcc_code_2006_for_standard_report"].map(IPCC_TO_EDGAR_SECTOR)
    df = df[-df["Country_code_A3"].isin(NON_COUNTRY_CODES)]

    df = df.melt(
        id_vars=["Country_code_A3", "Name", "sector"],
        value_vars=[c for c in df.columns if c.startswith("Y_")],
        var_name="year",
        value_name="co2",
    )

    df["year"] = df["year"].str.removeprefix("Y_").astype(int)
    print("IEA_EDGAR_CO2_1970_2024.xlsx: ", df) # DEBUG
    return df