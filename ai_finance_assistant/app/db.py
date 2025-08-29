from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path
DB_URL = f"sqlite:///{Path('finance.db').absolute()}"
engine = create_engine(DB_URL, echo=False)

def init_db():
    from .models import Transaction, Category, Budget, Rule
    SQLModel.metadata.create_all(engine)

def SessionLocal():
    return Session(engine)
