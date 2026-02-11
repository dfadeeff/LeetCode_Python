import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets

# ============================================================
# LOGISTIC REGRESSION FROM SCRATCH
# ============================================================
# Same as linear regression, but for CLASSIFICATION (0 or 1).
#
# Linear regression:   ŷ = w · x + b              → any number
# Logistic regression: ŷ = sigmoid(w · x + b)     → between 0 and 1
#                                                    (interpreted as probability)
#
# The sigmoid squashes any number into [0, 1]:
#   sigmoid(z) = 1 / (1 + e^(-z))
#   sigmoid(-∞) → 0,  sigmoid(0) = 0.5,  sigmoid(+∞) → 1
#
# Loss: Binary Cross-Entropy (not MSE!)
#   L = -(1/n) * Σ [ y_i * log(ŷ_i) + (1-y_i) * log(1-ŷ_i) ]
#
#   Why not MSE? MSE + sigmoid creates a non-convex loss surface
#   with many local minima. BCE is convex → guaranteed to find optimum.
#
# Gradient (surprisingly same shape as linear regression!):
#   dw = (1/n) * X^T · (ŷ - y)
#   db = (1/n) * Σ(ŷ - y)
#
# Prediction: if sigmoid output > 0.5 → class 1, else → class 0
# ============================================================


class LogisticRegression:
    def __init__(self, lr=0.001, epochs=1000, tol=1e-6):
        self.lr = lr
        self.epochs = epochs
        self.tol = tol
        self.w = None       # weight vector, shape (n_features,)
        self.b = 0.0        # bias scalar
        self.losses = []

    def _sigmoid(self, z):
        # squash any number to [0, 1]
        # clip z to avoid overflow in exp
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        n_samples, n_features = X.shape

        # initialize weights to zero
        self.w = np.zeros(n_features)
        self.b = 0.0
        self.losses = []

        for epoch in range(self.epochs):
            # STEP 1: linear combination, same as linear regression
            z = X @ self.w + self.b

            # STEP 2: sigmoid — this is the ONLY difference from linear regression
            y_pred = self._sigmoid(z)

            # STEP 3: binary cross-entropy loss
            # y=1: we want y_pred close to 1 → -log(y_pred) is small
            # y=0: we want y_pred close to 0 → -log(1-y_pred) is small
            eps = 1e-9  # avoid log(0)
            loss = -np.mean(y * np.log(y_pred + eps) + (1 - y) * np.log(1 - y_pred + eps))
            self.losses.append(loss)

            # STEP 4: convergence check
            if epoch > 0 and abs(self.losses[-1] - self.losses[-2]) < self.tol:
                print(f"Converged at epoch {epoch}, loss={loss:.4f}")
                break

            # STEP 5: gradients — exact same formula as linear regression
            # (the sigmoid derivative cancels out nicely with BCE derivative)
            error = y_pred - y
            dw = (1 / n_samples) * X.T @ error
            db = (1 / n_samples) * np.sum(error)

            # STEP 6: update weights
            self.w -= self.lr * dw
            self.b -= self.lr * db

    def predict_proba(self, X):
        # raw probabilities
        return self._sigmoid(X @ self.w + self.b)

    def predict(self, X):
        # threshold at 0.5: probability > 0.5 → class 1
        return (self.predict_proba(X) > 0.5).astype(int)


# ============================================================
# EVALUATION — Classification metrics
# ============================================================
# Accuracy:  % of correct predictions (misleading if classes imbalanced)
# Precision: of all predicted 1s, how many were actually 1? (TP / (TP+FP))
# Recall:    of all actual 1s, how many did we catch?       (TP / (TP+FN))
# F1:        harmonic mean of precision and recall
# ============================================================

def confusion_matrix(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return tp, tn, fp, fn


def accuracy(y_true, y_pred):
    return np.mean(y_true == y_pred)


def precision(tp, fp):
    return tp / (tp + fp) if (tp + fp) > 0 else 0


def recall(tp, fn):
    return tp / (tp + fn) if (tp + fn) > 0 else 0


def f1_score(prec, rec):
    return 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0


# ============================================================
# RUN — Breast cancer dataset (569 samples, 30 features, binary: malignant/benign)
# ============================================================

if __name__ == "__main__":
    dataset = datasets.load_breast_cancer()
    X, y = dataset.data, dataset.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=1234
    )

    model = LogisticRegression(lr=0.0001, epochs=1000)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    tp, tn, fp, fn = confusion_matrix(y_test, preds)
    prec = precision(tp, fp)
    rec = recall(tp, fn)
    f1 = f1_score(prec, rec)

    print("=== Logistic Regression ===")
    print(f"Accuracy:  {accuracy(y_test, preds):.3f}")
    print(f"Precision: {prec:.3f}")
    print(f"Recall:    {rec:.3f}")
    print(f"F1 Score:  {f1:.3f}")
    print(f"Confusion Matrix: TP={tp}, TN={tn}, FP={fp}, FN={fn}")
    print(f"Epochs: {len(model.losses)}")