import numpy as np


def cosine_similarity(a, b):
    """
    cos(a, b) = (a · b) / (||a|| × ||b||)

    Measures ANGLE between vectors (ignores magnitude).
    Range: -1 (opposite) to +1 (identical direction).
    """
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return np.dot(a, b) / (norm_a * norm_b)


def dot_product_similarity(a, b):
    """
    a · b = Σ aᵢbᵢ

    Measures alignment. Affected by magnitude (longer vectors score higher).
    Used when magnitude carries information (e.g., popularity).
    """
    return np.dot(a, b)


class VectorSearch:

    def __init__(self, dim):
        self.dim = dim
        self.vectors = []
        self.metadata = []

    def add(self, vector, metadata):
        self.vectors.append(vector)
        self.metadata.append(metadata)

    def search(self, query, k=1, metric="cosine"):
        scores = []
        for index, vec in enumerate(self.vectors):
            if metric == "cosine":
                score = cosine_similarity(query, vec)
            scores.append((score, index))

        scores.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, idx in scores[:k]:
            results.append((score, self.metadata[idx]))
        return results


index = VectorSearch(3)
index.add([0.1, 0.2, 0.3], {"text": "hello"})
index.add([0.4, 0.5, 0.6], {"text": "world"})

print(index.vectors)
print(index.metadata)

print(index.search([0.1, 0.2, 0.3]))
