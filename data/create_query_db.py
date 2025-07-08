import os
import sqlite3

conn = sqlite3.connect(os.path.join(os.getcwd(), 'data', 'saved_queries.db'))

cursor = conn.cursor()

# Create the saved_queries table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS saved_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL,
    sql_query TEXT NOT NULL,
    chart_code TEXT
);''')