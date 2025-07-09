# This file is for handling CRUD operatiions and other database related operations.
from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Table, MetaData, inspect
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

import os
from db_setup import UserDetails  # Import the UserDetails Schema
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


# Check user credentials for login
def check_user_credentials(email, password):
    session = Session()
    try:
        user = session.query(UserDetails).filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            print(f"Credentials match for user {email}")
            return user  # Return the user object on successful login
        else:
            print(f"Credentials do not match for user {email} or user not found.")
            return None  # Return None if user not found or password incorrect
    except Exception as e:
        print(f"Error checking user credentials: {e}")
        return None
    finally:
        session.close()


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

# activate user email
def activate_user_email(email):
    session = Session()
    try:
        user = session.query(UserDetails).filter_by(email=email).first()
        if user:
            user.email_verified = 1
            session.commit()
            print(f"Email {email} activated successfully.")
        else:
            print(f"Email {email} not found.")
            return "Email not found."    
    except Exception as e:
        print(f"Error activating email: {e}")
        session.rollback()
    finally:
        session.close()


def get_user_by_email(email):
    """Retrieve a user from the database by email."""
    session = Session()
    try:
        user = session.query(UserDetails).filter_by(email=email).first()
        return user
    except Exception as e:
        print(f"Error retrieving user by email: {e}")
        return None
    finally:
        session.close()

# # Example usage
# hashed_password = hash_password("my_secure_password")
# print("Password hashed successfully.\ndecrypting...")
# verify_password(hashed_password, "my_secure_password")
