import requests
from agents.vector_memory_agent import search_transactions

OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_finance_question(question, transactions):

    # Convert transactions into text
    transaction_context = ""

    relevant_transactions = search_transactions(question)

    transaction_context = ""

    for transaction in relevant_transactions:

        transaction_context += transaction + "\n"

    # Create AI prompt
    prompt = f"""
    You are a personal finance AI assistant.

    Here are the user's transactions:

    {transaction_context}

    User Question:
    {question}

    Give a helpful financial answer.
    """

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    result = response.json()

    return result["response"]