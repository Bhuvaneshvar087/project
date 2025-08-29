from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db, SessionLocal
from .models import Transaction, Category, Budget
from .services import csv_ingest, insights, chat
from .schemas import TxQuery, ChatQuery

app = FastAPI(title="AI Finance Assistant API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def startup():
    init_db()

@app.post("/ingest/csv")
async def ingest_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.CSV')):
        raise HTTPException(400, "Only CSV supported in MVP")
    inserted = csv_ingest.process_csv(await file.read())
    return {"status":"ok","inserted":inserted}

@app.post("/chat/query")
def chat_query(q: ChatQuery):
    answer = chat.answer(q.question)
    return answer

@app.post("/transactions/query")
def tx_query(q: TxQuery):
    return insights.query_transactions(q)

@app.get("/insights/summary")
def insights_summary(period: str = "month"):
    return insights.summary(period)
