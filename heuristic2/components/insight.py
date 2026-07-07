import streamlit as st


def render(insight: str):
    """
    Renders a key insight callout using native Streamlit components.

    Displays a bordered container with a clear label and insight text.
    Designed for UN/IPCC policymaker audience — minimal, professional,
    content-focused rather than container-focused.

    Parameters
    ----------
    insight : str
        The insight text to display. Written in page.py, not here.
    """
    with st.container(border=True):
        st.markdown("**♦ WHAT THIS SHOWS**")
        st.markdown(insight)