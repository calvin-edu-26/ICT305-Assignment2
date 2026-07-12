import streamlit as st

# ── LOGO ──────────────────────────────────────────────────────────────────────
# Displays the title as a text wordmark at the top of the sidebar, above the
# navigation links. st.logo() is the only Streamlit call that reliably
# renders above the nav widget — CSS attempts to resize its image-based
# preset sizes fought Streamlit's own inline styling and didn't hold, so
# instead of a picture logo this is a pre-rendered text image sized exactly
# as intended up front. Regenerate assets/title_logo.png (via PIL) if the
# wording or size ever needs to change.
st.logo("assets/title_logo.png", size="large")


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
# Passing a dict instead of a flat list groups pages under collapsible
# section headers in the sidebar. Each key becomes a header; Overview keeps
# its own header so it isn't visually orphaned above the grouped sections.
pg = st.navigation({
    "": [
        overview,
    ],
    "Sub-Heuristics": [
        heuristic1,
        heuristic2,
        heuristic3,
        heuristic4,
        heuristic5,
    ],
    "Appendix": [
        references,
        about,
    ],
})
 
pg.run()