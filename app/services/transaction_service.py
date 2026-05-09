from db.database import get_connection
from agents.ml_agent import predict_category


def process_transaction(transaction):

    # ML prediction
    prediction = predict_category(
        transaction.description
    )

    category = prediction["category"]

    confidence = prediction["confidence"]

    # Connect DB
    conn = get_connection()

    cursor = conn.cursor()

    # Insert transaction
    cursor.execute(
        """
        INSERT INTO transactions
        (amount, description, category)

        VALUES (%s, %s, %s)

        RETURNING id
        """,
        (
            transaction.amount,
            transaction.description,
            category
        )
    )

    transaction_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Transaction saved",
        "category": category,
        "confidence": confidence,
        "transaction_id": transaction_id
    }