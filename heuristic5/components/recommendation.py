from dataclasses import dataclass

import streamlit as st


@dataclass
class Recommendation:
    audience: str
    recommendations: list[str]


def render(recommendations: list[Recommendation]):
    sections = [
        f"**{item.audience}**\n" + "\n".join(f"- {rec}" for rec in item.recommendations)
        for item in recommendations
    ]
    return st.success("**WHAT YOU CAN DO**\n\n" + "\n\n".join(sections))
