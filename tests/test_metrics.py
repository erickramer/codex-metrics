"""Tests for metrics data models and parsing utilities."""

from datetime import date
from pathlib import Path
import json
import csv

from typing import Any
from app.metrics import Metric, parse_json, parse_csv
from app.loaders import load_active_users, fetch_active_users
import requests


def test_parse_json(tmp_path: Path) -> None:
    """Verify JSON parsing into Metric objects."""
    data = [
        {"name": "pull_request_count", "date": "2023-01-01", "value": 10, "repo": "example"}
    ]
    file = tmp_path / "metrics.json"
    file.write_text(json.dumps(data))
    metrics = parse_json(file)
    assert metrics == [Metric(name="pull_request_count", date=date(2023, 1, 1), value=10.0, metadata={"repo": "example"})]


def test_parse_csv(tmp_path: Path) -> None:
    """Verify CSV parsing into Metric objects."""
    rows = [
        ["name", "date", "value", "repo"],
        ["pull_request_count", "2023-01-01", "5", "example"],
    ]
    file = tmp_path / "metrics.csv"
    with file.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerows(rows)
    metrics = parse_csv(file)
    assert metrics == [Metric(name="pull_request_count", date=date(2023, 1, 1), value=5.0, metadata={"repo": "example"})]


def test_load_active_users(tmp_path: Path) -> None:
    """Aggregate unique authors per repo and date from search results."""
    data = {
        "items": [
            {
                "repository": {"full_name": "repo1"},
                "author": {"login": "alice"},
                "commit": {"author": {"date": "2023-01-01T12:00:00Z"}},
            },
            {
                "repository": {"full_name": "repo1"},
                "author": {"login": "bob"},
                "commit": {"author": {"date": "2023-01-01T13:00:00Z"}},
            },
            {
                "repository": {"full_name": "repo1"},
                "author": {"login": "bob"},
                "commit": {"author": {"date": "2023-01-02T10:00:00Z"}},
            },
            {
                "repository": {"full_name": "repo2"},
                "author": {"login": "alice"},
                "commit": {"author": {"date": "2023-01-01T14:00:00Z"}},
            },
        ]
    }
    file = tmp_path / "search.json"
    file.write_text(json.dumps(data))
    metrics = load_active_users(file)
    metrics = sorted(metrics, key=lambda m: (m.metadata["repo"], m.date))
    assert metrics == [
        Metric(name="active_users", date=date(2023, 1, 1), value=2.0, metadata={"repo": "repo1"}),
        Metric(name="active_users", date=date(2023, 1, 2), value=1.0, metadata={"repo": "repo1"}),
        Metric(name="active_users", date=date(2023, 1, 1), value=1.0, metadata={"repo": "repo2"}),
    ]


def test_fetch_active_users(monkeypatch) -> None:
    """Fetch search results via GitHub API and aggregate metrics."""

    pages = [
        {
            "items": [
                {
                    "repository": {"full_name": "repo1"},
                    "author": {"login": "alice"},
                    "commit": {"author": {"date": "2023-01-01T12:00:00Z"}},
                },
            ]
        },
        {"items": []},
    ]

    def fake_get(url: str, headers: dict[str, str] | None = None, params: dict[str, Any] | None = None):
        page = int(params.get("page", 1)) - 1
        data = pages[page]

        class Resp:
            status_code = 200
            def __init__(self, data):
                self._data = data
                self.links = {} if page == len(pages) - 1 else {"next": {"url": "x"}}
            def json(self) -> Any:
                return self._data
            def raise_for_status(self) -> None:
                pass

        return Resp(data)

    monkeypatch.setattr(requests, "get", fake_get)

    metrics = fetch_active_users(query="codex")
    assert metrics == [
        Metric(name="active_users", date=date(2023, 1, 1), value=1.0, metadata={"repo": "repo1"})
    ]

