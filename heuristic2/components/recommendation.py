import streamlit as st
from dataclasses import dataclass


@dataclass
class Recommendation:
    audience: str
    recommendations: list[str]


def render(recommendations: list[Recommendation]):
    """
    Renders a decision support callout using native Streamlit components.

    Displays a bordered container with audience-specific recommended actions.
    Each audience group is labelled clearly with its recommendations listed below.

    Parameters
    ----------
    recommendations : list[Recommendation]
        List of Recommendation dataclass instances. Written in page.py, not here.
    """
    with st.container(border=True):
        st.markdown("**Recommended Actions**")
        for rec in recommendations:
            st.markdown(f"**{rec.audience}**")
            for action in rec.recommendations:
                st.markdown(f"- {action}")