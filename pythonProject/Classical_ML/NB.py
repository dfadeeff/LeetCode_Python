import numpy as np

np.random.seed(10)

n_per_class = 5
X_0 = np.random.randn(n_per_class, 2) * 1.0 + np.array([-1, -1])
X_1 = np.random.randn(n_per_class, 2) * 1.0 + np.array([1, 1])
X = np.vstack([X_0, X_1])
y = np.array([0] * n_per_class + [1] * n_per_class)

if __name__ == "__main__":
    # print(X)
    # print(y)
    # Training: just compute statistics
    print("    TRAINING (just computing statistics):")
    print()

    for k in [0, 1]:
        X_k = X[y == k]
        prior = len(X_k) / len(X)
        mean = X_k.mean(axis=0)
        var = X_k.var(axis=0)
        print(f"    Class {k}:")
        print(f"      Prior P(y={k}) = {prior:.2f}")
        print(f"      Feature 1: mean={mean[0]:.3f}, variance={var[0]:.3f}")
        print(f"      Feature 2: mean={mean[1]:.3f}, variance={var[1]:.3f}")
        print()
print("    → This IS the trained model. Just 6 numbers per class.")
print("    → No gradient descent. No iterations. Instant training.")

# Prediction for a new point
x_new = np.array([0.5, 0.8])
print(f"\n    PREDICTION for new point x = {x_new}:")
print()

for k in [0, 1]:
    X_k = X[y == k]
    prior = len(X_k) / len(X)
    mean = X_k.mean(axis=0)
    var = X_k.var(axis=0) + 1e-9

    # Log-likelihood for each feature
    log_prior = np.log(prior)
    log_likelihood = -0.5 * np.log(2 * np.pi * var) - (x_new - mean)**2 / (2 * var)
    total_log_likelihood = np.sum(log_likelihood)
    log_posterior = log_prior + total_log_likelihood

    print(f"    Class {k}:")
    print(f"      log P(y={k}) = {log_prior:.4f}")
    print(f"      log P(x₁={x_new[0]:.1f} | y={k}) = {log_likelihood[0]:.4f}")
    print(f"      log P(x₂={x_new[1]:.1f} | y={k}) = {log_likelihood[1]:.4f}")
    print(f"      log P(y={k}|x) ∝ {log_prior:.4f} + {total_log_likelihood:.4f} = {log_posterior:.4f}")
    print()

print("    → Class 1 has higher log-posterior → predict class 1")
print("    → Makes sense: x=[0.5, 0.8] is closer to the class 1 center at [1, 1]")