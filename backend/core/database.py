# core/database.py
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")

# Railway's MySQL template provides a DATABASE_URL using the plain
# "mysql://" scheme, which causes SQLAlchemy to default to the MySQLdb
# driver. Explicitly use the PyMySQL driver instead, since that's what's
# installed in requirements.txt.
if SQLALCHEMY_DATABASE_URL.startswith("mysql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "mysql://", "mysql+pymysql://", 1
    )
elif SQLALCHEMY_DATABASE_URL.startswith("mysql+") and not SQLALCHEMY_DATABASE_URL.startswith(
    "mysql+pymysql://"
):
    raise RuntimeError(
        "DATABASE_URL specifies a MySQL dialect other than pymysql, "
        "which is not installed. Use 'mysql+pymysql://' or 'mysql://'."
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()