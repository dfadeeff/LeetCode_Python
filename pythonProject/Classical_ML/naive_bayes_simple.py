"""
Naive Bayes — e2e implementation with toy dataset.

The algorithm in 4 steps:
  1. For each class: compute mean & variance of each feature
  2. Compute prior probability of each class (how common is it?)
  3. For a new point: compute P(features | class) using Gaussian density
  4. Pick the class with highest: prior * likelihood

No gradient descent. No iterations. Just statistics.
"""
import numpy as np
import numpy.typing as npt


class NaiveBayesClassifier:
    def get_descriptives(self, x_train: npt.NDArray, y_train: npt.NDArray):
        """Step 1: mean and variance per feature per class."""
        classes = np.unique(y_train)
        n_classes = len(classes)
        n_features = x_train.shape[1]

        self.classes = classes
        self.mean = np.zeros((n_classes, n_features))
        self.variance = np.zeros((n_classes, n_features))

        for i, c in enumerate(classes):
            x_c = x_train[y_train == c]
            self.mean[i] = x_c.mean(axis=0)
            self.variance[i] = x_c.var(axis=0)

        return self.mean, self.variance

    def get_priors(self, y_train: npt.NDArray):
        """Step 2: P(y=k) = count(class k) / total."""
        n = len(y_train)
        self.prior = np.array([np.sum(y_train == c) / n for c in self.classes])
        return self.prior

    def gaussian_density(self, class_idx: int, x: npt.NDArray):
        """Step 3: P(x | class) assuming Gaussian distribution."""
        mean = self.mean[class_idx]
        var = self.variance[class_idx] + 1e-9  # avoid division by zero
        numerator = np.exp(-0.5 * ((x - mean) ** 2) / var)
        denominator = np.sqrt(2 * np.pi * var)
        return numerator / denominator

    def get_prediction(self, x: npt.NDArray) -> int:
        """Step 4: posterior = prior * likelihood → pick argmax."""
        posteriors = []
        for i, c in enumerate(self.classes):
            prior = self.prior[i]
            likelihood = np.prod(self.gaussian_density(i, x))
            posterior = prior * likelihood
            posteriors.append(posterior)
        return int(self.classes[np.argmax(posteriors)])

    def fit(self, x_train: npt.NDArray, y_train: npt.NDArray):
        self.get_descriptives(x_train, y_train)
        self.get_priors(y_train)

    def predict(self, x_test: npt.NDArray) -> list:
        return [self.get_prediction(x) for x in x_test]


# ── Toy dataset & walkthrough ──
if __name__ == "__main__":
    # 10 patients: [temperature, cough_severity] → 0=healthy, 1=sick
    X_train = np.array([
        [6.0, 1.0], [6.2, 0.5], [6.5, 2.0], [5.8, 1.5], [6.1, 0.8],  # healthy
        [9.0, 7.0], [8.5, 8.0], [9.2, 6.5], [8.8, 7.5], [9.5, 8.5],  # sick
    ])
    y_train = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

    clf = NaiveBayesClassifier()

    # ── Step 1: Descriptives ──
    print("=" * 60)
    print("STEP 1: Compute mean & variance per class")
    print("=" * 60)
    means, variances = clf.get_descriptives(X_train, y_train)

    X_c0 = X_train[y_train == 0]
    X_c1 = X_train[y_train == 1]
    print(X_c0)
    print(X_c1)

    print(np.sum(X_c0,axis=0))
    print(np.sum(X_c1, axis=0))
#     labels = {0: "healthy", 1: "sick"}
#     for i, c in enumerate(clf.classes):
#         pts = X_train[y_train == c]
#         print(f"\n  Class {c} ({labels[c]}): {len(pts)} patients")
#         print(f"    Temp values:  {pts[:, 0].tolist()}")
#         print(f"    Temp mean:    ({' + '.join(f'{v:.1f}' for v in pts[:, 0])}) / {len(pts)} = {means[i, 0]:.2f}")
#         print(f"    Temp var:     {variances[i, 0]:.4f}")
#         print(f"    Cough values: {pts[:, 1].tolist()}")
#         print(f"    Cough mean:   {means[i, 1]:.2f}")
#         print(f"    Cough var:    {variances[i, 1]:.4f}")
#
#     # ── Step 2: Priors ──
#     print(f"\n{'=' * 60}")
#     print("STEP 2: Compute priors P(y=k)")
#     print("=" * 60)
#     priors = clf.get_priors(y_train)
#     for i, c in enumerate(clf.classes):
#         count = np.sum(y_train == c)
#         print(f"  P(y={c}) = {count}/{len(y_train)} = {priors[i]:.2f}")
#
#     # ── Step 3 & 4: Predict with full trace ──
#     X_test = np.array([
#         [8.0, 6.0],  # should be sick
#         [6.0, 1.0],  # should be healthy
#         [7.5, 4.0],  # borderline
#     ])
#
#     print(f"\n{'=' * 60}")
#     print("STEP 3 & 4: Predict new patients")
#     print("=" * 60)
#
#     for x in X_test:
#         print(f"\n  Patient: temp={x[0]:.1f}, cough={x[1]:.1f}")
#         print(f"  {'─' * 50}")
#
#         posteriors = []
#         for i, c in enumerate(clf.classes):
#             # Gaussian density per feature
#             densities = clf.gaussian_density(i, x)
#             prior = clf.prior[i]
#             likelihood = np.prod(densities)
#             posterior = prior * likelihood
#
#             print(f"\n    Class {c} ({labels[c]}):")
#             print(f"      Prior: P(y={c}) = {prior:.2f}")
#             print(f"      P(temp={x[0]:.1f} | {labels[c]}):  mean={means[i, 0]:.2f}, "
#                   f"var={variances[i, 0]:.4f} → density = {densities[0]:.6f}")
#             print(f"      P(cough={x[1]:.1f} | {labels[c]}): mean={means[i, 1]:.2f}, "
#                   f"var={variances[i, 1]:.4f} → density = {densities[1]:.6f}")
#             print(f"      Likelihood = {densities[0]:.6f} × {densities[1]:.6f} = {likelihood:.8f}")
#             print(f"      Posterior  = {prior:.2f} × {likelihood:.8f} = {posterior:.8f}")
#             posteriors.append(posterior)
#
#         pred = clf.classes[np.argmax(posteriors)]
#         print(f"\n    → {labels[0]}: {posteriors[0]:.8f}")
#         print(f"    → {labels[1]}: {posteriors[1]:.8f}")
#         print(f"    → PREDICT: {labels[pred]} ({'correct!' if (pred == 1) == (x[0] > 7) else ''})")
#
#     # ── Batch predict ──
#     print(f"\n{'=' * 60}")
#     print("BATCH PREDICT")
#     print("=" * 60)
#     preds = clf.predict(X_test)
#     for i, x in enumerate(X_test):
#         print(f"  [{x[0]:.1f}, {x[1]:.1f}] → {labels[preds[i]]}")
#
#     print(f"""
# {'=' * 60}
# WHAT EACH STEP DOES
# {'=' * 60}
#
#   fit():
#     Step 1: mean[class][feature], var[class][feature]  ← just numpy
#     Step 2: prior[class] = count / total               ← just counting
#
#   predict(x):
#     Step 3: P(feature | class) = Gaussian(feature, mean, var)
#             = exp(-(x - mean)² / 2var) / sqrt(2π·var)
#
#     Step 4: posterior = prior × P(feat1|class) × P(feat2|class) × ...
#                                   ↑ NAIVE assumption: features independent
#             return argmax(posterior)
#
#   The "naive" part: we MULTIPLY individual feature probabilities.
#   This assumes temp and cough are INDEPENDENT given the class.
#   Usually wrong, but works surprisingly well in practice.
# """)
