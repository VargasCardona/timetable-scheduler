import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "pass")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "scheduler")
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "pass")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:3306/{MYSQL_DATABASE}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@contextmanager
def get_db_session():
    db = SessionLocal()  # ✅ Create an instance of the session
    try:
        yield db
    finally:
        db.close()
