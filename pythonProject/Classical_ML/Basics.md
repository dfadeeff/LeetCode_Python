# ML Basics: Linear & Logistic Regression Derivations

## The Universal ML Training Loop

Every ML model (linear regression, logistic regression, neural networks) follows the same loop:

```
┌─────────────────────────────────────────────────────┐
│  1. FORWARD PASS (feed_forward)                     │
│     Push input through the model → get prediction   │
│                                                     │
│  2. COMPUTE LOSS                                    │
│     Compare prediction to truth → get single number │
│                                                     │
│  3. BACKWARD PASS (backpropagation)                 │
│     Compute gradients: how does each weight          │
│     affect the loss? (chain rule of calculus)        │
│                                                     │
│  4. UPDATE WEIGHTS                                  │
│     Nudge weights opposite to gradient               │
│     w = w - lr * gradient                           │
│                                                     │
│  5. REPEAT until loss stops decreasing              │
└─────────────────────────────────────────────────────┘
```

In our simple implementations, `fit()` contains all 5 steps.
In neural network frameworks (PyTorch), they are split into separate calls:
- `output = model.forward(X)` → step 1
- `loss = criterion(output, y)` → step 2
- `loss.backward()` → step 3
- `optimizer.step()` → step 4

---

## Linear Regression

### Model (Forward Pass)

```
ŷ = w · x + b
```

- `w` (weight/slope) — how much y changes per unit of x
- `b` (bias/intercept) — value of y when x = 0
- `ŷ` (y-hat) — our prediction

With multiple features: `ŷ = X @ w + b` (matrix multiply)

### Loss Function

**Mean Squared Error (MSE):**

```
L = (1/2n) · Σ(ŷᵢ - yᵢ)²
```

Why squared?
- Makes all errors positive (error of -10 is as bad as +10)
- Penalizes big errors more (error of 20 → 400, error of 10 → 100)
- Smooth and differentiable → we can take derivatives
- Convex → only one minimum, gradient descent will find it

Why 1/2n? The `1/2` cancels with the `2` when we differentiate. Optional — just makes the gradient cleaner.

### Backward Pass (Gradient Derivation)

We need: **how does the loss change when we nudge w?** → `∂L/∂w`

```
L = (1/2n) · Σ(ŷᵢ - yᵢ)²           ← loss
  = (1/2n) · Σ(w·xᵢ + b - yᵢ)²     ← substitute ŷ = w·x + b
```

**Derivative with respect to w** (chain rule):

```
∂L/∂w = (1/2n) · Σ 2·(w·xᵢ + b - yᵢ) · xᵢ     ← chain rule: derivative of ()² times derivative of inside w.r.t. w
       = (1/n) · Σ (ŷᵢ - yᵢ) · xᵢ                ← the 2 and 1/2 cancel
       = (1/n) · Xᵀ · (ŷ - y)                     ← vector form
```

**Derivative with respect to b:**

```
∂L/∂b = (1/2n) · Σ 2·(w·xᵢ + b - yᵢ) · 1        ← derivative of (w·x + b) w.r.t. b is 1
       = (1/n) · Σ (ŷᵢ - yᵢ)                      ← simplify
```

### Update Rule

```
w = w - lr · ∂L/∂w
b = b - lr · ∂L/∂b
```

Minus because gradient points **uphill** (direction of steepest increase). We want to go **downhill**.

### Mapping to Code

```python
# FORWARD
y_pred = self.w * X + self.b              # ŷ = w·x + b

# LOSS
loss = 0.5 * np.mean((y_pred - y) ** 2)  # (1/2n) · Σ(ŷ-y)²

# BACKWARD
error = y_pred - y                        # (ŷ - y), shape (n,)
dw = (1/n) * np.dot(X, error)            # ∂L/∂w = (1/n) · Xᵀ · error
db = (1/n) * np.sum(error)               # ∂L/∂b = (1/n) · Σ error

# UPDATE
self.w -= self.lr * dw
self.b -= self.lr * db
```

The `1/2` in the loss cancels with the `2` from the derivative of `()²`, so the gradient is cleanly `(1/n)` — matching logistic regression exactly.

---

## Logistic Regression

### Model (Forward Pass)

```
z = w · x + b          ← same linear combination as linear regression
ŷ = σ(z)               ← sigmoid squashes z into [0, 1]
```

**Sigmoid function:**

```
σ(z) = 1 / (1 + e⁻ᶻ)
```

```
σ(-∞) → 0       "definitely class 0"
σ(0)  = 0.5     "50/50"
σ(+∞) → 1       "definitely class 1"
```

The output ŷ is now a **probability**: P(class=1 | x).

**Key sigmoid property** (used in backward pass):

```
σ'(z) = σ(z) · (1 - σ(z))
```

### Loss Function

**Binary Cross-Entropy (BCE):**

```
L = -(1/n) · Σ [ yᵢ · log(ŷᵢ) + (1-yᵢ) · log(1-ŷᵢ) ]
```

How to read this — it has two cases:
- When `y=1`: loss = `-log(ŷ)`. If ŷ=0.99 → loss=0.01 (good!). If ŷ=0.01 → loss=4.6 (terrible!)
- When `y=0`: loss = `-log(1-ŷ)`. If ŷ=0.01 → loss=0.01 (good!). If ŷ=0.99 → loss=4.6 (terrible!)

Why not MSE?
- MSE + sigmoid = non-convex loss surface (many local minima, GD gets stuck)
- BCE + sigmoid = convex → guaranteed to find the best weights

### Backward Pass (Gradient Derivation)

This is the beautiful part. Despite different loss and sigmoid, **the gradient has the same form as linear regression**.

**Step-by-step chain rule:**

We need `∂L/∂w`. The chain goes: `L → ŷ → z → w`

```
∂L/∂w = (∂L/∂ŷ) · (∂ŷ/∂z) · (∂z/∂w)
         ↑            ↑          ↑
         BCE          sigmoid    linear
         derivative   derivative derivative
```

**Each piece:**

```
∂z/∂w = x                                    ← z = w·x + b, derivative w.r.t. w is x

∂ŷ/∂z = σ(z)·(1-σ(z)) = ŷ·(1-ŷ)            ← sigmoid derivative

∂L/∂ŷ = -(y/ŷ) + (1-y)/(1-ŷ)               ← BCE derivative
       = -(y/ŷ) + (1-y)/(1-ŷ)
       = (-y·(1-ŷ) + (1-y)·ŷ) / (ŷ·(1-ŷ))  ← common denominator
       = (-y + yŷ + ŷ - yŷ) / (ŷ·(1-ŷ))
       = (ŷ - y) / (ŷ·(1-ŷ))                ← simplify
```

**Now multiply all three:**

```
∂L/∂w = [(ŷ - y) / (ŷ·(1-ŷ))] · [ŷ·(1-ŷ)] · x
                                   ↑___________↑
                                   these cancel!
       = (ŷ - y) · x
```

**The sigmoid derivative perfectly cancels with the BCE derivative!**

For the full batch:

```
∂L/∂w = (1/n) · Xᵀ · (ŷ - y)       ← SAME as linear regression!
∂L/∂b = (1/n) · Σ(ŷ - y)           ← SAME as linear regression!
```

This is why the gradient code is identical in both implementations.

### Mapping to Code

```python
# FORWARD
z = X @ self.w + self.b               # linear combination (same as LinReg)
y_pred = self._sigmoid(z)             # NEW: squash to [0,1]

# LOSS
eps = 1e-9                             # avoid log(0)
loss = -np.mean(y * np.log(y_pred + eps) + (1-y) * np.log(1 - y_pred + eps))  # BCE

# BACKWARD — identical to linear regression!
error = y_pred - y
dw = (1/n) * X.T @ error
db = (1/n) * np.sum(error)

# UPDATE — identical to linear regression
self.w -= self.lr * dw
self.b -= self.lr * db

# PREDICT
prediction = 1 if sigmoid(w·x + b) > 0.5 else 0
```

---

## Side-by-Side Comparison

```
                    LINEAR REGRESSION          LOGISTIC REGRESSION
                    ─────────────────          ───────────────────
Task                Predict a number           Predict a class (0/1)

Forward pass        ŷ = w·x + b               ŷ = sigmoid(w·x + b)
                    ↑ any real number           ↑ between 0 and 1

Loss function       MSE = mean((ŷ-y)²)        BCE = -mean(y·log(ŷ) + (1-y)·log(1-ŷ))

Gradient ∂L/∂w      (1/n) · Xᵀ · (ŷ-y)       (1/n) · Xᵀ · (ŷ-y)    ← SAME!
Gradient ∂L/∂b      (1/n) · Σ(ŷ-y)            (1/n) · Σ(ŷ-y)        ← SAME!

Update rule         w -= lr · dw               w -= lr · dw            ← SAME!

Output              continuous value            0 or 1 (threshold 0.5)

Evaluation          RMSE, R²                   Accuracy, Precision,
                                               Recall, F1
```

---

## Forward & Backward — Neural Network Terminology

In neural networks, the same steps have specific names:

### Forward Pass (`feed_forward` / `forward`)

Data flows **input → output**, layer by layer:

```
Input X → [Linear: z = W·x + b] → [Activation: a = σ(z)] → Output ŷ
```

Each layer transforms the data. We save intermediate values (z, a) because we need them for the backward pass.

### Backward Pass (`backward` / `backpropagation`)

Gradients flow **output → input**, layer by layer (reverse order):

```
Loss → ∂L/∂ŷ → ∂L/∂z → ∂L/∂W, ∂L/∂b → ∂L/∂x (passed to previous layer)
```

This is just the **chain rule** applied repeatedly. Each layer computes:
1. Gradient of loss w.r.t. its output (received from next layer)
2. Gradient of loss w.r.t. its weights (used to update this layer)
3. Gradient of loss w.r.t. its input (passed to previous layer)

### Why the names?

```
FORWARD:  X ──→ z ──→ ŷ ──→ Loss        (compute prediction)
                                          data flows forward

BACKWARD: X ←── z ←── ŷ ←── Loss        (compute gradients)
                                          gradients flow backward
```

In our simple models, there's only **one layer**, so forward = one multiply, backward = one gradient. In deep networks with 100 layers, the chain rule propagates through all of them — hence "back-propagation."

### Our Code vs Neural Network Code

```
OUR fit() FUNCTION:              PYTORCH EQUIVALENT:
─────────────────────            ─────────────────────
y_pred = w*X + b                 output = model.forward(X)
loss = mean((y_pred-y)²)         loss = criterion(output, y)
dw = (1/n) * X.T @ error        loss.backward()
self.w -= lr * dw                optimizer.step()
```

Same 4 steps, just packaged differently. Understanding our from-scratch version means you understand what PyTorch does under the hood.

---

## Interview Quick Reference

**Q: "Walk me through how gradient descent works."**
> Start with random weights. Forward pass to get predictions. Compute loss. Backward pass to get gradients (partial derivatives telling us which direction increases loss). Update weights in the opposite direction. Repeat until loss converges.

**Q: "Why is the gradient the same for linear and logistic regression?"**
> The sigmoid derivative σ'(z) = σ(z)·(1-σ(z)) cancels with the BCE loss derivative, leaving just (ŷ - y)·x — the same as MSE gradient for linear regression. This isn't a coincidence; BCE was specifically designed as the "natural" loss for sigmoid outputs.

**Q: "Why BCE and not MSE for classification?"**
> MSE + sigmoid creates a non-convex loss surface with flat regions where gradients vanish. BCE is convex for logistic regression, so gradient descent always finds the global minimum.

**Q: "How do you know when to stop training?"**
> Monitor the loss. Stop when the change between consecutive epochs is below a threshold (tolerance). Other options: validation loss starts increasing (early stopping / overfitting signal), or gradient magnitude approaches zero.

**Q: "What is backpropagation?"**
> Just the chain rule applied layer by layer from output back to input. Each layer computes its local gradient and passes it backward. In our 1-layer models, it's one chain rule step. In deep networks, it chains through many layers.