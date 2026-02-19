"""
Decision Tree — minimal interview implementation.
Recursive tree that splits on best Gini until pure or max depth.
"""
import numpy as np


def gini(y):
    if len(y) == 0:
        return 0
    _, counts = np.unique(y, return_counts=True)
    probs = counts / len(y)
    return 1 - np.sum(probs ** 2)



def best_split(X, y):
    best_gini, best_f, best_t = float('inf'), 0, 0
    for f in range(X.shape[1]):
        for t in np.unique(X[:, f]):
            left, right = y[X[:, f] <= t], y[X[:, f] > t]
            if len(left) == 0 or len(right) == 0:
                continue
            wg = (len(left) * gini(left) + len(right) * gini(right)) / len(y)
            if wg < best_gini:
                best_gini, best_f, best_t = wg, f, t
    return best_f, best_t, best_gini


def build_tree(X, y, depth=0, max_depth=3):
    # leaf: pure node or max depth reached
    if gini(y) == 0 or depth >= max_depth:
        return int(np.round(np.mean(y)))

    f, t, g = best_split(X, y)
    if g >= gini(y):  # split doesn't improve anything
        return int(np.round(np.mean(y)))

    left_mask = X[:, f] <= t
    return {
        'feature': f,
        'threshold': t,
        'left': build_tree(X[left_mask], y[left_mask], depth + 1, max_depth),
        'right': build_tree(X[~left_mask], y[~left_mask], depth + 1, max_depth),
    }


def predict_one(x, tree):
    if not isinstance(tree, dict):
        return tree
    if x[tree['feature']] <= tree['threshold']:
        return predict_one(x, tree['left'])
    return predict_one(x, tree['right'])


def predict(X, tree):
    return np.array([predict_one(x, tree) for x in X])


def print_tree(tree, indent=0):
    pad = "  " * indent
    if not isinstance(tree, dict):
        print(f"{pad}→ class {tree}")
        return
    print(f"{pad}feature {tree['feature']} <= {tree['threshold']}?")
    print(f"{pad}  YES:")
    print_tree(tree['left'], indent + 2)
    print(f"{pad}  NO:")
    print_tree(tree['right'], indent + 2)


# ── Test ──
if __name__ == "__main__":
    X = np.array([
        [6.0, 1.0],  [6.2, 0.5],  [6.5, 2.0],  [5.8, 1.5],  [6.1, 0.8],
        [9.0, 7.0],  [8.5, 8.0],  [9.2, 6.5],  [8.8, 7.5],  [9.5, 8.5],
    ])
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

    tree = build_tree(X, y, max_depth=3)

    print("TREE:")
    print_tree(tree)

    preds = predict(X, tree)
    print(f"\nAccuracy: {np.mean(preds == y):.0%}")

    x_new = np.array([[8.0, 6.0]])
    print(f"New patient temp=8.0 cough=6.0 → class {predict(x_new, tree)[0]}")