import streamlit as st



# ── PAGE DEFINITIONS ──────────────────────────────────────────────────────────
# Each page maps to a page.py file in its respective folder.
# Title appears in Streamlit's native sidebar navigation.

overview    = st.Page("overview/page.py",    title="Overview",              url_path="overview",    default=True)
heuristic1  = st.Page("heuristic1/page.py",  title="Carbon Emissions",      url_path="heuristic1")
heuristic2  = st.Page("heuristic2/page.py",  title="Climate Vulnerability", url_path="heuristic2")
heuristic3  = st.Page("heuristic3/page.py",  title="Extreme Weather",       url_path="heuristic3")
heuristic4  = st.Page("heuristic4/page.py",  title="Sea Level Rise",        url_path="heuristic4")
heuristic5  = st.Page("heuristic5/page.py",  title="Climate Finance",       url_path="heuristic5")
references  = st.Page("references/page.py",  title="Data References",       url_path="references")
about       = st.Page("about/page.py",       title="About the Team",        url_path="about")

# ── NAVIGATION ────────────────────────────────────────────────────────────────
# st.navigation() renders Streamlit's native sidebar with all pages listed.
# Overview is the default landing page (first in the list).

pg = st.navigation([
    overview,
    heuristic1,
    heuristic2,
    heuristic3,
    heuristic4,
    heuristic5,
    references,
    about,
])

pg.run()