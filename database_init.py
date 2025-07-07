# This file is for initializing the database and creating the userdetails table.
# Also houses the UserDetails schema that will be imported in dbm.py for CRUD operations.
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, inspect, Index, text
from sqlalchemy.orm import sessionmaker,declarative_base
from datetime import datetime
from dotenv import load_dotenv
import os
import logging
load_dotenv()
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)


db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_user_email = os.getenv("DB_USER_EMAIL")

# Database connection
DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_name}"

# Create engine and session
engine = create_engine(DATABASE_URL, echo=False)  # Replace with your credentials
Base = declarative_base()

class UserDetails(Base):
    __tablename__ = 'userdetails'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    
    full_name = Column(String(150), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    
    # Store hashed password only (e.g., bcrypt hash)
    password = Column(String(255), nullable=False)

    # Security-related fields
    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)  # Account activation toggle
    email_verified = Column(Boolean, default=False, nullable=False)

    failed_logins = Column(Integer, default=0, nullable=False)  # Useful for throttling
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Optional: password reset tokens or MFA (multi-factor authentication)
    reset_token = Column(String(255), nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)


# Check if tables exist and print appropriate messages
def create_tables():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    if 'userdetails' in existing_tables:
        print("Table 'userdetails' already exists.")
    else:
        Base.metadata.tables['userdetails'].create(bind=engine)
        print("Table 'userdetails' created.")


# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Run the table creation
if __name__ == "__main__":
    create_tables()
    # Close the session
    session.close()
    print("Database setup complete.")

