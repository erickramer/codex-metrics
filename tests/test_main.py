"""Tests for the Streamlit app skeleton."""

from importlib import import_module, reload
from types import ModuleType
from pathlib import Path
import sys

# Ensure repository root is in sys.path when tests are executed from the tests directory.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


class DummyStreamlit(ModuleType):
    """Minimal stand-in for the Streamlit module."""

    def __init__(self) -> None:
        super().__init__("streamlit")
        self.titles: list[str] = []
        self.writes: list[str] = []

    def title(self, text: str) -> None:
        self.titles.append(text)

    def write(self, text: str) -> None:
        self.writes.append(text)


def test_main_displays_title(monkeypatch) -> None:
    """Ensure the app displays the placeholder title."""
    dummy = DummyStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", dummy)
    app_main = reload(import_module("app.main"))
    app_main.main()
    assert dummy.titles == ["Metrics Dashboard"]

