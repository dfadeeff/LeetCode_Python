"""
SVM — Linear and Kernel, same class structure.
The ONLY difference between linear and kernel SVM is ONE function: the dot product.
"""
import numpy as np


# ================================================================
# LINEAR SVM
# ================================================================
class LinearSVM:
    def __init__(self, C=1.0, lr=0.01, epochs=300):
        self.C = C          # penalty for misclassification
        self.lr = lr
        self.epochs = epochs
        self.w = None
        self.b = 0.0

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)
        self.b = 0.0

        for epoch in range(self.epochs):
            for i in range(n_samples):
                # margin: how confident? want y_i * (w·x_i + b) >= 1
                margin = y[i] * (np.dot(self.w, X[i]) + self.b)

                if margin >= 1:
                    # correct & confident → just shrink w (widen margin)
                    self.w -= self.lr * self.w
                else:
                    # wrong or too close → fix it
                    self.w -= self.lr * (self.w - self.C * y[i] * X[i])
                    self.b += self.lr * self.C * y[i]

    def predict(self, X):
        scores = X @ self.w + self.b
        return np.sign(scores).astype(int)


# ================================================================
# KERNEL SVM
# ================================================================
# What changes? Instead of learning w (a vector), we learn alpha (one weight
# per training point). Prediction becomes:
#
#   LINEAR:  sign(w · x + b)              ← one dot product
#   KERNEL:  sign(Σ αᵢyᵢK(xᵢ, x) + b)   ← sum over support vectors
#
# The kernel K replaces the dot product. That's the ONLY change.
# ================================================================
class KernelSVM:
    def __init__(self, C=1.0, lr=0.01, epochs=500, kernel='rbf', gamma=0.5):
        self.C = C
        self.lr = lr
        self.epochs = epochs
        self.gamma = gamma
        self.kernel = kernel
        self.alpha = None      # ← replaces self.w
        self.b = 0.0
        self.X_train = None    # must store training data for prediction
        self.y_train = None

    def _kernel(self, X1, X2):
        """THE key function. Swap this to change the SVM type."""
        if self.kernel == 'linear':
            return X1 @ X2.T
        elif self.kernel == 'rbf':
            # K(x,z) = exp(-gamma * ||x-z||²)
            sq1 = np.sum(X1 ** 2, axis=1).reshape(-1, 1)
            sq2 = np.sum(X2 ** 2, axis=1).reshape(1, -1)
            dists = sq1 + sq2 - 2 * X1 @ X2.T
            return np.exp(-self.gamma * dists)

    def fit(self, X, y):
        n_samples = len(X)
        self.X_train = X
        self.y_train = y
        self.alpha = np.zeros(n_samples)
        self.b = 0.0

        # precompute kernel matrix: K[i,j] = kernel(x_i, x_j)
        K = self._kernel(X, X)

        for epoch in range(self.epochs):
            for i in range(n_samples):
                # prediction for point i using all other points
                decision = np.sum(self.alpha * y * K[i]) + self.b
                margin = y[i] * decision

                if margin < 1:
                    self.alpha[i] += self.lr * (1 - margin)
                    self.alpha[i] = np.clip(self.alpha[i], 0, self.C)
                    self.b += self.lr * y[i] * (1 - margin)

    def predict(self, X):
        # K between new points and ALL training points
        K = self._kernel(X, self.X_train)
        # Σ αᵢyᵢK(xᵢ, x) + b
        scores = K @ (self.alpha * self.y_train) + self.b
        return np.sign(scores).astype(int)


# ================================================================
# TEST: Linear data → both work
# ================================================================
if __name__ == "__main__":
    np.random.seed(42)

    # ── Linearly separable data ──
    X_train = np.array([
        [1.0, 2.0], [2.0, 3.0], [1.5, 1.5], [2.0, 1.0], [1.0, 0.5],
        [5.0, 5.0], [6.0, 4.0], [5.5, 5.5], [4.5, 4.0], [6.0, 6.0],
    ])
    y_train = np.array([-1, -1, -1, -1, -1, 1, 1, 1, 1, 1])

    print("=" * 55)
    print("TEST 1: Linearly separable data")
    print("=" * 55)

    linear = LinearSVM(C=1.0, lr=0.01, epochs=300)
    linear.fit(X_train, y_train)
    preds = linear.predict(X_train)
    print(f"\n  Linear SVM:  accuracy = {np.mean(preds == y_train):.0%}")
    print(f"  w = [{linear.w[0]:.3f}, {linear.w[1]:.3f}], b = {linear.b:.3f}")

    kernel_lin = KernelSVM(C=1.0, lr=0.01, epochs=300, kernel='linear')
    kernel_lin.fit(X_train, y_train)
    preds2 = kernel_lin.predict(X_train)
    print(f"  Kernel(linear): accuracy = {np.mean(preds2 == y_train):.0%}")

    kernel_rbf = KernelSVM(C=1.0, lr=0.01, epochs=300, kernel='rbf', gamma=0.5)
    kernel_rbf.fit(X_train, y_train)
    preds3 = kernel_rbf.predict(X_train)
    print(f"  Kernel(RBF):    accuracy = {np.mean(preds3 == y_train):.0%}")

    # ── Circular data (NOT linearly separable) ──
    print(f"\n{'=' * 55}")
    print("TEST 2: Circular data (NOT linearly separable)")
    print("=" * 55)
    print("\n  Inner ring = class -1, Outer ring = class +1")
    print("  A straight line CANNOT separate them.\n")

    angles = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    X_inner = 1.0 * np.column_stack([np.cos(angles), np.sin(angles)])
    X_outer = 3.0 * np.column_stack([np.cos(angles), np.sin(angles)])
    X_circle = np.vstack([X_inner, X_outer])
    y_circle = np.array([-1] * 8 + [1] * 8)

    linear2 = LinearSVM(C=1.0, lr=0.01, epochs=500)
    linear2.fit(X_circle, y_circle)
    preds_lin = linear2.predict(X_circle)
    print(f"  Linear SVM:  accuracy = {np.mean(preds_lin == y_circle):.0%}  ← FAILS")

    kernel_rbf2 = KernelSVM(C=10.0, lr=0.01, epochs=500, kernel='rbf', gamma=0.5)
    kernel_rbf2.fit(X_circle, y_circle)
    preds_rbf = kernel_rbf2.predict(X_circle)
    print(f"  Kernel(RBF): accuracy = {np.mean(preds_rbf == y_circle):.0%}  ← WORKS")

    # Show predictions on new points
    print(f"\n  New point predictions (RBF kernel):")
    test_pts = np.array([[0.0, 0.0], [0.5, 0.5], [2.0, 2.0], [3.0, 0.0]])
    test_preds = kernel_rbf2.predict(test_pts)
    for i in range(len(test_pts)):
        dist = np.sqrt(test_pts[i][0]**2 + test_pts[i][1]**2)
        label = "inner" if test_preds[i] <= 0 else "outer"
        print(f"    [{test_pts[i][0]:>4.1f}, {test_pts[i][1]:>4.1f}]"
              f"  dist={dist:.1f}  → {label}")

    print(f"""
{'=' * 55}
WHAT CHANGED: Linear → Kernel
{'=' * 55}

  LINEAR SVM:
    learns:   w (one weight per feature)
    predicts: sign(w · x + b)
    boundary: a straight line

  KERNEL SVM:
    learns:   alpha (one weight per TRAINING POINT)
    predicts: sign(Σ αᵢyᵢK(xᵢ, x) + b)
    boundary: any shape (depends on kernel)

  The ONLY real change:
    dot product x·z  →  kernel function K(x, z)

  Everything else (loss, margin, gradient) stays the same idea.

  ┌────────────────────────────────────────────────┐
  │  LinearSVM                KernelSVM            │
  │  ─────────                ──────────           │
  │  self.w = zeros(feats)    self.alpha = zeros(n)│
  │  w · x                    Σ αᵢyᵢK(xᵢ, x)     │
  │  update w                 update alpha         │
  │  predict: w·x + b         predict: K @ (α*y)+b │
  └────────────────────────────────────────────────┘
""")