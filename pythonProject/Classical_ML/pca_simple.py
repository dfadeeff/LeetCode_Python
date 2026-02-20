"""
PCA (Principal Component Analysis) — simplified.

THE PROBLEM:
  You have 100 features but most are redundant or correlated.
  You want to reduce to 10 features while keeping the most information.

THE IDEA:
  Find the directions where data VARIES THE MOST.
  Project all data onto those directions.

  Imagine a cloud of points shaped like a football (elongated).
  PCA finds the LONG axis (most variance) and the SHORT axis (least variance).
  If you only keep the long axis, you capture most of the information
  with just 1 dimension instead of 2.

ALGORITHM (4 steps):
  1. Center the data (subtract mean)
  2. Compute covariance matrix
  3. Find eigenvectors (directions) and eigenvalues (variance along each)
  4. Pick top-k eigenvectors → project data onto them
"""
import numpy as np

np.random.seed(42)

# ── Data: 10 points in 3D, but really only 2D matters ──
# x₃ ≈ x₁ + x₂ (redundant — perfectly correlated)
n = 10
x1 = np.random.randn(n)
x2 = np.random.randn(n)
x3 = x1 + x2 + np.random.randn(n) * 0.01  # almost exactly x1 + x2
X = np.column_stack([x1, x2, x3])

print(X)
print("=" * 60)
print("PCA: Reduce 3 features to 2")
print("=" * 60)
print(f"\n  Data shape: {X.shape}  (10 points, 3 features)")
print(f"  x₃ ≈ x₁ + x₂, so feature 3 is REDUNDANT")
print(f"  PCA should discover this and reduce to 2 dimensions\n")

# ── Step 1: Center the data ──
print("─" * 60)
print("STEP 1: Center the data (subtract mean from each feature)")
print("─" * 60)

mean = X.mean(axis=0)
X_centered = X - mean

print(f"  Means: [{mean[0]:.3f}, {mean[1]:.3f}, {mean[2]:.3f}]")
print(f"  After centering, each feature has mean ≈ 0")
print(f"  Verify: {X_centered.mean(axis=0).round(10)}")

# ── Step 2: Covariance matrix ──
print(f"\n{'─' * 60}")
print("STEP 2: Compute covariance matrix")
print("─" * 60)

# cov[i,j] = how much feature i and feature j vary TOGETHER
cov_matrix = (X_centered.T @ X_centered) / (n - 1)

print(f"  Formula: Cov = (X_centered.T @ X_centered) / (n-1)")
print(f"  Shape: {cov_matrix.shape}  (3×3: one entry per feature pair)\n")
print(f"  Covariance matrix:")
for i in range(3):
    print(f"    [{cov_matrix[i, 0]:>6.3f}, {cov_matrix[i, 1]:>6.3f}, {cov_matrix[i, 2]:>6.3f}]")

print(f"\n  Diagonal = variance of each feature:")
print(f"    Var(x₁)={cov_matrix[0,0]:.3f}, Var(x₂)={cov_matrix[1,1]:.3f}, Var(x₃)={cov_matrix[2,2]:.3f}")
print(f"  Off-diagonal = covariance (correlation):")
print(f"    Cov(x₁,x₃)={cov_matrix[0,2]:.3f} ← high! because x₃ ≈ x₁ + x₂")

# ── Step 3: Eigendecomposition ──
print(f"\n{'─' * 60}")
print("STEP 3: Find eigenvectors and eigenvalues")
print("─" * 60)

eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

# eigh returns in ascending order, we want descending (biggest first)
idx = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

print(f"\n  Eigenvectors = DIRECTIONS of maximum variance")
print(f"  Eigenvalues  = HOW MUCH variance along each direction\n")

total_var = np.sum(eigenvalues)
for i in range(3):
    pct = eigenvalues[i] / total_var * 100
    print(f"  PC{i+1}: eigenvalue={eigenvalues[i]:.3f}"
          f"  ({pct:.1f}% of variance)"
          f"  direction=[{eigenvectors[0,i]:>6.3f}, {eigenvectors[1,i]:>6.3f}, {eigenvectors[2,i]:>6.3f}]")

print(f"\n  PC3 has eigenvalue ≈ 0 → that direction has NO variance")
print(f"  That's the redundant dimension (x₃ = x₁ + x₂)")
print(f"  PC1 + PC2 capture {(eigenvalues[0]+eigenvalues[1])/total_var*100:.1f}% of all variance")

# ── Step 4: Project onto top-k components ──
print(f"\n{'─' * 60}")
print("STEP 4: Project data onto top 2 principal components")
print("─" * 60)

k = 2
W = eigenvectors[:, :k]  # take first 2 eigenvectors as columns

print(f"\n  Projection matrix W (3×2): pick top {k} eigenvectors")
for i in range(3):
    print(f"    [{W[i, 0]:>6.3f}, {W[i, 1]:>6.3f}]")

X_reduced = X_centered @ W

print(f"\n  X_reduced = X_centered @ W")
print(f"  Shape: {X.shape} → {X_reduced.shape}  (3D → 2D!)\n")

print(f"  Original 3D → Reduced 2D:")
for i in range(min(5, n)):
    print(f"    [{X[i,0]:>6.3f}, {X[i,1]:>6.3f}, {X[i,2]:>6.3f}]"
          f"  →  [{X_reduced[i,0]:>6.3f}, {X_reduced[i,1]:>6.3f}]")
print(f"    ... ({n} points total)")

# ── Verify: reconstruct and check error ──
X_reconstructed = X_reduced @ W.T + mean
recon_error = np.mean((X - X_reconstructed) ** 2)
print(f"\n  Reconstruction error (project back to 3D): {recon_error:.6f}")
print(f"  Almost zero! We lost nearly nothing by dropping dimension 3.")

print(f"""
{'=' * 60}
THE COMPLETE ALGORITHM (4 lines of real code)
{'=' * 60}

  mean = X.mean(axis=0)
  X_centered = X - mean
  eigenvalues, eigenvectors = np.linalg.eigh(X_centered.T @ X_centered / (n-1))
  X_reduced = X_centered @ eigenvectors[:, -k:]   # top k

  That's PCA. Everything else is details.

{'=' * 60}
INTERVIEW QUESTIONS
{'=' * 60}

  Q: "What does PCA do?"
  A: Finds the directions of maximum variance and projects onto them.
     Reduces dimensions while keeping the most information.

  Q: "When to use PCA?"
  A: - Too many features (curse of dimensionality)
     - Features are correlated / redundant
     - Visualization (reduce to 2D or 3D)
     - Speed up other models by reducing input size

  Q: "Limitations?"
  A: - Only finds LINEAR relationships (use t-SNE/UMAP for nonlinear)
     - Components are hard to interpret (mixtures of original features)
     - Sensitive to feature scales → always standardize first!

  Q: "How many components to keep?"
  A: Plot cumulative explained variance. Pick k where it reaches ~95%.
     Or use the "elbow" in the scree plot.
""")