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

def list_all_users():
    session = Session()
    try:
        users = session.query(UserDetails).all()
        for u in users:
            print(f"User ID: {u.user_id}, Full Name: {u.full_name}, Email: {u.email}, Phone: {u.phone}, "
                  f"Is Admin: {u.is_admin}, Is Active: {u.is_active}, Email Verified: {u.email_verified}, "
                  f"Created At: {u.created_at}, Updated At: {u.updated_at}")
    except Exception as e:
        print(f"Error fetching users: {e}")
    finally:
        session.close()

list_all_users()