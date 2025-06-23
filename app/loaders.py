"""Metric loaders for specialized GitHub data."""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Optional
import json
import requests

from .metrics import Metric


def _aggregate_active_users(items: Iterable[dict[str, Any]]) -> list[Metric]:
    """Aggregate unique contributors by repository and day."""
    users_by_repo_day: dict[tuple[str, str], set[str]] = defaultdict(set)
    for item in items:
        repo = item["repository"]["full_name"]
        user = item["author"]["login"]
        dt = (
            item.get("commit", {})
            .get("author", {})
            .get("date", item.get("created_at", ""))
        )
        day = dt.split("T", 1)[0]
        if day:
            users_by_repo_day[(repo, day)].add(user)

    metrics = [
        Metric(
            name="active_users",
            date=date.fromisoformat(day),
            value=float(len(users)),
            metadata={"repo": repo},
        )
        for (repo, day), users in sorted(users_by_repo_day.items())
    ]
    return metrics


def load_active_users(path: Path) -> list[Metric]:
    """Aggregate unique contributors per repo and day from GitHub search results."""
    with path.open() as fh:
        data = json.load(fh)

    return _aggregate_active_users(data.get("items", []))


def fetch_active_users(query: str = "codex", token: Optional[str] = None) -> list[Metric]:
    """Search GitHub commits across all repositories and aggregate contributors."""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    params: dict[str, int | str] = {"q": query, "per_page": 100}
    url = "https://api.github.com/search/commits"

    all_metrics: list[Metric] = []
    page = 1
    while True:
        resp = requests.get(url, headers=headers, params={**params, "page": page})
        if resp.status_code == 422:  # invalid query or no results
            break
        resp.raise_for_status()
        data = resp.json()
        all_metrics.extend(_aggregate_active_users(data.get("items", [])))
        if "next" not in resp.links:
            break
        page += 1

    return all_metrics
