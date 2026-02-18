"""
Naive Bayes vs Logistic Regression — simplified side-by-side comparison.
Same tiny dataset, same task, two completely different approaches.
"""
import numpy as np

np.random.seed(42)

# ── 10 patients, 2 features, 2 classes ──────────────────────────
# Features: [temperature, cough_severity]  (both 0-10 scale)
# Label: 0 = healthy, 1 = flu
X = np.array([
    [6.0, 1.0],  # 0 healthy
    [6.2, 0.5],  # 1 healthy
    [6.5, 2.0],  # 2 healthy
    [5.8, 1.5],  # 3 healthy
    [6.1, 0.8],  # 4 healthy
    [9.0, 7.0],  # 5 flu
    [8.5, 8.0],  # 6 flu
    [9.2, 6.5],  # 7 flu
    [8.8, 7.5],  # 8 flu
    [9.5, 8.5],  # 9 flu
])
y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

print("=" * 60)
print("DATASET: 10 patients")
print("=" * 60)
print(f"  {'Patient':>8}  {'Temp':>5}  {'Cough':>6}  {'Label':>6}")
print(f"  {'─' * 8}  {'─' * 5}  {'─' * 6}  {'─' * 6}")
for i in range(len(X)):
    label = "flu" if y[i] == 1 else "healthy"
    print(f"  {i:>8}  {X[i][0]:>5.1f}  {X[i][1]:>6.1f}  {label:>6}")


# ================================================================
#  NAIVE BAYES  (generative: learns what each class "looks like")
# ================================================================
print("\n" + "=" * 60)
print("NAIVE BAYES — Training")
print("=" * 60)
print()
print("  Approach: for each class, compute mean & variance of each feature.")
print("  That's it. No optimization. Just statistics.\n")

means = {}
variances = {}
priors = {}

for k in [0, 1]:
    X_k = X[y == k]
    label = "healthy" if k == 0 else "flu"

    priors[k] = len(X_k) / len(X)
    means[k] = X_k.mean(axis=0)
    variances[k] = X_k.var(axis=0)

    print(f"  Class {k} ({label}): {len(X_k)} patients")
    print(f"    Prior P(y={k}) = {len(X_k)}/{len(X)} = {priors[k]:.1f}")
    print(f"    Temp:  mean={means[k][0]:.2f}  var={variances[k][0]:.2f}")
    print(f"    Cough: mean={means[k][1]:.2f}  var={variances[k][1]:.2f}")
    print()

print("  Done! The 'model' is just these 6 numbers per class.")

# ── Predict a new patient ──
x_new = np.array([8.0, 6.0])
print(f"\n{'─' * 60}")
print(f"  PREDICT: new patient with temp={x_new[0]}, cough={x_new[1]}")
print(f"{'─' * 60}\n")
print("  Use Bayes rule: P(y|x) ∝ P(y) * P(x|y)")
print("  P(x|y) = P(temp|y) * P(cough|y)  ← naive assumption\n")


def gaussian_log_prob(x, mean, var):
    """Log probability of x under Gaussian(mean, var)."""
    return -0.5 * np.log(2 * np.pi * var) - (x - mean) ** 2 / (2 * var)


nb_scores = {}
for k in [0, 1]:
    label = "healthy" if k == 0 else "flu"
    var = variances[k] + 1e-9  # avoid division by zero

    log_prior = np.log(priors[k])
    log_p_temp = gaussian_log_prob(x_new[0], means[k][0], var[0])
    log_p_cough = gaussian_log_prob(x_new[1], means[k][1], var[1])
    log_posterior = log_prior + log_p_temp + log_p_cough

    nb_scores[k] = log_posterior

    print(f"  Class {k} ({label}):")
    print(f"    log P(y={k})                    = {log_prior:>8.4f}")
    print(f"    log P(temp={x_new[0]}  | {label:>7}) = {log_p_temp:>8.4f}"
          f"   (mean={means[k][0]:.1f}, how far is {x_new[0]} from it?)")
    print(f"    log P(cough={x_new[1]} | {label:>7}) = {log_p_cough:>8.4f}"
          f"   (mean={means[k][1]:.1f}, how far is {x_new[1]} from it?)")
    print(f"    log P(y={k}|x) ∝ {log_prior:.4f} + {log_p_temp:.4f} + {log_p_cough:.4f} = {log_posterior:.4f}")
    print()

nb_pred = max(nb_scores, key=nb_scores.get)
nb_label = "healthy" if nb_pred == 0 else "flu"
print(f"  → Naive Bayes predicts: class {nb_pred} ({nb_label})")
print(f"    (class 1 score {nb_scores[1]:.4f} > class 0 score {nb_scores[0]:.4f})")


# ================================================================
#  LOGISTIC REGRESSION  (discriminative: learns decision boundary)
# ================================================================
print("\n" + "=" * 60)
print("LOGISTIC REGRESSION — Training")
print("=" * 60)
print()
print("  Approach: find weights w and bias b such that")
print("  sigmoid(w1*temp + w2*cough + b) predicts the label.")
print("  Requires iterative gradient descent.\n")


def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))


w = np.zeros(2)
b = 0.0
lr = 0.1

print(f"  Starting weights: w=[{w[0]:.2f}, {w[1]:.2f}], b={b:.2f}\n")

for epoch in range(200):
    # Forward: predict probabilities
    z = X @ w + b
    y_pred = sigmoid(z)

    # Loss: binary cross-entropy
    eps = 1e-9
    loss = -np.mean(y * np.log(y_pred + eps) + (1 - y) * np.log(1 - y_pred + eps))

    # Gradients
    error = y_pred - y
    dw = (1 / len(X)) * X.T @ error
    db = (1 / len(X)) * np.sum(error)

    # Update
    w -= lr * dw
    b -= lr * db

    if epoch < 5 or epoch % 50 == 49:
        preds = (y_pred >= 0.5).astype(int)
        acc = np.mean(preds == y)
        print(f"  Epoch {epoch + 1:>3}: loss={loss:.4f}  "
              f"w=[{w[0]:.3f}, {w[1]:.3f}]  b={b:.3f}  "
              f"accuracy={acc:.0%}")

print(f"\n  Final weights: w=[{w[0]:.3f}, {w[1]:.3f}], b={b:.3f}")
print(f"  Meaning: decision = sigmoid({w[0]:.2f}*temp + {w[1]:.2f}*cough + ({b:.2f}))")

# ── Predict same new patient ──
print(f"\n{'─' * 60}")
print(f"  PREDICT: same patient with temp={x_new[0]}, cough={x_new[1]}")
print(f"{'─' * 60}\n")

z_new = w @ x_new + b
p_new = sigmoid(z_new)
lr_pred = 1 if p_new >= 0.5 else 0
lr_label = "healthy" if lr_pred == 0 else "flu"

print(f"  z = {w[0]:.3f}*{x_new[0]} + {w[1]:.3f}*{x_new[1]} + ({b:.3f}) = {z_new:.4f}")
print(f"  P(flu) = sigmoid({z_new:.4f}) = {p_new:.4f}")
print(f"  {p_new:.4f} {'>' if p_new >= 0.5 else '<'} 0.5 → predict class {lr_pred} ({lr_label})")


# ================================================================
#  FINAL COMPARISON
# ================================================================
print("\n" + "=" * 60)
print("COMPARISON")
print("=" * 60)

# Predict all 10 training points with both models
nb_all = []
for i in range(len(X)):
    scores = {}
    for k in [0, 1]:
        var = variances[k] + 1e-9
        lp = np.log(priors[k])
        lp += gaussian_log_prob(X[i][0], means[k][0], var[0])
        lp += gaussian_log_prob(X[i][1], means[k][1], var[1])
        scores[k] = lp
    nb_all.append(max(scores, key=scores.get))
nb_all = np.array(nb_all)

lr_probs = sigmoid(X @ w + b)
lr_all = (lr_probs >= 0.5).astype(int)

print(f"\n  {'Patient':>8}  {'Temp':>5}  {'Cough':>6}  {'True':>6}  {'NB':>4}  {'LR':>4}  {'LR prob':>8}")
print(f"  {'─' * 8}  {'─' * 5}  {'─' * 6}  {'─' * 6}  {'─' * 4}  {'─' * 4}  {'─' * 8}")
for i in range(len(X)):
    true_label = "flu" if y[i] == 1 else "hlth"
    nb_label = "flu" if nb_all[i] == 1 else "hlth"
    lr_label = "flu" if lr_all[i] == 1 else "hlth"
    match_nb = "✓" if nb_all[i] == y[i] else "✗"
    match_lr = "✓" if lr_all[i] == y[i] else "✗"
    print(f"  {i:>8}  {X[i][0]:>5.1f}  {X[i][1]:>6.1f}  {true_label:>6}  "
          f"{nb_label:>3}{match_nb}  {lr_label:>3}{match_lr}  {lr_probs[i]:>8.4f}")

nb_acc = np.mean(nb_all == y)
lr_acc = np.mean(lr_all == y)
print(f"\n  Naive Bayes accuracy:        {nb_acc:.0%}")
print(f"  Logistic Regression accuracy: {lr_acc:.0%}")

print(f"""
{'─' * 60}
KEY TAKEAWAYS
{'─' * 60}

  NAIVE BAYES (generative):
    • Learned what healthy/flu patients LOOK LIKE (mean & variance)
    • Training = just compute statistics (instant, no iterations)
    • Predicts by asking: "which class does this patient resemble?"
    • Assumes features are independent (temp & cough unrelated)

  LOGISTIC REGRESSION (discriminative):
    • Learned a DECISION BOUNDARY (w1*temp + w2*cough + b = 0)
    • Training = gradient descent (200 iterations)
    • Predicts by checking which side of the boundary the point falls
    • No assumption about feature independence

  WHEN TO PICK WHICH:
    • Few samples → Naive Bayes (no optimization needed, stable)
    • Lots of data → Logistic Regression (fewer assumptions)
    • Features truly independent → Naive Bayes shines
    • Features correlated → Logistic Regression handles it better
""")