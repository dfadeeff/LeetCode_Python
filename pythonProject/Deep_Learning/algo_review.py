"""
ALGO REVIEW — Code from memory in <5 minutes each
===================================================
Interview focus: implement, explain convergence, evaluate, discuss tradeoffs.
"""
import numpy as np


# ══════════════════════════════════════════════════════════════
# 1. LINEAR REGRESSION (Gradient Descent)
# ══════════════════════════════════════════════════════════════
# Model:  y = X @ w + b
# Loss:   MSE = (1/n) Σ (y_pred - y)²
# Gradient: dw = (1/n) X^T @ error,  db = (1/n) Σ error
# Convergence: stop when loss change < tol
# Evaluate: RMSE, R²
# Overfit prevention: regularization (ridge: + λ||w||²)

class LinearRegression:
    def __init__(self, lr=0.01, epochs=1000, tol=1e-6):
        self.lr = lr
        self.epochs = epochs
        self.tol = tol
        self.w = None
        self.b = 0.0
        self.losses = []

    def fit(self, X, y):
        n, d = X.shape
        self.w = np.zeros(d)
        self.b = 0.0
        self.losses = []

        for epoch in range(self.epochs):
            y_pred = X @ self.w + self.b
            loss = np.mean((y_pred - y) ** 2)
            self.losses.append(loss)

            # convergence check
            if epoch > 0 and abs(self.losses[-2] - self.losses[-1]) < self.tol:
                print(f"  Converged at epoch {epoch}, MSE={loss:.6f}")
                break

            error = y_pred - y
            dw = (1 / n) * X.T @ error
            db = (1 / n) * np.sum(error)
            self.w -= self.lr * dw
            self.b -= self.lr * db

    def predict(self, X):
        return X @ self.w + self.b


# ══════════════════════════════════════════════════════════════
# 2. LOGISTIC REGRESSION
# ══════════════════════════════════════════════════════════════
# Model:  y = sigmoid(X @ w + b)       → output in [0, 1]
# Sigmoid: 1 / (1 + exp(-z))
# Loss:   BCE = -(1/n) Σ [y*log(p) + (1-y)*log(1-p)]
# Gradient: SAME as linear regression!  dw = (1/n) X^T @ (p - y)
# Predict: if sigmoid > 0.5 → class 1
# Evaluate: accuracy, precision, recall, F1, confusion matrix

class LogisticRegression:
    def __init__(self, lr=0.01, epochs=1000, tol=1e-6):
        self.lr = lr
        self.epochs = epochs
        self.tol = tol
        self.w = None
        self.b = 0.0
        self.losses = []

    def _sigmoid(self, z):
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        n, d = X.shape
        self.w = np.zeros(d)
        self.b = 0.0
        self.losses = []

        for epoch in range(self.epochs):
            z = X @ self.w + self.b
            y_pred = self._sigmoid(z)

            # BCE loss
            eps = 1e-9
            loss = -np.mean(y * np.log(y_pred + eps) + (1 - y) * np.log(1 - y_pred + eps))
            self.losses.append(loss)

            # convergence check
            if epoch > 0 and abs(self.losses[-2] - self.losses[-1]) < self.tol:
                print(f"  Converged at epoch {epoch}, BCE={loss:.6f}")
                break

            error = y_pred - y
            dw = (1 / n) * X.T @ error
            db = (1 / n) * np.sum(error)
            self.w -= self.lr * dw
            self.b -= self.lr * db

    def predict_proba(self, X):
        return self._sigmoid(X @ self.w + self.b)

    def predict(self, X):
        return (self.predict_proba(X) > 0.5).astype(int)


# ══════════════════════════════════════════════════════════════
# EVALUATION FUNCTIONS
# ══════════════════════════════════════════════════════════════

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

def r_squared(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - ss_res / ss_tot

def accuracy(y_true, y_pred):
    return np.mean(y_true == y_pred)

def confusion_matrix(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return tp, tn, fp, fn


# ══════════════════════════════════════════════════════════════
# DEMOS WITH TOY DATASETS (you generate these in the interview)
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    np.random.seed(42)

    # --- LINEAR REGRESSION DEMO ---
    print("=" * 50)
    print("LINEAR REGRESSION")
    print("=" * 50)

    # Generate toy dataset: y = 3x1 + 5x2 + noise
    n = 100
    X_reg = np.random.randn(n, 2)
    y_reg = 3 * X_reg[:, 0] + 5 * X_reg[:, 1] + np.random.randn(n) * 0.5

    # Train/test split (80/20)
    split = 80
    X_train, X_test = X_reg[:split], X_reg[split:]
    y_train, y_test = y_reg[:split], y_reg[split:]

    model = LinearRegression(lr=0.01, epochs=5000)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    print(f"  Learned weights: {model.w}  (should be ~[3, 5])")
    print(f"  Learned bias:    {model.b:.4f}  (should be ~0)")
    print(f"  RMSE:  {rmse(y_test, preds):.4f}")
    print(f"  R²:    {r_squared(y_test, preds):.4f}")
    print(f"  Epochs: {len(model.losses)}")

    # --- LOGISTIC REGRESSION DEMO ---
    print()
    print("=" * 50)
    print("LOGISTIC REGRESSION")
    print("=" * 50)

    # Generate toy dataset: 2 classes, 2 features
    n = 200
    X_class0 = np.random.randn(n // 2, 2) + np.array([-1, -1])
    X_class1 = np.random.randn(n // 2, 2) + np.array([1, 1])
    X_cls = np.vstack([X_class0, X_class1])
    y_cls = np.array([0] * (n // 2) + [1] * (n // 2))

    # Shuffle
    idx = np.random.permutation(n)
    X_cls, y_cls = X_cls[idx], y_cls[idx]

    # Train/test split
    split = 160
    X_train, X_test = X_cls[:split], X_cls[split:]
    y_train, y_test = y_cls[:split], y_cls[split:]

    model = LogisticRegression(lr=0.1, epochs=1000)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    tp, tn, fp, fn = confusion_matrix(y_test, preds)
    print(f"  Accuracy:  {accuracy(y_test, preds):.3f}")
    print(f"  TP={tp}, TN={tn}, FP={fp}, FN={fn}")
    print(f"  Precision: {tp / (tp + fp):.3f}")
    print(f"  Recall:    {tp / (tp + fn):.3f}")
    print(f"  Epochs: {len(model.losses)}")