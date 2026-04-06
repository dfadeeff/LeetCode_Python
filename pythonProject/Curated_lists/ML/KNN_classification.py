import numpy as np
from collections import Counter


def euclidean(a, b):
    return np.sqrt(np.sum((np.array(a) - np.array(b)) ** 2))


class KNNClassifier:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        # Lazy: just store
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def predict_one(self, x):
        # Compute distances to all training points
        dists = [(euclidean(x, xi), yi) for xi, yi in zip(self.X_train, self.y_train)]

        # Sort by distance, take k nearest
        dists.sort(key=lambda t: t[0])
        k_labels = [label for _, label in dists[:self.k]]

        # Majority vote
        return Counter(k_labels).most_common(1)[0][0]

    def predict(self, X):
        return [self.predict_one(x) for x in X]

    def predict_one_weighted(self, x):
        dists = [(euclidean(x, xi), yi)
                 for xi, yi in zip(self.X_train, self.y_train)]
        dists.sort(key=lambda t: t[0])
        k_nearest = dists[:self.k]
        weights = {}
        for dist, label in k_nearest:
            w = 1.0 / (dist + 1e-8)  # avoid div by zero
            weights[label] = weights.get(label, 0) + w
        return max(weights, key=weights.get)

    def predict(self, X):
        # return [self.predict_one(x) for x in X]
        return [self.predict_one_weighted(x) for x in X]


if __name__ == "__main__":
    X_train = [[1, 2], [2, 3], [3, 4], [8, 8], [9, 7], [8, 9]]
    y_train = ['A', 'A', 'A', 'B', 'B', 'B']
    clf = KNNClassifier(k=3)
    clf.fit(X_train, y_train)
    print(clf.predict([[2, 2], [8, 8]]))  # ['A', 'B']
