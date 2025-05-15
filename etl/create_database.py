import os
import sqlite3

if __name__ == "__main__":
    current_directory = os.getcwd()
    
    conn = sqlite3.connect(os.path.join(current_directory, 'data', 'test.db'))
    cursor = conn.cursor()

    # create tables
    # Read SQL queries from an external file
    with open(os.path.join(current_directory, 'others', 'sql', 'table_creation.sql'), 'r') as sql_file:
        sql_script = sql_file.read()

    # Execute the SQL script to create tables
    cursor.executescript(sql_script)

    # Read SQL queries from an external file
    with open(os.path.join(current_directory, 'others', 'sql', 'date_time_table_insertion.sql'), 'r') as sql_file:
        sql_script = sql_file.read()

    # Execute the SQL script to create tables
    cursor.executescript(sql_script)