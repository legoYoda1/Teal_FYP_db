import os
import sqlite3

def execute_sql_script(script_name : str, cursor : sqlite3.Cursor):
    with open(os.path.join(current_directory, 'others', 'sql', f'{script_name}.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    

if __name__ == "__main__":
    current_directory = os.getcwd()
    
    conn = sqlite3.connect(os.path.join(current_directory, 'data', 'test.db'))
    cursor = conn.cursor()
    
    execute_sql_script('table_deletion', cursor)
    execute_sql_script('table_creation', cursor)
    execute_sql_script('date_time_dim_insertion', cursor)
    execute_sql_script('categorical_dim_insertion', cursor)

    # with open(os.path.join(current_directory, 'others', 'sql', 'table_deletion.sql'), 'r') as sql_file:
    #     sql_script = sql_file.read()
    # cursor.executescript(sql_script)

    # with open(os.path.join(current_directory, 'others', 'sql', 'table_creation.sql'), 'r') as sql_file:
    #     sql_script = sql_file.read()
    # cursor.executescript(sql_script)

    # with open(os.path.join(current_directory, 'others', 'sql', 'date_time_dim_insertion.sql'), 'r') as sql_file:
    #     sql_script = sql_file.read()
    # cursor.executescript(sql_script)

    # with open(os.path.join(current_directory, 'others', 'sql', 'date_time_dim_insertion.sql'), 'r') as sql_file:
    #     sql_script = sql_file.read()
    # cursor.executescript(sql_script)