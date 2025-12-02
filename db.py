import sqlite3, os, re

DB_PATH = "campus.db"
SQL_PATH = os.path.join("data", "data.sql")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_db():
    if not os.path.exists(DB_PATH):
        with open(SQL_PATH, "r", encoding="utf-8") as f:
            sql_script = f.read()
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
