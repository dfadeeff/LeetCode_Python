import numpy as np


def cosine_similarity(a, b):
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    return np.dot(a, b) / (norm_a * norm_b)


class VectorIndex:

    def __init__(self, dim):
        self.dim = dim
        self.vectors = []
        self.metadata = []

    def add(self, vector, meta):
        self.vectors.append(vector)
        self.metadata.append(meta)

    def search(self, query, k=3):
        scores = []
        for i, vec in enumerate(self.vectors):
            sim = float(cosine_similarity(query, vec))
            scores.append((sim, self.metadata[i]))
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:k]


# ══════════════════════════════════════════════════════════════
# TOY DATASET — 8 documents in 3D space, 3 clusters
# ══════════════════════════════════════════════════════════════
# Cluster 1: "cats" — vectors pointing roughly toward [1, 0, 0]
# Cluster 2: "dogs" — vectors pointing roughly toward [0, 1, 0]
# Cluster 3: "cars" — vectors pointing roughly toward [0, 0, 1]
#
# This makes it easy to verify: a "cat" query should return cat docs.

docs = [
    # cats (x-axis dominant)
    ([0.9, 0.1, 0.0], "cat sits on mat"),
    ([0.8, 0.2, 0.1], "kitten plays with yarn"),
    ([0.85, 0.1, 0.05], "cats are fluffy"),
    # dogs (y-axis dominant)
    ([0.1, 0.9, 0.0], "dog fetches ball"),
    ([0.2, 0.8, 0.1], "puppy loves walks"),
    ([0.1, 0.85, 0.05], "dogs are loyal"),
    # cars (z-axis dominant)
    ([0.0, 0.1, 0.9], "car drives fast"),
    ([0.1, 0.0, 0.8], "engine needs repair"),
]

# Build index
index = VectorIndex(dim=3)
for vec, text in docs:
    index.add(vec, text)

print("\n=== Brute force: cat query ===")
print(index.search([0.9, 0.1, 0.0], k=3))
print("\n=== Brute force: dog query ===")
print(index.search([0.1, 0.9, 0.0], k=3))


# random_vectors = ([[1, "shit"], [2, "bad"], [15, "vogel"], [7, "tiger"]])
# random_vectors.sort(key=lambda x: x[0], reverse=True)


class VectorIndexLSH:
    def __init__(self, dim, n_planes=4):
        # Random hyperplanes

        self.planes = np.random.randn(n_planes, dim)
        self.buckets = {}  # hash → list of (vector, metadata)

    def _hash(self, vector):
        projections = self.planes @ vector
        bits = tuple((projections > 0).astype(int))
        return bits

    def add(self, vector, meta):
        hashed_vector = self._hash(vector)
        if hashed_vector not in self.buckets:
            self.buckets[hashed_vector] = []

        self.buckets[hashed_vector].append((vector, meta))

    def search(self, query, k=3):
        h = self._hash(query)
        candidates = self.buckets.get(h, [])

        scores = []
        for vec, meta in candidates:
            score = float(cosine_similarity(query, vec))
            scores.append((score, meta))
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:k]


np.random.seed(42)
indexLSH = VectorIndexLSH(dim=3)
for vec, text in docs:
    indexLSH.add(vec, text)

print("\n=== LSH: cat query ===")
print(indexLSH.search([0.9, 0.1, 0.0], k=3))
print("\n=== LSH: dog query ===")
print(indexLSH.search([0.1, 0.9, 0.0], k=3))
