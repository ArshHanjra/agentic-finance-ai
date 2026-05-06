import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# -----------------------------
# 1. Create dataset
# -----------------------------
data = {
    "text": [
        "Swiggy order",
        "Zomato dinner",
        "Uber ride",
        "Ola cab",
        "Amazon shopping",
        "Flipkart order",
        "Movie ticket",
        "Netflix subscription",
        "Electricity bill",
        "Water bill"
    ],
    "category": [
        "Food",
        "Food",
        "Transport",
        "Transport",
        "Shopping",
        "Shopping",
        "Entertainment",
        "Entertainment",
        "Bills",
        "Bills"
    ]
}

df = pd.DataFrame(data)

# -----------------------------
# 2. Split features and labels
# -----------------------------
X_text = df["text"]      # input text
y = df["category"]       # target labels

# -----------------------------
# 3. Convert text → numbers
# -----------------------------
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(X_text)

# -----------------------------
# 4. Train model
# -----------------------------
model = LogisticRegression()

model.fit(X, y)

# -----------------------------
# 5. Save model and vectorizer
# -----------------------------
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model and vectorizer saved successfully!")