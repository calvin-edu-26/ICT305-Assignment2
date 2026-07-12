from plotly.graph_objects import Figure

def compact_style(fig: Figure):
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10)
    )

    return fig