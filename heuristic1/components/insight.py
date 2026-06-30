from streamlit import info

def render(insight: str):
    return info(f"""
    **♦ WHAT THIS SHOWS**

    {insight}
    """)