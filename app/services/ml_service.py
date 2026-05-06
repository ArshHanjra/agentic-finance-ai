import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../ml/model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "../ml/vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict_category(text: str):
    X = vectorizer.transform([text])

    prediction = model.predict(X)[0]

    # 🔥 NEW: confidence score
    probabilities = model.predict_proba(X)
    confidence = max(probabilities[0])

    return prediction, confidence