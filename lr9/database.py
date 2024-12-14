'''подключение к бд'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Подключение к PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:Q1w2E#@localhost:5432/lr9"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
