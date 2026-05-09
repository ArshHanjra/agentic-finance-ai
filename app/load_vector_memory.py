from agents.data_agent import fetch_transactions

from agents.vector_memory_agent import store_transactions


transactions = fetch_transactions()

store_transactions(transactions)

print("Vector memory loaded successfully")