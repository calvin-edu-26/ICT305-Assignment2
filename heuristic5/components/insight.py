import streamlit as st


def render(insights: list[str]):
    content = "\n\n".join(f"- {item}" for item in insights)
    return st.info(f"**WHAT THIS SHOWS**\n\n{content}")
