# Calculate cosine similarity

# utils/similarity.py

from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity_matrix(embeddings):
    """Calculate pairwise cosine similarity between all embeddings."""
    similarity = cosine_similarity(embeddings)
    # Round results to 4 decimal places and convert to list for JSON
    return [[round(score, 4) for score in row] for row in similarity]
