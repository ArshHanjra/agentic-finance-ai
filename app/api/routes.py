from fastapi import APIRouter
from pydantic import BaseModel

from agents.orchestrator import run_financial_analysis
from services.transaction_service import (
    add_transaction,
    get_transactions
)

from ml.ml_model import predict_category

router = APIRouter()


# -----------------------------
# Request Model
# -----------------------------
class TransactionRequest(BaseModel):
    description: str
    amount: float


# -----------------------------
# Home Route
# -----------------------------
@router.get("/")
def home():
    return {
        "message": "Agentic Finance AI Backend Running"
    }


# -----------------------------
# Add Transaction
# -----------------------------
@router.post("/add-transaction")
def create_transaction(transaction: TransactionRequest):

    # ML Category Prediction
    predicted_category = predict_category(
        transaction.description
    )

    # Save into PostgreSQL
    saved_transaction = add_transaction(
        description=transaction.description,
        amount=transaction.amount,
        category=predicted_category
    )

    return {
        "message": "Transaction added successfully",
        "transaction": saved_transaction
    }


# -----------------------------
# Get All Transactions
# -----------------------------
@router.get("/transactions")
def fetch_transactions():

    transactions = get_transactions()

    return {
        "count": len(transactions),
        "transactions": transactions
    }


# -----------------------------
# Full AI Financial Analysis
# -----------------------------
@router.get("/full-analysis")
def full_analysis():

    analysis = run_financial_analysis()

    return analysis


# -----------------------------
# Health Check
# -----------------------------
@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "backend": "running",
        "ai_agents": "active",
        "database": "connected"
    }