from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


class Transaction(BaseModel):
    amount: float
    description: str

@app.get("/")
def root():
    return {"message": "Welcome to Agentic Finance AI"}

@app.get("/health")
def health_check():
    return {"status": "API is running"}


@app.post("/transaction")
def add_transaction(transaction: Transaction):
    return {
        "message": "Transaction received",
        "data": transaction,
        "timestamp": datetime.now()
    }