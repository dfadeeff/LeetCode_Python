import numpy as np

X = np.array([[1, 2], [3, 4]])
print(X)

w = np.array([0.5, 0.3])

print(np.dot(X, w))
print(np.dot(w, X))
print(X @ w)
print(w @ X)

print("manual check: ", [1 * 0.5 + 2 * 0.3, 3 * 0.5 + 4 * 0.3])
