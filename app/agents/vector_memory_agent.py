import chromadb

from sentence_transformers import SentenceTransformer


# Create Chroma client
client = chromadb.Client()


# Create collection
collection = client.get_or_create_collection(
    name="finance_memory"
)


# Load embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def store_transactions(transactions):

    for index, transaction in enumerate(transactions):

        text = (
            f"Category: {transaction.get('category', '')}, "
            f"Amount: {transaction.get('amount', '')}, "
            f"Description: {transaction.get('description', '')}"
        )

        embedding = embedding_model.encode(text).tolist()

        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[str(index)]
        )


def search_transactions(query):

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    return results["documents"][0]