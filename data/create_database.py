import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load database URI directly
DATABASE_URI = os.getenv('MYSQL_DB_URI')
if not DATABASE_URI:
    raise ValueError("MYSQL_DB_URI not set in environment variables.")

# Extract server URI (without database) to create the DB if needed
# Example: mysql+mysqlconnector://user:pass@host
parts = DATABASE_URI.rsplit('/', 1)
if len(parts) != 2:
    raise ValueError("Invalid MYSQL_DB_URI format. Expected: mysql+driver://user:pass@host/dbname")

SERVER_URI, DB_NAME = parts[0], parts[1]

def execute_sql_script(script_name: str, connection):
    """
    Executes all SQL statements from a script file.
    """
    file_path = os.path.join(os.getcwd(), 'others', 'sql', f'{script_name}.sql')
    print(f"Executing {script_name}.sql...")

    with open(file_path, 'r') as sql_file:
        sql_script = sql_file.read()
        commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]

    for command in commands:
        connection.execute(text(command))

    print(f"Finished {script_name}.sql")

def reinit_db():
    """
    Ensures the MySQL database exists, then runs SQL initialization scripts.
    """
    try:
        # Step 1: Create the database if it doesn't exist
        server_engine = create_engine(SERVER_URI)
        with server_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'"))
            print(f"Database '{DB_NAME}' ensured to exist.")

        # Step 2: Run scripts on the created database
        db_engine = create_engine(DATABASE_URI)
        with db_engine.connect() as conn:
            with conn.begin():
                print(f"Connected to '{DB_NAME}'. Running initialization scripts...")
                execute_sql_script('table_deletion', conn)
                execute_sql_script('table_creation', conn)
                execute_sql_script('date_time_dim_insertion', conn)
            print("Initialization complete.")
    except Exception as e:
        print(f"Error during database initialization: {e}")

if __name__ == "__main__":
    reinit_db()
