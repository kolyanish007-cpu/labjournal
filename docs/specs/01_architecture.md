# Спецификация: Общая архитектура

Статус: утверждена. Реализация: milestone 1.

## Компоненты

```
src/labjournal/
├── __main__.py          # точка входа: python -m labjournal
├── app.py               # main(): создание QApplication, запуск главного окна
├── core/                # доменное ядро (БЕЗ Qt)
│   ├── db/
│   │   ├── connection.py    # открытие БД, PRAGMA, миграции
│   │   ├── migrations/      # 001_init.sql, 002_..., ...
│   │   └── queries.py       # все SQL-запросы приложения
│   ├── entries.py       # создание/чтение записей экспериментов
│   ├── protocols.py     # шаблоны протоколов и снимки
│   ├── attachments.py   # приём, копирование, хеширование файлов
│   ├── search.py        # FTS5-поиск, теги
│   ├── integrity.py     # проверка хеш-цепочки
│   └── export.py        # экспорт записи в PDF
└── ui/                  # PySide6 (единственное место, где живёт Qt)
    ├── main_window.py
    ├── entry_editor.py
    ├── entry_list.py
    ├── attachment_view.py
    ├── protocol_manager.py
    ├── search_panel.py
    └── strings.py       # все пользовательские строки UI (рус.)
```

## Правила взаимодействия

- `ui` вызывает только публичные функции `core` (см. сигнатуры в спеках 02–06).
- Ядро не знает о существовании Qt: тесты ядра запускаются без GUI.
- Все пути к данным приложения вычисляет `core.db.connection.app_data_dir()`:
  Windows — `%LOCALAPPDATA%/labjournal`, Linux — `~/.local/share/labjournal`,
  macOS — `~/Library/Application Support/labjournal`. Переопределяется
  переменной окружения `LABJOURNAL_DATA_DIR` (используется тестами).

## Хранилище

```
<app_data_dir>/
├── labjournal.db          # база SQLite (WAL-режим)
└── attachments/<uuid>__<safe_filename>   # копии вложений
```

Бэкап — копирование этих двух сущностей; функция
`core.db.connection.backup_to(dest_dir)` делает это атомарно
(`VACUUM INTO` для БД + `shutil.copytree` для вложений).

## Не входит в MVP

Синхронизация, многопользовательность, OCR, плагины. Схема БД проектируется
так, чтобы их добавить без миграций, ломающих данные (см. спеку 02).
