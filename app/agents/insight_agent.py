import requests


def generate_ai_insight(transactions):

    # Build AI prompt
    prompt = f"""
    You are a financial advisor AI.

    Analyze the following transactions:

    {transactions}

    Give:
    1. Spending analysis
    2. Saving tips
    3. Financial warnings if needed
    """

    # Send request to Ollama
    response = requests.post(

        "http://localhost:11434/api/generate",

        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    # Convert response JSON into Python dictionary
    result = response.json()

    # Return AI-generated response
    return result["response"]