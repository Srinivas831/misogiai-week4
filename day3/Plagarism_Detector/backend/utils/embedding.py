# Generate embeddings using OpenAI

# utils/embedding.py

import openai

def get_openai_embeddings(texts, api_key, model="text-embedding-3-small"):
    """Call OpenAI API to get embeddings for a list of texts."""
    openai.api_key = api_key
    print("get_openai_embeddings",texts)
    response = openai.embeddings.create(
        input=texts,
        model=model
    )

    embeddings = [item.embedding for item in response.data]
    return embeddings
