import math

import pandas as pd


def usd_millions(series: pd.Series) -> float:
    return float(series.sum() / 1000)


def compact_money(value_million: float) -> str:
    if not math.isfinite(value_million):
        return "USD 0m"
    if abs(value_million) >= 1000:
        return f"USD {value_million / 1000:,.2f}b"
    return f"USD {value_million:,.1f}m"


def pct(value: float) -> str:
    if not math.isfinite(value):
        return "0.0%"
    return f"{value * 100:,.1f}%"
