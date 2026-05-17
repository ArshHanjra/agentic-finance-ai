from collections import defaultdict


def generate_budget_plan(transactions):

    category_totals = defaultdict(float)

    total_spending = 0

    # -----------------------------------
    # Calculate category spending
    # -----------------------------------
    for transaction in transactions:

        category = transaction.get(
            "category",
            "Other"
        )

        amount = float(
            transaction.get(
                "amount",
                0
            )
        )

        category_totals[category] += amount
        total_spending += amount

    # -----------------------------------
    # Build structured analysis
    # -----------------------------------
    budget_analysis = []

    high_risk_categories = []

    for category, spent in category_totals.items():

        percentage = 0

        if total_spending > 0:
            percentage = round(
                (spent / total_spending) * 100,
                2
            )

        # Risk detection
        if percentage >= 40:
            risk_level = "high"
            high_risk_categories.append(category)

        elif percentage >= 25:
            risk_level = "medium"

        else:
            risk_level = "low"

        # Recommendation logic
        if risk_level == "high":
            recommendation = (
                f"Reduce spending in {category} category"
            )

        elif risk_level == "medium":
            recommendation = (
                f"Monitor spending in {category}"
            )

        else:
            recommendation = (
                f"Spending in {category} looks healthy"
            )

        budget_analysis.append({
            "agent": "budget_agent",
            "category": category,
            "spent": round(spent, 2),
            "percentage": percentage,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "action_required": risk_level != "low"
        })

    # -----------------------------------
    # Overall financial status
    # -----------------------------------
    overall_status = "healthy"

    if len(high_risk_categories) >= 2:
        overall_status = "critical"

    elif len(high_risk_categories) == 1:
        overall_status = "warning"

    # -----------------------------------
    # Final structured output
    # -----------------------------------
    return {
        "agent": "budget_agent",
        "overall_status": overall_status,
        "total_spending": round(total_spending, 2),
        "high_risk_categories": high_risk_categories,
        "budget_analysis": budget_analysis
    }