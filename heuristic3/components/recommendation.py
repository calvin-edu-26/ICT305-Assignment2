import streamlit as st
from dataclasses import dataclass


@dataclass
class DecisionCard:
    decision: str
    action: str


def render(cards: list[DecisionCard]):
    """
    Renders a 2x2 grid of decision cards, each mapping a strategic decision
    to a specific recommended action.

    Each card contains:
        - Strategic decision label (bold header)
        - Recommended action (body text)

    Parameters
    ----------
    cards : list[DecisionCard]
        Exactly 4 DecisionCard instances. Written in page.py, not here.
        Order: top-left, top-right, bottom-left, bottom-right.
    """
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    cols = [row1_col1, row1_col2, row2_col1, row2_col2]

    for col, card in zip(cols, cards):
        with col:
            with st.container(border=True):
                st.markdown(f"**{card.decision}**")
                st.markdown(card.action)
