import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("synthetic_data.csv")

# -----------------------------
# 2. Select required columns
# -----------------------------
df = df[["title", "category", ]]

# -----------------------------
# 3. Handle missing values
# -----------------------------
df["title"] = df["title"].fillna("")
# df["description"] = df["description"].fillna("")
df["category"] = df["category"].fillna("Unknown")

# -----------------------------
# 4. Create input text
# -----------------------------
df["text"] = df["title"].astype(str) 
# -----------------------------
# 5. Clean data
# -----------------------------
df["text"] = df["text"].str.lower().str.strip()
df["category"] = df["category"].str.strip()

# Remove empty rows
df = df[df["text"] != ""]
df = df[df["category"] != ""]

# Keep only needed columns
df = df[["text", "category"]]

print("Sample data:")
print(df.head())

# -----------------------------
# 6. Train-test split
# -----------------------------
X_text = df["text"]
y = df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X_text, y, test_size=0.2, random_state=42
)

# -----------------------------
# 7. Vectorization
# -----------------------------
vectorizer = TfidfVectorizer()

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# -----------------------------
# 8. Train model
# -----------------------------
model = LogisticRegression(max_iter=200)

model.fit(X_train_vec, y_train)

# -----------------------------
# 9. Evaluate model
# -----------------------------
y_pred = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------
# 10. Save model
# -----------------------------
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nModel and vectorizer saved successfully!")