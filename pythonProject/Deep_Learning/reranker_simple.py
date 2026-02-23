"""
RE-RANKER — from scratch.

You retrieved 100 candidates with ANN search. Now what?
Those 100 are ranked by EMBEDDING SIMILARITY — fast but rough.
A re-ranker looks at each (query, document) pair MORE CAREFULLY
and re-orders them.

TWO TYPES OF ENCODERS:

  BI-ENCODER (Stage 1: Retrieval)
  ──────────────────────────────
  Encode query and document SEPARATELY, then dot product.

    query  → [Encoder] → q_emb ─┐
                                 ├── dot product → score
    doc    → [Encoder] → d_emb ─┘

  Fast: doc embeddings are pre-computed. Only encode query at search time.
  But: query and doc never "see" each other. Shallow matching.

  CROSS-ENCODER (Stage 2: Re-ranking)
  ────────────────────────────────────
  Encode query AND document TOGETHER. Full attention between them.

    [query + doc] → [Encoder] → score

  Slow: must run encoder for EVERY (query, doc) pair.
  But: query and doc interact deeply. Much more accurate.

  WHY THE DIFFERENCE?
    Bi-encoder:    "python tutorial" → vector, "Learn Python" → vector, dot product.
                   They never see each other. Can't understand "tutorial" matches "Learn".

    Cross-encoder: "python tutorial [SEP] Learn Python Basics for Beginners"
                   The model sees BOTH and can figure out "tutorial" = "Learn...for Beginners".
                   Much deeper understanding.
"""
import numpy as np

np.random.seed(42)


# ================================================================
# HELPER FUNCTIONS
# ================================================================
def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))


def softmax(x):
    e = np.exp(x - np.max(x))
    return e / e.sum()


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)


# ================================================================
# BI-ENCODER (what you already know)
# ================================================================
print("=" * 60)
print("BI-ENCODER — encode separately, dot product")
print("=" * 60)


class BiEncoder:
    """
    Encode query and doc separately. Score = cosine similarity.
    This is what you use for RETRIEVAL (Stage 1).
    """

    def __init__(self, vocab_size, embed_dim):
        self.embeddings = np.random.randn(vocab_size, embed_dim) * 0.3
        self.W = np.random.randn(embed_dim, embed_dim) * 0.3

    def encode(self, token_ids):
        """Encode a sequence → single vector (mean pooling)."""
        embs = self.embeddings[token_ids]    # (seq_len, embed_dim)
        pooled = embs.mean(axis=0)           # (embed_dim,) — average all tokens
        projected = pooled @ self.W          # (embed_dim,)
        # Normalize to unit length
        norm = np.linalg.norm(projected)
        if norm > 0:
            projected = projected / norm
        return projected

    def score(self, query_ids, doc_ids):
        """Score = cosine similarity between separate encodings."""
        q_emb = self.encode(query_ids)
        d_emb = self.encode(doc_ids)
        return cosine_similarity(q_emb, d_emb)


# Demo
# Vocab: 0=pad, 1=python, 2=tutorial, 3=learn, 4=basics, 5=java, 6=cooking, 7=advanced
bi = BiEncoder(vocab_size=8, embed_dim=4)

query = [1, 2]          # "python tutorial"
doc_good = [3, 1, 4]    # "learn python basics"
doc_bad = [6, 5]         # "cooking java"

score_good = bi.score(query, doc_good)
score_bad = bi.score(query, doc_bad)

print(f"""
  Query: "python tutorial"    tokens: {query}
  Doc A: "learn python basics" tokens: {doc_good}
  Doc B: "cooking java"       tokens: {doc_bad}

  Bi-encoder scores (before training, random weights):
    Query ↔ Doc A: {score_good:.4f}
    Query ↔ Doc B: {score_bad:.4f}

  How it works:
    1. Encode query   → q_emb = [0.23, -0.15, 0.44, 0.12]
    2. Encode doc     → d_emb = [0.31, -0.08, 0.39, 0.18]
    3. Score = cosine(q_emb, d_emb)

  Key: query and doc are encoded INDEPENDENTLY.
  Doc embeddings can be pre-computed → search is just dot product → fast!
""")


# ================================================================
# CROSS-ENCODER (the re-ranker)
# ================================================================
print("=" * 60)
print("CROSS-ENCODER — encode together, deep interaction")
print("=" * 60)


class CrossEncoder:
    """
    Encode query + doc TOGETHER. Full interaction between them.
    This is what you use for RE-RANKING (Stage 2).

    Input: [query tokens] + [separator] + [doc tokens] → single score
    """

    def __init__(self, vocab_size, embed_dim, hidden_dim):
        self.embeddings = np.random.randn(vocab_size, embed_dim) * 0.3

        # Self-attention (simplified: single head)
        self.W_Q = np.random.randn(embed_dim, embed_dim) * 0.3
        self.W_K = np.random.randn(embed_dim, embed_dim) * 0.3
        self.W_V = np.random.randn(embed_dim, embed_dim) * 0.3

        # Classification head: attention output → single score
        self.W1 = np.random.randn(embed_dim, hidden_dim) * 0.3
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, 1) * 0.3
        self.b2 = np.zeros(1)

    def score(self, query_ids, doc_ids, verbose=False):
        """
        Concatenate query + doc, run through attention, output relevance score.
        """
        # Step 1: Concatenate query + separator(=0) + doc
        combined = query_ids + [0] + doc_ids
        if verbose:
            print(f"    Combined input: {combined}")

        # Step 2: Embed all tokens
        x = self.embeddings[combined]  # (total_len, embed_dim)
        if verbose:
            print(f"    Embedded shape: {x.shape}")

        # Step 3: Self-attention — QUERY AND DOC TOKENS ATTEND TO EACH OTHER
        Q = x @ self.W_Q
        K = x @ self.W_K
        V = x @ self.W_V

        d_k = Q.shape[-1]
        scores = Q @ K.T / np.sqrt(d_k)    # (total_len, total_len)
        weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        weights = weights / weights.sum(axis=-1, keepdims=True)

        attended = weights @ V  # (total_len, embed_dim)

        if verbose:
            print(f"    Attention weights shape: {weights.shape}")
            print(f"    This is where query tokens attend to doc tokens!")
            # Show: does query token 0 attend to doc tokens?
            q_len = len(query_ids)
            d_start = q_len + 1  # after separator
            print(f"    Query token 0 attention to doc tokens: "
                  f"{weights[0, d_start:].round(3).tolist()}")

        # Step 4: Pool (mean of all token representations)
        pooled = attended.mean(axis=0)  # (embed_dim,)

        # Step 5: Classification head → relevance score
        hidden = np.maximum(0, pooled @ self.W1 + self.b1)  # ReLU
        logit = (hidden @ self.W2 + self.b2)[0]
        relevance = sigmoid(logit)

        if verbose:
            print(f"    Relevance score: {relevance:.4f}")

        return relevance


# Demo
cross = CrossEncoder(vocab_size=8, embed_dim=4, hidden_dim=8)

print(f"\n  Query: 'python tutorial' tokens: {query}")
print(f"\n  --- Doc A: 'learn python basics' ---")
score_a = cross.score(query, doc_good, verbose=True)

print(f"\n  --- Doc B: 'cooking java' ---")
score_b = cross.score(query, doc_bad, verbose=True)

print(f"""
  Cross-encoder scores (before training, random):
    Query ↔ Doc A: {score_a:.4f}
    Query ↔ Doc B: {score_b:.4f}

  KEY DIFFERENCE from bi-encoder:
    Bi-encoder:    query and doc encoded SEPARATELY, never interact
    Cross-encoder: query and doc in SAME sequence, attend to EACH OTHER

    The attention layer lets "tutorial" directly look at "learn" and "basics"
    and figure out they match. Bi-encoder can't do this.
""")


# ================================================================
# FULL TWO-STAGE PIPELINE
# ================================================================
print("=" * 60)
print("FULL PIPELINE — bi-encoder retrieve → cross-encoder re-rank")
print("=" * 60)

# Simulate a document collection
documents = {
    0: {"tokens": [3, 1, 4], "text": "learn python basics"},
    1: {"tokens": [5, 2],    "text": "java tutorial"},
    2: {"tokens": [1, 7],    "text": "python advanced"},
    3: {"tokens": [6, 4],    "text": "cooking basics"},
    4: {"tokens": [1, 4, 2], "text": "python basics tutorial"},
}

query_tokens = [1, 2]  # "python tutorial"
print(f"\n  Query: 'python tutorial'")
print(f"  Documents: {[d['text'] for d in documents.values()]}")

# Stage 1: Bi-encoder retrieval (fast — in practice, pre-computed)
print(f"\n  --- Stage 1: Bi-encoder retrieval ---")
bi_scores = []
for doc_id, doc in documents.items():
    score = bi.score(query_tokens, doc["tokens"])
    bi_scores.append((score, doc_id))
    print(f"    Doc {doc_id} ({doc['text']:25}) → bi-encoder: {score:.4f}")

bi_scores.sort(key=lambda x: x[0], reverse=True)
top_3 = bi_scores[:3]
print(f"\n  Top 3 candidates: {[documents[did]['text'] for _, did in top_3]}")

# Stage 2: Cross-encoder re-ranking (slow — only on top candidates)
print(f"\n  --- Stage 2: Cross-encoder re-ranking (only top 3) ---")
cross_scores = []
for bi_score, doc_id in top_3:
    doc = documents[doc_id]
    ce_score = cross.score(query_tokens, doc["tokens"])
    cross_scores.append((ce_score, doc_id))
    print(f"    Doc {doc_id} ({doc['text']:25}) → bi: {bi_score:.4f}  cross: {ce_score:.4f}")

cross_scores.sort(key=lambda x: x[0], reverse=True)
print(f"\n  Final ranking after re-ranking:")
for rank, (score, doc_id) in enumerate(cross_scores, 1):
    print(f"    {rank}. [{score:.4f}] {documents[doc_id]['text']}")

print(f"""
  Notice: the ORDER may change after cross-encoder re-ranking!
  Bi-encoder gives rough ranking, cross-encoder fixes mistakes.
""")


# ================================================================
# TRAINING A CROSS-ENCODER
# ================================================================
print("=" * 60)
print("TRAINING — how cross-encoders learn")
print("=" * 60)

print("""
  Training data: (query, doc, label) triplets

    ("python tutorial", "Learn Python Basics", relevant=1)
    ("python tutorial", "Cooking Recipes",     relevant=0)
    ("ML course",       "Deep Learning Guide", relevant=1)
    ("ML course",       "Car Repair Manual",   relevant=0)

  Loss: binary cross-entropy (same as logistic regression)
    L = -[y·log(score) + (1-y)·log(1-score)]

  Training loop:
    1. Concatenate: [query_tokens, SEP, doc_tokens]
    2. Forward pass through attention + classification head → score
    3. Compute loss against label
    4. Backprop, update weights
    5. Repeat

  Data sources:
    - Click logs: user clicked doc → relevant=1
    - Hard negatives: top results user DIDN'T click → relevant=0
    - Human annotations: gold standard labels
""")

# Simple training demo
print(f"  --- Training demo ---\n")

training_data = [
    ([1, 2], [3, 1, 4], 1),    # "python tutorial" + "learn python basics" = relevant
    ([1, 2], [6, 5], 0),        # "python tutorial" + "cooking java" = not relevant
    ([1, 2], [1, 4, 2], 1),     # "python tutorial" + "python basics tutorial" = relevant
    ([1, 2], [6, 4], 0),        # "python tutorial" + "cooking basics" = not relevant
]

cross_train = CrossEncoder(vocab_size=8, embed_dim=4, hidden_dim=8)

# Train with numerical gradients
eps_num = 1e-5
lr = 0.1
all_params = [cross_train.embeddings, cross_train.W_Q, cross_train.W_K,
              cross_train.W_V, cross_train.W1, cross_train.b1,
              cross_train.W2, cross_train.b2]

for epoch in range(30):
    total_loss = 0
    correct = 0

    for q, d, label in training_data:
        pred = cross_train.score(q, d)
        eps = 1e-9
        loss = -(label * np.log(pred + eps) + (1 - label) * np.log(1 - pred + eps))
        total_loss += loss
        if (pred >= 0.5) == (label == 1):
            correct += 1

        # Numerical gradients
        for param in all_params:
            grad = np.zeros_like(param)
            it = np.nditer(param, flags=['multi_index'])
            while not it.finished:
                idx = it.multi_index
                old = param[idx]

                param[idx] = old + eps_num
                p_plus = cross_train.score(q, d)
                l_plus = -(label * np.log(p_plus + eps) + (1 - label) * np.log(1 - p_plus + eps))

                param[idx] = old - eps_num
                p_minus = cross_train.score(q, d)
                l_minus = -(label * np.log(p_minus + eps) + (1 - label) * np.log(1 - p_minus + eps))

                grad[idx] = (l_plus - l_minus) / (2 * eps_num)
                param[idx] = old
                it.iternext()

            np.clip(grad, -1, 1, out=grad)
            param -= lr * grad

    if epoch < 3 or (epoch + 1) % 10 == 0:
        acc = correct / len(training_data)
        print(f"    Epoch {epoch + 1:>3}: loss={total_loss / len(training_data):.4f}  acc={acc:.0%}")

print(f"\n  --- After training ---")
for q, d, label in training_data:
    pred = cross_train.score(q, d)
    print(f"    label={label}  pred={pred:.4f} → {'correct' if (pred >= 0.5) == (label == 1) else 'wrong'}")


# ================================================================
# SUMMARY
# ================================================================
print(f"""
{'=' * 60}
BI-ENCODER vs CROSS-ENCODER
{'=' * 60}

  ┌──────────────────┬───────────────────────┬───────────────────────┐
  │                  │ Bi-Encoder            │ Cross-Encoder         │
  ├──────────────────┼───────────────────────┼───────────────────────┤
  │ Input            │ Query and doc         │ [Query SEP Doc]       │
  │                  │ encoded SEPARATELY    │ encoded TOGETHER      │
  │ Interaction      │ Only at the end       │ Full attention        │
  │                  │ (dot product)         │ (every token pair)    │
  │ Speed            │ Fast (pre-compute     │ Slow (must encode     │
  │                  │ doc embeddings)       │ every pair)           │
  │ Accuracy         │ Good                  │ Much better           │
  │ Use for          │ Stage 1: Retrieval    │ Stage 2: Re-ranking   │
  │                  │ (search millions)     │ (re-rank ~100)        │
  │ Examples         │ sentence-transformers │ cross-encoder models  │
  │                  │ DPR, E5, BGE          │ ms-marco-MiniLM       │
  └──────────────────┴───────────────────────┴───────────────────────┘

  THE TWO-STAGE RECIPE:
    1. Bi-encoder: embed query → ANN search → top 100 candidates  (~5ms)
    2. Cross-encoder: score each (query, candidate) → re-rank     (~50ms)
    3. Return top 10 to user

  WHY NOT JUST USE CROSS-ENCODER FOR EVERYTHING?
    10 million docs × 1 forward pass each = 10 million forward passes.
    At 5ms per pass = 50,000 seconds = 14 hours per query.
    Impossible. That's why we need bi-encoder to narrow first.

  INTERVIEW QUESTION: "Bi-encoder vs cross-encoder?"
    → "Bi-encoder encodes query and doc separately — fast, can pre-compute
       doc embeddings, use for retrieval over millions.
       Cross-encoder encodes them together — slow but much more accurate,
       use for re-ranking a small set of candidates.
       Always use both in a two-stage pipeline."
""")


# ================================================================
# RE-RANKER #2: FEATURE-BASED (Learning to Rank with XGBoost-style)
# ================================================================
print("=" * 60)
print("FEATURE-BASED RE-RANKER — hand-crafted features + ML model")
print("=" * 60)

print("""
  Instead of a neural cross-encoder, compute FEATURES for each
  (query, doc) pair and feed them into a simple ML model.

  Features:
    - cosine similarity (from Stage 1)
    - BM25 keyword score
    - document recency (days since last updated)
    - document popularity (click count)
    - query-doc word overlap
    - source type (Slack=1, Docs=2, GitHub=3)

  Model: gradient boosted tree (XGBoost / LambdaMART)
  This is called "Learning to Rank" (LTR).
""")


class FeatureBasedReranker:
    """
    Compute features for each (query, doc) pair.
    Train a simple model (logistic regression here) to predict relevance.
    In production: use XGBoost / LambdaMART for better quality.
    """

    def __init__(self, n_features):
        self.w = np.random.randn(n_features) * 0.1
        self.b = 0.0

    def compute_features(self, query, doc):
        """
        Extract features from a (query, doc) pair.
        Returns a feature vector.
        """
        features = []

        # Feature 1: cosine similarity (from embedding)
        features.append(doc.get("cosine_sim", 0))

        # Feature 2: BM25 keyword score
        features.append(doc.get("bm25_score", 0))

        # Feature 3: word overlap (how many query words appear in doc)
        q_words = set(query.lower().split())
        d_words = set(doc["text"].lower().split())
        overlap = len(q_words & d_words) / max(len(q_words), 1)
        features.append(overlap)

        # Feature 4: document recency (1.0 = today, 0.0 = very old)
        features.append(doc.get("recency", 0.5))

        # Feature 5: document popularity (normalized click count)
        features.append(doc.get("popularity", 0))

        return np.array(features)

    def score(self, features):
        """Simple linear model: score = sigmoid(w · features + b)"""
        return sigmoid(np.dot(self.w, features) + self.b)

    def train(self, training_data, lr=0.1, epochs=50, verbose=True):
        """
        training_data: list of (features, label) pairs
        """
        for epoch in range(epochs):
            total_loss = 0
            correct = 0

            for features, label in training_data:
                pred = self.score(features)
                eps = 1e-9
                loss = -(label * np.log(pred + eps) +
                         (1 - label) * np.log(1 - pred + eps))
                total_loss += loss

                if (pred >= 0.5) == (label == 1):
                    correct += 1

                # Gradient descent
                error = pred - label
                self.w -= lr * error * features
                self.b -= lr * error

            if verbose and (epoch < 3 or (epoch + 1) % 10 == 0):
                acc = correct / len(training_data)
                print(f"    Epoch {epoch + 1:>3}: loss={total_loss / len(training_data):.4f}  acc={acc:.0%}")


# Demo data: query = "python tutorial"
query_text = "python tutorial"
candidates = [
    {"text": "learn python basics",          "cosine_sim": 0.92, "bm25_score": 0.85,
     "recency": 0.9, "popularity": 0.7},
    {"text": "java enterprise tutorial",     "cosine_sim": 0.65, "bm25_score": 0.40,
     "recency": 0.3, "popularity": 0.2},
    {"text": "python advanced guide",        "cosine_sim": 0.88, "bm25_score": 0.70,
     "recency": 0.6, "popularity": 0.8},
    {"text": "cooking recipes for beginners","cosine_sim": 0.15, "bm25_score": 0.05,
     "recency": 0.8, "popularity": 0.9},
    {"text": "python data science tutorial", "cosine_sim": 0.90, "bm25_score": 0.80,
     "recency": 0.95, "popularity": 0.6},
]
labels = [1, 0, 1, 0, 1]  # relevant or not

reranker = FeatureBasedReranker(n_features=5)

# Show features
print(f"  Query: '{query_text}'\n")
print(f"  {'Document':<35} {'CosSim':>7} {'BM25':>7} {'Overlap':>7} {'Recency':>7} {'Popular':>7}")
print(f"  {'─' * 75}")

train_data = []
for doc, label in zip(candidates, labels):
    feats = reranker.compute_features(query_text, doc)
    train_data.append((feats, label))
    print(f"  {doc['text']:<35} {feats[0]:>7.2f} {feats[1]:>7.2f} {feats[2]:>7.2f} "
          f"{feats[3]:>7.2f} {feats[4]:>7.2f}  label={label}")

# Train
print(f"\n  --- Training feature-based re-ranker ---")
reranker.train(train_data, lr=0.5, epochs=50)

# Re-rank
print(f"\n  --- Re-ranking results ---")
scored = []
for doc, label in zip(candidates, labels):
    feats = reranker.compute_features(query_text, doc)
    score = reranker.score(feats)
    scored.append((score, doc["text"], label))

scored.sort(key=lambda x: x[0], reverse=True)
for rank, (score, text, label) in enumerate(scored, 1):
    print(f"    {rank}. [{score:.4f}] {text}  (actual: {'relevant' if label else 'not'})")

print(f"\n  Learned weights (which features matter):")
feature_names = ["cosine_sim", "bm25_score", "word_overlap", "recency", "popularity"]
for name, w in zip(feature_names, reranker.w):
    print(f"    {name:<15}: {w:>6.3f}  {'← important' if abs(w) > 0.3 else ''}")

print(f"""
  The model learns: cosine_sim and bm25 matter most,
  popularity alone doesn't mean relevant.

  In production (LambdaMART / XGBoost):
    - 50-100 features instead of 5
    - Optimizes nDCG directly (not just binary classification)
    - Handles nonlinear feature interactions (trees!)
""")


# ================================================================
# RE-RANKER #3: LLM-BASED
# ================================================================
print("=" * 60)
print("LLM RE-RANKER — ask an LLM to rank results")
print("=" * 60)


class LLMReranker:
    """
    Simulate an LLM re-ranker.
    In practice: send a prompt to GPT-4/Claude asking to rank docs.
    Here we simulate the LLM's judgment with a scoring function.
    """

    def build_prompt(self, query, docs):
        """Build the prompt we'd send to an LLM."""
        doc_list = ""
        for i, doc in enumerate(docs):
            doc_list += f"  Document {i + 1}: {doc['text']}\n"

        prompt = f"""Given the search query: "{query}"

Rank the following documents by relevance (most relevant first):
{doc_list}
Return a ranked list of document numbers, e.g., [3, 1, 2, 4]
"""
        return prompt

    def score_docs(self, query, docs):
        """
        Simulate LLM scoring.
        In production: call LLM API, parse the ranked list from response.

        LLM understands MEANING deeply:
          - "merge PDFs" matches "combine PDF files" (synonyms)
          - "python tutorial" matches "learn programming with Python" (paraphrase)
          - Can understand negation: "NOT about python" → low score
        """
        scores = []
        q_words = set(query.lower().split())

        for doc in docs:
            d_words = set(doc["text"].lower().split())

            # Simulate LLM understanding:
            score = 0

            # Direct word overlap (simple matching)
            overlap = len(q_words & d_words)
            score += overlap * 2.0

            # Synonym detection (LLM understands "learn" ≈ "tutorial")
            synonyms = {
                "learn": ["tutorial", "guide", "course", "basics"],
                "python": ["programming", "code", "coding"],
                "advanced": ["deep", "expert", "professional"],
            }
            for q_word in q_words:
                for d_word in d_words:
                    for key, syns in synonyms.items():
                        if (q_word == key and d_word in syns) or \
                           (d_word == key and q_word in syns):
                            score += 1.5

            # Penalize off-topic (LLM knows "cooking" is unrelated to "python")
            off_topic = {"cooking", "recipes", "food", "sports", "weather"}
            if d_words & off_topic:
                score -= 3.0

            scores.append(score)

        return scores

    def rerank(self, query, docs, verbose=False):
        """Full LLM re-ranking pipeline."""
        if verbose:
            prompt = self.build_prompt(query, docs)
            print(f"  Prompt sent to LLM:\n")
            for line in prompt.strip().split('\n'):
                print(f"    {line}")

        scores = self.score_docs(query, docs)

        # Rank by score
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

        if verbose:
            print(f"\n  LLM's judgment (simulated):")
            for rank, (idx, score) in enumerate(ranked, 1):
                print(f"    {rank}. [{score:.1f}] {docs[idx]['text']}")

        return ranked


# Demo
llm_reranker = LLMReranker()

llm_docs = [
    {"text": "learn python basics for beginners"},
    {"text": "java enterprise application development"},
    {"text": "python advanced guide and tutorial"},
    {"text": "cooking recipes for Italian food"},
    {"text": "python programming tutorial and course"},
]

print(f"\n  Query: 'python tutorial'\n")
ranked = llm_reranker.rerank("python tutorial", llm_docs, verbose=True)

print(f"""
  WHY LLM RE-RANKER IS POWERFUL:
    - Understands synonyms: "tutorial" = "guide" = "course"
    - Understands context: "python" = programming, not the snake
    - Understands negation and nuance
    - No training needed (zero-shot)

  WHY NOT USE IT FOR EVERYTHING:
    - SLOW: 500ms-2000ms per call (vs 50ms for cross-encoder)
    - EXPENSIVE: API cost per query
    - UNPREDICTABLE: LLM might change its mind, non-deterministic

  WHEN TO USE:
    - RAG: selecting which chunks to include in context
    - High-value queries where quality matters more than speed
    - As a teacher: generate training labels for cross-encoder

{'=' * 60}
ALL 3 RE-RANKERS COMPARED
{'=' * 60}

  ┌──────────────────┬────────────────┬─────────────────┬────────────────┐
  │                  │ Feature-based  │ Cross-encoder   │ LLM            │
  │                  │ (LambdaMART)   │ (BERT)          │ (GPT/Claude)   │
  ├──────────────────┼────────────────┼─────────────────┼────────────────┤
  │ Input            │ Hand-crafted   │ [query SEP doc] │ Text prompt    │
  │                  │ features       │ tokens          │ with all docs  │
  │ Understanding    │ Shallow        │ Deep (attention)│ Deepest        │
  │ Speed            │ ~1ms           │ ~50ms           │ ~500-2000ms    │
  │ Training needed  │ Yes (features  │ Yes (labeled    │ No (zero-shot) │
  │                  │ + labels)      │ pairs)          │                │
  │ Quality          │ Good           │ Very good       │ Best           │
  │ Interpretable    │ Yes (feature   │ No              │ Somewhat       │
  │                  │ importance)    │                 │ (can explain)  │
  │ Use case         │ Fast re-rank,  │ Standard        │ RAG context,   │
  │                  │ many features  │ re-ranking      │ high-value     │
  └──────────────────┴────────────────┴─────────────────┴────────────────┘

  INTERVIEW: "How would you re-rank search results?"
    → "Start with feature-based for speed and interpretability.
       Add cross-encoder for quality on top candidates.
       Use LLM re-ranker for RAG context selection.
       In practice, blend all three: feature scores as base,
       cross-encoder for precision, LLM for hardest cases."
""")