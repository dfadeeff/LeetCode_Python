"""
VECTOR RETRIEVAL / SEMANTIC SEARCH — from scratch.

Traditional search: match KEYWORDS ("python tutorial" → docs containing those words).
Semantic search: match MEANING ("python tutorial" → docs about learning Python,
  even if they don't contain the exact words).

HOW IT WORKS:
  1. EMBED: convert text/images to dense vectors (embeddings)
  2. INDEX: store all embeddings in a database
  3. QUERY: embed the query → find nearest embeddings → return those docs

THE KEY: similar meaning → similar vectors → close in vector space.

  "I love dogs"  → [0.8, 0.2, 0.9]
  "I adore puppies" → [0.7, 0.3, 0.85]   ← CLOSE (similar meaning)
  "The stock market" → [-0.5, 0.9, -0.1]  ← FAR (different meaning)
"""
import numpy as np

np.random.seed(42)


# ================================================================
# SIMILARITY FUNCTIONS
# ================================================================
print("=" * 60)
print("STEP 1: SIMILARITY FUNCTIONS — how to compare vectors")
print("=" * 60)


def cosine_similarity(a, b):
    """
    cos(a, b) = (a · b) / (||a|| × ||b||)

    Measures ANGLE between vectors (ignores magnitude).
    Range: -1 (opposite) to +1 (identical direction).
    """
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot / (norm_a * norm_b)


def dot_product_similarity(a, b):
    """
    a · b = Σ aᵢbᵢ

    Measures alignment. Affected by magnitude (longer vectors score higher).
    Used when magnitude carries information (e.g., popularity).
    """
    return np.dot(a, b)


def euclidean_distance(a, b):
    """
    ||a - b|| = √(Σ (aᵢ - bᵢ)²)

    Measures DISTANCE (lower = more similar).
    Affected by magnitude.
    """
    return np.linalg.norm(a - b)


# Demo
a = np.array([0.8, 0.2, 0.9])
b = np.array([0.7, 0.3, 0.85])
c = np.array([-0.5, 0.9, -0.1])

print(f"""
  Three vectors:
    a = "I love dogs"      = {a.tolist()}
    b = "I adore puppies"  = {b.tolist()}
    c = "The stock market"  = {c.tolist()}

  Cosine similarity (most common for text):
    cos(a, b) = {cosine_similarity(a, b):.4f}   ← similar meaning, high score
    cos(a, c) = {cosine_similarity(a, c):.4f}  ← different meaning, low score

  Dot product:
    a · b = {dot_product_similarity(a, b):.4f}
    a · c = {dot_product_similarity(a, c):.4f}

  Euclidean distance (lower = more similar):
    ||a - b|| = {euclidean_distance(a, b):.4f}   ← close
    ||a - c|| = {euclidean_distance(a, c):.4f}   ← far

  WHEN TO USE WHICH:
    Cosine:    text search (meaning matters, not length)
    Dot product: when vectors are normalized, or magnitude matters
    Euclidean: when absolute position in space matters
""")


# ================================================================
# STEP 2: BUILD A SIMPLE VECTOR INDEX
# ================================================================
print("=" * 60)
print("STEP 2: VECTOR INDEX — store and search embeddings")
print("=" * 60)


class VectorIndex:
    """
    Simplest vector database: brute-force search.
    Store embeddings, find k nearest neighbors.
    """

    def __init__(self, dim):
        self.dim = dim
        self.vectors = []   # list of numpy arrays
        self.metadata = []  # list of dicts (doc text, id, etc.)

    def add(self, vector, meta):
        """Add a vector with metadata."""
        self.vectors.append(vector)
        self.metadata.append(meta)


    def search(self, query, k=3, metric="cosine"):
        """
        Find k most similar vectors to query.
        Returns: list of (score, metadata)
        """
        scores = []
        for i, vec in enumerate(self.vectors):
            if metric == "cosine":
                score = cosine_similarity(query, vec)
            elif metric == "dot":
                score = dot_product_similarity(query, vec)
            elif metric == "euclidean":
                score = -euclidean_distance(query, vec)  # negate so higher = better
            scores.append((score, i))

        # Sort by score descending
        scores.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, idx in scores[:k]:
            results.append((score, self.metadata[idx]))
        return results


# ── Simulate document embeddings (in practice, these come from a model) ──
# Pretend we have a simple embedding function
documents = [
    "Python programming tutorial for beginners",
    "Advanced machine learning with Python",
    "Cooking Italian pasta at home",
    "Deep learning and neural networks explained",
    "Best hiking trails in Colorado",
    "Natural language processing with transformers",
    "How to train a dog",
    "Introduction to data science with Python",
    "Mediterranean diet recipes",
    "Vector databases and similarity search",
]

# Fake embeddings: in reality, these come from BERT/OpenAI/etc.
# We'll create embeddings where similar docs have similar vectors
np.random.seed(42)
dim = 8

# Create embeddings with some structure
# Tech/ML docs get similar vectors, food docs similar, outdoor docs similar
embeddings = []
for doc in documents:
    base = np.random.randn(dim) * 0.3
    if "python" in doc.lower() or "learning" in doc.lower() or "data" in doc.lower():
        base += np.array([1, 1, 0, 0, 0, 0, 0, 0]) * 0.5  # tech cluster
    if "neural" in doc.lower() or "transformer" in doc.lower() or "vector" in doc.lower():
        base += np.array([1, 1, 0.5, 0.5, 0, 0, 0, 0]) * 0.5  # ML cluster
    if "cook" in doc.lower() or "recipe" in doc.lower() or "pasta" in doc.lower():
        base += np.array([0, 0, 0, 0, 1, 1, 0, 0]) * 0.5  # food cluster
    if "hik" in doc.lower() or "trail" in doc.lower() or "dog" in doc.lower():
        base += np.array([0, 0, 0, 0, 0, 0, 1, 1]) * 0.5  # outdoor cluster
    embeddings.append(base / np.linalg.norm(base))  # normalize

# Build index
index = VectorIndex(dim=dim)
for doc, emb in zip(documents, embeddings):
    index.add(emb, {"text": doc})

print(f"\n  Indexed {len(documents)} documents, each with {dim}D embedding\n")

# Search
queries = [
    ("Learn Python basics", np.array([1, 1, 0, 0, 0, 0, 0, 0], dtype=float)),
    ("Deep learning tutorial", np.array([1, 1, 0.5, 0.5, 0, 0, 0, 0], dtype=float)),
    ("Food recipes", np.array([0, 0, 0, 0, 1, 1, 0, 0], dtype=float)),
]

for query_text, query_vec in queries:
    query_vec = query_vec / np.linalg.norm(query_vec)
    results = index.search(query_vec, k=3, metric="cosine")

    print(f"  Query: \"{query_text}\"")
    for rank, (score, meta) in enumerate(results, 1):
        print(f"    {rank}. [{score:.4f}] {meta['text']}")
    print()


# ================================================================
# STEP 3: APPROXIMATE NEAREST NEIGHBORS (ANN)
# ================================================================
print("=" * 60)
print("STEP 3: ANN — scaling to millions of vectors")
print("=" * 60)

print("""
  Brute-force search: compare query to ALL vectors → O(n × d)
  With 100M documents, this is WAY too slow.

  Solution: Approximate Nearest Neighbors (ANN)
  Trade a tiny bit of accuracy for massive speed gains.

  THREE MAIN APPROACHES:

  1. LSH (Locality-Sensitive Hashing):
     ─────────────────────────────────
     Hash similar vectors to the same bucket.
     Only search within the bucket → much faster.

     How: random hyperplanes split space into regions.
     Similar vectors → same side of hyperplanes → same hash.
""")


class SimpleLSH:
    """
    Locality-Sensitive Hashing with random hyperplanes.
    Each hyperplane splits space in two → binary hash code.
    """

    def __init__(self, dim, n_planes=4):
        # Random hyperplanes
        self.planes = np.random.randn(n_planes, dim)
        self.buckets = {}  # hash → list of (vector, metadata)

    def _hash(self, vector):
        """Project onto hyperplanes, sign → binary hash."""
        projections = self.planes @ vector
        bits = tuple((projections > 0).astype(int))
        return bits

    def add(self, vector, meta):
        h = self._hash(vector)
        if h not in self.buckets:
            self.buckets[h] = []
        self.buckets[h].append((vector, meta))

    def search(self, query, k=3):
        h = self._hash(query)
        candidates = self.buckets.get(h, [])

        # Search only within the bucket
        scores = []
        for vec, meta in candidates:
            score = cosine_similarity(query, vec)
            scores.append((score, meta))

        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:k]


# Demo LSH
lsh = SimpleLSH(dim=dim, n_planes=3)
for doc, emb in zip(documents, embeddings):
    lsh.add(emb, {"text": doc})

print(f"  LSH with 3 hyperplanes → {2**3} possible buckets")
print(f"  Buckets used: {len(lsh.buckets)}")
for h, items in lsh.buckets.items():
    docs_in_bucket = [item[1]['text'][:30] for item in items]
    print(f"    Hash {h}: {docs_in_bucket}")

query_vec = np.array([1, 1, 0.5, 0.5, 0, 0, 0, 0], dtype=float)
query_vec = query_vec / np.linalg.norm(query_vec)
results = lsh.search(query_vec, k=3)
print(f"\n  LSH search for 'deep learning':")
print(f"  Only searched {len(lsh.buckets.get(lsh._hash(query_vec), []))} "
      f"vectors instead of {len(documents)}!")
for score, meta in results:
    print(f"    [{score:.4f}] {meta['text']}")

class SimpleIVF:
    """
    Inverted File Index: K-Means clustering for ANN search.
    Assign vectors to clusters. At query time, only search nearest cluster(s).
    """

    def __init__(self, dim, n_clusters=3, nprobe=1):
        self.dim = dim
        self.n_clusters = n_clusters
        self.nprobe = nprobe          # how many clusters to search
        self.centroids = None
        self.clusters = {}            # cluster_id → list of (vector, metadata)

    def _kmeans(self, vectors, n_iter=20):
        """Simple K-Means to find cluster centroids."""
        n = len(vectors)
        # Random init: pick n_clusters random vectors as centroids
        idx = np.random.choice(n, self.n_clusters, replace=False)
        self.centroids = np.array([vectors[i] for i in idx])

        for _ in range(n_iter):
            # Assign each vector to nearest centroid
            assignments = []
            for v in vectors:
                dists = [np.linalg.norm(v - c) for c in self.centroids]
                assignments.append(np.argmin(dists))

            # Update centroids
            for c in range(self.n_clusters):
                members = [vectors[i] for i in range(n) if assignments[i] == c]
                if members:
                    self.centroids[c] = np.mean(members, axis=0)

    def build(self, vectors, metadata):
        """Build index: run K-Means, assign all vectors to clusters."""
        self._kmeans(vectors)

        # Assign each vector to its nearest centroid
        for vec, meta in zip(vectors, metadata):
            dists = [np.linalg.norm(vec - c) for c in self.centroids]
            cluster_id = np.argmin(dists)
            if cluster_id not in self.clusters:
                self.clusters[cluster_id] = []
            self.clusters[cluster_id].append((vec, meta))

    def search(self, query, k=3):
        """
        1. Find nearest nprobe centroids
        2. Search only those clusters
        """
        # Find nearest centroids
        centroid_dists = [(np.linalg.norm(query - c), i)
                         for i, c in enumerate(self.centroids)]
        centroid_dists.sort()
        probe_ids = [idx for _, idx in centroid_dists[:self.nprobe]]

        # Search only those clusters
        scores = []
        n_searched = 0
        for cid in probe_ids:
            for vec, meta in self.clusters.get(cid, []):
                score = cosine_similarity(query, vec)
                scores.append((score, meta))
                n_searched += 1

        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:k], n_searched


# Demo IVF
print(f"\n  --- IVF (Inverted File Index) ---\n")
ivf = SimpleIVF(dim=dim, n_clusters=3, nprobe=1)
ivf.build(embeddings, [{"text": doc} for doc in documents])

print(f"  IVF with {ivf.n_clusters} clusters:")
for cid, items in ivf.clusters.items():
    docs_in_cluster = [item[1]['text'][:35] for item in items]
    print(f"    Cluster {cid}: {docs_in_cluster}")

query_vec = np.array([1, 1, 0.5, 0.5, 0, 0, 0, 0], dtype=float)
query_vec = query_vec / np.linalg.norm(query_vec)
results_ivf, n_searched = ivf.search(query_vec, k=3)
print(f"\n  IVF search for 'deep learning' (nprobe=1):")
print(f"  Searched {n_searched} vectors instead of {len(documents)}!")
for score, meta in results_ivf:
    print(f"    [{score:.4f}] {meta['text']}")

# Show nprobe effect
ivf_wide = SimpleIVF(dim=dim, n_clusters=3, nprobe=2)
ivf_wide.build(embeddings, [{"text": doc} for doc in documents])
results_wide, n_searched_wide = ivf_wide.search(query_vec, k=3)
print(f"\n  IVF search with nprobe=2:")
print(f"  Searched {n_searched_wide} vectors (more recall, slower)")
for score, meta in results_wide:
    print(f"    [{score:.4f}] {meta['text']}")


class SimpleHNSW:
    """
    Simplified HNSW: single-layer navigable small world graph.
    Each node connects to its M nearest neighbors.
    Search by greedy walk: always move to the neighbor closest to query.
    """

    def __init__(self, dim, M=3, ef_search=10):
        """
        M: max connections per node (more = better recall, more memory)
        ef_search: how many candidates to track during search (more = better recall)
        """
        self.dim = dim
        self.M = M
        self.ef_search = ef_search
        self.vectors = []
        self.metadata = []
        self.graph = {}  # node_id → list of neighbor_ids

    def build(self, vectors, metadata):
        """Build graph: connect each vector to its M nearest neighbors."""
        self.vectors = vectors
        self.metadata = metadata
        n = len(vectors)

        # For each vector, find M nearest neighbors and connect
        for i in range(n):
            dists = []
            for j in range(n):
                if i == j:
                    continue
                d = np.linalg.norm(vectors[i] - vectors[j])
                dists.append((d, j))
            dists.sort()

            # Connect to M nearest
            neighbors = [j for _, j in dists[:self.M]]
            self.graph[i] = neighbors

            # Make connections bidirectional
            for j in neighbors:
                if j not in self.graph:
                    self.graph[j] = []
                if i not in self.graph[j]:
                    self.graph[j].append(i)

    def search(self, query, k=3):
        """
        Greedy search: start at random node, always move to
        the neighbor closest to query. Track best candidates.
        """
        n = len(self.vectors)
        if n == 0:
            return [], 0

        # Start at a random entry point
        current = np.random.randint(n)
        visited = set()
        visited.add(current)

        # Track top candidates (score, node_id)
        best = [(cosine_similarity(query, self.vectors[current]), current)]
        n_searched = 1

        # Greedy walk: keep exploring neighbors
        improved = True
        while improved:
            improved = False
            # Check all neighbors of current best candidates
            candidates_to_check = []
            for _, node_id in best:
                for neighbor in self.graph.get(node_id, []):
                    if neighbor not in visited:
                        candidates_to_check.append(neighbor)
                        visited.add(neighbor)

            for neighbor in candidates_to_check:
                score = cosine_similarity(query, self.vectors[neighbor])
                n_searched += 1
                best.append((score, neighbor))
                improved = True

            # Keep only top ef_search candidates
            best.sort(key=lambda x: x[0], reverse=True)
            best = best[:self.ef_search]

        # Return top-k
        results = [(score, self.metadata[idx]) for score, idx in best[:k]]
        return results, n_searched


# Demo HNSW
print(f"\n  --- HNSW (Hierarchical Navigable Small World) ---\n")
hnsw = SimpleHNSW(dim=dim, M=3, ef_search=5)
hnsw.build(embeddings, [{"text": doc} for doc in documents])

print(f"  HNSW graph (each node → its {hnsw.M} nearest neighbors):")
for node_id, neighbors in sorted(hnsw.graph.items()):
    doc_name = documents[node_id][:30]
    neighbor_names = [documents[n][:20] for n in neighbors]
    print(f"    {node_id} ({doc_name}) → {neighbor_names}")

query_vec = np.array([1, 1, 0.5, 0.5, 0, 0, 0, 0], dtype=float)
query_vec = query_vec / np.linalg.norm(query_vec)
results_hnsw, n_searched_hnsw = hnsw.search(query_vec, k=3)
print(f"\n  HNSW search for 'deep learning':")
print(f"  Visited {n_searched_hnsw} nodes (graph walk, not brute force):")
for score, meta in results_hnsw:
    print(f"    [{score:.4f}] {meta['text']}")


print(f"""
  ┌──────────────────┬──────────┬────────────┬───────────────────┐
  │ Method           │ Build    │ Search     │ Recall             │
  ├──────────────────┼──────────┼────────────┼───────────────────┤
  │ Brute force      │ O(1)     │ O(n·d)     │ 100% (exact)       │
  │ LSH              │ O(n)     │ O(n/buckets│ ~90-95%            │
  │ IVF (FAISS)      │ O(n·k)   │ O(n/k · d) │ ~95-99%            │
  │ HNSW             │ O(n·logn)│ O(log n)   │ ~95-99%            │
  └──────────────────┴──────────┴────────────┴───────────────────┘
""")


# ================================================================
# BM25 — keyword search (Best Matching 25)
# ================================================================
print("=" * 60)
print("BM25 — keyword matching (the other half of hybrid search)")
print("=" * 60)

print("""
  Embedding search finds MEANING: "python tutorial" → "learn programming"
  BM25 finds exact KEYWORDS:      "python tutorial" → docs with those exact words

  Both miss things the other catches. That's why production uses BOTH.

  BM25 score = Σ IDF(word) × saturated_TF(word, doc)
               for each word in query
""")


class BM25:
    """
    BM25 keyword search from scratch.
    k1: TF saturation (1.2 = default, higher = less saturation)
    b:  length normalization (0.75 = default, 0 = ignore length, 1 = full penalty)
    """

    def __init__(self, k1=1.2, b=0.75):
        self.k1 = k1
        self.b = b
        self.docs = []           # list of word lists
        self.doc_metadata = []
        self.N = 0               # total docs
        self.avgdl = 0           # average doc length
        self.df = {}             # word → how many docs contain it

    def add(self, text, metadata):
        """Add a document. Tokenize by splitting on spaces."""
        words = text.lower().split()
        self.docs.append(words)
        self.doc_metadata.append(metadata)
        self.N += 1

        # Update document frequency
        for word in set(words):  # set() = count each word once per doc
            self.df[word] = self.df.get(word, 0) + 1

        # Update average doc length
        total_words = sum(len(d) for d in self.docs)
        self.avgdl = total_words / self.N

    def _idf(self, word):
        """
        IDF = log((N - n + 0.5) / (n + 0.5))
        n = docs containing this word
        Rare words → high IDF, common words → low IDF
        """
        n = self.df.get(word, 0)
        return max(0, np.log((self.N - n + 0.5) / (n + 0.5)))

    def _tf_saturated(self, word, doc_words):
        """
        Saturated TF = tf × (k1 + 1) / (tf + k1 × (1 - b + b × dl/avgdl))

        tf=1 → ~1.2,  tf=10 → ~2.0,  tf=100 → ~2.2  (saturates!)
        Long docs are penalized (dl/avgdl > 1 → higher denominator)
        """
        tf = doc_words.count(word)
        if tf == 0:
            return 0
        dl = len(doc_words)
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
        return numerator / denominator

    def score(self, query, doc_idx):
        """BM25 score for one (query, doc) pair."""
        query_words = query.lower().split()
        doc_words = self.docs[doc_idx]

        total = 0
        for word in query_words:
            idf = self._idf(word)
            tf_sat = self._tf_saturated(word, doc_words)
            total += idf * tf_sat
        return total

    def search(self, query, k=3, verbose=False):
        """Score all docs, return top-k."""
        scores = []
        for i in range(self.N):
            s = self.score(query, i)
            scores.append((s, i))

        scores.sort(key=lambda x: x[0], reverse=True)

        if verbose:
            query_words = query.lower().split()
            print(f"\n  Query: '{query}'")
            print(f"  Query words: {query_words}")
            print(f"  avgdl = {self.avgdl:.1f} words\n")
            for word in query_words:
                n = self.df.get(word, 0)
                idf = self._idf(word)
                print(f"    '{word}': in {n}/{self.N} docs → IDF = {idf:.3f}")
            print()

        results = []
        for s, idx in scores[:k]:
            results.append((s, self.doc_metadata[idx]))
        return results


# Demo
bm25 = BM25(k1=1.2, b=0.75)

bm25_docs = [
    "python programming tutorial for beginners",
    "advanced machine learning with python",
    "cooking italian pasta at home",
    "deep learning and neural networks explained",
    "best hiking trails in colorado",
    "natural language processing with transformers",
    "how to train a dog",
    "introduction to data science with python",
    "mediterranean diet recipes",
    "vector databases and similarity search",
]

for doc_text in bm25_docs:
    bm25.add(doc_text, {"text": doc_text})

# Search with step-by-step
results_bm25 = bm25.search("python tutorial", k=5, verbose=True)

print(f"  BM25 results for 'python tutorial':")
for rank, (score, meta) in enumerate(results_bm25, 1):
    print(f"    {rank}. [{score:.4f}] {meta['text']}")

# Show saturation effect
print(f"\n  --- TF Saturation demo ---")
print(f"  How score changes as word appears more times:\n")
print(f"  {'tf':<5} {'TF_saturated':<15} {'vs linear tf':<15}")
print(f"  {'─' * 35}")
test_bm25 = BM25(k1=1.2, b=0.75)
for tf_count in [1, 2, 5, 10, 50, 100]:
    fake_doc = ["python"] * tf_count + ["other"] * 50
    test_bm25.docs = [fake_doc]
    test_bm25.N = 1
    test_bm25.avgdl = len(fake_doc)
    sat = test_bm25._tf_saturated("python", fake_doc)
    print(f"  {tf_count:<5} {sat:<15.3f} {tf_count:<15}")

print(f"""
  See? tf=1 → 1.1, tf=100 → 2.0. BM25 flattens out.
  TF-IDF would give tf=100 → 100. Way too much credit.
""")

# Hybrid search demo
print("─" * 60)
print("HYBRID SEARCH — BM25 + Embeddings combined")
print("─" * 60)

print(f"\n  Query: 'python tutorial'\n")

# BM25 ranking
bm25_results = bm25.search("python tutorial", k=5)
print(f"  BM25 ranking (keyword match):")
for rank, (score, meta) in enumerate(bm25_results, 1):
    print(f"    {rank}. {meta['text']}")

# Embedding ranking (reuse existing index)
emb_query = np.array([1, 1, 0, 0, 0, 0, 0, 0], dtype=float)
emb_query = emb_query / np.linalg.norm(emb_query)
emb_results = index.search(emb_query, k=5, metric="cosine")
print(f"\n  Embedding ranking (meaning match):")
for rank, (score, meta) in enumerate(emb_results, 1):
    print(f"    {rank}. {meta['text']}")

# Reciprocal Rank Fusion
print(f"\n  Hybrid (Reciprocal Rank Fusion):")
print(f"  RRF score = 1/(k + rank_bm25) + 1/(k + rank_emb), k=60\n")

rrf_k = 60
doc_scores = {}

for rank, (_, meta) in enumerate(bm25_results, 1):
    text = meta['text']
    doc_scores[text] = doc_scores.get(text, 0) + 1.0 / (rrf_k + rank)

for rank, (_, meta) in enumerate(emb_results, 1):
    text = meta['text']
    doc_scores[text] = doc_scores.get(text, 0) + 1.0 / (rrf_k + rank)

hybrid_ranked = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
for rank, (text, score) in enumerate(hybrid_ranked[:5], 1):
    print(f"    {rank}. [{score:.5f}] {text}")

print(f"""
  Hybrid combines both signals:
    - BM25 catches exact keyword "python" and "tutorial"
    - Embeddings catch meaning (e.g. "data science" is related)
    - RRF merges both rankings without needing to normalize scores
""")


# ================================================================
# STEP 4: TWO-STAGE RETRIEVAL (how production systems work)
# ================================================================
print("=" * 60)
print("STEP 4: TWO-STAGE RETRIEVAL — how Dropbox Dash works")
print("=" * 60)

print("""
  Real search systems have TWO stages:

  Stage 1: RETRIEVAL (recall-focused)
  ───────────────────────────────────
    Goal: quickly find ~100 candidates from millions.
    Methods: ANN search, BM25 (keyword), hybrid.
    Speed: must be <10ms.

  Stage 2: RANKING / RE-RANKING (precision-focused)
  ──────────────────────────────────────────────────
    Goal: re-order the ~100 candidates by quality.
    Methods: cross-encoder, LLM re-ranker, learned ranking model.
    Speed: can be slower (~50-100ms), fewer candidates.

  Why two stages?
    - Can't run an expensive model on ALL documents
    - Cheap retrieval narrows the field
    - Expensive ranker picks the best from the shortlist

  ┌─────────────────────────────────────────────────────┐
  │  Query: "how to merge PDFs"                        │
  │                                                     │
  │  Stage 1 (Retrieval):                               │
  │    10M docs → ANN search → top 100 candidates      │
  │    ~5ms, cosine similarity on embeddings            │
  │                                                     │
  │  Stage 2 (Re-ranking):                              │
  │    100 candidates → cross-encoder → top 10          │
  │    ~50ms, compares query+doc jointly for relevance  │
  │                                                     │
  │  Return top 10 to user                              │
  └─────────────────────────────────────────────────────┘
""")


# Simple two-stage demo
def two_stage_search(query_vec, index, documents, embeddings, k_retrieve=5, k_final=3):
    """
    Stage 1: fast vector search (retrieval)
    Stage 2: simple re-ranking (simulate cross-encoder with a score boost)
    """
    # Stage 1: retrieve top-k candidates
    results_stage1 = index.search(query_vec, k=k_retrieve, metric="cosine")

    print(f"  Stage 1 (retrieve top {k_retrieve}):")
    for rank, (score, meta) in enumerate(results_stage1, 1):
        print(f"    {rank}. [{score:.4f}] {meta['text']}")

    # Stage 2: re-rank (simulate a more sophisticated model)
    # In practice: cross-encoder that takes (query, doc) pair
    reranked = []
    for score, meta in results_stage1:
        # Simulate re-ranking: bonus for exact keyword overlap
        doc_lower = meta['text'].lower()
        bonus = 0
        for word in ["python", "learning", "tutorial"]:
            if word in doc_lower:
                bonus += 0.1
        reranked.append((score + bonus, meta))

    reranked.sort(key=lambda x: x[0], reverse=True)

    print(f"\n  Stage 2 (re-rank → top {k_final}):")
    for rank, (score, meta) in enumerate(reranked[:k_final], 1):
        print(f"    {rank}. [{score:.4f}] {meta['text']}")

    return reranked[:k_final]


print(f"\n  Query: \"Python learning tutorial\"\n")
query_vec = np.array([1, 1, 0.2, 0, 0, 0, 0, 0], dtype=float)
query_vec = query_vec / np.linalg.norm(query_vec)
two_stage_search(query_vec, index, documents, embeddings)


# ================================================================
# SUMMARY
# ================================================================
print(f"""
{'=' * 60}
VECTOR RETRIEVAL SUMMARY
{'=' * 60}

  THE PIPELINE:
    1. Embed documents (offline, once)
    2. Build ANN index (offline, once)
    3. Embed query (online, per request)
    4. ANN search → top K candidates (fast, recall-focused)
    5. Re-rank candidates (slower, precision-focused)
    6. Return top results

  SIMILARITY METRICS:
    Cosine:    angle between vectors (most common for text)
    Dot product: when vectors are normalized
    Euclidean: when absolute distance matters

  ANN METHODS:
    LSH:  hash-based, simple, decent recall
    IVF:  cluster-based (FAISS), great for large datasets
    HNSW: graph-based, best recall/speed tradeoff

  VECTOR DATABASES (production):
    FAISS (Meta), Pinecone, Weaviate, Qdrant, Milvus, ChromaDB

  INTERVIEW: "Design a semantic search system"
    → embed docs with BERT/OpenAI → ANN index (HNSW/FAISS)
    → two-stage: retrieve candidates → re-rank with cross-encoder
    → optimize for nDCG, MRR
""")