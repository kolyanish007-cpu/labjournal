# Спецификация: Модель данных и целостность

Статус: утверждена. Реализация: milestone 1.

## Таблицы (миграция 001_init.sql)

```sql
-- Записи журнала. Append-only: UPDATE и DELETE запрещены приложением.
CREATE TABLE entries (
    id          TEXT PRIMARY KEY,          -- UUIDv4
    seq         INTEGER NOT NULL UNIQUE,   -- монотонный счётчик
    created_at  TEXT NOT NULL,             -- ISO 8601 UTC с таймзоной
    entry_type  TEXT NOT NULL CHECK (entry_type IN ('experiment','note','correction')),
    title       TEXT NOT NULL,
    body_md     TEXT NOT NULL,             -- markdown
    supersedes  TEXT REFERENCES entries(id),  -- только для correction
    prev_hash   TEXT NOT NULL,             -- SHA-256 предыдущей записи ('' для первой)
    hash        TEXT NOT NULL UNIQUE       -- SHA-256 этой записи
);

CREATE TABLE tags (
    id   TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE
);

CREATE TABLE entry_tags (
    entry_id TEXT NOT NULL REFERENCES entries(id),
    tag_id   TEXT NOT NULL REFERENCES tags(id),
    PRIMARY KEY (entry_id, tag_id)
);

CREATE TABLE protocols (
    id         TEXT PRIMARY KEY,
    name       TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE protocol_versions (
    id          TEXT PRIMARY KEY,
    protocol_id TEXT NOT NULL REFERENCES protocols(id),
    version     INTEGER NOT NULL,
    created_at  TEXT NOT NULL,
    body_md     TEXT NOT NULL,
    UNIQUE (protocol_id, version)
);

CREATE TABLE attachments (
    id           TEXT PRIMARY KEY,
    entry_id     TEXT NOT NULL REFERENCES entries(id),
    original_name TEXT NOT NULL,
    stored_path  TEXT NOT NULL,   -- относительный путь в attachments/
    sha256       TEXT NOT NULL,
    size_bytes   INTEGER NOT NULL,
    mime_type    TEXT NOT NULL
);

CREATE TABLE entry_links (          -- связи «эксперимент → эксперимент»
    from_id TEXT NOT NULL REFERENCES entries(id),
    to_id   TEXT NOT NULL REFERENCES entries(id),
    PRIMARY KEY (from_id, to_id)
);
```

Полнотекстовый индекс — FTS5-таблица `entries_fts(title, body_md, tags)`,
синхронизация триггерами (см. спеку 05).

## Хеш-цепочка

- Каноническое представление записи для хеширования:
  `f"{id}|{seq}|{created_at}|{entry_type}|{title}|{body_md}|{supersedes or ''}|{prev_hash}"`,
  кодировка UTF-8.
- `hash = sha256(canonical).hexdigest()`, `prev_hash` = `hash` предыдущей по
  `seq` записи; у первой записи `prev_hash = ""`.
- `core.integrity.verify_chain(db) -> IntegrityReport` проходит всю цепочку и
  возвращает список нарушений (битый хеш, разрыв prev_hash, пропуск seq).
  Вызывается при старте приложения; при нарушении — диалог с предложением
  восстановить из бэкапа, запись в журнал запрещена.

## Правила реализации

- `seq` выдаёт `core.db.queries.next_seq()` в одной транзакции с INSERT
  (`BEGIN IMMEDIATE`), чтобы исключить дыры при падении.
- `created_at` — только UTC (`datetime.now(timezone.utc).isoformat()`).
- Триггеры БД, поднимающие `UPDATE`/`DELETE` на `entries`, должны вызывать
  `RAISE(ABORT, 'entries are append-only')` — защита на уровне БД.
- UUIDv4, не UUIDv7: сортировка — по `seq`, не по id.
