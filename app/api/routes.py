from fastapi import APIRouter
from pydantic import BaseModel

from pydantic import BaseModel
from agents.data_agent import fetch_transactions
from agents.rag_agent import ask_finance_question
from services.transaction_service import process_transaction
from agents.orchestrator import run_financial_analysis
from db.database import get_connection

class QuestionRequest(BaseModel):

    question: str

router = APIRouter()


class Transaction(BaseModel):
    amount: float
    description: str


@router.post("/transaction")
def add_transaction(transaction: Transaction):

    result = process_transaction(transaction)

    return result


@router.get("/insights")
def get_insights():

    result = run_financial_analysis()

    return result


@router.post("/ask-ai")
def ask_ai(request: QuestionRequest):

    # Fetch all transactions
    transactions = fetch_transactions()

    # Ask AI with transaction context
    answer = ask_finance_question(
        request.question,
        transactions
    )

    return {
        "question": request.question,
        "answer": answer
    }