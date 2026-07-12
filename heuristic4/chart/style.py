def clean_fig(fig, height=650):
    """
    Applies a consistent Plotly style that automatically
    adapts to Streamlit Light and Dark mode.
    """

    fig.update_layout(

        # Use Plotly's default template instead of white
        template="plotly",

        height=height,

        # Transparent backgrounds
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=60
        ),

        font=dict(size=14),

        title=dict(
            font=dict(size=20)
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0
        )
    )

    fig.update_xaxes(
        showgrid=True,
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        zeroline=False
    )

    return fig
