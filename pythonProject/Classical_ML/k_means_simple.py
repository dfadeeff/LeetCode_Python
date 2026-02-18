import numpy as np

# === 10 simple 2D points — two obvious groups ===
# Group A: points near (1, 1)
# Group B: points near (5, 5)
X = np.array([
    [0.5, 0.8],   # 0  ← clearly group A
    [1.0, 1.2],   # 1
    [1.5, 0.5],   # 2
    [0.8, 1.5],   # 3
    [1.2, 0.9],   # 4
    [4.5, 5.0],   # 5  ← clearly group B
    [5.0, 4.8],   # 6
    [5.5, 5.2],   # 7
    [4.8, 5.5],   # 8
    [5.2, 4.5],   # 9
])

K = 2  # we want 2 clusters

# ── Step 0: Pick 2 random points as initial centroids ──
np.random.seed(0)
indices = np.random.choice(len(X), K, replace=False)
centroids = X[indices].copy()

print("=" * 50)
print("DATA POINTS:")
for i, point in enumerate(X):
    print(f"  Point {i}: [{point[0]:.1f}, {point[1]:.1f}]")

print(f"\nRandomly picked points {indices} as initial centroids:")
for k in range(K):
    print(f"  Centroid {k}: [{centroids[k][0]:.1f}, {centroids[k][1]:.1f}]")
print("=" * 50)

for iteration in range(10):
    print(f"\n{'─' * 50}")
    print(f"ITERATION {iteration + 1}")
    print(f"{'─' * 50}")

    # ── Step 1: ASSIGN — find nearest centroid for each point ──
    print("\n[STEP 1: ASSIGN] — compute distance from each point to each centroid\n")

    assignments = np.zeros(len(X), dtype=int)

    for i in range(len(X)):
        # distance = sqrt((x1-x2)² + (y1-y2)²)
        dist_to_0 = np.sqrt((X[i][0] - centroids[0][0])**2 + (X[i][1] - centroids[0][1])**2)
        dist_to_1 = np.sqrt((X[i][0] - centroids[1][0])**2 + (X[i][1] - centroids[1][1])**2)

        if dist_to_0 < dist_to_1:
            assignments[i] = 0
        else:
            assignments[i] = 1

        winner = "A" if assignments[i] == 0 else "B"
        print(f"  Point {i} [{X[i][0]:.1f}, {X[i][1]:.1f}]"
              f"  →  dist to C0: {dist_to_0:.2f}  |  dist to C1: {dist_to_1:.2f}"
              f"  →  cluster {winner}")

    # ── Step 2: UPDATE — move centroids to mean of their points ──
    print(f"\n[STEP 2: UPDATE] — recompute centroids as the mean of assigned points\n")

    old_centroids = centroids.copy()

    for k in range(K):
        cluster_points = X[assignments == k]
        label = "A" if k == 0 else "B"
        print(f"  Cluster {label} points: {[f'[{p[0]:.1f}, {p[1]:.1f}]' for p in cluster_points]}")

        centroids[k] = cluster_points.mean(axis=0)
        print(f"    mean x = {' + '.join(f'{p[0]:.1f}' for p in cluster_points)} / {len(cluster_points)} = {centroids[k][0]:.2f}")
        print(f"    mean y = {' + '.join(f'{p[1]:.1f}' for p in cluster_points)} / {len(cluster_points)} = {centroids[k][1]:.2f}")
        print(f"    Centroid {k}: [{old_centroids[k][0]:.2f}, {old_centroids[k][1]:.2f}]  →  [{centroids[k][0]:.2f}, {centroids[k][1]:.2f}]")
        print()

    # ── Step 3: CHECK — did centroids stop moving? ──
    shift = np.sqrt(np.sum((centroids - old_centroids) ** 2))
    print(f"[STEP 3: CONVERGENCE CHECK]")
    print(f"  Total centroid shift: {shift:.6f}")

    if shift < 1e-6:
        print(f"  Centroids stopped moving → CONVERGED! Done.\n")
        break
    else:
        print(f"  Still moving → go to next iteration")

print("=" * 50)
print("FINAL CLUSTERS:")
for k in range(K):
    label = "A" if k == 0 else "B"
    cluster_points = X[assignments == k]
    print(f"  Cluster {label}: centroid=[{centroids[k][0]:.2f}, {centroids[k][1]:.2f}],"
          f" points={[i for i in range(len(X)) if assignments[i] == k]}")
print("=" * 50)