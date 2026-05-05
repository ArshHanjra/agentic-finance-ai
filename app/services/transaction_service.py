from datetime import datetime

def process_transaction(transaction):
    return {
        "message": "Transaction processed",
        "data": transaction.dict(),
        "timestamp": datetime.now()
    }