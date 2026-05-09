import requests


OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_financial_insight(transactions):

    total_spent = sum(t["amount"] for t in transactions)

    categories = {}

    for t in transactions:
        cat = t["category"]

        if cat not in categories:
            categories[cat] = 0

        categories[cat] += t["amount"]

    summary = "\n".join(
        [f"{k}: ₹{v}" for k, v in categories.items()]
    )

    prompt = f"""
    You are a financial advisor AI.

    Analyze this spending data and give smart financial insights.

    Total spent: ₹{total_spent}

    Category breakdown:
    {summary}

    Give:
    1. Spending analysis
    2. Saving tips
    3. Financial warning if needed
    """

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    result = response.json()

    return result["response"]