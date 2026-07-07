from streamlit import info

def render(insights: list[str]):
    return info(f"**♦ WHAT THIS SHOWS**\n\n{"\n\n".join(f"- {insight}" for insight in insights)}")