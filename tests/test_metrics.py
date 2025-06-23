"""Tests for metrics data models and parsing utilities."""

from datetime import date
from pathlib import Path
import json
import csv

from app.metrics import Metric, parse_json, parse_csv


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

