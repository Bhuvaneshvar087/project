from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = 1
    name: str
    parent_id: Optional[int] = None

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = 1
    account_id: Optional[int] = None
    date: date
    description: str
    amount: float
    type: str = "debit"
    category_id: Optional[int] = None
    merchant: Optional[str] = None
    is_recurring: bool = False
    raw_json: Optional[str] = None

class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = 1
    category_id: int
    month: str
    limit_amount: float

class Rule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = 1
    pattern: str
    category_id: int
    priority: int = 0
