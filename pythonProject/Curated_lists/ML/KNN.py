import math
from collections import Counter


def knn_predict(X_train, y_train, X_test, k=3):
    predictions = []
    for test_point in X_test:
        # distances to all training points
        distances = []
        for i, train_point in enumerate(X_train):
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(test_point, train_point)))

            distances.append((dist, y_train[i]))

        distances.sort(key=lambda x: x[0])
        print("distances", distances)
        k_labels = [label for _, label in distances[:k]]

        # .most_common(1) returns a list of the 1 most frequent (label, count) pair
        # give me the most frequent label among the k nearest neighbors
        predicted_label = Counter(k_labels).most_common(1)[0][0]
        predictions.append(predicted_label)
        print("counter k labels", Counter(k_labels))
    return predictions


if __name__ == '__main__':
    # KNN
    X_train = [[1, 1], [1, 2], [2, 1], [8, 8], [8, 9], [9, 8]]
    y_train = [0, 0, 0, 1, 1, 1]
    print(knn_predict(X_train, y_train, [[8, 2]], k=3))
