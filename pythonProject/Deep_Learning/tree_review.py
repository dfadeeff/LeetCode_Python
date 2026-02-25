"""
TREE REVIEW — Decision Tree, Bagging, Boosting
================================================
Code from memory in <5 minutes each.

Decision Tree: split data by best feature/threshold (lowest Gini)
Bagging:       N trees on bootstrap samples → majority vote
Boosting:      trees sequentially fix previous tree's errors
"""
import numpy as np


# ══════════════════════════════════════════════════════════════
# 1. DECISION TREE (Classification)
# ══════════════════════════════════════════════════════════════
# Gini impurity = 1 - Σ p_k²
#   pure (all same class):  Gini = 0       ← want this
#   worst (50/50):          Gini = 0.5     ← avoid this
#
# Algorithm:
#   for each feature, for each threshold:
#       split data into left/right
#       compute weighted Gini
#   pick split with LOWEST weighted Gini
#   recurse on each side
#   stop when: pure, too small, or max depth

def gini(y):
    """Gini = 1 - p0² - p1²  (binary case)"""
    if len(y) == 0:
        return 0
    p = np.mean(y)                    # fraction of class 1
    return 1 - p ** 2 - (1 - p) ** 2  # = 2 * p * (1 - p)


class Node:
    """A node is either a split or a leaf."""
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature      # which feature to split on
        self.threshold = threshold  # split value
        self.left = left            # left child (Node)
        self.right = right          # right child (Node)
        self.value = value          # leaf prediction (majority class)


class DecisionTree:
    def __init__(self, max_depth=5, min_samples=2):
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.root = None

    def _best_split(self, X, y):
        """Try every feature × threshold combo, return best."""
        best_gini = float('inf')
        best_feat, best_thresh = None, None

        for f in range(X.shape[1]):                     # each feature
            thresholds = np.unique(X[:, f])              # each unique value
            for t in thresholds:
                left_mask = X[:, f] <= t                 # left: feature <= threshold
                right_mask = ~left_mask                  # right: feature > threshold

                if left_mask.sum() == 0 or right_mask.sum() == 0:
                    continue                             # skip empty splits

                n = len(y)
                w_gini = (left_mask.sum() / n) * gini(y[left_mask]) + \
                         (right_mask.sum() / n) * gini(y[right_mask])

                if w_gini < best_gini:
                    best_gini = w_gini
                    best_feat = f
                    best_thresh = t

        return best_feat, best_thresh

    def _build(self, X, y, depth):
        """Recursively build the tree."""
        # STOP conditions: pure node, too small, or max depth
        if gini(y) == 0 or len(y) < self.min_samples or depth >= self.max_depth:
            return Node(value=int(np.round(np.mean(y))))  # majority class

        feat, thresh = self._best_split(X, y)
        if feat is None:
            return Node(value=int(np.round(np.mean(y))))

        left_mask = X[:, feat] <= thresh
        left = self._build(X[left_mask], y[left_mask], depth + 1)
        right = self._build(X[~left_mask], y[~left_mask], depth + 1)
        return Node(feature=feat, threshold=thresh, left=left, right=right)

    def fit(self, X, y):
        self.root = self._build(X, y, depth=0)

    def _predict_one(self, x, node):
        """Walk down the tree for one sample."""
        if node.value is not None:       # leaf — return prediction
            return node.value
        if x[node.feature] <= node.threshold:
            return self._predict_one(x, node.left)
        else:
            return self._predict_one(x, node.right)

    def predict(self, X):
        return np.array([self._predict_one(x, self.root) for x in X])


# ══════════════════════════════════════════════════════════════
# 2. BAGGING (Bootstrap AGGregatING)
# ══════════════════════════════════════════════════════════════
# 1. BOOTSTRAP: sample N points WITH replacement (some repeated, some missing)
# 2. FIT: train a tree on each bootstrap sample
# 3. PREDICT: each tree votes → majority wins
#
# Why it works: each tree sees different data → different mistakes
#               majority vote cancels out individual errors
# Random Forest = Bagging + random feature subsets at each split

class BaggingClassifier:
    def __init__(self, n_trees=5, max_depth=5):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.trees = []

    def _bootstrap(self, X, y):
        """Sample N indices WITH replacement."""
        n = len(y)
        idx = np.random.randint(0, n, size=n)  # random indices, allows repeats
        return X[idx], y[idx]

    def fit(self, X, y):
        self.trees = []
        for _ in range(self.n_trees):
            X_boot, y_boot = self._bootstrap(X, y)
            tree = DecisionTree(max_depth=self.max_depth)
            tree.fit(X_boot, y_boot)
            self.trees.append(tree)

    def predict(self, X):
        # collect votes from all trees
        all_preds = np.array([tree.predict(X) for tree in self.trees])  # (n_trees, n_samples)
        # majority vote per sample (axis=0 = across trees)
        results = []
        for i in range(X.shape[0]):
            votes = all_preds[:, i]
            results.append(int(np.round(np.mean(votes))))  # >0.5 → class 1
        return np.array(results)


# ══════════════════════════════════════════════════════════════
# 3. GRADIENT BOOSTING (simplified, regression)
# ══════════════════════════════════════════════════════════════
# Key idea: each tree fits the RESIDUALS (errors) of the previous model.
#
# Algorithm:
#   prediction = mean(y)                  # start with simple guess
#   for each round:
#       residuals = y - prediction        # what's left to fix
#       tree = fit tree on residuals      # learn the errors
#       prediction += lr * tree(X)        # add small correction
#
# vs Bagging:
#   Bagging:   trees are INDEPENDENT, vote together (parallel)
#   Boosting:  trees are SEQUENTIAL, each fixes previous errors
#
# Overfit prevention: small learning rate (0.1), max_depth=3, early stopping

class GradientBoosting:
    def __init__(self, n_trees=10, lr=0.1, max_depth=3):
        self.n_trees = n_trees
        self.lr = lr
        self.max_depth = max_depth
        self.base_prediction = 0.0
        self.trees = []
        self.losses = []

    def _build_stump(self, X, residuals):
        """Find best split, predict mean residual on each side."""
        best_mse = float('inf')
        best_feat, best_thresh = 0, 0
        best_left_val, best_right_val = 0, 0

        for f in range(X.shape[1]):
            for t in np.unique(X[:, f]):
                left = X[:, f] <= t
                right = ~left
                if left.sum() == 0 or right.sum() == 0:
                    continue

                l_val = residuals[left].mean()
                r_val = residuals[right].mean()
                mse = (np.sum((residuals[left] - l_val) ** 2) +
                       np.sum((residuals[right] - r_val) ** 2)) / len(residuals)

                if mse < best_mse:
                    best_mse = mse
                    best_feat, best_thresh = f, t
                    best_left_val, best_right_val = l_val, r_val

        return best_feat, best_thresh, best_left_val, best_right_val

    def fit(self, X, y):
        self.base_prediction = np.mean(y)
        prediction = np.full(len(y), self.base_prediction)
        self.trees = []
        self.losses = []

        for i in range(self.n_trees):
            residuals = y - prediction                     # what's still wrong
            loss = np.mean(residuals ** 2)
            self.losses.append(loss)

            feat, thresh, l_val, r_val = self._build_stump(X, residuals)
            self.trees.append((feat, thresh, l_val, r_val))

            # update: add small correction
            correction = np.where(X[:, feat] <= thresh, l_val, r_val)
            prediction += self.lr * correction

    def predict(self, X):
        prediction = np.full(X.shape[0], self.base_prediction)
        for feat, thresh, l_val, r_val in self.trees:
            correction = np.where(X[:, feat] <= thresh, l_val, r_val)
            prediction += self.lr * correction
        return prediction


# ══════════════════════════════════════════════════════════════
# EVALUATION
# ══════════════════════════════════════════════════════════════

def accuracy(y_true, y_pred):
    return np.mean(y_true == y_pred)

def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)


# ══════════════════════════════════════════════════════════════
# DEMOS
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    np.random.seed(42)

    # --- Classification dataset: sick vs healthy ---
    # Features: [temperature °C, cough severity 1-10]
    X_cls = np.array([
        [36.6, 1], [36.8, 2], [37.0, 1], [36.9, 3], [37.1, 2],  # healthy
        [38.5, 7], [39.0, 8], [38.8, 9], [39.2, 7], [39.5, 8],  # sick
    ])
    y_cls = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

    X_test_cls = np.array([
        [36.7, 2],   # should be healthy
        [39.1, 8],   # should be sick
        [37.5, 5],   # borderline
        [38.9, 9],   # should be sick
    ])
    y_test_cls = np.array([0, 1, 0, 1])

    # --- 1. DECISION TREE ---
    print("=" * 50)
    print("1. DECISION TREE")
    print("=" * 50)
    dt = DecisionTree(max_depth=3)
    dt.fit(X_cls, y_cls)
    preds = dt.predict(X_test_cls)
    print(f"  Predictions: {preds}")
    print(f"  Actual:      {y_test_cls}")
    print(f"  Accuracy:    {accuracy(y_test_cls, preds):.3f}")

    # --- 2. BAGGING ---
    print(f"\n{'=' * 50}")
    print("2. BAGGING (5 trees)")
    print("=" * 50)
    bag = BaggingClassifier(n_trees=5, max_depth=3)
    bag.fit(X_cls, y_cls)
    preds = bag.predict(X_test_cls)
    print(f"  Predictions: {preds}")
    print(f"  Actual:      {y_test_cls}")
    print(f"  Accuracy:    {accuracy(y_test_cls, preds):.3f}")

    # --- 3. GRADIENT BOOSTING (regression) ---
    print(f"\n{'=' * 50}")
    print("3. GRADIENT BOOSTING (regression)")
    print("=" * 50)

    # Regression dataset: y = 2*x1 + 3*x2 + noise
    n = 50
    X_reg = np.random.randn(n, 2)
    y_reg = 2 * X_reg[:, 0] + 3 * X_reg[:, 1] + np.random.randn(n) * 0.5
    X_train, X_test = X_reg[:40], X_reg[40:]
    y_train, y_test = y_reg[:40], y_reg[40:]

    gb = GradientBoosting(n_trees=20, lr=0.3, max_depth=3)
    gb.fit(X_train, y_train)
    preds = gb.predict(X_test)
    print(f"  MSE (just mean): {mse(y_test, np.full(10, y_train.mean())):.4f}")
    print(f"  MSE (boosting):  {mse(y_test, preds):.4f}")
    print(f"  Loss curve:      {gb.losses[0]:.3f} → {gb.losses[-1]:.3f}")

    # --- CHEAT SHEET ---
    print(f"""
{'=' * 50}
CHEAT SHEET — Interview talking points
{'=' * 50}

DECISION TREE:
  Gini = 1 - p0² - p1²  (0=pure, 0.5=worst)
  For each feature × threshold: pick lowest weighted Gini
  Stop: pure, min_samples, max_depth
  Overfit: prune (limit depth), min samples per leaf

BAGGING:
  Bootstrap sample → fit tree → repeat N times → majority vote
  Each tree: different data → different mistakes → vote cancels errors
  Random Forest = bagging + random feature subsets

BOOSTING:
  pred = mean(y)
  for each tree: residuals = y - pred; fit tree on residuals; pred += lr * tree
  Sequential: each tree fixes previous errors
  Overfit prevention: small lr, shallow trees, early stopping

  ┌─────────────┬────────────────────┬────────────────────┐
  │             │ Bagging            │ Boosting           │
  ├─────────────┼────────────────────┼────────────────────┤
  │ Trees       │ Independent        │ Sequential         │
  │ Each fits   │ Bootstrap of data  │ Residuals (errors) │
  │ Combine     │ Majority vote/avg  │ Sum of corrections │
  │ Tree depth  │ Full               │ Shallow (3-6)      │
  │ Parallel?   │ Yes                │ No                 │
  │ Overfit     │ Resistant          │ Can overfit         │
  └─────────────┴────────────────────┴────────────────────┘

CONVERGENCE — "How do you know when to stop?"
  Decision Tree: node is pure (Gini=0) or max depth reached
  Bagging: more trees = more stable (diminishing returns after ~100)
  Boosting: early stopping — if validation loss stops improving for N rounds
""")