from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

from heuristic3.constants import COLORS, INCOME_ORDER


@dataclass
class RegressionResult:
    fig: object
    r2: float
    slope: float
    pred_low: float
    pred_high: float
    ratio: float


def fit(scatter_data: pd.DataFrame):
    """
    Section 4 ML model — fits a simple linear regression of disaster damage
    (% of GDP) on GDP per capita, and builds the annotated scatter +
    regression-line chart used in the "Decision Support & Predictive
    Insight" section.

    Parameters
    ----------
    scatter_data : pd.DataFrame
        Output of heuristic3.chart.wealth_vs_damage.build_scatter_data().
        Needs at least 10 rows for a meaningful fit.

    Returns
    -------
    RegressionResult or None
        None if scatter_data has 10 rows or fewer (page.py shows a warning
        in that case instead of the chart).
    """
    if len(scatter_data) <= 10:
        return None

    X = scatter_data[["gdp_per_capita"]].values
    y = scatter_data["All disasters"].values
    model = LinearRegression()
    model.fit(X, y)

    scatter_data = scatter_data.copy()
    scatter_data["predicted"] = model.predict(X)
    r2 = model.score(X, y)
    slope = model.coef_[0]

    pred_low = float(model.predict([[1500]])[0])
    pred_high = float(model.predict([[45000]])[0])
    ratio = pred_low / max(pred_high, 0.0001)

    fig = px.scatter(
        scatter_data, x="gdp_per_capita", y="All disasters",
        color="income_group", color_discrete_map=COLORS,
        hover_name="Entity",
        labels={
            "gdp_per_capita": "GDP per Capita (USD)",
            "All disasters": "Avg Economic Damage (% of GDP)",
            "income_group": "Income Group",
        },
        title=f"Linear Regression: GDP per Capita → Disaster Damage % GDP (R²={r2:.3f})",
        template="plotly_white",
        category_orders={"income_group": INCOME_ORDER},
    )
    x_line = np.linspace(scatter_data["gdp_per_capita"].min(),
                         scatter_data["gdp_per_capita"].max(), 200)
    y_line = model.predict(x_line.reshape(-1, 1))
    fig.add_trace(go.Scatter(
        x=x_line, y=y_line, mode="lines",
        name=f"Regression Line (R²={r2:.3f})",
        line=dict(color="#333333", width=2, dash="dash"),
    ))

    return RegressionResult(
        fig=fig, r2=r2, slope=slope,
        pred_low=pred_low, pred_high=pred_high, ratio=ratio,
    )
