from datetime import datetime
from db.database import get_connection
from services.ml_service import predict_category


def process_transaction(transaction):
    conn = get_connection()
    cursor = conn.cursor()

    # 🔥 ML prediction
    category = predict_category(transaction.description)

    query = """
    INSERT INTO transactions (amount, description, category)
    VALUES (%s, %s, %s)
    RETURNING id;
    """

    cursor.execute(query, (
        transaction.amount,
        transaction.description,
        category
    ))

    transaction_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message": "Transaction saved",
        "category": category,
        "transaction_id": transaction_id,
        "timestamp": datetime.now()
    }