import sqlite3
import pandas as pd

DB_PATH = "campus.db"
EXCEL_PATH = "data/all_faculty_full_combined.xlsx"

# EXACT COLUMN MAP taken from your Excel headers
COLUMN_MAP = {
    "name": "Professor Name",
    "position": "Position",
    "office": "Office",
    "email": "Email",
    "phone": "Phone",
    "faculty": "Faculty"
}

def main():
    df = pd.read_excel(EXCEL_PATH)

    # Rename columns to internal names
    rename_dict = {}
    for key, col in COLUMN_MAP.items():
        if col in df.columns:
            rename_dict[col] = key
        else:
            print(f"WARNING: Column '{col}' not found in Excel.")

    df = df.rename(columns=rename_dict)

    # Ensure all expected columns exist
    needed = ["name", "position", "office", "email", "phone", "faculty"]
    for col in needed:
        if col not in df.columns:
            df[col] = None

    df = df[needed]
    df = df.dropna(subset=["name"])

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Drop & recreate table to ensure correct schema
    cur.execute("DROP TABLE IF EXISTS professors")

    # Create table if missing
    cur.execute("""
        CREATE TABLE IF NOT EXISTS professors (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          position TEXT,
          office TEXT,
          email TEXT,
          phone TEXT,
          faculty TEXT
        )
    """)

    # Insert rows
    for _, r in df.iterrows():
        cur.execute("""
            INSERT INTO professors (name, position, office, email, phone, faculty)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            r["name"], r["position"], r["office"],
            r["email"], r["phone"], r["faculty"]
        ))

    conn.commit()
    conn.close()
    print(f"Imported {len(df)} professors into {DB_PATH}.")

if __name__ == "__main__":
    main()
