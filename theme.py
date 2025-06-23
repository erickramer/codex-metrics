"""Plotly theme configuration for the Codex Metrics dashboard."""

from __future__ import annotations

import plotly.graph_objects as go


def codex_theme() -> go.layout.Template:
    """Return the Plotly template for the dashboard.

    The palette blends Bostock's vibrant hues with Tufte's minimalist
    backgrounds. The modern ``Inter`` font offers readability and a
    clean aesthetic.
    """
    colorway = [
        "#2369BD",  # deep blue inspired by classic D3 examples
        "#F25F5C",  # coral accent for highlights
        "#FFE066",  # soft yellow for contrast
        "#70C1B3",  # muted teal for variety
        "#247BA0",  # darker blue for balance
    ]

    layout = go.Layout(
        colorway=colorway,
        font=dict(
            family="Inter, Helvetica, sans-serif",
            size=14,
            color="#333333",
        ),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f9f9f9",
        title=dict(x=0.02, xanchor="left"),
    )
    return go.layout.Template(layout=layout)
