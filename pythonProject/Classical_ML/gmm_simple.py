"""
GAUSSIAN MIXTURE MODEL (GMM) — simplified.

GMM is like K-Means but SOFT:
  K-Means: each point belongs to ONE cluster (hard assignment)
  GMM:     each point has a PROBABILITY of belonging to each cluster

It assumes data is generated from a mixture of Gaussian (bell-curve) distributions.
Each cluster is one Gaussian with its own mean, variance, and weight.

Algorithm: Expectation-Maximization (EM)
  E-step: for each point, compute probability it belongs to each cluster
  M-step: update each cluster's mean, variance, weight using those probabilities

It's the probabilistic version of K-Means.
"""
import numpy as np

np.random.seed(42)

# ── 10 points, 2 obvious groups ──
X = np.array([1.0, 1.5, 2.0, 1.8, 1.2,  # group near 1.5
              8.0, 8.5, 9.0, 8.8, 8.2])  # group near 8.5

K = 2  # two clusters

print("=" * 60)
print("GMM: 10 points, 2 clusters (1D for simplicity)")
print("=" * 60)
print(f"\nData: {X}")
print(f"Eyeball answer: cluster A ≈ [1.0–2.0], cluster B ≈ [8.0–9.0]\n")

# ── Initialize parameters ──
# Each cluster k has: mean μ_k, variance σ²_k, weight π_k
means = np.array([2.0, 7.0])  # initial guesses (don't need to be perfect)
variances = np.array([1.0, 1.0])  # start with variance = 1
weights = np.array([0.5, 0.5])  # start 50/50

print("Initial parameters:")
for k in range(K):
    print(f"  Cluster {k}: mean={means[k]:.1f}, var={variances[k]:.1f}, weight={weights[k]:.1f}")
print()


def gaussian_pdf(x, mean, var):
    """Probability of x under a Gaussian(mean, var)."""
    return (1 / np.sqrt(2 * np.pi * var)) * np.exp(-(x - mean) ** 2 / (2 * var))


for iteration in range(8):
    print(f"{'─' * 60}")
    print(f"ITERATION {iteration + 1}")
    print(f"{'─' * 60}")

    # ── E-STEP: compute responsibilities ──
    # "How much does each cluster CLAIM each point?"
    # r[i, k] = how responsible cluster k is for point i
    print("\n  [E-STEP] Compute responsibility of each cluster for each point\n")

    r = np.zeros((len(X), K))
    for i in range(len(X)):
        # numerator: weight_k * P(x_i | cluster_k)
        for k in range(K):
            r[i, k] = weights[k] * gaussian_pdf(X[i], means[k], variances[k])

        # normalize so responsibilities sum to 1
        total = r[i].sum()
        r[i] /= total

        print(f"    Point {X[i]:>4.1f}: "
              f"r(cluster0)={r[i, 0]:.3f}  r(cluster1)={r[i, 1]:.3f}  "
              f"({'← A' if r[i, 0] > 0.5 else '← B'})")

    # ── M-STEP: update parameters using responsibilities ──
    print(f"\n  [M-STEP] Update parameters using soft assignments\n")

    for k in range(K):
        # effective number of points assigned to cluster k
        N_k = r[:, k].sum()

        # new mean = weighted average of all points
        new_mean = np.sum(r[:, k] * X) / N_k

        # new variance = weighted average of squared deviations
        new_var = np.sum(r[:, k] * (X - new_mean) ** 2) / N_k

        # new weight = fraction of total responsibility
        new_weight = N_k / len(X)

        print(f"    Cluster {k}: N_k={N_k:.2f} effective points")
        print(f"      mean:   {means[k]:.3f} → {new_mean:.3f}")
        print(f"      var:    {variances[k]:.3f} → {new_var:.3f}")
        print(f"      weight: {weights[k]:.3f} → {new_weight:.3f}")

        means[k] = new_mean
        variances[k] = new_var
        weights[k] = new_weight
    print()

print("=" * 60)
print("FINAL RESULT")
print("=" * 60)
for k in range(K):
    print(f"  Cluster {k}: mean={means[k]:.3f}, var={variances[k]:.3f}, weight={weights[k]:.2f}")
print(f"""
COMPARISON TO K-MEANS:
  K-Means:  point 1.0 → cluster A (100%)
  GMM:      point 1.0 → cluster A (99.9%), cluster B (0.1%)

  K-Means gives HARD labels. GMM gives SOFT probabilities.
  GMM is better when clusters overlap and you need uncertainty.

RECIPE:
  E-step: r[i,k] = weight[k] * P(x_i|k) / Σ_j weight[j] * P(x_i|j)
  M-step: mean[k]   = Σ r[i,k]*x_i / Σ r[i,k]
          var[k]    = Σ r[i,k]*(x_i - mean[k])² / Σ r[i,k]
          weight[k] = (Σ r[i,k]) / n
""")
