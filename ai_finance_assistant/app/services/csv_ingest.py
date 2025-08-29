import pandas as pd
import io
from ..db import SessionLocal
from ..models import Transaction
from datetime import datetime

COLS = {
    'date': ['Date','Transaction Date','Txn Date'],
    'description': ['Description','Narration','Details'],
    'amount': ['Amount','Txn Amount','Debit/Credit']
}

def normalize_amount(val):
    if isinstance(val, str):
        val = val.replace(',', '').strip()
    return float(val)

def process_csv(raw_bytes: bytes) -> int:
    df = pd.read_csv(io.BytesIO(raw_bytes))
    def pick(cols):
        for c in cols:
            if c in df.columns: return c
        return cols[0]
    c_date = pick(COLS['date']); c_desc = pick(COLS['description']); c_amt = pick(COLS['amount'])
    rows = []
    for _, r in df.iterrows():
        rows.append(Transaction(
            date = pd.to_datetime(r[c_date]).date(),
            description = str(r[c_desc])[:255],
            amount = normalize_amount(r[c_amt]),
            type = 'debit' if float(r[c_amt]) < 0 else 'credit'
        ))
    with SessionLocal() as s:
        s.add_all(rows); s.commit()
    return len(rows)
