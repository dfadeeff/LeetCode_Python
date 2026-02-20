"""
t-SNE & UMAP — nonlinear dimensionality reduction, simplified.

PCA finds LINEAR directions of max variance. Great for correlated features.
But if your data lives on a CURVE or SPIRAL, PCA fails completely.

t-SNE and UMAP preserve LOCAL STRUCTURE — points that are close in high-D
stay close in low-D, even if the structure is curved or twisted.

t-SNE (t-distributed Stochastic Neighbor Embedding):
  1. Compute "similarity" between all pairs in high-D (using Gaussian)
  2. Place points randomly in 2D
  3. Compute "similarity" between all pairs in 2D (using Student-t)
  4. Gradient descent: move 2D points until 2D similarities match high-D similarities

UMAP (Uniform Manifold Approximation and Projection):
  Similar idea but:
  - Uses k-nearest neighbors (not all pairs) → much faster
  - Different similarity function → better preserves global structure
  - Uses attractive + repulsive forces instead of KL divergence

Both answer: "how do I squash high-D data to 2D while keeping neighbors close?"
"""
import numpy as np

np.random.seed(42)


# ================================================================
# DATA: 3 clusters in 5D (but really just 2D structure)
# ================================================================
n_per_cluster = 15
# Clusters live in first 2 dimensions, other 3 are noise
c1 = np.hstack([np.random.randn(n_per_cluster, 2) * 0.3 + [0, 0],
                np.random.randn(n_per_cluster, 3) * 0.1])
c2 = np.hstack([np.random.randn(n_per_cluster, 2) * 0.3 + [3, 3],
                np.random.randn(n_per_cluster, 3) * 0.1])
c3 = np.hstack([np.random.randn(n_per_cluster, 2) * 0.3 + [0, 3],
                np.random.randn(n_per_cluster, 3) * 0.1])
X = np.vstack([c1, c2, c3])
labels = np.array([0] * n_per_cluster + [1] * n_per_cluster + [2] * n_per_cluster)


print("Subset of the data: ")
print(X[:5,:])
print("=" * 60)
print("DATA: 3 clusters, 45 points, 5 dimensions")
print("=" * 60)
print(f"  Shape: {X.shape}")
print(f"  Clusters live in dimensions 0-1, dimensions 2-4 are noise")
print(f"  Goal: reduce 5D → 2D while keeping clusters separated\n")


# ================================================================
# PCA (for comparison — linear baseline)
# ================================================================
print("─" * 60)
print("PCA (linear) — for comparison")
print("─" * 60)

X_centered = X - X.mean(axis=0)
cov = X_centered.T @ X_centered / (len(X) - 1)
eigenvalues, eigenvectors = np.linalg.eigh(cov)
idx = np.argsort(eigenvalues)[::-1]
X_pca = X_centered @ eigenvectors[:, idx[:2]]

# Check if clusters are separated
for c in range(3):
    pts = X_pca[labels == c]
    print(f"  Cluster {c}: center=[{pts[:, 0].mean():>5.2f}, {pts[:, 1].mean():>5.2f}]")
print("  PCA works here (clusters are linearly separable)")
print("  But would FAIL on curved/spiral data\n")


# ================================================================
# t-SNE FROM SCRATCH
# ================================================================
print("=" * 60)
print("t-SNE — step by step")
print("=" * 60)


def pairwise_distances(X):
    """||xᵢ - xⱼ||² for all pairs."""
    sq = np.sum(X ** 2, axis=1)
    return sq.reshape(-1, 1) + sq.reshape(1, -1) - 2 * X @ X.T


def high_d_similarities(X, perplexity=10.0):
    """
    Step 1: Convert distances to probabilities in HIGH-D space.
    Uses Gaussian: p_j|i = exp(-||xi-xj||² / 2σ²) / Σ_k exp(...)
    σ is chosen per point so each point has ~perplexity effective neighbors.
    """
    n = len(X)
    dists = pairwise_distances(X)
    P = np.zeros((n, n))

    # For each point, find σ that gives desired perplexity
    for i in range(n):
        # Binary search for the right σ
        sigma_low, sigma_high = 1e-10, 100.0

        for _ in range(50):  # binary search iterations
            sigma = (sigma_low + sigma_high) / 2.0
            # Gaussian similarity (exclude self)
            pi = np.exp(-dists[i] / (2 * sigma ** 2))
            pi[i] = 0
            pi_sum = max(pi.sum(), 1e-10)
            pi = pi / pi_sum

            # Perplexity = 2^(entropy)
            entropy = -np.sum(pi[pi > 0] * np.log2(pi[pi > 0]))
            perp = 2 ** entropy

            if perp > perplexity:
                sigma_high = sigma  # σ too big → too many neighbors
            else:
                sigma_low = sigma   # σ too small → too few neighbors

        P[i] = pi

    # Symmetrize: P = (P + P.T) / 2n
    P = (P + P.T) / (2 * n)
    P = np.maximum(P, 1e-12)
    return P


def low_d_similarities(Y):
    """
    Step 3: Convert distances to probabilities in LOW-D space.
    Uses Student-t distribution (heavy tails) instead of Gaussian.
    Q_ij = (1 + ||yi-yj||²)^(-1) / Σ_k,l (1 + ||yk-yl||²)^(-1)

    WHY Student-t? In high-D, distances between points are all roughly similar
    (curse of dimensionality). In low-D we need to SPREAD things out more.
    Student-t's heavy tails allow far-apart points to be modeled as "very far"
    while keeping close points close. Gaussian would CRUSH everything together.
    """
    dists = pairwise_distances(Y)
    Q = 1.0 / (1.0 + dists)       # Student-t with 1 degree of freedom
    np.fill_diagonal(Q, 0)         # no self-similarity
    Q = Q / max(Q.sum(), 1e-10)
    Q = np.maximum(Q, 1e-12)
    return Q


def tsne(X, n_components=2, perplexity=10.0, lr=50.0, n_iter=300):
    """
    Full t-SNE: gradient descent to make Q (low-D) match P (high-D).
    Minimizes KL divergence: KL(P||Q) = Σ P_ij * log(P_ij / Q_ij)
    """
    n = len(X)

    # Step 1: high-D similarities (computed once)
    print("\n  [Step 1] Computing high-D similarities (Gaussian)...")
    P = high_d_similarities(X, perplexity)
    print(f"    P matrix: {P.shape}, sum={P.sum():.4f}")
    print(f"    Example: P[0,1]={P[0,1]:.6f} (similarity between points 0 and 1)")

    # Step 2: random initialization in low-D
    print(f"\n  [Step 2] Random initialization in {n_components}D")
    Y = np.random.randn(n, n_components) * 0.01

    # Step 4: gradient descent
    print(f"\n  [Step 3-4] Gradient descent ({n_iter} iterations)")
    print(f"    Moving 2D points so their similarities match the 5D similarities\n")

    velocity = np.zeros_like(Y)
    momentum = 0.5

    for iteration in range(n_iter):
        # Compute low-D similarities
        Q = low_d_similarities(Y)

        # Gradient of KL divergence
        # dY_i = 4 * Σ_j (P_ij - Q_ij)(y_i - y_j)(1 + ||y_i - y_j||²)^(-1)
        dists = pairwise_distances(Y)
        inv = 1.0 / (1.0 + dists)
        diff = P - Q

        grad = np.zeros_like(Y)
        for i in range(n):
            grad[i] = 4 * np.sum(((diff[i] * inv[i])[:, np.newaxis]) * (Y[i] - Y), axis=0)

        # Update with momentum
        if iteration > 100:
            momentum = 0.8
        velocity = momentum * velocity - lr * grad
        Y += velocity

        if iteration < 3 or (iteration + 1) % 100 == 0:
            kl = np.sum(P * np.log(P / Q))
            print(f"    Iter {iteration + 1:>3}: KL divergence = {kl:.4f}")

    return Y


# ── Run t-SNE ──
Y_tsne = tsne(X, perplexity=10.0, lr=50.0, n_iter=300)

print(f"\n  Result: {X.shape} → {Y_tsne.shape}")
print(f"\n  Cluster centers in 2D:")
for c in range(3):
    pts = Y_tsne[labels == c]
    print(f"    Cluster {c}: center=[{pts[:, 0].mean():>6.2f}, {pts[:, 1].mean():>6.2f}]")


# ================================================================
# UMAP (simplified concept)
# ================================================================
print(f"\n{'=' * 60}")
print("UMAP — simplified")
print("=" * 60)
print("""
  UMAP is similar to t-SNE but with key differences:

  t-SNE:                              UMAP:
  ─────                               ─────
  Gaussian similarity (all pairs)     k-nearest neighbors only
  Student-t in low-D                  (1 + a·||y||²ᵇ)⁻¹ in low-D
  KL divergence loss                  Cross-entropy loss
  O(n²) — slow for large data        O(n·log(n)) — much faster
  Random init                         Spectral init (smarter start)
  Preserves LOCAL structure           Better GLOBAL structure too
""")


def umap_simple(X, n_neighbors=5, n_components=2, lr=1.0, n_iter=200):
    """
    Simplified UMAP:
    1. Build k-nearest-neighbor graph
    2. Compute high-D similarities from neighbor distances
    3. Initialize low-D positions
    4. Optimize: attract neighbors, repel non-neighbors
    """
    n = len(X)
    dists = pairwise_distances(X)

    # Step 1: Find k nearest neighbors for each point
    print(f"  [Step 1] Find {n_neighbors} nearest neighbors per point")
    neighbors = np.zeros((n, n_neighbors), dtype=int)
    for i in range(n):
        sorted_idx = np.argsort(dists[i])
        neighbors[i] = sorted_idx[1:n_neighbors + 1]  # skip self

    print(f"    Point 0's neighbors: {neighbors[0].tolist()}")
    print(f"    Point {n-1}'s neighbors: {neighbors[n-1].tolist()}")

    # Step 2: High-D similarities (only for neighbors)
    print(f"\n  [Step 2] Compute similarities for neighbor pairs only")
    # Use exponential decay: similarity = exp(-dist / σ)
    P = np.zeros((n, n))
    for i in range(n):
        sigma = np.sort(dists[i])[n_neighbors]  # distance to k-th neighbor
        for j in neighbors[i]:
            P[i, j] = np.exp(-max(dists[i, j] - np.sort(dists[i])[1], 0) / sigma)
    # Symmetrize
    P = (P + P.T)
    P = np.clip(P, 1e-10, 1.0)

    # Step 3: Random init
    print(f"\n  [Step 3] Random initialization in {n_components}D")
    Y = np.random.randn(n, n_components) * 0.1

    # Step 4: SGD with attractive + repulsive forces
    print(f"\n  [Step 4] Optimize: attract neighbors, repel non-neighbors")

    for iteration in range(n_iter):
        low_dists = pairwise_distances(Y)

        grad = np.zeros_like(Y)
        for i in range(n):
            # ATTRACTIVE force: pull neighbors closer
            for j in neighbors[i]:
                d = max(low_dists[i, j], 1e-4)
                w = 1.0 / (1.0 + d)  # high when close
                attractive = P[i, j] * w * (Y[i] - Y[j])
                grad[i] -= attractive  # pull toward neighbor

            # REPULSIVE force: push random non-neighbors away
            for _ in range(n_neighbors):
                j = np.random.randint(n)
                if j == i:
                    continue
                d = max(low_dists[i, j], 1e-4)
                w = 1.0 / (1.0 + d)
                repulsive = (1.0 - P[i, j]) * w * w * (Y[i] - Y[j])
                grad[i] += repulsive  # push away from non-neighbor

        Y -= lr * np.clip(grad, -4, 4)

        if iteration < 3 or (iteration + 1) % 50 == 0:
            print(f"    Iter {iteration + 1:>3}")

    return Y


Y_umap = umap_simple(X, n_neighbors=5, lr=0.5, n_iter=200)

print(f"\n  Result: {X.shape} → {Y_umap.shape}")
print(f"\n  Cluster centers in 2D:")
for c in range(3):
    pts = Y_umap[labels == c]
    print(f"    Cluster {c}: center=[{pts[:, 0].mean():>6.2f}, {pts[:, 1].mean():>6.2f}]")


# ================================================================
# COMPARISON
# ================================================================
print(f"""
{'=' * 60}
COMPARISON: PCA vs t-SNE vs UMAP
{'=' * 60}

  ┌────────────────┬──────────────────┬──────────────────┬──────────────────┐
  │                │ PCA              │ t-SNE            │ UMAP             │
  ├────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │ Type           │ Linear           │ Nonlinear        │ Nonlinear        │
  │ Preserves      │ Global variance  │ Local structure   │ Local + global   │
  │ Speed          │ Fast O(nd²)      │ Slow O(n²)       │ Fast O(n·log n)  │
  │ Deterministic  │ Yes              │ No (random init)  │ No (random init) │
  │ New points     │ Yes (transform)  │ No (must rerun)   │ Yes (transform)  │
  │ Interpretable  │ Somewhat         │ No               │ No               │
  │ Use for        │ Preprocessing    │ Visualization    │ Visualization +  │
  │                │ Feature reduce   │ only             │ preprocessing    │
  └────────────────┴──────────────────┴──────────────────┴──────────────────┘

  WHEN TO USE:
    PCA:   reduce features before training a model, or data is linear
    t-SNE: visualize clusters in high-D data (papers, presentations)
    UMAP:  same as t-SNE but faster, better for large datasets,
           can also be used as preprocessing (not just visualization)

  KEY INTERVIEW POINTS:
    - PCA is linear → fails on curves/spirals
    - t-SNE/UMAP are nonlinear → preserve neighborhood structure
    - t-SNE is O(n²) → struggles past ~10k points
    - UMAP uses nearest-neighbor graphs → scales much better
    - Neither t-SNE nor UMAP distances in 2D are meaningful!
      Only the CLUSTERS matter, not the distances between them.
""")