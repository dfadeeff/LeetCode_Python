import numpy as np

np.random.seed(42)

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("KNN — Step by Step with Numbers")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()

# Training data: apartments with (size_m2, distance_to_center_km) → cheap(0) or expensive(1)
X_train = np.array([
    [30, 5.0],  # small, far → cheap
    [40, 4.5],  # small, far → cheap
    [35, 4.0],  # small, medium → cheap
    [80, 1.0],  # big, central → expensive
    [90, 0.5],  # big, central → expensive
    [75, 1.5],  # big, central → expensive
    [60, 2.0],  # medium, medium → expensive
])

y_train = np.array([0, 0, 0, 1, 1, 1, 1])  # 0=cheap, 1=expensive
labels = ["cheap", "expensive"]

# New apartment to classify
x_new = np.array([55, 2.5])
K = 3


def calculate_distances(X_train):
    """Step 1: Compute all distances"""
    distances = []
    for i in range(len(X_train)):
        diff = x_new - X_train[i]
        dist = np.sqrt(np.sum(diff ** 2))
        distances.append(dist)

    return np.array(distances)


def find_indices(X_train):
    """Step 2: Find K nearest"""
    distances = calculate_distances(X_train)
    return np.argsort(distances)[:K]


def vote(X_train, y_train):
    """Step 3: Vote"""
    indices = find_indices(X_train)
    neighbor_labels = y_train[indices]
    vote_counts = np.bincount(neighbor_labels, minlength=2)
    prediction = np.argmax(vote_counts)

    return prediction


if __name__ == "__main__":
    for i in range(len(X_train)):
        print(X_train[i], labels[y_train[i]])

    distances = calculate_distances(X_train)
    print(distances)

    indices = find_indices(X_train)
    print(indices)

    for idx in indices:
        print(f"Point {idx}: {X_train[idx]} → {labels[y_train[idx]]} (distance={distances[idx]:.2f})")

    prediction = vote(X_train, y_train)
    print(prediction)
