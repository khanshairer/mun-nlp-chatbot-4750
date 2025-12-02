import sqlite3
import os
import re
import difflib

DB_PATH = "campus.db"
SQL_PATH = os.path.join("data", "data.sql")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_db():
    if not os.path.exists(DB_PATH):
        if os.path.exists(SQL_PATH):
            with open(SQL_PATH, "r", encoding="utf-8") as f:
                sql_script = f.read()
        else:
            sql_script = """
            CREATE TABLE IF NOT EXISTS professors (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              position TEXT,
              office TEXT,
              email TEXT,
              phone TEXT,
              faculty TEXT
            );
            """
        conn = sqlite3.connect(DB_PATH)
        conn.executescript(sql_script)
        conn.commit()
        conn.close()


def find_prof_by_name(name_part: str):
    """
    Case-insensitive, token-based match.
    Works even if DB has 'Wareham, Todd' and user types 'Todd Wareham'.
    """
    name_part = (name_part or "").strip().lower()
    if not name_part:
        return []

    parts = [p for p in re.split(r"\s+", name_part) if p]

    with get_db() as db:
        sql = (
            "SELECT name, position, office, email, phone, faculty "
            "FROM professors WHERE 1=1"
        )
        params = []

        for p in parts:
            sql += " AND lower(name) LIKE ?"
            params.append(f"%{p}%")

        sql += " ORDER BY name LIMIT 10"

        cur = db.execute(sql, params)
        rows = [dict(r) for r in cur.fetchall()]

    return rows


def find_prof_by_office(office_code: str):
    """
    Returns all professors whose office exactly matches a room code,
    e.g. EN-2008.
    """
    office_code = (office_code or "").strip().upper()
    if not office_code:
        return []

    with get_db() as db:
        cur = db.execute(
            """
            SELECT name, position, office, email, phone, faculty
            FROM professors
            WHERE upper(office) = ?
            ORDER BY name
            """,
            (office_code,),
        )
        return [dict(r) for r in cur.fetchall()]


def suggest_prof_names(prefix: str, limit: int = 5):
    """
    Autocomplete suggestions for professor names given a prefix.
    """
    prefix = (prefix or "").strip().lower()
    if not prefix:
        return []

    with get_db() as db:
        cur = db.execute(
            """
            SELECT DISTINCT name
            FROM professors
            WHERE lower(name) LIKE ?
            ORDER BY name
            LIMIT ?
            """,
            (f"{prefix}%", limit),
        )
        return [row["name"] for row in cur.fetchall()]


def find_prof_by_name_fuzzy(name_part: str, cutoff: float = 0.7):
    """
    Fuzzy fallback using difflib.
    Handles typos like 'Tod Wareham' -> 'Wareham, Todd'.
    Returns (rows, best_name_string).
    """
    name_part = (name_part or "").strip().lower()
    if not name_part:
        return [], None

    with get_db() as db:
        cur = db.execute(
            "SELECT name, position, office, email, phone, faculty FROM professors"
        )
        rows = [dict(r) for r in cur.fetchall()]

    if not rows:
        return [], None

    names = [r["name"] for r in rows]
    lowers = [n.lower() for n in names]

    # try full string first
    candidates = difflib.get_close_matches(name_part, lowers, n=3, cutoff=cutoff)

    # if nothing, try per-token
    if not candidates:
        for token in name_part.split():
            if len(token) < 3:
                continue
            token_matches = difflib.get_close_matches(token, lowers, n=3, cutoff=cutoff)
            if token_matches:
                candidates = token_matches
                break

    if not candidates:
        return [], None

    best_lc = candidates[0]
    idx = lowers.index(best_lc)
    best_row = rows[idx]
    return [best_row], best_row["name"]
