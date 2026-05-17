from db.database import get_connection


# -----------------------------------
# Add Transaction
# -----------------------------------
def add_transaction(description, amount, category):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (
            description,
            amount,
            category
        )
        VALUES (%s, %s, %s)
        RETURNING id;
        """,
        (description, amount, category)
    )

    transaction_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": transaction_id,
        "description": description,
        "amount": float(amount),
        "category": category
    }


# -----------------------------------
# Get All Transactions
# -----------------------------------
def get_transactions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            description,
            amount,
            category
        FROM transactions
        ORDER BY id DESC;
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    transactions = []

    for row in rows:
        transactions.append({
            "id": row[0],
            "description": row[1],
            "amount": float(row[2]),
            "category": row[3]
        })

    return transactions


# -----------------------------------
# Get Transactions By Category
# -----------------------------------
def get_transactions_by_category(category):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            description,
            amount,
            category
        FROM transactions
        WHERE category = %s
        ORDER BY id DESC;
        """,
        (category,)
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    transactions = []

    for row in rows:
        transactions.append({
            "id": row[0],
            "description": row[1],
            "amount": float(row[2]),
            "category": row[3]
        })

    return transactions


# -----------------------------------
# Get Total Spending
# -----------------------------------
def get_total_spending():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions;
        """
    )

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return float(total)


# -----------------------------------
# Delete Transaction
# -----------------------------------
def delete_transaction(transaction_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM transactions
        WHERE id = %s;
        """,
        (transaction_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Transaction deleted successfully"
    }


# -----------------------------------
# Update Transaction
# -----------------------------------
def update_transaction(
    transaction_id,
    description,
    amount,
    category
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE transactions
        SET
            description = %s,
            amount = %s,
            category = %s
        WHERE id = %s;
        """,
        (
            description,
            amount,
            category,
            transaction_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": transaction_id,
        "description": description,
        "amount": float(amount),
        "category": category,
        "message": "Transaction updated successfully"
    }