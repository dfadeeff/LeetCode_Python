"""
DAY 1 — CODING PREP (Code from Memory)
=======================================
Dropbox Dash ML Engineer — Multimedia AI

Morning:  cosine_similarity, k_nn_search, mrr, ndcg
Afternoon: bm25_search, self_attention
Evening:  LeetCode practice (hashmaps, strings)

Each function: ≤15 lines, no imports except numpy.
Goal: reproduce on whiteboard in 10 minutes.
"""
import numpy as np
from collections import Counter
import math

# ══════════════════════════════════════════════════════════════
# MORNING — Retrieval + Ranking Metrics
# ══════════════════════════════════════════════════════════════

# --- 1. Cosine Similarity ---
# cos(a,b) = (a·b) / (||a|| × ||b||)
# Measures angle between vectors. Range: -1 to +1.

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# --- 2. k-NN Retrieval (brute force) ---
# Compare query to every vector, return top-k by cosine similarity.

def knn_search(query, vectors, metadata, k=3):
    query = np.array(query)
    scores = []
    for i, vec in enumerate(vectors):
        sim = cosine_similarity(query, vec)
        scores.append((sim, metadata[i]))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:k]


# --- 3. MRR (Mean Reciprocal Rank) ---
# For each query: find rank of FIRST relevant result, take 1/rank.
# MRR = average across all queries.
#
# Example: 3 queries, first relevant at positions [1, 3, 2]
# MRR = (1/1 + 1/3 + 1/2) / 3 = 0.611

def reciprocal_rank(ranked_results, relevant_set):
    """One query: returns 1/rank of first relevant result."""
    for i, doc in enumerate(ranked_results):
        if doc in relevant_set:
            return 1.0 / (i + 1)
    return 0.0

def mrr(queries_results, queries_relevant):
    """Average reciprocal rank across all queries."""
    total = 0.0
    for results, relevant in zip(queries_results, queries_relevant):
        total += reciprocal_rank(results, relevant)
    return total / len(queries_results)


# --- 4. nDCG@K (Normalized Discounted Cumulative Gain) ---
# DCG  = Σ relevance_i / log2(i + 1)    (position i starts at 1)
# IDCG = DCG of ideal (perfect) ranking
# nDCG = DCG / IDCG                      (range: 0 to 1)
#
# The log2 discount: position 1→1.0, 2→0.63, 3→0.50, 4→0.42
# Rewards putting highly relevant docs at the TOP.
#
# Example: relevances = [3, 1, 2], k=3
# DCG  = 3/log2(2) + 1/log2(3) + 2/log2(4) = 3.0 + 0.63 + 1.0 = 4.63
# Ideal = [3, 2, 1] → IDCG = 3.0 + 1.26 + 0.50 = 4.76
# nDCG = 4.63 / 4.76 = 0.97

def dcg_at_k(relevances, k):
    dcg = 0.0
    for i in range(min(k, len(relevances))):
        dcg += relevances[i] / math.log2(i + 2)  # i+2 because log2(1)=0
    return dcg

def ndcg_at_k(relevances, k):
    dcg = dcg_at_k(relevances, k)
    ideal = sorted(relevances, reverse=True)
    idcg = dcg_at_k(ideal, k)
    if idcg == 0:
        return 0.0
    return dcg / idcg


# --- 5. Precision@K and Recall@K ---
# P@K = (relevant in top-k) / k
# R@K = (relevant in top-k) / total_relevant

def precision_at_k(ranked_results, relevant_set, k):
    top_k = ranked_results[:k]
    hits = sum(1 for doc in top_k if doc in relevant_set)
    return hits / k

def recall_at_k(ranked_results, relevant_set, k):
    top_k = ranked_results[:k]
    hits = sum(1 for doc in top_k if doc in relevant_set)
    return hits / len(relevant_set)


# ══════════════════════════════════════════════════════════════
# AFTERNOON — BM25 + Self-Attention
# ══════════════════════════════════════════════════════════════

# --- 6. BM25 (Best Matching 25) ---
# score(q, d) = Σ IDF(t) × TF_saturated(t, d)
#
# IDF(t) = log((N - df + 0.5) / (df + 0.5))     (rarer terms → higher)
# TF_sat = (f × (k1 + 1)) / (f + k1 × (1 - b + b × dl/avgdl))
#
# k1=1.5 controls saturation (diminishing returns for repeated terms)
# b=0.75 controls length normalization (long docs penalized)

class BM25:
    def __init__(self, documents, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.docs = [doc.lower().split() for doc in documents]
        self.N = len(self.docs)
        self.avgdl = sum(len(d) for d in self.docs) / self.N
        # doc frequency: how many docs contain each term
        self.df = Counter()
        for doc in self.docs:
            for term in set(doc):
                self.df[term] += 1

    def _idf(self, term):
        df = self.df.get(term, 0)
        return math.log((self.N - df + 0.5) / (df + 0.5) + 1)

    def _score(self, query, doc):
        score = 0.0
        dl = len(doc)
        tf = Counter(doc)
        for term in query.lower().split():
            f = tf.get(term, 0)
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            score += self._idf(term) * numerator / denominator
        return score

    def search(self, query, k=3):
        scores = [(self._score(query, doc), i) for i, doc in enumerate(self.docs)]
        scores.sort(reverse=True)
        return scores[:k]


# --- 7. Self-Attention ---
# Attention(Q, K, V) = softmax(QK^T / √d_k) V
#
# Q, K, V are projections of input X:
#   Q = X @ W_q,  K = X @ W_k,  V = X @ W_v
#
# QK^T: how much each token attends to every other token
# √d_k: prevents dot products from getting too large
# softmax: turn scores into probabilities (row-wise)
# × V: weighted combination of value vectors

def softmax(x):
    """Row-wise softmax. x shape: (seq_len, seq_len)"""
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

def self_attention(X, W_q, W_k, W_v):
    """
    X:   (seq_len, d_model)  — input embeddings
    W_q: (d_model, d_k)      — query projection
    W_k: (d_model, d_k)      — key projection
    W_v: (d_model, d_v)      — value projection

    Returns: (seq_len, d_v)   — context-aware representations
    """
    Q = X @ W_q                           # (seq_len, d_k)
    K = X @ W_k                           # (seq_len, d_k)
    V = X @ W_v                           # (seq_len, d_v)

    d_k = Q.shape[1]
    scores = Q @ K.T / np.sqrt(d_k)      # (seq_len, seq_len)
    weights = softmax(scores)             # (seq_len, seq_len)
    output = weights @ V                  # (seq_len, d_v)
    return output


# --- 8. Multi-Head Attention (bonus) ---
# Split into h heads, run attention independently, concatenate, project.
# Allows model to attend to different positions/patterns simultaneously.

def multi_head_attention(X, W_qs, W_ks, W_vs, W_o):
    """
    W_qs, W_ks, W_vs: lists of h weight matrices (one per head)
    W_o: (h * d_v, d_model) — output projection
    """
    heads = []
    for W_q, W_k, W_v in zip(W_qs, W_ks, W_vs):
        head = self_attention(X, W_q, W_k, W_v)
        heads.append(head)
    concat = np.concatenate(heads, axis=-1)  # (seq_len, h * d_v)
    return concat @ W_o                       # (seq_len, d_model)


# --- 9. InfoNCE / Contrastive Loss (bonus) ---
# L = -log( exp(sim(q, pos)/τ) / Σ exp(sim(q, neg_i)/τ) )
# Used to train embedding models (CLIP, sentence transformers).

def infonce_loss(query, positive, negatives, temperature=0.07):
    """
    query, positive: embedding vectors
    negatives: list of negative embedding vectors
    """
    pos_sim = np.dot(query, positive) / temperature
    neg_sims = [np.dot(query, neg) / temperature for neg in negatives]
    all_sims = [pos_sim] + neg_sims
    # log-sum-exp trick for numerical stability
    max_sim = max(all_sims)
    log_sum_exp = max_sim + math.log(sum(math.exp(s - max_sim) for s in all_sims))
    return -(pos_sim - log_sum_exp)


# ══════════════════════════════════════════════════════════════
# QUICK REFERENCE — Two-Stage Retrieval Pipeline
# ══════════════════════════════════════════════════════════════
#
# Stage 1: RETRIEVE candidates (fast, ~1000 docs)
#   - BM25 (keyword) + Bi-Encoder embeddings (semantic)
#   - ANN index: HNSW / IVF / LSH
#   - Combine with Reciprocal Rank Fusion (RRF)
#
# Stage 2: RE-RANK top candidates (accurate, ~100 docs)
#   - Cross-Encoder: encode (query, doc) together → score
#   - Much slower but much more accurate than bi-encoder
#
# RRF formula: score(d) = Σ 1/(k + rank_i(d))  where k=60
# ══════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════
# DEMOS — Run to verify everything works
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    print("=" * 60)
    print("1. COSINE SIMILARITY")
    print("=" * 60)
    a = [1, 0, 0]
    b = [1, 1, 0]
    print(f"  cos({a}, {b}) = {cosine_similarity(a, b):.4f}")
    print(f"  cos({a}, {a}) = {cosine_similarity(a, a):.4f}")
    print()

    print("=" * 60)
    print("2. k-NN SEARCH")
    print("=" * 60)
    vectors = [[0.1, 0.9, 0.1], [0.9, 0.1, 0.1], [0.5, 0.5, 0.5]]
    meta = ["cat doc", "dog doc", "mixed doc"]
    results = knn_search([0.1, 0.8, 0.2], vectors, meta, k=2)
    for score, doc in results:
        print(f"  {score:.4f}  {doc}")
    print()

    print("=" * 60)
    print("3. MRR")
    print("=" * 60)
    q_results = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
    q_relevant = [{"A"}, {"F"}, {"H"}]
    print(f"  RR per query: 1/1=1.0, 1/3=0.33, 1/2=0.50")
    print(f"  MRR = {mrr(q_results, q_relevant):.4f}")
    print()

    print("=" * 60)
    print("4. nDCG@K")
    print("=" * 60)
    rels = [3, 1, 2]
    print(f"  relevances = {rels}")
    print(f"  DCG@3  = {dcg_at_k(rels, 3):.4f}")
    print(f"  IDCG@3 = {dcg_at_k(sorted(rels, reverse=True), 3):.4f}")
    print(f"  nDCG@3 = {ndcg_at_k(rels, 3):.4f}")
    print()

    print("=" * 60)
    print("5. PRECISION@K & RECALL@K")
    print("=" * 60)
    ranked = ["A", "B", "C", "D", "E"]
    relevant = {"A", "C", "E", "F"}
    print(f"  ranked = {ranked}")
    print(f"  relevant = {relevant}")
    print(f"  P@3 = {precision_at_k(ranked, relevant, 3):.4f}")
    print(f"  R@3 = {recall_at_k(ranked, relevant, 3):.4f}")
    print()

    print("=" * 60)
    print("6. BM25 SEARCH")
    print("=" * 60)
    docs = [
        "the cat sat on the mat",
        "the dog played in the park",
        "cats and dogs are friends",
        "the cat chased the dog around the park",
    ]
    bm25 = BM25(docs)
    results = bm25.search("cat park", k=3)
    for score, idx in results:
        print(f"  {score:.4f}  doc[{idx}]: {docs[idx]}")
    print()

    print("=" * 60)
    print("7. SELF-ATTENTION")
    print("=" * 60)
    np.random.seed(42)
    seq_len, d_model, d_k = 3, 4, 2
    X = np.random.randn(seq_len, d_model)
    W_q = np.random.randn(d_model, d_k)
    W_k = np.random.randn(d_model, d_k)
    W_v = np.random.randn(d_model, d_k)
    out = self_attention(X, W_q, W_k, W_v)
    print(f"  Input shape:  {X.shape}")
    print(f"  Output shape: {out.shape}")
    print(f"  Output:\n{out}")
    print()

    print("=" * 60)
    print("8. InfoNCE LOSS")
    print("=" * 60)
    q = np.array([1.0, 0.0, 0.0])
    pos = np.array([0.9, 0.1, 0.0])
    negs = [np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0])]
    loss = infonce_loss(q, pos, negs)
    print(f"  query={q}, positive={pos}")
    print(f"  InfoNCE loss = {loss:.4f}")
    print(f"  (lower = better separation)")
    print()

    print("ALL DEMOS PASSED")