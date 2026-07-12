import streamlit as st

def load_css():
    st.markdown("""
<style>
/* =========================================================
   GENERAL PAGE SPACING
   ========================================================= */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* =========================================================
   HERO HEADER
   Keeps its own dark-blue design in both themes.
   ========================================================= */

.hero {
    padding: 30px;
    border-radius: 22px;
    background: linear-gradient(90deg, #082032, #0F4C75);
    color: #ffffff;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 8px;
    color: #ffffff;
}

.hero p {
    font-size: 18px;
    color: #dbeafe;
}


/* =========================================================
   STORY, INSIGHT AND RECOMMENDATION CARDS
   Uses Streamlit theme variables so light and dark modes work.
   ========================================================= */

.section-card,
.story-box {
    padding: 22px;
    border-radius: 18px;
    border: 1px solid rgba(128, 128, 128, 0.30);
    margin: 18px 0;

    background-color: var(--secondary-background-color);
    color: var(--text-color);
}


/* Headings inside cards */
.section-card h1,
.section-card h2,
.section-card h3,
.section-card h4,
.story-box h1,
.story-box h2,
.story-box h3,
.story-box h4 {
    color: var(--text-color) !important;
    margin-top: 0;
}


/* Paragraphs and list items inside cards */
.section-card p,
.section-card li,
.story-box p,
.story-box li {
    color: var(--text-color) !important;
    font-size: 15px;
    line-height: 1.7;
}


/* Bold text must also follow the active theme */
.section-card b,
.section-card strong,
.story-box b,
.story-box strong {
    color: var(--text-color) !important;
}


/* Improve list spacing */
.story-box ul,
.section-card ul {
    margin-top: 10px;
    margin-bottom: 12px;
    padding-left: 24px;
}

.story-box li,
.section-card li {
    margin-bottom: 7px;
}


/* =========================================================
   TABS
   ========================================================= */

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background-color: var(--secondary-background-color);
    padding: 12px;
    border-radius: 18px;
    margin-bottom: 20px;
}

.stTabs [data-baseweb="tab"] {
    height: 55px;
    padding: 12px 20px;
    border-radius: 14px;

    background-color: var(--background-color);
    border: 1px solid rgba(128, 128, 128, 0.30);
    font-weight: 700;
    color: var(--text-color);
}

.stTabs [aria-selected="true"] {
    background-color: #0F4C75 !important;
    color: #ffffff !important;
    border: 1px solid #0F4C75 !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    padding: 20px;
    text-align: center;
    color: var(--text-color);
    opacity: 0.75;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)
