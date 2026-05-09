import numpy as np


def forecast_spending(transactions):

    amounts = []

    # Extract transaction amounts
    for transaction in transactions:

        amounts.append(transaction["amount"])

    # Handle empty data
    if len(amounts) == 0:

        return {
            "predicted_next_month_spending": 0
        }

    # Calculate average spending
    average_spending = np.mean(amounts)

    # Simple monthly prediction
    predicted_spending = average_spending * 30

    return {
        "predicted_next_month_spending":
            round(predicted_spending, 2)
    }