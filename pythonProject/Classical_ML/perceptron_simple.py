"""
PERCEPTRON — the simplest possible classifier.

The perceptron is the ancestor of ALL neural networks.
Invented in 1958. Understanding it makes neural nets click.

HOW IT WORKS:
  1. Compute score: z = w · x + b
  2. Predict: if z >= 0 → class +1, else → class -1
  3. If WRONG: nudge weights toward the correct answer
     If RIGHT: do nothing

That's it. No loss function. No gradient. No sigmoid.
Just: "if wrong, fix it."

UPDATE RULE (only when wrong):
  w = w + lr * y * x
  b = b + lr * y

  If y=+1 but we predicted -1 (score was negative):
    w += lr * (+1) * x  → increases w·x → pushes score positive → fixes it

  If y=-1 but we predicted +1 (score was positive):
    w += lr * (-1) * x  → decreases w·x → pushes score negative → fixes it

LIMITATION:
  Perceptron can ONLY learn linearly separable data.
  If data can't be split by a straight line, it will never converge.
  (This was proven by Minsky & Papert in 1969 and nearly killed neural nets.)

  Solution: stack multiple perceptrons → Multi-Layer Perceptron (MLP)
  → that's a neural network.
"""
import numpy as np

np.random.seed(42)

# ── 10 points, 2 classes, linearly separable ──
X = np.array([
    [1.0, 2.0], [2.0, 3.0], [1.5, 1.5], [2.0, 1.0], [1.0, 0.5],
    [5.0, 5.0], [6.0, 4.0], [5.5, 5.5], [4.5, 4.0], [6.0, 6.0],
])
y = np.array([-1, -1, -1, -1, -1, 1, 1, 1, 1, 1])

print("=" * 60)
print("PERCEPTRON on 10 points")
print("=" * 60)

w = np.zeros(2)
b = 0.0
lr = 0.1

print(f"  Starting: w=[{w[0]:.1f}, {w[1]:.1f}], b={b:.1f}\n")

for epoch in range(20):
    n_mistakes = 0

    for i in range(len(X)):
        # Step 1: compute score
        score = np.dot(w, X[i]) + b

        # Step 2: predict
        pred = 1 if score >= 0 else -1

        # Step 3: if wrong, update
        if pred != y[i]:
            n_mistakes += 1
            w += lr * y[i] * X[i]   # nudge w toward correct answer
            b += lr * y[i]           # nudge b

            print(f"  Epoch {epoch+1}, point {i}: "
                  f"score={score:>6.2f} → pred={pred:>+2}, actual={y[i]:>+2} "
                  f"WRONG → w=[{w[0]:.3f}, {w[1]:.3f}] b={b:.3f}")

    if n_mistakes == 0:
        print(f"\n  Epoch {epoch+1}: 0 mistakes → CONVERGED!")
        break
    else:
        print(f"  Epoch {epoch+1}: {n_mistakes} mistakes\n")

# ── Final result ──
print(f"\n  Final: w=[{w[0]:.3f}, {w[1]:.3f}], b={b:.3f}")
print(f"  Boundary: {w[0]:.3f}*x₁ + {w[1]:.3f}*x₂ + ({b:.3f}) = 0")

preds = np.sign(X @ w + b).astype(int)
print(f"  Accuracy: {np.mean(preds == y):.0%}")

# ── Predict new points ──
print(f"\n  Predictions:")
test = np.array([[3.0, 3.0], [1.0, 1.0], [5.0, 5.0]])
for x in test:
    score = np.dot(w, x) + b
    pred = "+1" if score >= 0 else "-1"
    print(f"    [{x[0]:.1f}, {x[1]:.1f}]: score={score:>6.2f} → {pred}")


# ── Show XOR failure ──
print(f"\n{'=' * 60}")
print("XOR: Perceptron FAILS (not linearly separable)")
print("=" * 60)

X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([-1, 1, 1, -1])  # XOR pattern

print("""
    x₁  x₂  │  y
    ─────────┼────
     0   0   │  -1
     0   1   │  +1
     1   0   │  +1
     1   1   │  -1    ← no line can separate this!
""")

w_xor = np.zeros(2)
b_xor = 0.0

for epoch in range(100):
    mistakes = 0
    for i in range(len(X_xor)):
        score = np.dot(w_xor, X_xor[i]) + b_xor
        pred = 1 if score >= 0 else -1
        if pred != y_xor[i]:
            mistakes += 1
            w_xor += 0.1 * y_xor[i] * X_xor[i]
            b_xor += 0.1 * y_xor[i]
    if mistakes == 0:
        break

preds_xor = np.sign(X_xor @ w_xor + b_xor)
acc = np.mean(preds_xor == y_xor)
print(f"  After 100 epochs: accuracy = {acc:.0%}")
print(f"  Never converges! A single perceptron CANNOT learn XOR.")

print(f"""
{'=' * 60}
PERCEPTRON → NEURAL NETWORK (the bridge)
{'=' * 60}

  Perceptron:       z = w·x + b → sign(z)
                    One linear boundary. Can't do XOR.

  MLP (2 layers):   h = σ(W₁·x + b₁)     ← hidden layer
                    z = W₂·h + b₂          ← output layer
                    Multiple boundaries combined. CAN do XOR.

  That's the jump from classical ML to deep learning.
  Stack perceptrons → neural network.

{'=' * 60}
COMPARISON: Perceptron vs SVM vs Logistic Regression
{'=' * 60}

  ┌──────────────────┬──────────────────┬──────────────────┬─────────────────┐
  │                  │ Perceptron       │ SVM              │ Logistic Reg    │
  ├──────────────────┼──────────────────┼──────────────────┼─────────────────┤
  │ Finds boundary?  │ ANY boundary     │ BEST boundary    │ A boundary      │
  │                  │ (first one that  │ (maximum margin) │ (max likelihood)│
  │                  │  works)          │                  │                 │
  │ Loss function    │ None             │ Hinge loss       │ Cross-entropy   │
  │ Output           │ -1 or +1 (hard)  │ -1 or +1 (hard)  │ probability     │
  │ Update rule      │ if wrong: w+=y*x │ gradient descent │ gradient descent│
  │ Non-separable    │ Never converges  │ Soft margin (C)  │ Always works    │
  │ Invented         │ 1958             │ 1992             │ 1958            │
  └──────────────────┴──────────────────┴──────────────────┴─────────────────┘
""")