from fastapi import APIRouter
from pydantic import BaseModel

from ml.ml_model import (
    predict_category
)

router = APIRouter()

# --------------------------------
# Temporary in-memory storage
# --------------------------------
transactions = []


# --------------------------------
# Request schema
# --------------------------------
class TransactionCreate(BaseModel):
    description: str
    amount: float


# --------------------------------
# Add Transaction Route
# --------------------------------
@router.post("/add-transaction")
def add_transaction(
    transaction: TransactionCreate
):

    # Predict category using ML model
    predicted_category = (
        predict_category(
            transaction.description
        )
    )

    # Create transaction object
    new_transaction = {
        "description":
        transaction.description,

        "amount":
        transaction.amount,

        "category":
        predicted_category
    }

    # Save transaction
    transactions.append(
        new_transaction
    )

    return {
        "message":
        "Transaction saved",

        "transaction":
        new_transaction
    }


# --------------------------------
# Get All Transactions
# --------------------------------
@router.get("/transactions")
def get_transactions():

    return transactions


# --------------------------------
# Full Dashboard Analysis
# --------------------------------
@router.get("/full-analysis")
def full_analysis():

    # Total spending
    total_spent = sum(
        item["amount"]
        for item in transactions
    )

    # Category-wise totals
    category_totals = {}

    for item in transactions:

        category = (
            item["category"]
        )

        if category not in (
            category_totals
        ):
            category_totals[
                category
            ] = 0

        category_totals[
            category
        ] += item["amount"]

    # Budget chart data
    budget_analysis = [

        {
            "category": key,
            "spent": value
        }

        for key, value
        in category_totals.items()
    ]

    # AI insight text
    insight_text = (
        f"Your total spending "
        f"is ₹{total_spent}. "
        f"You are spending mostly "
        f"on "
        f"{max(category_totals, key=category_totals.get) if category_totals else 'No Category'}."
    )

    # Forecast
    forecast_amount = round(
        total_spent * 1.2,
        2
    )

    return {

        "insights":
        insight_text,

        "forecast": {
            "predicted_next_month_spending":
            forecast_amount
        },

        "budget_plan": {
            "budget_analysis":
            budget_analysis
        }
    }