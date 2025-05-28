import os
import sqlite3

import pandas as pd

from load.loader import load

def execute_sql_script(script_name : str, cursor : sqlite3.Cursor):
    current_directory = os.getcwd()
    
    with open(os.path.join(current_directory, 'others', 'sql', f'{script_name}.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    
def reinit_db():
    current_directory = os.getcwd()
    
    conn = sqlite3.connect(os.path.join(current_directory, 'data', 'test.db'))
    cursor = conn.cursor()
    
    print("Reinitializing database...")
    execute_sql_script('table_deletion', cursor)
    print("Tables deleted successfully.")
    execute_sql_script('table_creation', cursor)
    print("Tables created successfully.")
    execute_sql_script('date_time_dim_insertion', cursor)
    execute_sql_script('categorical_dim_insertion', cursor)
    
    conn.close()
    
    df = pd.read_csv(r'others\misc\dummy_report_batch.csv')
    load(df)
    

if __name__ == "__main__":
    reinit_db()

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