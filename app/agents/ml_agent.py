import joblib


# Load trained ML model
model = joblib.load("ml/model.pkl")

# Load vectorizer
vectorizer = joblib.load("ml/vectorizer.pkl")


def predict_category(description):

    # Convert text into vector
    text_vector = vectorizer.transform([description])

    # Predict category
    category = model.predict(text_vector)[0]

    # Prediction confidence
    confidence = model.predict_proba(text_vector).max()

    return {
        "category": category,
        "confidence": round(float(confidence), 2)
    }