"""
SVM (Support Vector Machine) — simplified.

CORE IDEA:
  Logistic Regression finds A boundary between classes.
  SVM finds the BEST boundary — the one with the MAXIMUM MARGIN.

  Margin = distance between the boundary and the closest points from each class.
  Those closest points are called "support vectors" (they "support" the boundary).

  Imagine two groups of balls on a table. You place a ruler between them.
  SVM places the ruler so it's as FAR as possible from both groups.
  Only the balls touching the ruler matter — those are support vectors.

LINEAR SVM:
  Find w, b that maximize the margin while classifying correctly.
  Decision: sign(w·x + b)
    > 0 → class +1
    < 0 → class -1

  We minimize: (1/2)||w||² + C * Σ max(0, 1 - yᵢ(w·xᵢ + b))
                ↑ small w = wide margin    ↑ hinge loss (penalize mistakes)

  C is the tradeoff:
    big C   → "don't tolerate mistakes" → narrow margin, fits training data
    small C → "wide margin is more important" → allows some misclassifications

KERNEL TRICK (explained below after the linear version):
  What if data ISN'T linearly separable? Use a kernel.
"""
import numpy as np

np.random.seed(42)

# ── 10 points, 2 classes, linearly separable ──
X = np.array([
    [1.0, 2.0], [2.0, 3.0], [1.5, 1.5], [2.0, 1.0], [1.0, 0.5],  # class -1
    [5.0, 5.0], [6.0, 4.0], [5.5, 5.5], [4.5, 4.0], [6.0, 6.0],  # class +1
])
y = np.array([-1, -1, -1, -1, -1, 1, 1, 1, 1, 1])  # SVM uses -1/+1, not 0/1

print("=" * 60)
print("LINEAR SVM on 10 points")
print("=" * 60)
print(f"\n  {'Point':>8}  {'x1':>5}  {'x2':>5}  {'class':>6}")
for i in range(len(X)):
    print(f"  {i:>8}  {X[i][0]:>5.1f}  {X[i][1]:>5.1f}  {y[i]:>+6}")

# ── Train with gradient descent on hinge loss ──
w = np.zeros(2)
b = 0.0
C = 1.0       # penalty for misclassification
lr = 0.01

print(f"\n  Training: minimize (1/2)||w||² + C * Σ hinge_loss")
print(f"  C={C}, lr={lr}\n")

for epoch in range(300):
    for i in range(len(X)):
        # margin: how confident are we? want yᵢ(w·xᵢ + b) >= 1
        margin = y[i] * (np.dot(w, X[i]) + b)

        if margin >= 1:
            # correctly classified with enough margin → only regularize
            w -= lr * w  # push w toward 0 (wider margin)
        else:
            # misclassified or too close → fix it
            w -= lr * (w - C * y[i] * X[i])
            b += lr * C * y[i]

    if epoch < 3 or epoch % 100 == 99:
        # compute total loss
        margins = y * (X @ w + b)
        hinge = np.sum(np.maximum(0, 1 - margins))
        loss = 0.5 * np.dot(w, w) + C * hinge
        acc = np.mean(np.sign(X @ w + b) == y)
        print(f"  Epoch {epoch + 1:>3}: w=[{w[0]:.3f}, {w[1]:.3f}]  b={b:.3f}  "
              f"loss={loss:.3f}  acc={acc:.0%}")

# ── Show support vectors ──
print(f"\n  Final boundary: {w[0]:.3f}*x1 + {w[1]:.3f}*x2 + ({b:.3f}) = 0")
print(f"\n  Which points are closest to the boundary? (support vectors)")
margins = y * (X @ w + b)
for i in range(len(X)):
    status = "← SUPPORT VECTOR" if margins[i] < 1.5 else ""
    print(f"    Point {i}: margin={margins[i]:.3f}  {status}")

# ── Predict ──
x_new = np.array([3.5, 3.0])
score = np.dot(w, x_new) + b
print(f"\n  Predict [{x_new[0]}, {x_new[1]}]: score={score:.3f} → class {'+1' if score > 0 else '-1'}")


# ================================================================
# KERNEL TRICK
# ================================================================
print(f"""

{'=' * 60}
KERNEL TRICK — when data is NOT linearly separable
{'=' * 60}

THE PROBLEM:
  Some data can't be split with a straight line:

      - - - + + + - - -      ← can't draw a line between + and -

  But if you ADD a new feature (e.g. x²), it becomes separable
  in a HIGHER dimension:

      Original 1D:    -2  -1  0  1  2     (not separable)
      Add x² feature:  4   1  0  1  4

      In 2D (x, x²):
          x²
        4 | -           -
          |
        1 |    -     -
          |
        0 |       +           ← now separable with a horizontal line!
          +──────────────── x

  This is called MAPPING to a higher-dimensional space.

THE TRICK:
  Mapping to high dimensions is EXPENSIVE (sometimes infinite dimensions).
  But SVM only needs DOT PRODUCTS between points, not the actual coordinates.

  A KERNEL function computes the dot product IN the higher space
  WITHOUT actually going there:

      K(x, z) = φ(x) · φ(z)    ← dot product in high-D space
                                   but computed directly from x, z

  Common kernels:
    Linear:     K(x,z) = x·z                (no mapping, just regular SVM)
    Polynomial: K(x,z) = (x·z + 1)^d        (maps to polynomial features)
    RBF/Gaussian: K(x,z) = exp(-γ||x-z||²)  (maps to INFINITE dimensions!)

  RBF is the most popular. γ controls how "local" each point's influence is:
    large γ → each point only affects nearby points (complex boundary)
    small γ → each point affects far away points (smooth boundary)
""")

# ── Demo: RBF kernel on non-linear data ──
print("─" * 60)
print("DEMO: RBF Kernel SVM on circular data")
print("─" * 60)

# Inner ring (class -1) and outer ring (class +1)
np.random.seed(42)
angles = np.linspace(0, 2 * np.pi, 6, endpoint=False)
X_inner = 1.0 * np.column_stack([np.cos(angles), np.sin(angles)])
X_outer = 3.0 * np.column_stack([np.cos(angles), np.sin(angles)])
X_kern = np.vstack([X_inner, X_outer])
y_kern = np.array([-1] * 6 + [1] * 6)

print(f"\n  Inner ring (class -1): radius ≈ 1")
print(f"  Outer ring (class +1): radius ≈ 3")
print(f"  A straight line CAN'T separate circles.\n")


def rbf_kernel(X1, X2, gamma=0.5):
    """K(x,z) = exp(-gamma * ||x-z||²) — computed for all pairs."""
    # ||x-z||² = ||x||² + ||z||² - 2*x·z
    sq1 = np.sum(X1 ** 2, axis=1).reshape(-1, 1)
    sq2 = np.sum(X2 ** 2, axis=1).reshape(1, -1)
    dists = sq1 + sq2 - 2 * X1 @ X2.T
    return np.exp(-gamma * dists)


# Kernel SVM via simplified SMO-like gradient descent
# In kernel space, prediction = sign(Σ αᵢyᵢK(xᵢ, x) + b)
# αᵢ > 0 only for support vectors
n = len(X_kern)
alpha = np.zeros(n)  # one weight per training point
b_kern = 0.0
gamma = 0.5
C_kern = 10.0

K = rbf_kernel(X_kern, X_kern, gamma)  # precompute all pairwise kernels

print(f"  Kernel matrix K (12×12): K[i,j] = exp(-{gamma}*||xᵢ-xⱼ||²)")
print(f"  Points close together → K ≈ 1, far apart → K ≈ 0\n")

for epoch in range(500):
    for i in range(n):
        # decision function: Σ αⱼyⱼK(xⱼ, xᵢ) + b
        decision = np.sum(alpha * y_kern * K[i]) + b_kern
        margin = y_kern[i] * decision

        if margin < 1:
            alpha[i] += lr * (1 - margin)
            alpha[i] = np.clip(alpha[i], 0, C_kern)
            b_kern += lr * y_kern[i] * (1 - margin)

support_mask = alpha > 0.01
print(f"  Support vectors: {np.sum(support_mask)} out of {n} points")
print(f"  (only these points define the boundary)\n")

for i in range(n):
    sv = "← SV" if support_mask[i] else ""
    ring = "inner" if i < 6 else "outer"
    print(f"    Point {i:>2} ({ring}): α={alpha[i]:.3f}  {sv}")

# Predict new points
print(f"\n  Predictions:")
test_points = [np.array([0.0, 0.0]), np.array([2.0, 2.0]), np.array([0.5, 0.5])]
for x_t in test_points:
    K_new = rbf_kernel(x_t.reshape(1, -1), X_kern, gamma)[0]
    decision = np.sum(alpha * y_kern * K_new) + b_kern
    pred = "+1 (outer)" if decision > 0 else "-1 (inner)"
    dist = np.sqrt(x_t[0] ** 2 + x_t[1] ** 2)
    print(f"    [{x_t[0]:>4.1f}, {x_t[1]:>4.1f}] (dist from center={dist:.1f}) → {pred}")

print(f"""
{'=' * 60}
INTERVIEW SUMMARY
{'=' * 60}

  LINEAR SVM:
    Find w,b that maximize margin between classes.
    Loss = (1/2)||w||² + C * Σ max(0, 1 - yᵢ(w·xᵢ+b))
    Only support vectors (closest points) matter.

  KERNEL TRICK:
    Map data to higher dimensions where it IS separable.
    But never compute the mapping — use kernel function instead.
    K(x,z) gives the dot product in high-D space directly.
    RBF kernel: K(x,z) = exp(-γ||x-z||²) → infinite dimensions.

  SVM vs LOGISTIC REGRESSION:
    Both find a linear boundary (without kernel).
    SVM maximizes MARGIN (geometric), LR maximizes LIKELIHOOD (probabilistic).
    SVM gives no probabilities. LR gives P(y|x).
    SVM with kernels handles non-linear boundaries. LR can't (natively).
""")