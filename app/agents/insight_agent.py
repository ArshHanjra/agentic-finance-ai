import requests
from collections import defaultdict


OLLAMA_URL = "http://localhost:11434/api/generate"


def calculate_category_totals(transactions):
    category_totals = defaultdict(float)

    for tx in transactions:
        category = tx.get("category", "Other")
        amount = float(tx.get("amount", 0))

        category_totals[category] += amount

    return dict(category_totals)


def detect_highest_spending(category_totals):
    if not category_totals:
        return None, 0

    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    return (
        highest_category,
        category_totals[highest_category]
    )


def generate_local_insights(transactions):

    if not transactions:
        return {
            "summary": "No transactions found.",
            "finance_score": 0,
            "recommendations": [],
        }

    total_spending = sum(
        float(tx.get("amount", 0))
        for tx in transactions
    )

    category_totals = calculate_category_totals(
        transactions
    )

    highest_category, highest_amount = (
        detect_highest_spending(
            category_totals
        )
    )

    recommendations = []

    if highest_amount > 5000:
        recommendations.append(
            f"Reduce spending on {highest_category}"
        )

    if total_spending > 20000:
        recommendations.append(
            "Your monthly spending is high. Try reducing unnecessary expenses."
        )

    if len(category_totals) <= 2:
        recommendations.append(
            "Your spending categories are limited. Track expenses more accurately."
        )

    finance_score = 100

    if total_spending > 20000:
        finance_score -= 20

    if highest_amount > 7000:
        finance_score -= 15

    if len(recommendations) > 2:
        finance_score -= 10

    finance_score = max(finance_score, 40)

    return {
        "summary": f"Your highest spending category is {highest_category} with ₹{highest_amount:.0f} spent.",
        "finance_score": finance_score,
        "recommendations": recommendations,
        "category_totals": category_totals,
        "total_spending": total_spending,
    }


def generate_ai_insight(transactions):

    local_analysis = generate_local_insights(
        transactions
    )

    prompt = f"""
    You are an AI financial advisor.

    Analyze the following spending data:

    {transactions}

    Give:
    1. Spending summary
    2. Savings advice
    3. Financial risk warning
    4. Smart recommendation

    Keep response short and professional.
    """

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
            },
            timeout=8,
        )

        ai_response = response.json().get(
            "response",
            "AI analysis unavailable."
        )

    except Exception:

        ai_response = (
            "AI service offline. Showing local analysis only."
        )

    return {
        "ai_summary": ai_response,
        "local_analysis": local_analysis,
    }