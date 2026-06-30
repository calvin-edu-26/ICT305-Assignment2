from streamlit import success
from dataclasses import dataclass

@dataclass
class Recommendation:
    audience: str
    recommendations: list[str]

def render(recommendations: list[Recommendation]):
    sections = [
        f"**{recommendation.audience}**\n" + "\n".join(f"- {rec}" for rec in recommendation.recommendations)
        for recommendation in recommendations
    ]

    print(f"Recommendation block: {sections}")

    success("**♦ WHAT YOU CAN DO**\n\n" + "\n\n".join(sections))