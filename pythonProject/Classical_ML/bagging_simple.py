"""
BAGGING (Bootstrap AGGregatING) — simplified.

3 steps:
  1. BOOTSTRAP: for each tree, sample N points WITH replacement
     (some points appear twice, some not at all)
  2. FIT: train each tree on its own bootstrap sample
  3. PREDICT: each tree votes, majority wins
"""
from random import randint, seed
from sklearn.tree import DecisionTreeClassifier


# ── Toy dataset: 12 patients ──
X_train = [
    [6.0, 1.0], [6.2, 0.5], [6.5, 2.0],  # healthy
    [5.8, 1.5], [6.1, 0.8], [6.3, 1.2],  # healthy
    [9.0, 7.0], [8.5, 8.0], [9.2, 6.5],  # sick
    [8.8, 7.5], [9.5, 8.5], [8.7, 7.2],  # sick
]
y_train = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

X_test = [
    [6.0, 1.5],  # should be healthy
    [8.0, 6.0],  # should be sick
    [7.0, 4.0],  # borderline
    [9.0, 8.0],  # should be sick
]


# ── Step 1: Bootstrap ──
def bootstrap(n):
    """Sample n indices WITH replacement."""
    return [randint(0, n - 1) for _ in range(n)]


# ── Step 2: Fit each tree on its own bootstrap sample ──
def fit(classifiers, x, y):
    n = len(x)
    for i, clf in enumerate(classifiers):
        indices = bootstrap(n)
        x_boot = [x[j] for j in indices]
        y_boot = [y[j] for j in indices]
        clf.fit(x_boot, y_boot)

        print(f"  Tree {i}: sampled indices {indices}")
        print(f"    healthy={y_boot.count(0)}, sick={y_boot.count(1)}")


# ── Step 3: Predict by majority vote ──
def predict(classifiers, x):
    # collect predictions from all trees
    all_preds = [list(clf.predict(x)) for clf in classifiers]

    results = []
    for i in range(len(x)):
        # count votes from each tree for this point
        votes = {}
        for j in range(len(classifiers)):
            label = int(all_preds[j][i])
            votes[label] = votes.get(label, 0) + 1

        # majority wins (tie → pick smallest label)
        max_count = max(votes.values())
        best_label = min(l for l, c in votes.items() if c == max_count)
        results.append(best_label)
    return results, all_preds


# ── Run it ──
if __name__ == "__main__":
    seed(42)
    n_estimators = 5

    print("=" * 55)
    print(f"BAGGING with {n_estimators} decision trees")
    print("=" * 55)

    print(f"\nTraining data: {len(X_train)} patients (6 healthy, 6 sick)")
    print(f"Test data: {len(X_test)} patients\n")

    # Step 1 & 2: create trees and fit on bootstrap samples
    print("─" * 55)
    print("STEP 1 & 2: Bootstrap + Fit")
    print("─" * 55)
    classifiers = [DecisionTreeClassifier() for _ in range(n_estimators)]
    fit(classifiers, X_train, y_train)

    # Step 3: predict by majority vote
    print(f"\n{'─' * 55}")
    print("STEP 3: Predict by majority vote")
    print(f"{'─' * 55}\n")

    results, all_preds = predict(classifiers, X_test)

    labels = {0: "healthy", 1: "sick"}
    for i in range(len(X_test)):
        votes = [all_preds[j][i] for j in range(n_estimators)]
        vote_str = [labels[v] for v in votes]
        print(f"  Patient {X_test[i]}")
        print(f"    Votes: {vote_str}")
        print(f"    → {labels[results[i]]} ({votes.count(results[i])}/{n_estimators})\n")

    print(f"""{'=' * 55}
THE WHOLE ALGORITHM
{'=' * 55}

  bootstrap(n):
      return [randint(0, n-1) for _ in range(n)]

  fit(trees, X, y):
      for each tree:
          indices = bootstrap(len(X))
          tree.fit(X[indices], y[indices])

  predict(trees, X):
      votes = [tree.predict(X) for tree in trees]
      return majority_vote(votes)

  That's bagging. 3 functions, ~10 lines of real logic.

WHY IT WORKS:
  Each tree sees different data → makes different mistakes.
  Majority vote cancels out individual errors.
  More trees → more stable (but each tree is independent).
""")