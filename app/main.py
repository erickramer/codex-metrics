"""Streamlit app entry point."""

import streamlit as st
import os
from collections import defaultdict
import plotly.graph_objects as go

from .loaders import fetch_active_users
from .metrics import Metric
from theme import codex_theme


def _build_active_users_chart(metrics: list[Metric]) -> go.Figure:
    """Create an active users line chart grouped by repository."""
    by_repo: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for m in metrics:
        repo = m.metadata.get("repo", "")
        by_repo[repo].append((m.date.isoformat(), m.value))

    fig = go.Figure()
    for repo, entries in by_repo.items():
        entries.sort(key=lambda e: e[0])
        fig.add_trace(
            go.Scatter(x=[d for d, _ in entries], y=[v for _, v in entries], mode="lines+markers", name=repo)
        )

    fig.update_layout(template=codex_theme(), title="Active Users by Repository")
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="Users")
    return fig


def main() -> None:
    """Run the metrics dashboard app."""
    st.title("Metrics Dashboard")

    token = os.getenv("GITHUB_TOKEN")
    metrics = fetch_active_users(query="codex", token=token)
    if metrics:
        fig = _build_active_users_chart(metrics)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available")


if __name__ == "__main__":
    main()

