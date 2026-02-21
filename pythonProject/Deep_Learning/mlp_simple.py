"""
MLP (Multi-Layer Perceptron) — from scratch.

The perceptron can't solve XOR. The fix: STACK perceptrons into layers.

  Perceptron:   x → [w·x + b] → sign() → output
                One boundary. Linear only.

  MLP:          x → [W₁·x + b₁] → ReLU → [W₂·h + b₂] → sigmoid → output
                     └─ layer 1 ──┘        └─ layer 2 ──┘
                Multiple boundaries combined. Can learn ANY function.

TWO KEY IDEAS:
  1. FORWARD PASS:  push data through layers, get prediction
  2. BACKPROPAGATION: push error backwards through layers, update weights

Backprop is just the CHAIN RULE from calculus applied layer by layer.
"""
import numpy as np

np.random.seed(42)


# ================================================================
# ACTIVATION FUNCTIONS
# ================================================================
def sigmoid(z):
    """Squashes any number to (0, 1). Used for output layer (probabilities)."""
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))


def sigmoid_derivative(a):
    """Derivative of sigmoid. Input is the ALREADY-ACTIVATED value."""
    return a * (1 - a)


def relu(z):
    """ReLU: max(0, z). Used for hidden layers. Dead simple, works great."""
    return np.maximum(0, z)


def relu_derivative(z):
    """Derivative of ReLU: 1 if z > 0, else 0."""
    return (z > 0).astype(float)


# ================================================================
# MLP CLASS
# ================================================================
class MLP:
    def __init__(self, layer_sizes):
        """
        layer_sizes: e.g. [2, 4, 1] means:
          - 2 input features
          - 4 neurons in hidden layer
          - 1 output neuron
        """
        self.layer_sizes = layer_sizes
        self.weights = []
        self.biases = []

        # Initialize weights (Xavier initialization)
        for i in range(len(layer_sizes) - 1):
            n_in = layer_sizes[i]
            n_out = layer_sizes[i + 1]
            w = np.random.randn(n_in, n_out) * np.sqrt(2.0 / n_in)
            b = np.zeros((1, n_out))
            self.weights.append(w)
            self.biases.append(b)

    def forward(self, X):
        """
        FORWARD PASS: push data through all layers.
        Store intermediate values for backprop.

        X → [W1·X + b1] → ReLU → [W2·h + b2] → sigmoid → output
        """
        self.z_values = []  # pre-activation (before ReLU/sigmoid)
        self.a_values = [X]  # post-activation (after ReLU/sigmoid)

        current = X
        for i in range(len(self.weights)):
            # Linear: z = X @ W + b
            z = current @ self.weights[i] + self.biases[i]
            self.z_values.append(z)

            # Activation
            if i == len(self.weights) - 1:
                # Last layer: sigmoid (output probability)
                a = sigmoid(z)
            else:
                # Hidden layers: ReLU
                a = relu(z)

            self.a_values.append(a)
            current = a

        return current

    def backward(self, X, y, lr):
        """
        BACKPROPAGATION: compute gradients layer by layer, back to front.

        This is just the chain rule:
          dL/dW2 = dL/da2 * da2/dz2 * dz2/dW2
          dL/dW1 = dL/da2 * da2/dz2 * dz2/da1 * da1/dz1 * dz1/dW1

        In code, we compute "delta" at each layer and propagate it backwards.
        """
        n = len(X)
        n_layers = len(self.weights)

        # Output layer error: dL/dz_last
        # For sigmoid + binary cross-entropy, this simplifies to: (prediction - actual)
        output = self.a_values[-1]
        delta = output - y.reshape(-1, 1)  # shape: (n_samples, 1)

        # Go backwards through layers
        for i in range(n_layers - 1, -1, -1):
            a_prev = self.a_values[i]  # activation of previous layer

            # Gradients for this layer's weights and biases
            dW = (1 / n) * a_prev.T @ delta
            db = (1 / n) * np.sum(delta, axis=0, keepdims=True)

            # Propagate delta to previous layer (if not at input)
            if i > 0:
                delta = delta @ self.weights[i].T  # push error back
                delta = delta * relu_derivative(self.z_values[i - 1])  # through activation

            # Update weights
            self.weights[i] -= lr * dW
            self.biases[i] -= lr * db

    def train(self, X, y, lr=0.1, epochs=1000, verbose=True):
        for epoch in range(epochs):
            # Forward
            output = self.forward(X)

            # Loss: binary cross-entropy
            eps = 1e-9
            loss = -np.mean(y.reshape(-1, 1) * np.log(output + eps) +
                            (1 - y.reshape(-1, 1)) * np.log(1 - output + eps))

            # Backward
            self.backward(X, y, lr)

            if verbose and (epoch < 5 or (epoch + 1) % 200 == 0):
                preds = (output.flatten() >= 0.5).astype(int)
                acc = np.mean(preds == y)
                print(f"    Epoch {epoch + 1:>4}: loss={loss:.4f}  acc={acc:.0%}")

    def predict(self, X):
        output = self.forward(X)
        return (output.flatten() >= 0.5).astype(int)


# ================================================================
# TEST 1: XOR — the problem perceptron couldn't solve
# ================================================================
print("=" * 60)
print("TEST 1: XOR (perceptron failed at this)")
print("=" * 60)

X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y_xor = np.array([0, 1, 1, 0])

print("""
    x₁  x₂  │  y
    ─────────┼────
     0   0   │  0
     0   1   │  1
     1   0   │  1
     1   1   │  0    ← no line can do this, MLP can!
""")

print(f"  Architecture: [2, 4, 1]  (2 inputs → 4 hidden → 1 output)\n")

mlp = MLP([2, 4, 1])
mlp.train(X_xor, y_xor, lr=1.0, epochs=1000)

print(f"\n  Predictions:")
probs = mlp.forward(X_xor).flatten()
for i in range(len(X_xor)):
    pred = 1 if probs[i] >= 0.5 else 0
    print(f"    [{X_xor[i][0]:.0f}, {X_xor[i][1]:.0f}] → {probs[i]:.4f} → {pred}  (actual: {y_xor[i]})")


# ================================================================
# TEST 2: Two moons — nonlinear boundary
# ================================================================
print(f"\n{'=' * 60}")
print("TEST 2: Nonlinear classification (two moons)")
print("=" * 60)

# Generate two interleaving half-moons
n = 100
t = np.linspace(0, np.pi, n)
X_moon1 = np.column_stack([np.cos(t), np.sin(t)]) + np.random.randn(n, 2) * 0.1
X_moon2 = np.column_stack([np.cos(t) + 0.5, -np.sin(t) + 0.5]) + np.random.randn(n, 2) * 0.1
X_moons = np.vstack([X_moon1, X_moon2])
y_moons = np.array([0] * n + [1] * n)

print(f"\n  Architecture: [2, 8, 4, 1]  (2 inputs → 8 hidden → 4 hidden → 1 output)")
print(f"  200 points, 2 classes\n")

mlp2 = MLP([2, 8, 4, 1])
mlp2.train(X_moons, y_moons, lr=0.5, epochs=1000)

preds = mlp2.predict(X_moons)
print(f"\n  Final accuracy: {np.mean(preds == y_moons):.0%}")


# ================================================================
# WALK THROUGH FORWARD + BACKWARD ON XOR
# ================================================================
print(f"\n{'=' * 60}")
print("DETAILED WALKTHROUGH: Forward + Backward on one XOR example")
print("=" * 60)

# Fresh small network: [2, 2, 1]
np.random.seed(0)
net = MLP([2, 2, 1])

x = np.array([[1.0, 0.0]])  # single input: [1, 0], should output 1
y_true = np.array([1])

print(f"\n  Input: x = [1, 0],  target: y = 1")
print(f"  Architecture: 2 → 2 → 1\n")

# Show weights
print(f"  Layer 1 weights (2×2):")
print(f"    W1 = {net.weights[0].round(3).tolist()}")
print(f"    b1 = {net.biases[0].round(3).tolist()}")
print(f"  Layer 2 weights (2×1):")
print(f"    W2 = {net.weights[1].round(3).tolist()}")
print(f"    b2 = {net.biases[1].round(3).tolist()}")

# FORWARD
print(f"\n  ── FORWARD PASS ──")

z1 = x @ net.weights[0] + net.biases[0]
print(f"  Layer 1: z1 = x @ W1 + b1 = {z1.round(4)}")

a1 = relu(z1)
print(f"  Layer 1: a1 = ReLU(z1)     = {a1.round(4)}  (negative values → 0)")

z2 = a1 @ net.weights[1] + net.biases[1]
print(f"  Layer 2: z2 = a1 @ W2 + b2 = {z2.round(4)}")

a2 = sigmoid(z2)
print(f"  Layer 2: a2 = sigmoid(z2)  = {a2.round(4)}  (this is our prediction)")

# LOSS
loss = -(y_true * np.log(a2 + 1e-9) + (1 - y_true) * np.log(1 - a2 + 1e-9))
print(f"\n  Loss = -[y·log(ŷ) + (1-y)·log(1-ŷ)] = {loss.flatten()[0]:.4f}")

# BACKWARD
print(f"\n  ── BACKWARD PASS (chain rule) ──")

delta2 = a2 - y_true.reshape(-1, 1)
print(f"  Output delta: a2 - y = {a2.round(4)} - {y_true} = {delta2.round(4)}")

dW2 = a1.T @ delta2
db2 = delta2
print(f"  dW2 = a1.T @ delta2 = {dW2.round(4).tolist()}")
print(f"  db2 = delta2        = {db2.round(4).tolist()}")

delta1 = delta2 @ net.weights[1].T * relu_derivative(z1)
print(f"\n  Propagate back: delta1 = delta2 @ W2.T * ReLU'(z1) = {delta1.round(4)}")

dW1 = x.T @ delta1
db1 = delta1
print(f"  dW1 = x.T @ delta1 = {dW1.round(4).tolist()}")
print(f"  db1 = delta1       = {db1.round(4).tolist()}")

print(f"""
{'=' * 60}
HOW TO THINK ABOUT IT
{'=' * 60}

  FORWARD:  x → multiply by W₁ → ReLU → multiply by W₂ → sigmoid → ŷ
            Just matrix multiplications with nonlinearities between them.

  BACKWARD: error at output → how much did W₂ contribute? → update W₂
            → push error back through W₂ → how much did W₁ contribute? → update W₁
            Each layer asks: "how much of this error is MY fault?"

  The chain rule is just:
    "error at my output" × "my derivative" × "my input"
    = gradient for my weights

{'=' * 60}
WHY MLP WORKS BUT PERCEPTRON DOESN'T
{'=' * 60}

  Perceptron:  one layer  → one line  → XOR impossible
  MLP:         layer 1 draws TWO lines (one per hidden neuron)
               layer 2 COMBINES them (AND/OR logic)
               → XOR solved!

  Hidden neurons = "feature detectors"
    Neuron 1 might learn: "x₁=1 AND x₂=0"
    Neuron 2 might learn: "x₁=0 AND x₂=1"
    Output combines: "neuron 1 OR neuron 2" → XOR!

  More neurons = more lines = more complex boundaries.
  More layers = compositions of boundaries = even more complex.
  That's the power of deep learning.

{'=' * 60}
THE RECIPE (what to memorize)
{'=' * 60}

  Forward:
    for each layer:
        z = a_prev @ W + b       # linear
        a = activation(z)         # nonlinear

  Backward:
    delta = prediction - actual   # output error
    for each layer (back to front):
        dW = a_prev.T @ delta     # gradient for weights
        db = sum(delta)            # gradient for biases
        delta = delta @ W.T * activation_derivative(z_prev)  # propagate back
        W -= lr * dW
        b -= lr * db
""")