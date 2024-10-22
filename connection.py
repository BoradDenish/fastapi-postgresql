import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch environment variables
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')  # Use IPv4
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PORT = os.getenv('DB_PORT')

# Debug: Print to verify that environment variables are correctly loaded
print(f"DB_USER={DB_USER}, DB_PASSWORD={DB_PASSWORD}, DB_HOST={DB_HOST}, DB_PORT={DB_PORT}, DB_NAME={DB_NAME}")

# Create PostgreSQL connection URL
DB_URL = f"postgresql://{DB_USER}:{quote(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print("DB_URL:", DB_URL)  # Debug: Print DB_URL

# Create engine
engine = create_engine(DB_URL, pool_pre_ping=True, pool_recycle=3600, pool_size=20, max_overflow=50)
connection = engine.connect()  # Try to connect to the database
print("Connection successful!")

# Declare session and Base
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()