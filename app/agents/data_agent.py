from db.database import get_connection


def fetch_transactions():

    # Create DB connection
    conn = get_connection()

    # Create cursor
    cursor = conn.cursor()

    # Run SQL query
    cursor.execute("""
        SELECT amount, category
        FROM transactions
    """)

    # Fetch all rows
    rows = cursor.fetchall()

    # Convert SQL rows into dictionaries
    transactions = []

    for row in rows:

        transactions.append({
            "amount": row[0],
            "category": row[1]
        })

    # Close DB resources
    cursor.close()
    conn.close()

    return transactions