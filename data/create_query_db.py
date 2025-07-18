import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Load the database URI from environment (fallback to sqlite if not set)
DB_URI = os.getenv("MYSQL_QUERY_DB_URI", "sqlite:///data/query.db")

# Set up SQLAlchemy
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define the table model
class SavedQuery(Base):
    __tablename__ = 'saved_queries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(255), nullable=False)
    sql_query = Column(Text, nullable=False)

# Create the table
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print(f"Database initialized at {DB_URI}")
