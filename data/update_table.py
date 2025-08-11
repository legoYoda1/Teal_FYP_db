import os
import sqlite3


conn = sqlite3.connect(os.path.join(os.getcwd(), 'data', 'test.db'))

cursor = conn.cursor()

cursor.executescript('''UPDATE location_dim
SET zone = 'NW'
WHERE zone = '0';''')

conn.close()