import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ArgumentError

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / 'backend' / '.env')

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./backend_dev.db')
connect_args = {'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {}

engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
