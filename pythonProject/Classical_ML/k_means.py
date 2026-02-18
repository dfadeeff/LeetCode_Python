import numpy as np

np.random.seed(42)

cluster_1 = np.random.randn(20, 2) * 0.5 + np.array([0, 0])
cluster_2 = np.random.randn(20, 2) * 0.5 + np.array([4, 4])
cluster_3 = np.random.randn(20, 2) * 0.5 + np.array([0, 4])

X = np.vstack([cluster_1, cluster_2, cluster_3])

# Step 1: Initialize centroids randomly
np.random.seed(7)


def gen_random_centroids(n_samples, K, replace=False):
    random_indices = np.random.choice(n_samples, K, replace=False)
    centroids = X[random_indices].copy()
    return centroids


def run_k_means(n_samples, K):
    """    ASSIGN step: each point → nearest centroid ───
    Compute distance from each point to each centroid
    distances shape: (n_samples, K)"""
    centroids = gen_random_centroids(n_samples, K)
    print(f"=== Starting K-Means with K={K}, n_samples={n_samples} ===\n")
    print(f"Initial centroids (randomly picked from data):")
    for k in range(K):
        print(f"  Centroid {k}: [{centroids[k, 0]:.2f}, {centroids[k, 1]:.2f}]")
    print()

    for iteration in range(10):
        print(f"--- Iteration {iteration + 1} ---")

        # === ASSIGN STEP ===
        print(f"  [ASSIGN] Computing distance from each of {n_samples} points to each of {K} centroids...")
        distances = np.zeros((n_samples, K))
        print(f"  distances matrix initialized: shape={distances.shape}  (rows=points, cols=centroids)")
        for k in range(K):
            # X - centroids[k] broadcasts centroid k across all 60 points → shape (60,2)
            # **2 squares each component, np.sum(..., axis=1) sums x²+y² per row → shape (60,)
            # np.sqrt gives Euclidean distance per point → stored in column k
            distances[:, k] = np.sqrt(np.sum((X - centroids[k]) ** 2, axis=1))
            print(f"    distances[:, {k}] = distance of all points to centroid {k}"
                  f"  (first 5: {np.round(distances[:5, k], 2)})")

        print(f"\n  Full distance matrix (first 5 points):")
        print(f"  {np.round(distances[:5], 2)}")

        # Assign each point to nearest centroid
        assignments = np.argmin(distances, axis=1)
        print(f"\n  [ASSIGN] np.argmin(distances, axis=1) → pick column with smallest distance per row")
        print(f"  assignments (first 10): {assignments[:10]}")
        print(
            f"  (e.g. point 0 assigned to cluster {assignments[0]} because its distances were {np.round(distances[0], 2)})")

        # === UPDATE STEP ===
        print(f"\n  [UPDATE] Recomputing centroids as mean of assigned points...")
        new_centroids = np.zeros_like(centroids)
        for k in range(K):
            mask = assignments == k
            points_in_cluster = X[mask]
            print(f"    Cluster {k}: {len(points_in_cluster)} points assigned")
            if len(points_in_cluster) > 0:
                new_centroids[k] = points_in_cluster.mean(axis=0)
                print(f"      old centroid: [{centroids[k, 0]:5.2f}, {centroids[k, 1]:5.2f}]"
                      f" → new centroid (mean): [{new_centroids[k, 0]:5.2f}, {new_centroids[k, 1]:5.2f}]")
            else:
                new_centroids[k] = centroids[k]
                print(f"      no points! keeping old centroid: [{centroids[k, 0]:5.2f}, {centroids[k, 1]:5.2f}]")

        # Check convergence
        centroid_shift = np.sqrt(np.sum((new_centroids - centroids) ** 2))
        converged = centroid_shift < 1e-6
        counts = [np.sum(assignments == k) for k in range(K)]

        print(f"\n  [CONVERGENCE CHECK] total centroid shift: {centroid_shift:.6f}"
              f"  (threshold: 1e-6)")
        if converged:
            print(f"  CONVERGED! Centroids barely moved. Stopping.\n")
        else:
            print(f"  Not converged yet — centroids still moving. Continuing...\n")

        centroids = new_centroids.copy()
        if converged:
            break

    print(f"=== Final Result ===")
    for k in range(K):
        count = np.sum(assignments == k)
        print(f"  Cluster {k}: centroid=[{centroids[k, 0]:5.2f}, {centroids[k, 1]:5.2f}], points={count}")
    print()


if __name__ == "__main__":
    K = 3
    n_samples = len(X)
    print(X)

    centroids = gen_random_centroids(n_samples, K)

    for k in range(K):
        print(f"Centroid {k}: [{centroids[k, 0]:.2f}, {centroids[k, 1]:.2f}]")

    run_k_means(n_samples, K)
