
# ML Coding Cheat Sheet — Dropbox Dash MLE Interview

## Quick Reference

| Algorithm | Type | Normalize? | Convergence | Key Hyperparameter |
|-----------|------|-----------|-------------|-------------------|
| Linear Regression | Regression | Yes | loss change < tol | learning rate |
| Logistic Regression | Classification | Yes | loss change < tol | learning rate |
| Naive Bayes | Classification | No | N/A (no training loop) | smoothing (Laplace) |
| GMM | Clustering | Yes | log-likelihood change < tol | n_components |
| KNN | Classification | Yes | N/A (no training) | k |
| SVM | Classification | Yes | loss change < tol | C (regularization) |
| Decision Tree | Both | No | pure nodes / max depth | max_depth |
| Random Forest | Both | No | n_trees (diminishing returns) | n_trees, max_depth |
| Gradient Boosting | Both | No | validation loss early stop | lr, n_trees, max_depth |
| K-Means | Clustering | Yes | centroids stop moving | k |

---

## 1. Linear Regression (Gradient Descent)

**Model**: `y = X @ w + b`
**Loss**: MSE = `mean((y_pred - y)^2)`
**Gradient**: `dw = (1/n) * X.T @ error`, `db = (1/n) * sum(error)`

```python
class LinearRegression:
    def __init__(self, lr=0.01, epochs=1000, tol=1e-6):
        self.lr, self.epochs, self.tol = lr, epochs, tol
        self.w, self.b, self.losses = None, 0.0, []

    def fit(self, X, y):
        n, d = X.shape
        self.w, self.b, self.losses = np.zeros(d), 0.0, []
        for epoch in range(self.epochs):
            y_pred = X @ self.w + self.b
            loss = np.mean((y_pred - y) ** 2)
            self.losses.append(loss)
            if epoch > 0 and abs(self.losses[-2] - self.losses[-1]) < self.tol:
                break
            error = y_pred - y
            self.w -= self.lr * (1/n) * X.T @ error
            self.b -= self.lr * (1/n) * np.sum(error)

    def predict(self, X):
        return X @ self.w + self.b
```

**Toy dataset**: `y = 3*X[:,0] + 5*X[:,1] + noise`
**Evaluate**: RMSE = `sqrt(mean((y-y_pred)^2))`, R^2 = `1 - SS_res/SS_tot`
**Convergence**: stop when loss change < tol
**Overfit**: add L2 regularization (Ridge): `dw += lambda * w`

---

## 2. Logistic Regression

**Only 3 differences from linear regression:**
1. Output: `sigmoid(X @ w + b)` instead of `X @ w + b`
2. Loss: BCE instead of MSE
3. Predict: `sigmoid > 0.5 → class 1`

**Gradient is IDENTICAL**: `dw = (1/n) * X.T @ (y_pred - y)`

```python
class LogisticRegression:
    def __init__(self, lr=0.01, epochs=1000, tol=1e-6):
        self.lr, self.epochs, self.tol = lr, epochs, tol
        self.w, self.b, self.losses = None, 0.0, []

    def _sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def fit(self, X, y):
        n, d = X.shape
        self.w, self.b, self.losses = np.zeros(d), 0.0, []
        for epoch in range(self.epochs):
            y_pred = self._sigmoid(X @ self.w + self.b)
            eps = 1e-9
            loss = -np.mean(y*np.log(y_pred+eps) + (1-y)*np.log(1-y_pred+eps))
            self.losses.append(loss)
            if epoch > 0 and abs(self.losses[-2] - self.losses[-1]) < self.tol:
                break
            error = y_pred - y
            self.w -= self.lr * (1/n) * X.T @ error
            self.b -= self.lr * (1/n) * np.sum(error)

    def predict(self, X):
        return (self._sigmoid(X @ self.w + self.b) > 0.5).astype(int)
```

**Toy dataset**: two blobs at `[-1,-1]` and `[1,1]`
**Evaluate**: accuracy, precision = `TP/(TP+FP)`, recall = `TP/(TP+FN)`, F1
**Why BCE not MSE?** MSE + sigmoid = non-convex (many local minima). BCE = convex.

---

## 3. Naive Bayes (Generative)

**Idea**: Use Bayes' theorem. Assume features are independent given the class.
`P(class|features) ∝ P(class) × P(f1|class) × P(f2|class) × ...`

**Generative** = models P(X|class) and P(class), then uses Bayes to get P(class|X).
**Discriminative** (logistic reg) = directly models P(class|X).

```python
class NaiveBayes:
    def fit(self, X, y):
        self.classes = np.unique(y)
        self.priors = {}    # P(class)
        self.means = {}     # mean of each feature per class
        self.stds = {}      # std of each feature per class
        for c in self.classes:
            X_c = X[y == c]
            self.priors[c] = len(X_c) / len(X)
            self.means[c] = X_c.mean(axis=0)
            self.stds[c] = X_c.std(axis=0) + 1e-9  # avoid /0

    def _log_prob(self, x, c):
        # log P(x|class) using Gaussian assumption
        log_prior = np.log(self.priors[c])
        log_likelihood = -0.5 * np.sum(
            np.log(2 * np.pi * self.stds[c]**2) +
            ((x - self.means[c]) / self.stds[c])**2
        )
        return log_prior + log_likelihood

    def predict(self, X):
        return np.array([
            max(self.classes, key=lambda c: self._log_prob(x, c))
            for x in X
        ])
```

**Key tradeoffs**:
- Fast training (just compute means/stds), fast inference
- Works well with small data and high-dimensional features (text/spam)
- Independence assumption is usually wrong but still works surprisingly well
- No convergence — single pass through data

---

## 4. GMM (Gaussian Mixture Model — Generative)

**Idea**: Data comes from K Gaussian clusters. Find their means, covariances, and mixing weights using EM (Expectation-Maximization).

```python
class GMM:
    def __init__(self, k=2, epochs=100, tol=1e-6):
        self.k, self.epochs, self.tol = k, epochs, tol

    def fit(self, X):
        n, d = X.shape
        # Initialize
        self.means = X[np.random.choice(n, self.k, replace=False)]
        self.covs = [np.eye(d)] * self.k
        self.weights = np.ones(self.k) / self.k  # equal mixing

        for _ in range(self.epochs):
            # E-step: compute responsibility of each cluster for each point
            resp = np.zeros((n, self.k))
            for j in range(self.k):
                resp[:, j] = self.weights[j] * self._gaussian(X, self.means[j], self.covs[j])
            resp /= resp.sum(axis=1, keepdims=True)  # normalize rows

            # M-step: update means, covs, weights using responsibilities
            for j in range(self.k):
                Nj = resp[:, j].sum()
                self.means[j] = (resp[:, j] @ X) / Nj
                diff = X - self.means[j]
                self.covs[j] = (resp[:, j][:, None] * diff).T @ diff / Nj
                self.weights[j] = Nj / n

    def _gaussian(self, X, mean, cov):
        d = X.shape[1]
        diff = X - mean
        inv_cov = np.linalg.inv(cov + 1e-6 * np.eye(d))
        exponent = -0.5 * np.sum(diff @ inv_cov * diff, axis=1)
        return np.exp(exponent) / np.sqrt((2*np.pi)**d * np.linalg.det(cov))
```

**Key tradeoffs**:
- Soft clustering (each point has % membership) vs K-Means (hard assignment)
- Can model elliptical clusters (K-Means only spherical)
- More expensive than K-Means (covariance matrices)
- Convergence: log-likelihood stops increasing

---

## 5. KNN (Distance-Based)

**Idea**: No training. For a new point, find K nearest neighbors, majority vote.

```python
class KNN:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X, self.y = X, y  # just store the data

    def predict(self, X):
        preds = []
        for x in X:
            dists = np.sqrt(np.sum((self.X - x)**2, axis=1))  # euclidean
            nearest = np.argsort(dists)[:self.k]               # k closest
            votes = self.y[nearest]
            preds.append(np.bincount(votes).argmax())          # majority vote
        return np.array(preds)
```

**Key tradeoffs**:
- No training (lazy learner), but slow prediction: O(n) per query
- k=1: overfits (noisy), k=large: underfits (too smooth)
- MUST normalize — distance is scale-dependent
- Curse of dimensionality: distances become meaningless in high-D

---

## 6. SVM (Support Vector Machine)

**Idea**: Find the hyperplane that maximizes the margin between classes.
Hinge loss: `max(0, 1 - y * (w·x + b))` — penalizes points inside the margin.

```python
class SVM:
    def __init__(self, lr=0.001, epochs=1000, C=1.0):
        self.lr, self.epochs, self.C = lr, epochs, C
        self.w, self.b = None, 0.0

    def fit(self, X, y):
        y = np.where(y == 0, -1, 1)  # SVM uses {-1, +1} not {0, 1}
        n, d = X.shape
        self.w, self.b = np.zeros(d), 0.0

        for _ in range(self.epochs):
            for i in range(n):
                margin = y[i] * (X[i] @ self.w + self.b)
                if margin >= 1:
                    # correctly classified, outside margin → just regularize
                    self.w -= self.lr * self.w
                else:
                    # misclassified or inside margin → update
                    self.w -= self.lr * (self.w - self.C * y[i] * X[i])
                    self.b += self.lr * self.C * y[i]

    def predict(self, X):
        return (X @ self.w + self.b >= 0).astype(int)
```

**Key tradeoffs**:
- C (regularization): large C = hard margin (overfit), small C = soft margin (underfit)
- Kernel trick: map to higher-D without computing it (RBF, polynomial)
- Works well on small-medium data, struggles with very large datasets
- Support vectors = the points closest to the boundary (the ones that matter)

---

## 7. Decision Tree

**Gini**: `1 - p0^2 - p1^2` (0 = pure, 0.5 = worst)
**Algorithm**: for each feature x threshold → pick lowest weighted Gini → recurse

```python
def gini(y):
    if len(y) == 0: return 0
    p = np.mean(y)
    return 1 - p**2 - (1-p)**2

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature, self.threshold = feature, threshold
        self.left, self.right, self.value = left, right, value

class DecisionTree:
    def __init__(self, max_depth=5, min_samples=2):
        self.max_depth, self.min_samples = max_depth, min_samples

    def _best_split(self, X, y):
        best_gini, best_f, best_t = float('inf'), None, None
        for f in range(X.shape[1]):
            for t in np.unique(X[:, f]):
                left = X[:, f] <= t
                if left.sum() == 0 or (~left).sum() == 0: continue
                n = len(y)
                wg = (left.sum()/n)*gini(y[left]) + ((~left).sum()/n)*gini(y[~left])
                if wg < best_gini:
                    best_gini, best_f, best_t = wg, f, t
        return best_f, best_t

    def _build(self, X, y, depth):
        if gini(y)==0 or len(y)<self.min_samples or depth>=self.max_depth:
            return Node(value=int(np.round(np.mean(y))))
        f, t = self._best_split(X, y)
        if f is None: return Node(value=int(np.round(np.mean(y))))
        mask = X[:, f] <= t
        return Node(f, t, self._build(X[mask],y[mask],depth+1),
                         self._build(X[~mask],y[~mask],depth+1))

    def fit(self, X, y): self.root = self._build(X, y, 0)

    def _predict_one(self, x, node):
        if node.value is not None: return node.value
        if x[node.feature] <= node.threshold:
            return self._predict_one(x, node.left)
        return self._predict_one(x, node.right)

    def predict(self, X):
        return np.array([self._predict_one(x, self.root) for x in X])
```

**Key tradeoffs**:
- Interpretable, no normalization needed
- Overfits easily → limit max_depth, min_samples
- Alternative to Gini: information gain (entropy-based): `H = -sum(p * log(p))`

---

## 8. Bagging / Random Forest

**Bagging**: N trees on bootstrap samples → majority vote
**Random Forest**: Bagging + random feature subsets at each split

```python
class BaggingClassifier:
    def __init__(self, n_trees=10, max_depth=5):
        self.n_trees, self.max_depth = n_trees, max_depth

    def fit(self, X, y):
        self.trees = []
        for _ in range(self.n_trees):
            idx = np.random.randint(0, len(y), size=len(y))  # bootstrap
            tree = DecisionTree(max_depth=self.max_depth)
            tree.fit(X[idx], y[idx])
            self.trees.append(tree)

    def predict(self, X):
        all_preds = np.array([t.predict(X) for t in self.trees])
        return np.array([int(np.round(np.mean(all_preds[:,i])))
                         for i in range(X.shape[0])])
```

**Key tradeoffs**:
- Reduces variance (overfitting) vs single tree
- More trees = more stable (but diminishing returns after ~100)
- Embarrassingly parallel (each tree is independent)
- Less interpretable than single tree

---

## 9. Gradient Boosting

**Idea**: Trees sequentially fix previous errors.
`prediction = mean(y)` → for each tree: `residuals = y - pred; fit tree on residuals; pred += lr * tree`

```python
class GradientBoosting:
    def __init__(self, n_trees=10, lr=0.1):
        self.n_trees, self.lr = n_trees, lr

    def fit(self, X, y):
        self.base = np.mean(y)
        pred = np.full(len(y), self.base)
        self.stumps = []
        for _ in range(self.n_trees):
            residuals = y - pred
            # fit stump: find best single split on residuals
            best_mse, best = float('inf'), (0, 0, 0, 0)
            for f in range(X.shape[1]):
                for t in np.unique(X[:, f]):
                    left = X[:, f] <= t
                    if left.sum()==0 or (~left).sum()==0: continue
                    lv, rv = residuals[left].mean(), residuals[~left].mean()
                    mse = (np.sum((residuals[left]-lv)**2) +
                           np.sum((residuals[~left]-rv)**2)) / len(y)
                    if mse < best_mse: best_mse, best = mse, (f,t,lv,rv)
            self.stumps.append(best)
            f,t,lv,rv = best
            pred += self.lr * np.where(X[:,f]<=t, lv, rv)

    def predict(self, X):
        pred = np.full(X.shape[0], self.base)
        for f,t,lv,rv in self.stumps:
            pred += self.lr * np.where(X[:,f]<=t, lv, rv)
        return pred
```

| | Bagging | Boosting |
|---|---|---|
| Trees | Independent | Sequential |
| Each fits | Bootstrap of data | Residuals (errors) |
| Combine | Majority vote / avg | Sum of corrections |
| Tree depth | Full | Shallow (3-6) |
| Parallel? | Yes | No |
| Overfit risk | Low | Higher (use early stopping) |

---

## 10. K-Means (Clustering)

**Algorithm**: assign points to nearest centroid → recompute centroids → repeat

```python
class KMeans:
    def __init__(self, k=3, epochs=100):
        self.k, self.epochs = k, epochs

    def fit(self, X):
        idx = np.random.choice(len(X), self.k, replace=False)
        self.centroids = X[idx].copy()
        for _ in range(self.epochs):
            # assign each point to nearest centroid
            dists = np.array([np.sqrt(np.sum((X - c)**2, axis=1))
                              for c in self.centroids])  # (k, n)
            labels = np.argmin(dists, axis=0)             # (n,)
            # recompute centroids
            new_centroids = np.array([X[labels==j].mean(axis=0)
                                      for j in range(self.k)])
            if np.allclose(self.centroids, new_centroids): break
            self.centroids = new_centroids
        self.labels = labels
```

**Convergence**: centroids stop moving (`np.allclose`)
**Evaluate**: inertia (within-cluster sum of squares), silhouette score
**Choosing k**: elbow method (plot inertia vs k, pick the "elbow")
**Limitations**: assumes spherical clusters, sensitive to initialization (use k-means++)

---

## 11. Deep Learning (Brief)

### MLP (Multi-Layer Perceptron)
```
Input → Linear(d, hidden) → ReLU → Linear(hidden, out) → Softmax
```
- Just stacked `y = activation(X @ W + b)` layers
- ReLU = `max(0, x)`, kills negatives
- Backprop: chain rule to compute gradients layer by layer
- Overfit: dropout, weight decay, early stopping

### Self-Attention (Transformers)
```python
Q, K, V = X @ W_q, X @ W_k, X @ W_v
attention = softmax(Q @ K.T / sqrt(d_k)) @ V
```
- Each token attends to every other token
- `sqrt(d_k)`: prevents dot products from getting too large
- Multi-head: run H attention heads in parallel, concatenate

### CNN
- Convolution: sliding filter extracts local features
- Pooling: downsamples (max pooling keeps strongest signal)
- Good for spatial/image data (translation invariance)

### Key DL concepts for interview:
- **Batch size**: larger = more stable gradients, smaller = more noise (regularization)
- **Learning rate scheduling**: warm up, then decay
- **Overfitting signals**: train loss drops, val loss increases → early stopping
- **Loss functions**: MSE (regression), BCE (binary), CrossEntropy (multiclass)

---

## 12. Evaluation Metrics — Quick Reference

### Regression
```python
RMSE = sqrt(mean((y - y_pred)^2))     # same units as y
R^2  = 1 - SS_res / SS_tot            # 1 = perfect, 0 = predicts mean
```

### Classification
```python
Accuracy  = (TP+TN) / (TP+TN+FP+FN)  # misleading if imbalanced
Precision = TP / (TP+FP)              # "of predicted positives, how many correct?"
Recall    = TP / (TP+FN)              # "of actual positives, how many caught?"
F1        = 2*P*R / (P+R)             # harmonic mean
```

### Ranking (Dropbox-specific)
```python
nDCG@K = DCG / IDCG                   # graded relevance, log discount
MRR    = mean(1/rank_first_relevant)  # first relevant result
```

### When to use which:
- Balanced classes → accuracy is fine
- Imbalanced (spam, fraud) → precision/recall/F1
- Ranking/search → nDCG, MRR
- Regression → RMSE, R^2

---

## 13. Common Interview Questions Per Algorithm

**"How do you know when to stop?" (Convergence)**
- GD-based (linear/logistic/SVM): loss change < tolerance
- Trees: node is pure (Gini=0) or max depth
- K-Means: centroids stop moving
- Boosting: validation loss early stopping

**"How do you prevent overfitting?"**
- Linear/Logistic: L1/L2 regularization, fewer features
- Trees: limit max_depth, min_samples_leaf
- Ensemble: more trees (bagging), early stopping (boosting)
- Neural nets: dropout, weight decay, data augmentation
- All: more data, cross-validation, simpler model

**"How do you evaluate?"**
- Train/test split (80/20), cross-validation (k-fold)
- Pick metric appropriate for the problem (see section 12)
- Look at learning curves: both train and val loss

**"Time complexity?"**
- Linear/Logistic: O(n * d * epochs)
- KNN predict: O(n * d) per query (no training)
- Decision Tree: O(n * d * log(n)) per level
- K-Means: O(n * k * d * epochs)

---

# Architecture Framework — Dropbox Dash ML System Design

## The 7-Step Framework

Use this for any "Design a ML system for X" question.

### Step 1: Clarify Requirements (2 min)
- What's the user experience? What goes in, what comes out?
- Scale: how many users/documents/QPS?
- Latency: real-time (<200ms) or batch?
- What metrics define success?

### Step 2: High-Level Architecture (5 min)
Draw the end-to-end pipeline:
```
Data Collection → Feature Engineering → Model Training →
Model Serving → Monitoring → Feedback Loop
```

For search/retrieval (Dropbox Dash likely topic):
```
Query → Encoder → Stage 1: Retrieve (BM25 + ANN, ~1000 docs)
                → Stage 2: Rerank (cross-encoder, ~100 docs)
                → Stage 3: Post-process (filter, dedup, ~10 results)
```

### Step 3: Data Pipeline (5 min)
- Where does training data come from?
- How to label? (human annotators, click logs, LLM-as-judge)
- How to handle updates? (event-driven, batch re-indexing)
- Data quality: duplicates, missing values, class imbalance

### Step 4: Model Selection (5 min)
- Why this model? What alternatives? Tradeoffs?
- Bi-encoder vs cross-encoder (speed vs quality)
- Embedding dimension (768 standard, 384 for speed)
- Loss function: InfoNCE for embeddings, BCE for classifier

### Step 5: Training (5 min)
- Train/val/test split
- Hard negative mining (BM25 top results that aren't relevant)
- Fine-tuning strategy (pre-trained → domain data)
- Hyperparameter tuning: learning rate, batch size, epochs

### Step 6: Serving & Infrastructure (5 min)
| Component | Hardware | Latency |
|-----------|----------|---------|
| Embedding | GPU | ~20ms |
| ANN search (HNSW) | CPU | ~10ms |
| BM25 (Elasticsearch) | CPU | ~15ms |
| Cross-encoder rerank | GPU | ~50ms |

- Batch inference for throughput
- Model optimization: ONNX, quantization (FP16/INT8)
- Caching: Redis for frequent queries

### Step 7: Evaluation & Monitoring (3 min)
**Offline**: nDCG@10, MRR, Recall@100
**Online**: CTR, abandonment rate, reformulation rate
**A/B testing**: interleaving (mix results from A and B)
**Alerting**: if nDCG drops > 5% → rollback

---

## Dropbox Dash Specific Scenarios

### Scenario 1: "Design multimodal search across files"
- Embedding: CLIP for images, E5/BGE for text, OCR for PDFs
- Shared embedding space via contrastive learning
- Chunking: ~512 tokens, 50-token overlap
- Vector index: HNSW (Faiss), ~100GB for 500M vectors
- Access control: post-retrieval filtering by user ACL

### Scenario 2: "Design a RAG system for company docs"
- Hybrid retrieval: BM25 + dense → RRF fusion
- Rerank top-100 with cross-encoder
- LLM generates answer with inline citations
- Hallucination prevention: ground in chunks, confidence threshold
- Evaluate: retrieval recall + answer faithfulness (human/LLM-judge)

### Scenario 3: "Improve search ranking quality"
1. Measure: establish nDCG@10 baseline with human judgments
2. Diagnose: is retrieval failing (recall) or ranking failing (precision)?
3. Improve retrieval: hybrid search, better embeddings, query expansion
4. Improve ranking: cross-encoder, add features (recency, popularity, CTR)
5. Feedback loop: click logs → training data → retrain → A/B test

### Scenario 4: "Design content classification (file type / topic)"
- Feature extraction: TF-IDF / embeddings from file content
- Model: start simple (logistic regression), upgrade if needed (BERT fine-tune)
- Training data: existing file metadata + human labels
- Multi-label: files can have multiple topics → sigmoid per class
- Serving: batch classify on upload, cache results

### Key Architecture Q&A:

**"How do you handle new file types (e.g., audio)?"**
> Add new encoder (Whisper → text → embed). Same retrieval infrastructure.

**"How do you handle model updates?"**
> Shadow index: build new embeddings in background → atomic swap.

**"Bi-encoder vs cross-encoder?"**
> Bi-encoder: encode separately, fast (stage 1). Cross-encoder: encode together, accurate (stage 2).

**"How to get training data for embeddings?"**
> Click logs: (query, clicked_doc) = positive. BM25 top results not clicked = hard negatives.

**"How to handle cold-start?"**
> New docs get embedded immediately. For popularity features, use priors by file type/author.

**"Latency budget?"**
> p99 < 200ms. Encode: 20ms, ANN: 10ms, BM25: 15ms, rerank: 50ms, overhead: 50ms.