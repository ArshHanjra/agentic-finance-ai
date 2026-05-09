from agents.data_agent import fetch_transactions
from agents.insight_agent import generate_ai_insight
from agents.action_agent import analyze_spending_behavior
from agents.forecast_agent import forecast_spending
from agents.budget_agent import generate_budget_plan


def run_financial_analysis():

    # Fetch transactions
    transactions = fetch_transactions()

    # AI insight generation
    insights = generate_ai_insight(transactions)

    # Spending warnings
    warnings = analyze_spending_behavior(transactions)

    # Future spending prediction
    forecast = forecast_spending(transactions)
    
    budget_plan = generate_budget_plan(transactions)

    return {
        "insights": insights,
        "warnings": warnings,
        "forecast": forecast,
        "budget_plan": budget_plan
    }