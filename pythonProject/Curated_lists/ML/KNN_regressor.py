import numpy as np


def euclidean(a, b):
    return np.sqrt(np.sum((np.array(a) - np.array(b)) ** 2))


class KNNRegressor:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_train = np.array(X, dtype=float)
        self.y_train = np.array(y, dtype=float)

    def predict_one(self, x):
        dists = [(euclidean(x, xi), yi)
                 for xi, yi in zip(self.X_train, self.y_train)]
        dists.sort(key=lambda t: t[0])
        k_vals = [v for _, v in dists[:self.k]]
        return np.mean(k_vals)  # ← only change vs classifier

    def predict(self, X):
        return [self.predict_one(x) for x in X]


if __name__ == "__main__":
    X_train = [[1], [2], [3], [4], [5]]
    y_train = [2.0, 4.0, 6.0, 8.0, 10.0]  # y = 2x
    reg = KNNRegressor(k=2)
    reg.fit(X_train, y_train)
    print(reg.predict([[2.5], [4.5]]))  # ~[5.0, 9.0]
