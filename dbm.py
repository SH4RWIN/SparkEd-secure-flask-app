# This file is for handling CRUD operatiions and other database related operations.
from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Table, MetaData, inspect
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os
from database_init import UserDetails  # Import the UserDetails Schema
from datetime import datetime, timedelta

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
base = declarative_base()

def check_email_exists(email):
    """check if the email exists in the database
       Returns True if email exists, False otherwise.
    """
    session = Session()
    try:
        user = session.query(UserDetails).filter_by(email=email).first()
        if user:
            print(f"Email {email} already exists.")
            return True
        else:
            print(f"Email {email} does not exist.")
            return False
    except IntegrityError as e:
        print(f"Integrity error: {e}")
        return False
    finally:
        session.close()

# print(check_email_exists("test@example.com"))

def create_user(email, full_name, phone, password, is_admin=0, is_active=0, email_verified=0, reset_token=0, reset_token_expiry=0):
    """Create a new user in the database."""
    # !!!! NEED TO ADD PASSWORD HASHING HERE !!!!
    session = Session()
    new_user = UserDetails(
        email=email,
        full_name=full_name,
        phone=phone,
        password=password,  # Ensure this is a hashed password
        is_admin=is_admin,
        is_active=is_active,
        email_verified=email_verified,
        failed_logins=0,
        last_login_at=datetime.utcnow(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        reset_token=reset_token,
        reset_token_expiry=datetime.utcnow() + timedelta(days=1) if reset_token_expiry else None
    )
    try:
        session.add(new_user)
        session.commit()
        print(f"User {full_name} created successfully.")
    except IntegrityError as e:
        print(f"Integrity error: {e}")
        session.rollback()
    finally:
        session.close()

# # lets add a sample user
# create_user(email="test@example.com", full_name="Test User", phone="1234567890", password="hashed_password" \
#             , is_admin=0, is_active=1, email_verified=0)

