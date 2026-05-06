import pandas as pd
import random

# Categories and sample keywords
data = {
    "Food & Drinks": [
        "swiggy order", "zomato food", "pizza", "burger", "biryani",
        "restaurant dinner", "coffee", "snacks", "juice", "breakfast"
    ],
    "Transport": [
        "uber ride", "ola cab", "bus ticket", "metro travel",
        "petrol pump", "auto fare", "train ticket"
    ],
    "Shopping": [
        "amazon order", "flipkart purchase", "clothes shopping",
        "buy shoes", "electronics purchase"
    ],
    "Bills & Fees": [
        "electricity bill", "internet recharge", "mobile recharge",
        "netflix subscription", "rent payment", "gym fee"
    ]
}

rows = []

# Generate 10,000 rows
for _ in range(1000000):
    category = random.choice(list(data.keys()))
    text = random.choice(data[category])

    rows.append({
        "title": text,
        "category": category
    })

df = pd.DataFrame(rows)

# Save file
df.to_csv("synthetic_data.csv", index=False)

print("✅ 10,000 rows generated: synthetic_data.csv")