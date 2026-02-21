"""
MLP — every single calculation printed, one XOR example.

Network:  2 inputs → 2 hidden neurons → 1 output
Input:    [1, 0]   target: 1   (XOR: 1 xor 0 = 1)

The picture:

         W1[0,0]=0.5   W2[0]=0.6
  x₁=1 ─────────────→ [h₀] ─────────→ [out] → ŷ
         W1[0,1]=0.3 ╲ ╱ W2[1]=-0.4
                      ╳
         W1[1,0]=-0.2╱ ╲
  x₂=0 ─────────────→ [h₁] ─────────→
         W1[1,1]=0.8
"""
import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def relu(z):
    return max(0.0, z)


# ════════════════════════════════════════════════════════════
#  SETUP
# ════════════════════════════════════════════════════════════
x1, x2 = 1.0, 0.0      # input
y_true = 1.0             # target

# Layer 1 weights (2 inputs → 2 hidden neurons)
w1_00 = 0.5    # x₁ → h₀
w1_01 = 0.3    # x₁ → h₁
w1_10 = -0.2   # x₂ → h₀
w1_11 = 0.8    # x₂ → h₁
b1_0 = 0.1     # bias for h₀
b1_1 = -0.1    # bias for h₁

# Layer 2 weights (2 hidden → 1 output)
w2_0 = 0.6     # h₀ → output
w2_1 = -0.4    # h₁ → output
b2 = 0.2       # bias for output

lr = 0.5        # learning rate

print("=" * 65)
print("MLP WALKTHROUGH: every calculation, one step at a time")
print("=" * 65)
print(f"""
  Network: 2 → 2 → 1
  Input: x = [{x1}, {x2}]    Target: y = {y_true}

  Weights:
              x₁={x1}                    h₀
             ╱      ╲                   ╱
    w1_00={w1_00}  w1_01={w1_01}   w2_0={w2_0}
           ╱          ╲             ╱
          ╱            ╲           ╱
                        ╲        ╱
                         → [out] → ŷ      b2={b2}
                        ╱        ╲
          ╲            ╱           ╲
           ╲          ╱             ╲
    w1_10={w1_10} w1_11={w1_11}  w2_1={w2_1}
             ╲      ╱                   ╲
              x₂={x2}                    h₁

  b1 = [{b1_0}, {b1_1}]    b2 = {b2}
""")


# ════════════════════════════════════════════════════════════
#  FORWARD PASS
# ════════════════════════════════════════════════════════════
print("─" * 65)
print("FORWARD PASS  (left → right)")
print("─" * 65)

# Hidden neuron 0
print(f"\n  ┌─ Hidden neuron 0 ─────────────────────────────────────────┐")
z_h0 = w1_00 * x1 + w1_10 * x2 + b1_0
print(f"  │  z_h0 = w1_00*x₁  +  w1_10*x₂  +  b1_0                  │")
print(f"  │       = {w1_00}*{x1}    +  {w1_10}*{x2}    +  {b1_0}                  │")
print(f"  │       = {w1_00*x1}      +  {w1_10*x2}       +  {b1_0}                  │")
print(f"  │       = {z_h0}                                            │")
a_h0 = relu(z_h0)
print(f"  │  a_h0 = ReLU({z_h0}) = {a_h0}  {'(positive → keep)' if z_h0 > 0 else '(negative → 0, neuron is DEAD)'}          │")
print(f"  └───────────────────────────────────────────────────────────┘")

# Hidden neuron 1
print(f"\n  ┌─ Hidden neuron 1 ─────────────────────────────────────────┐")
z_h1 = w1_01 * x1 + w1_11 * x2 + b1_1
print(f"  │  z_h1 = w1_01*x₁  +  w1_11*x₂  +  b1_1                  │")
print(f"  │       = {w1_01}*{x1}    +  {w1_11}*{x2}    +  {b1_1}                  │")
print(f"  │       = {w1_01*x1}      +  {w1_11*x2}       +  {b1_1}                 │")
print(f"  │       = {z_h1}                                           │")
a_h1 = relu(z_h1)
print(f"  │  a_h1 = ReLU({z_h1}) = {a_h1}  {'(positive → keep)' if z_h1 > 0 else '(negative → 0, neuron is DEAD)'}          │")
print(f"  └───────────────────────────────────────────────────────────┘")

# Output neuron
print(f"\n  ┌─ Output neuron ──────────────────────────────────────────┐")
z_out = w2_0 * a_h0 + w2_1 * a_h1 + b2
print(f"  │  z_out = w2_0*a_h0  +  w2_1*a_h1  +  b2                 │")
print(f"  │        = {w2_0}*{a_h0}    +  {w2_1}*{a_h1}     +  {b2}                │")
print(f"  │        = {w2_0*a_h0}       +  {w2_1*a_h1}      +  {b2}                │")
print(f"  │        = {z_out}                                         │")
y_hat = sigmoid(z_out)
print(f"  │  ŷ = sigmoid({z_out}) = 1/(1+exp(-{z_out})) = {y_hat:.4f}            │")
print(f"  └───────────────────────────────────────────────────────────┘")

print(f"\n  PREDICTION: ŷ = {y_hat:.4f}")
print(f"  TARGET:     y = {y_true}")
print(f"  {'TOO LOW — need to push prediction UP' if y_hat < y_true else 'TOO HIGH — need to push prediction DOWN'}")


# ════════════════════════════════════════════════════════════
#  LOSS
# ════════════════════════════════════════════════════════════
print(f"\n{'─' * 65}")
print("LOSS (how wrong are we?)")
print("─" * 65)

loss = -(y_true * np.log(y_hat) + (1 - y_true) * np.log(1 - y_hat))
print(f"\n  L = -[y·log(ŷ) + (1-y)·log(1-ŷ)]")
print(f"    = -[{y_true}·log({y_hat:.4f}) + {1-y_true}·log({1-y_hat:.4f})]")
print(f"    = -[{y_true}·({np.log(y_hat):.4f}) + {1-y_true}·({np.log(1-y_hat):.4f})]")
print(f"    = -[{y_true * np.log(y_hat):.4f}]")
print(f"    = {loss:.4f}")


# ════════════════════════════════════════════════════════════
#  BACKWARD PASS
# ════════════════════════════════════════════════════════════
print(f"\n{'─' * 65}")
print("BACKWARD PASS  (right → left)")
print("─" * 65)

# Step 1: Output error
print(f"""
  Step 1: How wrong is the output?
  ─────────────────────────────────
  delta_out = ŷ - y = {y_hat:.4f} - {y_true} = {y_hat - y_true:.4f}

  Negative → prediction too low → we need to INCREASE it
""")
delta_out = y_hat - y_true

# Step 2: Gradients for layer 2 weights
print(f"""  Step 2: How should layer 2 weights change?
  ───────────────────────────────────────────
  dL/dw2_0 = delta_out × a_h0  (input to this weight was a_h0)
           = {delta_out:.4f} × {a_h0}
           = {delta_out * a_h0:.4f}

  dL/dw2_1 = delta_out × a_h1  (input to this weight was a_h1)
           = {delta_out:.4f} × {a_h1}
           = {delta_out * a_h1:.4f}

  dL/db2   = delta_out
           = {delta_out:.4f}
""")
dw2_0 = delta_out * a_h0
dw2_1 = delta_out * a_h1
db2_grad = delta_out

# Step 3: Push error back to hidden layer
print(f"""  Step 3: How much error does each hidden neuron get? (backpropagate)
  ─────────────────────────────────────────────────────────────────
  Each hidden neuron's error = output error × its weight to output × ReLU'

  For h₀:
    error_from_output = delta_out × w2_0 = {delta_out:.4f} × {w2_0} = {delta_out * w2_0:.4f}
    ReLU'(z_h0) = ReLU'({z_h0}) = {1.0 if z_h0 > 0 else 0.0}  {'(was positive → gradient flows through)' if z_h0 > 0 else '(was ≤0 → gradient BLOCKED, neuron was dead)'}
    delta_h0 = {delta_out * w2_0:.4f} × {1.0 if z_h0 > 0 else 0.0} = {delta_out * w2_0 * (1.0 if z_h0 > 0 else 0.0):.4f}

  For h₁:
    error_from_output = delta_out × w2_1 = {delta_out:.4f} × {w2_1} = {delta_out * w2_1:.4f}
    ReLU'(z_h1) = ReLU'({z_h1}) = {1.0 if z_h1 > 0 else 0.0}  {'(was positive → gradient flows through)' if z_h1 > 0 else '(was ≤0 → gradient BLOCKED, neuron was dead)'}
    delta_h1 = {delta_out * w2_1:.4f} × {1.0 if z_h1 > 0 else 0.0} = {delta_out * w2_1 * (1.0 if z_h1 > 0 else 0.0):.4f}
""")
relu_d_h0 = 1.0 if z_h0 > 0 else 0.0
relu_d_h1 = 1.0 if z_h1 > 0 else 0.0
delta_h0 = delta_out * w2_0 * relu_d_h0
delta_h1 = delta_out * w2_1 * relu_d_h1

# Step 4: Gradients for layer 1 weights
print(f"""  Step 4: How should layer 1 weights change?
  ─────────────────────────────────────────
  dL/dw1_00 = delta_h0 × x₁ = {delta_h0:.4f} × {x1} = {delta_h0 * x1:.4f}
  dL/dw1_10 = delta_h0 × x₂ = {delta_h0:.4f} × {x2} = {delta_h0 * x2:.4f}
  dL/db1_0  = delta_h0       = {delta_h0:.4f}

  dL/dw1_01 = delta_h1 × x₁ = {delta_h1:.4f} × {x1} = {delta_h1 * x1:.4f}
  dL/dw1_11 = delta_h1 × x₂ = {delta_h1:.4f} × {x2} = {delta_h1 * x2:.4f}
  dL/db1_1  = delta_h1       = {delta_h1:.4f}
""")
dw1_00 = delta_h0 * x1
dw1_10 = delta_h0 * x2
db1_0_grad = delta_h0
dw1_01 = delta_h1 * x1
dw1_11 = delta_h1 * x2
db1_1_grad = delta_h1


# ════════════════════════════════════════════════════════════
#  UPDATE WEIGHTS
# ════════════════════════════════════════════════════════════
print(f"{'─' * 65}")
print("UPDATE WEIGHTS  (w = w - lr × gradient)")
print("─" * 65)

print(f"\n  Learning rate = {lr}\n")
print(f"  Layer 2:")
w2_0_new = w2_0 - lr * dw2_0
w2_1_new = w2_1 - lr * dw2_1
b2_new = b2 - lr * db2_grad
print(f"    w2_0: {w2_0:.4f} - {lr}×({dw2_0:.4f}) = {w2_0_new:.4f}")
print(f"    w2_1: {w2_1:.4f} - {lr}×({dw2_1:.4f}) = {w2_1_new:.4f}")
print(f"    b2:   {b2:.4f} - {lr}×({db2_grad:.4f}) = {b2_new:.4f}")

print(f"\n  Layer 1:")
w1_00_new = w1_00 - lr * dw1_00
w1_01_new = w1_01 - lr * dw1_01
w1_10_new = w1_10 - lr * dw1_10
w1_11_new = w1_11 - lr * dw1_11
b1_0_new = b1_0 - lr * db1_0_grad
b1_1_new = b1_1 - lr * db1_1_grad
print(f"    w1_00: {w1_00:.4f} - {lr}×({dw1_00:.4f}) = {w1_00_new:.4f}")
print(f"    w1_01: {w1_01:.4f} - {lr}×({dw1_01:.4f}) = {w1_01_new:.4f}")
print(f"    w1_10: {w1_10:.4f} - {lr}×({dw1_10:.4f}) = {w1_10_new:.4f}  (unchanged! x₂ was 0)")
print(f"    w1_11: {w1_11:.4f} - {lr}×({dw1_11:.4f}) = {w1_11_new:.4f}  (unchanged! x₂ was 0)")
print(f"    b1_0:  {b1_0:.4f} - {lr}×({db1_0_grad:.4f}) = {b1_0_new:.4f}")
print(f"    b1_1:  {b1_1:.4f} - {lr}×({db1_1_grad:.4f}) = {b1_1_new:.4f}")


# ════════════════════════════════════════════════════════════
#  VERIFY: run forward again with new weights
# ════════════════════════════════════════════════════════════
print(f"\n{'─' * 65}")
print("VERIFY: forward pass with UPDATED weights")
print("─" * 65)

z_h0_new = w1_00_new * x1 + w1_10_new * x2 + b1_0_new
a_h0_new = relu(z_h0_new)
z_h1_new = w1_01_new * x1 + w1_11_new * x2 + b1_1_new
a_h1_new = relu(z_h1_new)
z_out_new = w2_0_new * a_h0_new + w2_1_new * a_h1_new + b2_new
y_hat_new = sigmoid(z_out_new)

print(f"\n  Old prediction: ŷ = {y_hat:.4f}  (target: {y_true})")
print(f"  New prediction: ŷ = {y_hat_new:.4f}  (target: {y_true})")
print(f"  Moved {'closer' if abs(y_hat_new - y_true) < abs(y_hat - y_true) else 'further'}! "
      f"Error: {abs(y_hat - y_true):.4f} → {abs(y_hat_new - y_true):.4f}")

print(f"""
{'=' * 65}
SUMMARY: THE PATTERN AT EVERY LAYER
{'=' * 65}

  FORWARD (each layer):
    z = inputs × weights + bias     ← linear combination
    a = activation(z)                ← nonlinearity (ReLU or sigmoid)

  BACKWARD (each layer, back to front):
    1. gradient for weights = delta × input to this layer
    2. delta for prev layer = delta × weights × activation_derivative
    3. update: weight -= lr × gradient

  The CHAIN RULE connects them:
    output error → × W2 → hidden error → × W1 → input error
    Each layer passes blame backwards proportional to its weights.

  That's it. Repeat for 1000 epochs. Every weight gets a tiny nudge
  each time, and gradually the network learns the right mapping.
""")