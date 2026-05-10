import joblib


# -----------------------------
# Load trained ML model
# -----------------------------
model = joblib.load(
    "ml/model.pkl"
)

# -----------------------------
# Load TF-IDF vectorizer
# -----------------------------
vectorizer = joblib.load(
    "ml/vectorizer.pkl"
)


# -----------------------------
# Predict category function
# -----------------------------
def predict_category(text: str):

    # Clean input text
    cleaned_text = (
        text.lower().strip()
    )

    # Convert text into vectors
    text_vector = (
        vectorizer.transform(
            [cleaned_text]
        )
    )

    # Predict category
    prediction = (
        model.predict(text_vector)
    )

    # Return predicted category
    return prediction[0]


# -----------------------------
# Testing locally
# -----------------------------
if __name__ == "__main__":

    sample_text = "Uber ride to office"

    predicted = predict_category(
        sample_text
    )

    print(
        f"Text: {sample_text}"
    )

    print(
        f"Predicted Category: {predicted}"
    )