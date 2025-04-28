import sqlite3
from contextlib import contextmanager


def init_db(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()

    # Create the documents table.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        uri TEXT PRIMARY KEY,
        title TEXT,
        body TEXT NOT NULL,
        hash TEXT,
        metadata TEXT,

        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create virtual FTS5 table based on the documents table.
    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5 (
        uri,
        title,
        body,
        content=documents,
        tokenize="porter unicode61 remove_diacritics 1"
    );
    """)

    # Create trigger to keep the FTS5 index up to date.
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
        INSERT INTO documents_fts(rowid, uri, title, body) VALUES (new.rowid, new.uri, new.title, new.body);
    END;
    """)

    # Settings
    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("PRAGMA synchronous = NORMAL;")
    cursor.execute("PRAGMA busy_timeout = 5000;")
    cursor.execute("PRAGMA temp_store = FILE;")
    cursor.execute("PRAGMA cache_size = 2000;")
    cursor.execute("PRAGMA auto_vacuum = FULL;")

    conn.commit()


@contextmanager
def db_connection(db_url: str):
    conn = sqlite3.connect(db_url)

    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
