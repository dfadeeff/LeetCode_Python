"""
DECISION TREE — simplified.

A decision tree asks YES/NO questions to split data.

Imagine sorting animals:
  "Does it have wings?"
    YES → "Does it swim?" → YES: duck, NO: eagle
    NO  → "Does it bark?" → YES: dog, NO: cat

The algorithm figures out the BEST questions automatically
by picking the split that makes the groups most PURE
(all same class in each group).

How to measure "purity"? → GINI IMPURITY
  Gini = 1 - Σ p_k²
  Perfect purity (all same class): Gini = 0
  Worst (50/50 mix):               Gini = 0.5

The tree picks the split that reduces Gini the most.
"""
import numpy as np

# ── 10 patients: [temperature, cough_severity] → sick/healthy ──
X = np.array([
    [6.0, 1.0],  # healthy
    [6.2, 0.5],  # healthy
    [6.5, 2.0],  # healthy
    [5.8, 1.5],  # healthy
    [6.1, 0.8],  # healthy
    [9.0, 7.0],  # sick
    [8.5, 8.0],  # sick
    [9.2, 6.5],  # sick
    [8.8, 7.5],  # sick
    [9.5, 8.5],  # sick
])
y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
feature_names = ["temp", "cough"]

print("=" * 60)
print("DECISION TREE on 10 patients")
print("=" * 60)
for i in range(len(X)):
    label = "sick" if y[i] == 1 else "healthy"
    print(f"  Patient {i}: temp={X[i][0]:.1f}  cough={X[i][1]:.1f}  → {label}")


def gini(y):
    """Gini impurity: 0 = pure, 0.5 = worst (binary)."""
    if len(y) == 0:
        return 0
    p = np.mean(y)
    return 1 - p ** 2 - (1 - p) ** 2


def find_best_split(X, y):
    """Try every feature and every threshold. Pick the one with lowest weighted Gini."""
    best_gini = float('inf')
    best_feature = None
    best_threshold = None

    print("\n  [FINDING BEST SPLIT] Try every possible split:\n")

    for feature_idx in range(X.shape[1]):
        thresholds = np.unique(X[:, feature_idx])

        for threshold in thresholds:
            left_mask = X[:, feature_idx] <= threshold
            right_mask = ~left_mask

            if left_mask.sum() == 0 or right_mask.sum() == 0:
                continue

            left_gini = gini(y[left_mask])
            right_gini = gini(y[right_mask])

            # weighted average by group size
            n = len(y)
            weighted_gini = (left_mask.sum() / n) * left_gini + (right_mask.sum() / n) * right_gini

            fname = feature_names[feature_idx]
            print(f"    {fname} <= {threshold:.1f}? "
                  f"  left={y[left_mask].tolist()} (gini={left_gini:.3f})"
                  f"  right={y[right_mask].tolist()} (gini={right_gini:.3f})"
                  f"  weighted={weighted_gini:.3f}"
                  f"{'  ← BEST so far' if weighted_gini < best_gini else ''}")

            if weighted_gini < best_gini:
                best_gini = weighted_gini
                best_feature = feature_idx
                best_threshold = threshold

    return best_feature, best_threshold, best_gini


# ── Build the tree (just 1 split for simplicity) ──
print(f"\n  Gini of entire dataset: {gini(y):.3f} (5 healthy, 5 sick → maximum impurity)")

feature_idx, threshold, best_gini = find_best_split(X, y)

left_mask = X[:, feature_idx] <= threshold
right_mask = ~left_mask

print(f"\n{'=' * 60}")
print(f"BEST SPLIT: {feature_names[feature_idx]} <= {threshold:.1f}?")
print(f"  Weighted Gini after split: {best_gini:.3f}")
print(f"{'=' * 60}")
print(f"\n  LEFT ({feature_names[feature_idx]} <= {threshold:.1f}):")
for i in np.where(left_mask)[0]:
    label = "sick" if y[i] == 1 else "healthy"
    print(f"    Patient {i}: temp={X[i][0]:.1f} cough={X[i][1]:.1f} → {label}")
left_pred = int(np.mean(y[left_mask]) >= 0.5)
print(f"  → Majority class: {'sick' if left_pred else 'healthy'} ({np.sum(y[left_mask])}/{len(y[left_mask])} sick)")

print(f"\n  RIGHT ({feature_names[feature_idx]} > {threshold:.1f}):")
for i in np.where(right_mask)[0]:
    label = "sick" if y[i] == 1 else "healthy"
    print(f"    Patient {i}: temp={X[i][0]:.1f} cough={X[i][1]:.1f} → {label}")
right_pred = int(np.mean(y[right_mask]) >= 0.5)
print(f"  → Majority class: {'sick' if right_pred else 'healthy'} ({np.sum(y[right_mask])}/{len(y[right_mask])} sick)")

# ── Predict new patient ──
x_new = np.array([8.0, 6.0])
print(f"\n{'─' * 60}")
print(f"PREDICT: new patient temp={x_new[0]}, cough={x_new[1]}")
print(f"{'─' * 60}")
if x_new[feature_idx] <= threshold:
    pred = left_pred
    print(f"  {feature_names[feature_idx]}={x_new[feature_idx]} <= {threshold}? YES → go LEFT → {'sick' if pred else 'healthy'}")
else:
    pred = right_pred
    print(f"  {feature_names[feature_idx]}={x_new[feature_idx]} <= {threshold}? NO → go RIGHT → {'sick' if pred else 'healthy'}")

print(f"""
{'=' * 60}
THE TREE LOOKS LIKE THIS:
{'=' * 60}

         [{feature_names[feature_idx]} <= {threshold}?]
         /                \\
       YES                NO
       /                    \\
  {'healthy' if not left_pred else 'sick':>8}            {'healthy' if not right_pred else 'sick':>8}

RECIPE:
  1. For each feature, for each threshold:
       split data into left/right groups
       compute weighted Gini impurity
  2. Pick the split with lowest Gini
  3. Repeat recursively on each side (we did 1 level here)
  4. Stop when a node is pure (Gini=0) or too small

GINI: 1 - p_0² - p_1²
  All same class → 0 (pure, good)
  50/50 mix → 0.5 (impure, bad)
""")