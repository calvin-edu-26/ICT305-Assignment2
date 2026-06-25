import pandas as pd
import streamlit as st

@st.cache_data
def load() -> pd.DataFrame:
    df = pd.read_csv("heuristic1/data/owid-co2-data.csv")
    # TODO: Add data preprocessing logics 
    return df