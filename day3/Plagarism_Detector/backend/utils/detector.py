#  Flag clones based on thresholds

# utils/preprocess.py

# utils/detector.py

def detect_clones(similarity_matrix, threshold=0.85):
    """
    Return a list of index pairs where similarity > threshold.
    Avoid duplicate and self-pairs.
    """
    clones = []
    n = len(similarity_matrix)
    for i in range(n):
        for j in range(i + 1, n):
            if similarity_matrix[i][j] >= threshold:
                clones.append({"pair": [i, j], "similarity": similarity_matrix[i][j]})
    return clones

