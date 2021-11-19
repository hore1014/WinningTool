import sqlite3

file = open("src\database\drop_tables.sql", "r")
drop_cmd = file.read()
file.close()

file = open("src\database\create_tables.sql", "r")
create_cmd = file.read()
file.close()

# Create and Connect to SQLite database
conn = sqlite3.connect("src\database\ibsys2.db")

# Drop existing tables
conn.executescript(drop_cmd)

# Initialize database
conn.executescript(create_cmd)

conn.close()
