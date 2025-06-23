"""Tests for the custom Plotly theme."""

from theme import codex_theme


def test_theme_contains_expected_colors() -> None:
    """Verify the theme colorway begins with the defined palette."""
    tpl = codex_theme()
    assert list(tpl.layout.colorway)[:3] == ["#2369BD", "#F25F5C", "#FFE066"]


def test_theme_font_family() -> None:
    """Ensure the theme specifies the Inter font family."""
    tpl = codex_theme()
    assert "Inter" in tpl.layout.font.family
