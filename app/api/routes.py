from fastapi import APIRouter
from schemas.transaction import Transaction
from services.transaction_service import process_transaction

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "API is running"}


@router.post("/transaction")
def add_transaction(transaction: Transaction):
    return process_transaction(transaction)