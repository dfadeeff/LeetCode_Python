"""
XGBOOST (simplified) — Gradient Boosted Trees.

Random Forest: build trees INDEPENDENTLY, then vote (parallel).
XGBoost:       build trees ONE AT A TIME, each fixing the PREVIOUS tree's mistakes (sequential).

Analogy:
  Random Forest = 100 students take a test independently, average their answers.
  XGBoost       = Student 1 takes the test. Student 2 sees student 1's MISTAKES
                  and focuses on fixing those. Student 3 fixes student 2's
                  remaining mistakes. And so on.

Algorithm:
  1. Start with a simple prediction (e.g., average of all y)
  2. Compute RESIDUALS = actual - prediction (what we got wrong)
  3. Train a small tree to predict the RESIDUALS
  4. Add that tree's predictions (scaled by learning rate) to our model
  5. Repeat: compute new residuals, train new tree on them

Each tree is SMALL (a "weak learner") — typically depth 3-6.
The magic is in the SEQUENTIAL correction of errors.
"""
import numpy as np

np.random.seed(42)

# ── 8 houses: [size] → price ──  (regression, not classification)
X = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)  # size (100s sqft)
Y = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=float)   # price (100k)
# Add noise to make it interesting
Y = Y + np.array([0.5, -0.3, 0.8, -0.2, 0.1, -0.4, 0.6, -0.1])

print("=" * 60)
print("XGBOOST (simplified) on house prices")
print("=" * 60)
print(f"\n  {'Size':>6}  {'Price':>6}")
print(f"  {'─' * 6}  {'─' * 6}")
for i in range(len(X)):
    print(f"  {X[i]:>6.0f}  {Y[i]:>6.1f}")


def build_stump_regression(X, residuals):
    """Find the best split point. Predict mean residual on each side."""
    best_mse = float('inf')
    best_thresh = None
    best_left_val = None
    best_right_val = None

    for thresh in X:
        left_mask = X <= thresh
        right_mask = ~left_mask
        if left_mask.sum() == 0 or right_mask.sum() == 0:
            continue

        left_val = residuals[left_mask].mean()
        right_val = residuals[right_mask].mean()

        left_mse = np.mean((residuals[left_mask] - left_val) ** 2)
        right_mse = np.mean((residuals[right_mask] - right_val) ** 2)
        total_mse = (left_mask.sum() * left_mse + right_mask.sum() * right_mse) / len(X)

        if total_mse < best_mse:
            best_mse = total_mse
            best_thresh = thresh
            best_left_val = left_val
            best_right_val = right_val

    return best_thresh, best_left_val, best_right_val


def predict_stump(X, thresh, left_val, right_val):
    preds = np.where(X <= thresh, left_val, right_val)
    return preds


# ── Step 0: start with the average ──
prediction = np.full(len(X), Y.mean())
learning_rate = 0.3
n_trees = 5
trees = []

print(f"\n  Initial prediction for everything: mean(Y) = {Y.mean():.2f}")
print(f"  Learning rate: {learning_rate}")

for t in range(n_trees):
    print(f"\n{'─' * 60}")
    print(f"TREE {t + 1}")
    print(f"{'─' * 60}")

    # 1. Compute residuals (what are we getting wrong?)
    residuals = Y - prediction
    mse = np.mean(residuals ** 2)

    print(f"\n  [RESIDUALS] actual - prediction = what we still need to fix")
    print(f"  {'Size':>6}  {'Actual':>7}  {'Predict':>8}  {'Residual':>9}")
    print(f"  {'─' * 6}  {'─' * 7}  {'─' * 8}  {'─' * 9}")
    for i in range(len(X)):
        print(f"  {X[i]:>6.0f}  {Y[i]:>7.1f}  {prediction[i]:>8.2f}  {residuals[i]:>+9.2f}")
    print(f"  MSE = {mse:.4f}")

    # 2. Train a stump to predict residuals
    thresh, left_val, right_val = build_stump_regression(X, residuals)
    trees.append((thresh, left_val, right_val))

    print(f"\n  [FIT TREE on residuals] Best split: size <= {thresh:.0f}?")
    print(f"    YES → predict residual {left_val:+.3f}")
    print(f"    NO  → predict residual {right_val:+.3f}")

    # 3. Update prediction: add tree's correction (scaled by learning rate)
    tree_pred = predict_stump(X, thresh, left_val, right_val)
    correction = learning_rate * tree_pred

    print(f"\n  [UPDATE] prediction += {learning_rate} × tree_prediction")
    print(f"  {'Size':>6}  {'Old pred':>9}  {'Correction':>11}  {'New pred':>9}")
    print(f"  {'─' * 6}  {'─' * 9}  {'─' * 11}  {'─' * 9}")
    for i in range(len(X)):
        print(f"  {X[i]:>6.0f}  {prediction[i]:>9.2f}  {correction[i]:>+11.3f}  {prediction[i] + correction[i]:>9.2f}")

    prediction += correction

# ── Final result ──
final_mse = np.mean((Y - prediction) ** 2)
print(f"\n{'=' * 60}")
print(f"FINAL RESULT after {n_trees} trees")
print(f"{'=' * 60}")
print(f"\n  {'Size':>6}  {'Actual':>7}  {'Predicted':>10}  {'Error':>7}")
print(f"  {'─' * 6}  {'─' * 7}  {'─' * 10}  {'─' * 7}")
for i in range(len(X)):
    print(f"  {X[i]:>6.0f}  {Y[i]:>7.1f}  {prediction[i]:>10.2f}  {Y[i] - prediction[i]:>+7.2f}")
print(f"\n  Final MSE: {final_mse:.4f}")
print(f"  Started at MSE: {np.mean((Y - Y.mean()) ** 2):.4f} (just predicting the mean)")

print(f"""
{'=' * 60}
RECIPE:
{'=' * 60}

  prediction = mean(Y)                     # start simple
  for each tree:
      residuals = Y - prediction            # what's left to fix
      tree = fit small tree on residuals     # learn the errors
      prediction += lr * tree(X)            # add correction

  That's it. Each tree fixes the previous mistakes.

KEY DIFFERENCES FROM RANDOM FOREST:
  ┌─────────────────┬──────────────────────┬──────────────────────┐
  │                 │ Random Forest        │ XGBoost              │
  ├─────────────────┼──────────────────────┼──────────────────────┤
  │ Trees built     │ Independently        │ Sequentially         │
  │ Each tree fits  │ Original data        │ Residuals (errors)   │
  │ Combination     │ Average / vote       │ Sum of corrections   │
  │ Tree size       │ Full depth           │ Shallow (3-6)        │
  │ Parallelizable  │ Yes (embarrassingly) │ No (sequential)      │
  │ Risk            │ Less overfit         │ Can overfit if too   │
  │                 │                      │ many trees           │
  └─────────────────┴──────────────────────┴──────────────────────┘

  In practice, XGBoost usually wins on tabular data.
""")