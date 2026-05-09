def analyze_spending_behavior(transactions):

    category_totals = {}

    total_spending = 0

    # Calculate total spending per category
    for transaction in transactions:

        category = transaction["category"]
        amount = transaction["amount"]

        total_spending += amount

        if category not in category_totals:

            category_totals[category] = 0

        category_totals[category] += amount

    warnings = []

    # Detect overspending
    for category, amount in category_totals.items():

        percentage = (amount / total_spending) * 100

        if percentage > 50:

            warnings.append(
                f"High spending detected in {category}: {percentage:.1f}% of total expenses."
            )

    # Default response
    if not warnings:

        warnings.append("Spending distribution looks balanced.")

    return warnings