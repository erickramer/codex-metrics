"""Tests for the Streamlit app skeleton."""

from importlib import import_module, reload
from types import ModuleType
from pathlib import Path
import sys
from datetime import date

# Ensure repository root is in sys.path when tests are executed from the tests directory.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.metrics import Metric


class DummyStreamlit(ModuleType):
    """Minimal stand-in for the Streamlit module."""

    def __init__(self) -> None:
        super().__init__("streamlit")
        self.titles: list[str] = []
        self.writes: list[str] = []
        self.charts: list[object] = []

    def title(self, text: str) -> None:
        self.titles.append(text)

    def write(self, text: str) -> None:
        self.writes.append(text)

    def plotly_chart(self, fig, use_container_width: bool = False) -> None:
        self.charts.append(fig)


def test_main_displays_title(monkeypatch) -> None:
    """Ensure the app displays the placeholder title."""
    dummy = DummyStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", dummy)
    app_main = reload(import_module("app.main"))

    def fake_fetch_active_users(*_, **__):
        return [Metric(name="active_users", date=date(2023, 1, 1), value=1.0, metadata={"repo": "repo1"})]

    monkeypatch.setattr(app_main, "fetch_active_users", fake_fetch_active_users)
    app_main.main()
    assert dummy.titles == ["Metrics Dashboard"]
    assert len(dummy.charts) == 1

