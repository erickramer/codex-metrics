"""Metrics data models and parsing utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
import csv
import json


@dataclass
class Metric:
    """Representation of a single metric data point."""

    name: str
    date: date
    value: float
    metadata: dict[str, str] = field(default_factory=dict)


def _parse_common(record: dict[str, str]) -> Metric:
    """Parse common fields from a record dictionary."""
    rec = record.copy()
    name = rec.pop("name")
    dt = date.fromisoformat(rec.pop("date"))
    value = float(rec.pop("value"))
    return Metric(name=name, date=dt, value=value, metadata=rec)


def parse_json(path: Path) -> list[Metric]:
    """Load metrics from a JSON file.

    The file must contain a list of objects with at least ``name``, ``date`` and
    ``value`` keys. Remaining keys are stored in :attr:`Metric.metadata`.
    """
    with path.open() as fh:
        data = json.load(fh)
    return [_parse_common(rec) for rec in data]


def parse_csv(path: Path) -> list[Metric]:
    """Load metrics from a CSV file.

    The CSV must have headers including ``name``, ``date`` and ``value``. Any
    additional columns are preserved in :attr:`Metric.metadata`.
    """
    metrics: list[Metric] = []
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            metrics.append(_parse_common(row))
    return metrics
