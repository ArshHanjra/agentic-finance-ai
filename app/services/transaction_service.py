from services.ml_service import predict_category
from db.database import get_connection
def process_transaction(transaction):
    conn = get_connection()
    cursor = conn.cursor()

    category, confidence = predict_category(transaction.description)

    # 🔥 Handle low confidence
    if confidence < 0.6:
        category = "Other"

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
        "confidence": round(confidence, 2),
        "transaction_id": transaction_id
    }