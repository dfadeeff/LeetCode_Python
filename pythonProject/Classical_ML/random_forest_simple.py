"""
RANDOM FOREST — simplified.

Problem with a single decision tree: it OVERFITS.
It memorizes the training data perfectly but fails on new data.

Solution: build MANY trees, each slightly different, and VOTE.

How to make each tree different? Two tricks:
  1. BAGGING: each tree sees a random SUBSET of data (sample with replacement)
  2. FEATURE RANDOMNESS: at each split, only consider a random subset of features

Final prediction = majority vote of all trees.

Why it works: individual trees are noisy, but their ERRORS are random
and cancel out when you average. (Like asking 100 people vs 1 person.)
"""
import numpy as np

np.random.seed(42)

# ── 12 patients: [temperature, cough, fatigue] → sick/healthy ──
X = np.array([
    [6.0, 1.0, 2.0],  # healthy
    [6.2, 0.5, 1.5],  # healthy
    [6.5, 2.0, 3.0],  # healthy
    [5.8, 1.5, 2.5],  # healthy
    [6.1, 0.8, 1.0],  # healthy
    [6.3, 1.2, 2.0],  # healthy
    [9.0, 7.0, 8.0],  # sick
    [8.5, 8.0, 7.5],  # sick
    [9.2, 6.5, 9.0],  # sick
    [8.8, 7.5, 8.5],  # sick
    [9.5, 8.5, 7.0],  # sick
    [8.7, 7.2, 8.2],  # sick
])
y = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
feature_names = ["temp", "cough", "fatigue"]

print("=" * 60)
print("RANDOM FOREST: 3 trees, 12 patients, 3 features")
print("=" * 60)


def gini(y):
    if len(y) == 0:
        return 0
    p = np.mean(y)
    return 1 - p ** 2 - (1 - p) ** 2


def best_split(X, y, feature_subset):
    """Find best split considering only the given features."""
    best_gini = float('inf')
    best_feat = None
    best_thresh = None

    for feat in feature_subset:
        for thresh in np.unique(X[:, feat]):
            left = y[X[:, feat] <= thresh]
            right = y[X[:, feat] > thresh]
            if len(left) == 0 or len(right) == 0:
                continue
            wg = (len(left) * gini(left) + len(right) * gini(right)) / len(y)
            if wg < best_gini:
                best_gini = wg
                best_feat = feat
                best_thresh = thresh

    return best_feat, best_thresh


def build_stump(X, y, feature_subset):
    """Build a 1-level tree (stump) on the given data/features."""
    feat, thresh = best_split(X, y, feature_subset)
    left_pred = int(np.mean(y[X[:, feat] <= thresh]) >= 0.5)
    right_pred = int(np.mean(y[X[:, feat] > thresh]) >= 0.5)
    return feat, thresh, left_pred, right_pred


def predict_stump(x, feat, thresh, left_pred, right_pred):
    if x[feat] <= thresh:
        return left_pred
    return right_pred


# ── Build 3 trees, each with random data + random features ──
n_trees = 3
n_samples = len(X)
n_features = X.shape[1]
max_features = 2  # each tree considers 2 out of 3 features

trees = []

for t in range(n_trees):
    print(f"\n{'─' * 60}")
    print(f"TREE {t + 1}")
    print(f"{'─' * 60}")

    # 1. BAGGING: sample data WITH replacement
    sample_indices = np.random.choice(n_samples, n_samples, replace=True)
    X_sample = X[sample_indices]
    y_sample = y[sample_indices]

    unique, counts = np.unique(sample_indices, return_counts=True)
    print(f"\n  [BAGGING] Sampled patients (with replacement):")
    print(f"    Indices: {sample_indices.tolist()}")
    print(f"    Some patients appear multiple times, some not at all")
    print(f"    Healthy: {np.sum(y_sample == 0)}, Sick: {np.sum(y_sample == 1)}")

    # 2. FEATURE RANDOMNESS: pick random subset of features
    feature_subset = np.random.choice(n_features, max_features, replace=False)
    feature_subset.sort()
    print(f"\n  [FEATURE SUBSET] Using features: {[feature_names[f] for f in feature_subset]}")
    print(f"    (ignoring: {[feature_names[f] for f in range(n_features) if f not in feature_subset]})")

    # 3. Build a stump on this subset
    feat, thresh, left_pred, right_pred = build_stump(X_sample, y_sample, feature_subset)
    trees.append((feat, thresh, left_pred, right_pred))

    print(f"\n  [SPLIT] Best question: {feature_names[feat]} <= {thresh}?")
    print(f"    YES → {'sick' if left_pred else 'healthy'}")
    print(f"    NO  → {'sick' if right_pred else 'healthy'}")

# ── Predict new patient with all 3 trees ──
x_new = np.array([8.0, 6.0, 7.0])
print(f"\n{'=' * 60}")
print(f"PREDICT: new patient temp={x_new[0]}, cough={x_new[1]}, fatigue={x_new[2]}")
print(f"{'=' * 60}")

votes = []
for t, (feat, thresh, left_pred, right_pred) in enumerate(trees):
    pred = predict_stump(x_new, feat, thresh, left_pred, right_pred)
    votes.append(pred)
    direction = "YES → LEFT" if x_new[feat] <= thresh else "NO → RIGHT"
    label = "sick" if pred else "healthy"
    print(f"  Tree {t + 1}: {feature_names[feat]} <= {thresh}? "
          f"{direction} → {label}")

final = int(np.mean(votes) >= 0.5)
print(f"\n  VOTES: {['sick' if v else 'healthy' for v in votes]}")
print(f"  MAJORITY → {'sick' if final else 'healthy'} ({sum(votes)}/{len(votes)} say sick)")

print(f"""
{'=' * 60}
RECIPE:
{'=' * 60}

  For each tree (e.g. 100 trees):
    1. Sample N points WITH replacement (bagging)
    2. At each split, consider only sqrt(n_features) random features
    3. Build a full decision tree on that subset

  Predict = majority vote of all trees

  WHY IT WORKS:
    Each tree overfits differently (different data, different features).
    Averaging cancels out the individual errors.
    More trees = more stable (but diminishing returns past ~100).
""")