import urllib.request
import json
import streamlit as st

@st.cache_data
def load():
    with urllib.request.urlopen("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson") as res:
        return json.loads(res.read())