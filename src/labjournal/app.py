"""Запуск приложения. Реализация главного окна — milestone 2 (см. docs/specs)."""

from labjournal import __version__


def main() -> None:
    """Запускает GUI приложения.

    Пока UI не реализован (milestone 2), печатает версию и выходит.
    Кодинг-агенты: заменить на создание QApplication и главного окна
    согласно docs/specs/01_architecture.md.
    """
    print(f"labjournal {__version__} — UI ещё не реализован (milestone 2)")


if __name__ == "__main__":
    main()
