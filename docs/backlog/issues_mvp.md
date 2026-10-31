# Бэклог issues для MVP

Готовые тексты для создания в GitHub Issues. Каждый issue — задача для
Copilot Coding Agent. Создавать по порядку внутри milestone; issues одного
milestone независимы друг от друга, если не указано иное.

## Milestone 1: Ядро (core)

### Issue: «Core: инициализация БД, миграции, append-only триггеры»
```
Реализовать core/db/connection.py и миграцию 001_init.sql строго по
docs/specs/01_architecture.md и docs/specs/02_data_model.md.

Обязательно:
- app_data_dir() с поддержкой LABJOURNAL_DATA_DIR
- открытие БД в WAL-режиме, применение миграций по номерам
- триггеры RAISE(ABORT) на UPDATE/DELETE таблицы entries
- backup_to() через VACUUM INTO + копирование attachments
- next_seq() в транзакции BEGIN IMMEDIATE

Критерии приёмки: тесты на каждую функцию, включая запрет UPDATE/DELETE
и бэкап с последующим открытием копии.
```

### Issue: «Core: записи, хеш-цепочка, integrity-проверка»
```
Реализовать core/entries.py и core/integrity.py по docs/specs/02_data_model.md.

Обязательно:
- create_entry / create_correction (supersedes), чтение, список с пагинацией
- каноническое представление и sha256 ровно по формуле из спеки
- verify_chain() -> IntegrityReport: битый hash, разрыв prev_hash, пропуск seq
- тест: подмена body_md в БД напрямую обнаруживается verify_chain
```

### Issue: «Core: протоколы и снимки»
```
Реализовать core/protocols.py по docs/specs/03_protocols.md, включая
start_experiment_from_protocol со снимком и служебным комментарием.
Тесты: правка шаблона не меняет старые эксперименты; парсинг снимка обратно.
```

### Issue: «Core: вложения»
```
Реализовать core/attachments.py по docs/specs/04_attachments.md:
копирование с safe_filename, sha256, дедупликация в пределах записи,
verify_attachments, лимит 500 МБ, кириллица в именах. Колонку removed_at
добавить в миграцию 001 сразу. Тесты — все из критериев приёмки спеки.
```

### Issue: «Core: FTS5-поиск и теги»
```
Реализовать core/search.py по docs/specs/05_search_and_tags.md:
FTS5-таблица, синхронизация в транзакции INSERT, bm25-сортировка,
безопасный разбор ошибочного MATCH-запроса, теги с автодополнением,
фильтры по тегам и датам, entry_links. Тесты — включая перфоманс-тест
на 10 000 записей (< 100 мс).
```

## Milestone 2: Интерфейс (ui)

### Issue: «UI: главное окно, список записей, редактор»
```
Реализовать ui/main_window.py, ui/entry_list.py, ui/entry_editor.py по
docs/specs/01_architecture.md. Все строки — в ui/strings.py (рус.).
Markdown-превью тела записи. Статус-бар с результатом verify_chain.
Тесты pytest-qt (QT_QPA_PLATFORM=offscreen): создание записи через UI
попадает в БД, correction создаётся как новая запись.
```

### Issue: «UI: протоколы и вложения»
```
Реализовать ui/protocol_manager.py и ui/attachment_view.py по спекам 03 и 04:
диалог протоколов с версиями, «Новый эксперимент из протокола», drag-and-drop
вложений, превью изображений, кнопки «Открыть»/«Показать в папке».
```

### Issue: «UI: панель поиска»
```
Реализовать ui/search_panel.py по docs/specs/05_search_and_tags.md:
строка поиска с подсветкой совпадений, фильтры тегов (мультивыбор, AND)
и дат, автодополнение тегов.
```

### Issue: «UI: экспорт PDF и бэкап»
```
Реализовать ui-обвязку core/export.py по docs/specs/06_pdf_export.md:
экспорт записи и периода, диалог бэкапа, кнопка проверки вложений,
экспорт всего журнала в JSON. Тест: PDF-файл начинается с %PDF.
```

## Milestone 3: Полировка MVP

### Issue: «Первый запуск: мастер создания журнала»
```
При отсутствии БД — диалог выбора папки данных и создания журнала,
проверка записи/чтения, предложение сделать первый бэкап.
```

### Issue: «Упаковка: сборка exe через PyInstaller»
```
Добавить сборку one-file exe для Windows в отдельный workflow
(build.yml, артефакт релиза). Не включать в CI-тесты.
```
