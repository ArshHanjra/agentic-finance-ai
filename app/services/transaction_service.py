from datetime import datetime
from db.database import get_connection

def process_transaction(transaction):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO transactions (amount, description, category)
    VALUES (%s, %s, %s)
    RETURNING id;
    """

    cursor.execute(query, (
        transaction.amount,
        transaction.description,
        "uncategorized"
    ))

    transaction_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message": "Transaction saved",
        "transaction_id": transaction_id,
        "timestamp": datetime.now()
    }