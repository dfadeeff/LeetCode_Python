"""
RIDGE (L2) vs LASSO (L1) Regularization — simplified.

THE PROBLEM:
  Your model memorizes the training data too well (overfitting).
  Some weights become HUGE to fit noise in the data.
  We need to PENALIZE large weights to keep the model simple.

THE SOLUTION:
  Add a penalty to the loss function:

  Original loss:   L = (1/n) Σ (ŷᵢ - yᵢ)²              ← MSE
  Ridge (L2):      L = (1/n) Σ (ŷᵢ - yᵢ)² + λ Σ wⱼ²    ← MSE + sum of squared weights
  Lasso (L1):      L = (1/n) Σ (ŷᵢ - yᵢ)² + λ Σ |wⱼ|   ← MSE + sum of absolute weights

  λ (lambda) controls how much we penalize:
    λ = 0    → no penalty → regular regression (overfits)
    λ = big  → heavy penalty → all weights shrink toward 0 (underfits)

KEY DIFFERENCE:
  Ridge (L2): shrinks ALL weights toward zero, but never exactly zero
  Lasso (L1): pushes some weights to EXACTLY zero → feature selection!

  Why? Look at the gradients:
    Ridge gradient:  dw += 2λ * w      ← proportional to w. Small w → small push
    Lasso gradient:  dw += λ * sign(w) ← constant push regardless of w size
                                          keeps pushing until w hits exactly 0

WHEN TO USE:
  Ridge: when you think ALL features matter but some need to be smaller
  Lasso: when you think SOME features are irrelevant and should be eliminated
  ElasticNet: both combined (λ₁|w| + λ₂w²) — best of both worlds
"""
import numpy as np

np.random.seed(42)

# ── Data: y = 2*x₁ + 0*x₂ + 0*x₃ + noise ──
# x₂ and x₃ are IRRELEVANT features (just noise)
n = 50
X = np.random.randn(n, 3)
y = 2 * X[:, 0] + np.random.randn(n) * 0.5  # only x₁ matters

print("=" * 60)
print("DATA: y = 2*x₁ + 0*x₂ + 0*x₃ + noise")
print("True weights: [2.0, 0.0, 0.0]")
print("x₂ and x₃ are IRRELEVANT — good model should ignore them")
print("=" * 60)


# ── Plain Linear Regression (no regularization) ──
def fit_linear(X, y, lr=0.01, epochs=500):
    w = np.zeros(X.shape[1])
    b = 0.0
    for epoch in range(epochs):
        pred = X @ w + b
        error = pred - y
        dw = (2 / len(X)) * X.T @ error
        db = (2 / len(X)) * np.sum(error)
        w -= lr * dw
        b -= lr * db
    return w, b


# ── Ridge: add λ * Σ wⱼ² to loss ──
def fit_ridge(X, y, lam=1.0, lr=0.01, epochs=500):
    w = np.zeros(X.shape[1])
    b = 0.0
    for epoch in range(epochs):
        pred = X @ w + b
        error = pred - y
        dw = (2 / len(X)) * X.T @ error + 2 * lam * w   # ← only this changes
        db = (2 / len(X)) * np.sum(error)                 # b is NOT regularized
        w -= lr * dw
        b -= lr * db
    return w, b


# ── Lasso: add λ * Σ |wⱼ| to loss ──
def fit_lasso(X, y, lam=1.0, lr=0.01, epochs=500):
    w = np.zeros(X.shape[1])
    b = 0.0
    for epoch in range(epochs):
        pred = X @ w + b
        error = pred - y
        dw = (2 / len(X)) * X.T @ error + lam * np.sign(w)  # ← only this changes
        db = (2 / len(X)) * np.sum(error)
        w -= lr * dw
        b -= lr * db
    return w, b


# ── Compare all three ──
print(f"\n{'─' * 60}")
print("LINEAR REGRESSION (no regularization)")
print(f"{'─' * 60}")
w, b = fit_linear(X, y)
print(f"  Weights: [{w[0]:.4f}, {w[1]:.4f}, {w[2]:.4f}]")
print(f"  x₂ and x₃ weights are small but NOT zero")

print(f"\n{'─' * 60}")
print("RIDGE (L2) — λ = 0.1")
print(f"{'─' * 60}")
w_r, b_r = fit_ridge(X, y, lam=0.1)
print(f"  Weights: [{w_r[0]:.4f}, {w_r[1]:.4f}, {w_r[2]:.4f}]")
print(f"  ALL weights shrunk toward 0, but none are exactly 0")

print(f"\n{'─' * 60}")
print("LASSO (L1) — λ = 0.1")
print(f"{'─' * 60}")
w_l, b_l = fit_lasso(X, y, lam=0.1)
print(f"  Weights: [{w_l[0]:.4f}, {w_l[1]:.4f}, {w_l[2]:.4f}]")
print(f"  x₂ and x₃ pushed to ~0 → Lasso does FEATURE SELECTION")

# ── Show effect of different λ ──
print(f"\n{'=' * 60}")
print("EFFECT OF λ (lambda)")
print(f"{'=' * 60}")
print(f"\n  {'λ':>6}  {'Ridge w':>24}  {'Lasso w':>24}")
print(f"  {'─'*6}  {'─'*24}  {'─'*24}")

for lam in [0.0, 0.01, 0.1, 0.5, 1.0]:
    w_r, _ = fit_ridge(X, y, lam=lam)
    w_l, _ = fit_lasso(X, y, lam=lam)
    print(f"  {lam:>6.2f}  [{w_r[0]:>6.3f}, {w_r[1]:>6.3f}, {w_r[2]:>6.3f}]"
          f"  [{w_l[0]:>6.3f}, {w_l[1]:>6.3f}, {w_l[2]:>6.3f}]")

print(f"  (true weights: [2.0, 0.0, 0.0])")
print(f"  Notice: as λ grows, Ridge shrinks everything evenly.")
print(f"  Lasso kills irrelevant features first, preserves important ones.")


# ================================================================
# LOGISTIC REGRESSION with regularization
# ================================================================
print(f"\n{'=' * 60}")
print("REGULARIZATION IN LOGISTIC REGRESSION")
print("=" * 60)
print("""
  Exact same idea. Just add the penalty to cross-entropy loss:

  Plain:  L = -(1/n) Σ [y·log(ŷ) + (1-y)·log(1-ŷ)]
  Ridge:  L = -(1/n) Σ [y·log(ŷ) + (1-y)·log(1-ŷ)] + λ Σ wⱼ²
  Lasso:  L = -(1/n) Σ [y·log(ŷ) + (1-y)·log(1-ŷ)] + λ Σ |wⱼ|

  The gradient change is IDENTICAL:
    Ridge: dw += 2λ * w
    Lasso: dw += λ * sign(w)
""")


def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))


# Classification data: 2 relevant features, 2 irrelevant
np.random.seed(42)
n = 100
X_cls = np.random.randn(n, 4)
y_cls = (2 * X_cls[:, 0] - 1.5 * X_cls[:, 1] > 0).astype(float)  # only x₁, x₂ matter


def fit_logistic(X, y, lam=0.0, penalty='none', lr=0.01, epochs=500):
    w = np.zeros(X.shape[1])
    b = 0.0
    for epoch in range(epochs):
        pred = sigmoid(X @ w + b)
        error = pred - y
        dw = (1 / len(X)) * X.T @ error

        # THE ONLY DIFFERENCE: add penalty gradient
        if penalty == 'l2':
            dw += 2 * lam * w
        elif penalty == 'l1':
            dw += lam * np.sign(w)

        db = (1 / len(X)) * np.sum(error)
        w -= lr * dw
        b -= lr * db
    return w, b


print("Data: y depends on x₁ and x₂ only. x₃, x₄ are irrelevant.")
print("True pattern: 2*x₁ - 1.5*x₂ > 0\n")

for penalty, lam in [('none', 0), ('l2', 0.1), ('l1', 0.1)]:
    w, b = fit_logistic(X_cls, y_cls, lam=lam, penalty=penalty)
    name = f"{'Plain':>5}" if penalty == 'none' else f"{penalty.upper():>5}"
    print(f"  {name}: w=[{w[0]:>6.3f}, {w[1]:>6.3f}, {w[2]:>6.3f}, {w[3]:>6.3f}]"
          f"  (x₃,x₄ should be ~0)")

print(f"""
{'=' * 60}
SUMMARY
{'=' * 60}

  ┌────────────────┬─────────────────────┬──────────────────────┐
  │                │ RIDGE (L2)          │ LASSO (L1)           │
  ├────────────────┼─────────────────────┼──────────────────────┤
  │ Penalty        │ λ Σ wⱼ²            │ λ Σ |wⱼ|            │
  │ Gradient       │ dw += 2λw           │ dw += λ·sign(w)      │
  │ Effect         │ Shrinks all weights │ Kills some to zero   │
  │ Feature select │ No                  │ Yes                  │
  │ Correlated     │ Keeps all, splits   │ Picks one, drops     │
  │ features       │ weight among them   │ the rest             │
  │ Use when       │ All features matter │ Some are irrelevant  │
  │ Computation    │ Has closed form     │ No closed form       │
  └────────────────┴─────────────────────┴──────────────────────┘

  Works with: Linear Regression, Logistic Regression, SVM, Neural Nets
  The gradient change is always the same 1 line:
    Ridge: dw += 2λ * w
    Lasso: dw += λ * sign(w)
""")