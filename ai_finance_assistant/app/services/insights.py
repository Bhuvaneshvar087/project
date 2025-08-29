from ..db import SessionLocal
from ..models import Transaction
from sqlmodel import select
from datetime import date, timedelta

def query_transactions(q):
    with SessionLocal() as s:
        stmt = select(Transaction)
        txs = s.exec(stmt).all()
        return {"count": len(txs), "rows": [t.dict() for t in txs]}

def summary(period: str = "month"):
    today = date.today()
    start = today.replace(day=1) if period=="month" else (today - timedelta(days=30))
    with SessionLocal() as s:
        stmt = select(Transaction).where(Transaction.date >= start)
        txs = s.exec(stmt).all()
        total_spend = sum(t.amount for t in txs if t.type=='debit')
        top = sorted([t for t in txs if t.type=='debit'], key=lambda x: -abs(x.amount))[:5]
        return {
            "period_start": str(start),
            "total_spend": round(total_spend,2),
            "top_expenses": [dict(id=t.id, date=str(t.date), desc=t.description, amount=t.amount) for t in top]
        }
