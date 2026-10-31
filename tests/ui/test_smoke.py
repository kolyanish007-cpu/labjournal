"""Смоук-тесты UI (требуют PySide6, запускаются с QT_QPA_PLATFORM=offscreen)."""

import pytest

pytest.importorskip("PySide6", reason="PySide6 не установлен")


def test_qt_importable() -> None:
    from PySide6 import QtWidgets  # noqa: F401 — проверка наличия Qt

    assert QtWidgets.QApplication is not None
