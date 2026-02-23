"""
CONTRASTIVE LEARNING — how embeddings are trained, from scratch.

The Question: HOW do you get those magic vectors where
  "I love dogs" ≈ "I adore puppies" (close) and
  "I love dogs" ≠ "Stock market news" (far)?

Answer: CONTRASTIVE LEARNING.
  Train a model to PULL similar items TOGETHER and
  PUSH dissimilar items APART in embedding space.

THREE KEY LOSS FUNCTIONS:
  1. Contrastive Loss (pairs): similar → close, dissimilar → far
  2. Triplet Loss (anchor, positive, negative): anchor closer to pos than neg
  3. InfoNCE / NT-Xent (used in CLIP, SimCLR): multi-negative contrastive

This is how Dropbox Dash trains its embedding models for search.
"""
import numpy as np

np.random.seed(42)


# ================================================================
# SIMPLE EMBEDDING MODEL
# ================================================================
def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))


class SimpleEmbedder:
    """
    Tiny 2-layer network that maps input features to an embedding.
    input_dim → hidden → embed_dim
    """

    def __init__(self, input_dim, hidden_dim, embed_dim):
        scale = np.sqrt(2.0 / input_dim)
        self.W1 = np.random.randn(input_dim, hidden_dim) * scale
        self.b1 = np.zeros((1, hidden_dim))
        self.W2 = np.random.randn(hidden_dim, embed_dim) * scale
        self.b2 = np.zeros((1, embed_dim))

    def embed(self, x):
        """Forward pass: x → hidden → embedding (L2 normalized)."""
        x = x.reshape(1, -1)
        h = np.maximum(0, x @ self.W1 + self.b1)  # ReLU
        emb = h @ self.W2 + self.b2
        # L2 normalize (unit sphere)
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm
        return emb.flatten()


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)


# ================================================================
# 1. CONTRASTIVE LOSS (pairs)
# ================================================================
print("=" * 60)
print("1. CONTRASTIVE LOSS — pull similar, push dissimilar")
print("=" * 60)

print("""
  Given PAIRS of items with a label:
    (item_a, item_b, similar=1)  → pull embeddings CLOSE
    (item_a, item_b, similar=0)  → push embeddings FAR

  Loss:
    if similar:     L = ||emb_a - emb_b||²          (minimize distance)
    if dissimilar:  L = max(0, margin - ||emb_a - emb_b||)²  (push apart)

  The MARGIN says "I don't care if dissimilar items are FAR enough apart."
""")


def contrastive_loss(emb_a, emb_b, label, margin=1.0):
    """
    label=1: similar pair → minimize distance
    label=0: dissimilar pair → maximize distance (up to margin)
    """
    dist = np.linalg.norm(emb_a - emb_b)

    if label == 1:
        loss = dist ** 2  # pull together
    else:
        loss = max(0, margin - dist) ** 2  # push apart (up to margin)

    return loss, dist


# Demo
print(f"\n  Example with 3D embeddings:\n")
emb_dog1 = np.array([0.8, 0.2, 0.1])
emb_dog2 = np.array([0.7, 0.3, 0.15])
emb_stock = np.array([-0.5, 0.8, -0.3])

loss_sim, dist_sim = contrastive_loss(emb_dog1, emb_dog2, label=1)
loss_dis, dist_dis = contrastive_loss(emb_dog1, emb_stock, label=0, margin=1.0)

print(f"  Similar pair (dog1, dog2):    dist={dist_sim:.4f}  loss={loss_sim:.4f} (want LOW)")
print(f"  Dissimilar pair (dog1, stock): dist={dist_dis:.4f}  loss={loss_dis:.4f} (want LOW)")
print(f"\n  Training pushes dog1↔dog2 closer, dog1↔stock farther.")


# ================================================================
# 2. TRIPLET LOSS
# ================================================================
print(f"\n{'=' * 60}")
print("2. TRIPLET LOSS — anchor, positive, negative")
print("=" * 60)

print("""
  Instead of pairs, use TRIPLETS:
    anchor:   the reference item
    positive: item similar to anchor
    negative: item dissimilar to anchor

  Loss = max(0, ||anchor - positive||² - ||anchor - negative||² + margin)

  In words: "anchor should be closer to positive than to negative,
             by at least a margin."

    anchor ●──dist_pos──● positive
           │
           dist_neg (should be larger)
           │
           ● negative
""")


def triplet_loss(anchor, positive, negative, margin=0.5):
    """
    Triplet loss: anchor closer to positive than negative by margin.
    """
    dist_pos = np.sum((anchor - positive) ** 2)  # ||a - p||²
    dist_neg = np.sum((anchor - negative) ** 2)   # ||a - n||²

    loss = max(0, dist_pos - dist_neg + margin)
    return loss, dist_pos, dist_neg


# Demo
loss, dp, dn = triplet_loss(emb_dog1, emb_dog2, emb_stock, margin=0.5)
print(f"""
  anchor   = dog1  = {emb_dog1.tolist()}
  positive = dog2  = {emb_dog2.tolist()}
  negative = stock = {emb_stock.tolist()}

  dist(anchor, positive) = {dp:.4f}
  dist(anchor, negative) = {dn:.4f}

  Loss = max(0, {dp:.4f} - {dn:.4f} + 0.5) = max(0, {dp - dn + 0.5:.4f}) = {loss:.4f}

  Loss = 0 means negative is already far enough away.
""")


# ── Train with triplet loss ──
print("─" * 60)
print("Training embeddings with triplet loss")
print("─" * 60)

# Toy data: 3 categories, 2 items each, 4 features
items = {
    "dog1":   np.array([1.0, 0.5, 0.0, 0.1]),
    "dog2":   np.array([0.9, 0.6, 0.1, 0.0]),
    "cat1":   np.array([0.5, 1.0, 0.0, 0.2]),
    "cat2":   np.array([0.4, 0.9, 0.1, 0.1]),
    "car1":   np.array([0.0, 0.0, 1.0, 0.8]),
    "car2":   np.array([0.1, 0.0, 0.9, 0.9]),
}
categories = {"dog1": 0, "dog2": 0, "cat1": 1, "cat2": 1, "car1": 2, "car2": 2}

# Create triplets
triplets = [
    ("dog1", "dog2", "cat1"),   # dogs together, cat away
    ("dog1", "dog2", "car1"),   # dogs together, car away
    ("cat1", "cat2", "dog1"),   # cats together, dog away
    ("cat1", "cat2", "car1"),   # cats together, car away
    ("car1", "car2", "dog1"),   # cars together, dog away
    ("car1", "car2", "cat1"),   # cars together, cat away
]

embedder = SimpleEmbedder(input_dim=4, hidden_dim=8, embed_dim=3)

print(f"\n  Before training — embeddings:")
for name, features in items.items():
    emb = embedder.embed(features)
    print(f"    {name}: {emb.round(3).tolist()}")

# Check similarities before training
print(f"\n  Similarities before training:")
names = list(items.keys())
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        emb_i = embedder.embed(items[names[i]])
        emb_j = embedder.embed(items[names[j]])
        sim = cosine_similarity(emb_i, emb_j)
        same = "✓ same" if categories[names[i]] == categories[names[j]] else "✗ diff"
        print(f"    {names[i]:5} ↔ {names[j]:5}: cos={sim:>6.3f} ({same})")

# Train with numerical gradients
print(f"\n  Training with triplet loss (margin=0.3)...")
lr = 0.1
for epoch in range(50):
    total_loss = 0
    for anc_name, pos_name, neg_name in triplets:
        anc_emb = embedder.embed(items[anc_name])
        pos_emb = embedder.embed(items[pos_name])
        neg_emb = embedder.embed(items[neg_name])

        loss, _, _ = triplet_loss(anc_emb, pos_emb, neg_emb, margin=0.3)
        total_loss += loss

        # Numerical gradient update on W1, W2
        eps = 1e-5
        for param in [embedder.W1, embedder.b1, embedder.W2, embedder.b2]:
            grad = np.zeros_like(param)
            it = np.nditer(param, flags=['multi_index'])
            while not it.finished:
                idx = it.multi_index
                old = param[idx]

                param[idx] = old + eps
                a_p = embedder.embed(items[anc_name])
                p_p = embedder.embed(items[pos_name])
                n_p = embedder.embed(items[neg_name])
                l_plus, _, _ = triplet_loss(a_p, p_p, n_p, margin=0.3)

                param[idx] = old - eps
                a_m = embedder.embed(items[anc_name])
                p_m = embedder.embed(items[pos_name])
                n_m = embedder.embed(items[neg_name])
                l_minus, _, _ = triplet_loss(a_m, p_m, n_m, margin=0.3)

                grad[idx] = (l_plus - l_minus) / (2 * eps)
                param[idx] = old
                it.iternext()

            np.clip(grad, -1, 1, out=grad)
            param -= lr * grad

    if epoch < 3 or (epoch + 1) % 10 == 0:
        print(f"    Epoch {epoch + 1:>3}: total triplet loss = {total_loss:.4f}")

print(f"\n  After training — similarities:")
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        emb_i = embedder.embed(items[names[i]])
        emb_j = embedder.embed(items[names[j]])
        sim = cosine_similarity(emb_i, emb_j)
        same = "✓ same" if categories[names[i]] == categories[names[j]] else "✗ diff"
        print(f"    {names[i]:5} ↔ {names[j]:5}: cos={sim:>6.3f} ({same})")

print(f"\n  Same-category pairs should have HIGHER similarity now!")


# ================================================================
# 3. InfoNCE / NT-Xent (CLIP-style)
# ================================================================
print(f"\n{'=' * 60}")
print("3. InfoNCE LOSS — used in CLIP, SimCLR, sentence-transformers")
print("=" * 60)

print("""
  In a batch of N items, each has 1 positive and N-1 negatives.
  No need to manually construct pairs/triplets — use the batch!

  For query q and positive key k+:

    L = -log( exp(q·k+ / τ) / Σ_i exp(q·ki / τ) )

  τ (temperature) controls sharpness:
    τ → 0: very peaked (hard matching)
    τ → ∞: uniform (no distinction)

  This is basically SOFTMAX CROSS-ENTROPY on similarity scores.
  The positive pair should have the highest similarity.
""")


def infonce_loss(query_emb, key_embs, positive_idx, temperature=0.1):
    """
    InfoNCE loss for one query.
    query_emb: (d,) — the query embedding
    key_embs: (N, d) — all key embeddings (including the positive)
    positive_idx: which key is the positive match
    """
    # Compute similarities
    sims = np.dot(key_embs, query_emb) / temperature  # (N,)

    # Softmax
    exp_sims = np.exp(sims - np.max(sims))  # subtract max for numerical stability
    probs = exp_sims / exp_sims.sum()

    # Loss = -log(probability of the positive)
    loss = -np.log(probs[positive_idx] + 1e-9)

    return loss, probs


# Demo: batch of 4 items, each is its own positive
print(f"\n  Example: batch of 4 items")
batch_embs = np.array([
    [0.9, 0.1, 0.0],   # item 0 (query)
    [0.85, 0.15, 0.05], # item 1 (positive for item 0)
    [-0.5, 0.8, 0.1],   # item 2 (negative)
    [0.1, -0.3, 0.9],   # item 3 (negative)
])
batch_labels = ["dog photo", "puppy photo", "stock chart", "car image"]

print(f"\n  Query: item 0 '{batch_labels[0]}'")
print(f"  Positive: item 1 '{batch_labels[1]}' (same category)")
print(f"  Negatives: items 2-3 (different categories)\n")

loss, probs = infonce_loss(batch_embs[0], batch_embs, positive_idx=1, temperature=0.1)

print(f"  Similarities (before temperature):")
for i in range(len(batch_embs)):
    sim = np.dot(batch_embs[0], batch_embs[i])
    print(f"    item {i} ({batch_labels[i]:12}): sim={sim:.4f}")

print(f"\n  After softmax (temperature=0.1):")
for i in range(len(probs)):
    marker = " ← positive" if i == 1 else ""
    print(f"    item {i}: prob={probs[i]:.4f}{marker}")

print(f"\n  InfoNCE loss = -log({probs[1]:.4f}) = {loss:.4f}")
print(f"  (Lower = better. Loss=0 means positive has prob=1)")


# ================================================================
# CLIP: Contrastive Language-Image Pretraining
# ================================================================
print(f"""
{'=' * 60}
CLIP — connecting text and images (used in Dash multimodal search)
{'=' * 60}

  CLIP trains TWO encoders simultaneously:
    - Image encoder (ResNet/ViT) → image embedding
    - Text encoder (Transformer) → text embedding

  Training (InfoNCE on image-text pairs):
    Batch of N (image, text) pairs.
    Positive: matching image-text pair.
    Negatives: all other N-1 pairs in the batch.

    ┌────────┐     ┌────────┐     ┌────────┐
    │ Image1 │     │ Image2 │     │ Image3 │
    └───┬────┘     └───┬────┘     └───┬────┘
        │              │              │
    ┌───▼────┐     ┌───▼────┐     ┌───▼────┐
    │ Img Enc│     │ Img Enc│     │ Img Enc│
    └───┬────┘     └───┬────┘     └───┬────┘
        │              │              │
     emb_i1         emb_i2         emb_i3
        │ ╲            │              │ ╲
        │  ╲ high sim  │              │  ╲
     emb_t1         emb_t2         emb_t3
        │              │              │
    ┌───▼────┐     ┌───▼────┐     ┌───▼────┐
    │ Txt Enc│     │ Txt Enc│     │ Txt Enc│
    └───┬────┘     └───┬────┘     └───┬────┘
        │              │              │
    ┌───▼────┐     ┌───▼────┐     ┌───▼────┐
    │ Text1  │     │ Text2  │     │ Text3  │
    └────────┘     └────────┘     └────────┘

  After training: image embedding ≈ text embedding of its caption.
  Use for: text→image search, image→text search, zero-shot classification.
""")


# ================================================================
# HARD NEGATIVE MINING
# ================================================================
print(f"""
{'=' * 60}
HARD NEGATIVE MINING — training better embeddings
{'=' * 60}

  Not all negatives are equally useful:
    Easy negative: "dog photo" vs "stock chart"     (obviously different)
    Hard negative: "dog photo" vs "wolf photo"      (tricky!)

  Training on HARD negatives → much better embeddings.
  The model learns fine-grained distinctions.

  Strategies:
    1. In-batch negatives: use other items in the batch (simple, works ok)
    2. Hard mining: find negatives that are CLOSE but wrong (best quality)
    3. Semi-hard: negatives that are farther than positive but within margin

  For search: good negatives = documents that LOOK relevant but aren't.
    Query: "python tutorial"
    Easy negative: "cooking recipes"
    Hard negative: "python snake facts" (same word, different meaning!)

{'=' * 60}
SUMMARY — HOW EMBEDDINGS ARE TRAINED
{'=' * 60}

  ┌──────────────┬────────────────────┬──────────────────────────────┐
  │ Loss         │ Input              │ Used in                      │
  ├──────────────┼────────────────────┼──────────────────────────────┤
  │ Contrastive  │ Pairs + label      │ Siamese networks             │
  │ Triplet      │ Anchor/pos/neg     │ FaceNet, early embedding     │
  │              │                    │ models                       │
  │ InfoNCE      │ Batch (1 pos,      │ CLIP, SimCLR, sentence-      │
  │              │ N-1 neg)           │ transformers, Dash           │
  └──────────────┴────────────────────┴──────────────────────────────┘

  TRAINING RECIPE:
    1. Collect pairs: (query, relevant doc) from click logs / annotations
    2. Pick loss: InfoNCE (most popular now)
    3. Train encoder: minimize loss → similar items get close embeddings
    4. Normalize embeddings: L2 norm → cosine similarity = dot product
    5. Index embeddings: FAISS / HNSW for fast retrieval
    6. Mine hard negatives → retrain → repeat for better quality
""")