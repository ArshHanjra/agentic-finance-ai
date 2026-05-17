from agents.data_agent import fetch_transactions
from agents.insight_agent import generate_ai_insight
from agents.action_agent import analyze_spending_behavior
from agents.forecast_agent import forecast_spending
from agents.budget_agent import generate_budget_plan


def run_financial_analysis():

    transactions = fetch_transactions()

    insight_data = generate_ai_insight(
        transactions
    )

    warnings = analyze_spending_behavior(
        transactions
    )

    forecast = forecast_spending(
        transactions
    )

    budget_plan = generate_budget_plan(
        transactions
    )

    return {
        "insights": insight_data.get(
            "ai_summary",
            ""
        ),

        "local_analysis": insight_data.get(
            "local_analysis",
            {}
        ),

        "warnings": warnings,

        "forecast": forecast,

        "budget_plan": budget_plan,
    }