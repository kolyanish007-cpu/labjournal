"""Смоук-тесты ядра (без Qt)."""

import labjournal


def test_version() -> None:
    assert labjournal.__version__ == "0.1.0"
