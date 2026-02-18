"""
GRADIENT DESCENT — explained so simply you'll never forget it.

Imagine you're BLINDFOLDED on a hilly field.
You want to find the LOWEST point (the valley).

What do you do?

  1. Feel the ground with your feet — which way is DOWNHILL?
  2. Take a step in that direction.
  3. Repeat until the ground feels flat (you're at the bottom).

That's gradient descent. That's literally it.

  - "gradient"  = the slope under your feet (which way is downhill?)
  - "descent"   = walk downhill
  - "learning rate" = how BIG your steps are
      too big  → you overshoot the valley and bounce around
      too small → you get there but it takes forever
"""
import numpy as np

# ================================================================
# PROBLEM: find the x that minimizes f(x) = (x - 3)²
#
#   This is a simple parabola. The answer is obviously x = 3.
#   But pretend you DON'T know that. Let gradient descent find it.
#
#   f(x) = (x - 3)²         ← the "hill" (we want the bottom)
#   f'(x) = 2*(x - 3)       ← the slope (which way is downhill?)
#
#   slope > 0 → you're to the RIGHT of the valley → go LEFT
#   slope < 0 → you're to the LEFT of the valley → go RIGHT
#   slope = 0 → you're AT the bottom → stop
# ================================================================

print("=" * 55)
print("GRADIENT DESCENT on f(x) = (x-3)²")
print("Goal: find x that minimizes f(x). Answer should be 3.")
print("=" * 55)

x = 10.0           # start somewhere random (far from answer)
learning_rate = 0.1 # step size

print(f"\nStarting at x = {x}")
print(f"Learning rate = {learning_rate}\n")

for step in range(15):
    f_x = (x - 3) ** 2          # how high am I? (the loss)
    gradient = 2 * (x - 3)      # which way is downhill? (the slope)
    x_old = x
    x = x - learning_rate * gradient   # take a step downhill

    print(f"  Step {step + 1:>2}: x={x_old:>6.3f}  "
          f"f(x)={f_x:>7.3f}  "
          f"slope={gradient:>7.3f}  "
          f"→ new x={x:.3f}")

print(f"\nFinal x = {x:.6f}  (should be ~3.0)")


# ================================================================
# NOW THE REAL THING: linear regression with gradient descent
#
# You have data points. You want to find a line y = w*x + b
# that fits them. "Fitting" means minimizing the error (loss).
#
# Loss = average of (prediction - actual)² for all points
#      = (1/n) * Σ (w*xᵢ + b - yᵢ)²
#
# Two knobs to tune: w (slope of line) and b (intercept).
# Gradient descent adjusts both, one step at a time.
# ================================================================

print("\n" + "=" * 55)
print("LINEAR REGRESSION with gradient descent")
print("Find w and b so that y = w*x + b fits the data")
print("=" * 55)

# Simple data: y ≈ 2*x + 1 (with a little noise)
np.random.seed(42)
X = np.array([1, 2, 3, 4, 5], dtype=float)
Y = 2 * X + 1 + np.random.randn(5) * 0.3  # true w=2, b=1

print(f"\nData points:")
for i in range(len(X)):
    print(f"  x={X[i]:.0f}  y={Y[i]:.2f}")
print(f"\n(Generated from y = 2x + 1 + noise, so we expect w≈2, b≈1)\n")

# Start with random guesses
w = 0.0
b = 0.0
lr = 0.01
n = len(X)

print(f"Starting: w={w:.2f}, b={b:.2f}")
print(f"Learning rate = {lr}\n")

for epoch in range(200):
    # 1. Predict with current w and b
    predictions = w * X + b

    # 2. How wrong are we? (loss = mean squared error)
    errors = predictions - Y
    loss = np.mean(errors ** 2)

    # 3. Which way should we adjust w and b? (gradients)
    #    dL/dw = (2/n) * Σ (error * x)   — "how does w affect the error?"
    #    dL/db = (2/n) * Σ (error)        — "how does b affect the error?"
    dw = (2 / n) * np.sum(errors * X)
    db = (2 / n) * np.sum(errors)

    # 4. Take a step downhill
    w = w - lr * dw
    b = b - lr * db

    if epoch < 5 or epoch % 50 == 49:
        print(f"  Epoch {epoch + 1:>3}: w={w:.4f}  b={b:.4f}  loss={loss:.4f}")

print(f"\nFinal: w={w:.4f}, b={b:.4f}")
print(f"Expected: w≈2.0, b≈1.0")

print(f"""
{'=' * 55}
RECIPE TO CODE FROM MEMORY (4 lines inside a loop)
{'=' * 55}

  for each epoch:
      predictions = w * X + b              # 1. predict
      errors = predictions - Y             # 2. how wrong?
      w = w - lr * (2/n) * sum(errors * X) # 3. adjust w
      b = b - lr * (2/n) * sum(errors)     # 4. adjust b

  That's the entire algorithm. Everything else is details.

{'=' * 55}
WHY IT WORKS — one sentence
{'=' * 55}

  The gradient points UPHILL.
  We subtract it, so we go DOWNHILL.
  Repeat until we reach the bottom.

{'=' * 55}
LEARNING RATE — the only tricky part
{'=' * 55}

  Too big  (lr=1.0)  → steps overshoot, loss EXPLODES
  Too small (lr=0.0001) → works but takes 100,000 epochs
  Just right (lr=0.01) → converges in ~200 epochs

  Rule of thumb: start with 0.01, if loss explodes go smaller.
""")