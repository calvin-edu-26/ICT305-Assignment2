import streamlit as st


def render(insight: str):
    with st.container(border=True):
        st.markdown("**Key Finding**")
        st.markdown(insight)