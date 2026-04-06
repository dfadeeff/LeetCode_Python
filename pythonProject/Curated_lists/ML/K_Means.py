import random
import math


def kmeans(X, k, max_iter=100, seed=42):
    random.seed(seed)
    centroids = random.sample(X, k)
    for _ in range(max_iter):
        clusters = [[] for _ in range(k)]
        for point in X:
            # distance from centroids
            distances = [math.sqrt(sum((a - b) ** 2 for a, b in zip(point, c))) for c in centroids]
            # select index of centroid with min distance to the point
            clusters[distances.index(min(distances))].append(point)
        print("clusters:", clusters)
        new_centroids = []

        # Update
        for i, cluster in enumerate(clusters):
            if cluster:
                dim = len(cluster[0])
                mean = [sum(p[d] for p in cluster) / len(cluster) for d in range(dim)]
                new_centroids.append(mean)
            else:
                new_centroids.append(centroids[i])

        if new_centroids == centroids:
            break
        centroids = new_centroids
    assignments = []
    for point in X:
        distances = [math.sqrt(sum((a - b) ** 2 for a, b in zip(point, c))) for c in centroids]
        assignments.append(distances.index(min(distances)))

    return assignments, centroids


if __name__ == "__main__":
    X = [[1, 1], [1, 2], [2, 1], [8, 8], [8, 9], [9, 8]]
    print(kmeans(X, k=2))
