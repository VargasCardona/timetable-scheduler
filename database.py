import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "pass")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "scheduler")
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "pass")

if not all([MYSQL_USER, MYSQL_PASSWORD]):
    raise ValueError(
        "Missing required MySQL environment variables. Check your .env or Docker setup.")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:3306/{MYSQL_DATABASE}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
