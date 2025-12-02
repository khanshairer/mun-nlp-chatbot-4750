DROP TABLE IF EXISTS professors;

CREATE TABLE professors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  position TEXT,
  office TEXT,
  email TEXT,
  phone TEXT,
  faculty TEXT
);
