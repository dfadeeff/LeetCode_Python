import numpy as np
from regression_dataset import X_train, X_test, y_train, y_test

# ============================================================
# LINEAR REGRESSION FROM SCRATCH
# ============================================================
# Model:  y = b0 + b1 * x   (one feature)
#
# Data: Swedish insurance — X = number of claims, y = total payment (€1000s)
# Goal: find b0 (intercept) and b1 (slope) that minimize prediction error
#
# Two methods:
#   1. Closed-form — exact formula, instant, only works for 1 feature
#   2. Gradient descent — iterative, works for any # of features
# ============================================================


# ============================================================
# METHOD 1: CLOSED-FORM (OLS)
# ============================================================
# Formula derived by setting derivative of MSE to zero and solving:
#
#   b1 = Σ(xi - x̄)(yi - ȳ) / Σ(xi - x̄)²
#        ^^^^^^^^^^^^^^^^       ^^^^^^^^^^^
#        covariance(x, y)       variance(x)
#
#   b1 = "for each unit increase in x, how much does y change?"
#
#   b0 = ȳ - b1 * x̄
#   b0 = "what is y when x = 0?" (shifts the line vertically)
# ============================================================

class LinearRegressionClosedForm:
    def __init__(self):
        self.b0 = 0  # intercept (where line crosses y-axis)
        self.b1 = 0  # slope (rise over run)

    def fit(self, X, y):
        x_mean = np.mean(X)    # average number of claims
        y_mean = np.mean(y)    # average payment

        # numerator: how X and y move TOGETHER (covariance)
        # denominator: how much X varies on its own (variance)
        # ratio = how much y changes per unit of x
        self.b1 = np.sum((X - x_mean) * (y - y_mean)) / np.sum((X - x_mean) ** 2)

        # intercept: adjust so the line passes through (x_mean, y_mean)
        self.b0 = y_mean - self.b1 * x_mean

    def predict(self, X):
        # y = b0 + b1 * x
        return self.b0 + self.b1 * X


# ============================================================
# METHOD 2: GRADIENT DESCENT
# ============================================================
# Instead of a direct formula, we SEARCH for the best b0, b1:
#
#   1. Start with b0=0, b1=0 (bad guess)
#   2. Predict: ŷ = b0 + b1 * x
#   3. Measure error: MSE = (1/n) * Σ(ŷ - y)²
#   4. Ask: "which direction should I nudge b0, b1 to reduce error?"
#      → that direction is the GRADIENT (partial derivatives of MSE)
#   5. Update: move b0, b1 opposite to gradient (downhill)
#   6. Repeat until error stops decreasing
#
# Gradient formulas (from taking derivative of MSE):
#   dL/db1 = (2/n) * Σ (ŷ_i - y_i) * x_i    = (2/n) * X · error
#   dL/db0 = (2/n) * Σ (ŷ_i - y_i)           = (2/n) * sum(error)
#
# Update rule:
#   b1 = b1 - lr * dL/db1   (lr = learning rate = step size)
#   b0 = b0 - lr * dL/db0
#
# WHY MINUS? Gradient points uphill. We want to go downhill.
# ============================================================

class LinearRegressionGD:
    def __init__(self, lr=0.0001, epochs=1000, tol=1e-6):
        self.lr = lr          # learning rate — how big each step is
        self.epochs = epochs  # max number of steps before stopping
        self.tol = tol        # convergence threshold — "close enough"
        self.w = None         # weight (same as b1)
        self.b = 0.0          # bias (same as b0)
        self.losses = []

    def fit(self, X, y):
        n = len(y)

        # initialize weights to zero
        self.w = 0.0
        self.b = 0.0
        self.losses = []

        for epoch in range(self.epochs):
            # STEP 1: predict with current weights
            y_pred = self.w * X + self.b

            # STEP 2: measure how wrong we are (MSE)
            loss = np.mean((y_pred - y) ** 2)
            self.losses.append(loss)

            # STEP 3: convergence — if loss barely changed, stop
            # "How do you know when to stop?" → this is the answer
            if epoch > 0 and abs(self.losses[-1] - self.losses[-2]) < self.tol:
                print(f"Converged at epoch {epoch}, loss={loss:.4f}")
                break

            # STEP 4: compute gradients (which direction to move)
            error = y_pred - y                       # how far off each prediction is
            dw = (2 / n) * np.dot(X, error)          # gradient for weight
            db = (2 / n) * np.sum(error)             # gradient for bias

            # STEP 5: update — take a small step opposite to gradient
            self.w -= self.lr * dw
            self.b -= self.lr * db

    def predict(self, X):
        return self.w * X + self.b


# ============================================================
# EVALUATION
# ============================================================
# RMSE = √(mean of squared errors) — in same units as y
#   Lower = better. RMSE=0 means perfect predictions.
#
# R² = 1 - (unexplained variance / total variance)
#   R²=1.0 → perfect, R²=0 → no better than predicting the mean
# ============================================================

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def r_squared(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)       # error our model makes
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)  # error if we just predicted mean
    return 1 - ss_res / ss_tot


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    # --- Closed Form ---
    m1 = LinearRegressionClosedForm()
    m1.fit(X_train, y_train)
    p1 = m1.predict(X_test)
    print("=== Closed Form ===")
    print(f"b0={m1.b0:.3f}, b1={m1.b1:.3f}")
    print(f"Meaning: payment = {m1.b0:.1f} + {m1.b1:.1f} * claims")
    print(f"RMSE: {rmse(y_test, p1):.3f}")
    print(f"R²:   {r_squared(y_test, p1):.3f}")

    # --- Gradient Descent ---
    m2 = LinearRegressionGD(lr=0.0001, epochs=50000)
    m2.fit(X_train, y_train)
    p2 = m2.predict(X_test)
    print("\n=== Gradient Descent ===")
    print(f"w={m2.w:.3f}, b={m2.b:.3f}")
    print(f"RMSE: {rmse(y_test, p2):.3f}")
    print(f"R²:   {r_squared(y_test, p2):.3f}")
    print(f"Epochs: {len(m2.losses)}")

    # --- Both should find similar b0, b1 ---
    print(f"\n=== Comparison ===")
    print(f"Closed form: slope={m1.b1:.4f}, intercept={m1.b0:.4f}")
    print(f"Grad descent: slope={m2.w:.4f}, intercept={m2.b:.4f}")