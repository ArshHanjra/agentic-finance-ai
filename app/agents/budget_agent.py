from collections import defaultdict


def generate_budget_plan(transactions):

    category_totals = defaultdict(float)

    total_spending = 0

    # Calculate spending per category
    for transaction in transactions:

        amount = transaction.get("amount", 0)

        category = transaction.get(
            "category",
            "Other"
        )

        # Ignore invalid amounts
        if amount <= 0:
            continue

        category_totals[category] += amount

        total_spending += amount

    # Handle no spending
    if total_spending == 0:

        return {
            "message": "No spending data found"
        }

    # Generate recommendations
    recommendations = []

    for category, amount in category_totals.items():

        percentage = (
            amount / total_spending
        ) * 100

        recommendation = {
            "category": category,
            "spent": round(amount, 2),
            "percentage": round(percentage, 2)
        }

        # Overspending warning
        if percentage > 25:

            recommendation["warning"] = (
                f"High spending detected in "
                f"{category}"
            )

            recommendation["advice"] = (
                f"Try reducing expenses in "
                f"{category}"
            )

        recommendations.append(
            recommendation
        )

    return {
        "total_spending": round(
            total_spending,
            2
        ),
        "budget_analysis": recommendations
    }