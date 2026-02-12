"""
=============================================================================
HOW TO DIFFERENTIATE A SUM — From Basics to Logistic Regression
=============================================================================

This builds from basic calculus rules you already know to deriving
the logistic regression gradient. No steps skipped.

=============================================================================
"""

print("""
╔══════════════════════════════════════════════════════════════════════╗
║      HOW TO FIND THE DERIVATIVE OF A SUM                            ║
║      (and apply it to logistic regression)                          ║
╚══════════════════════════════════════════════════════════════════════╝


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULE 0: THE KEY INSIGHT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The derivative of a sum IS the sum of the derivatives.

    d/dw [f₁(w) + f₂(w) + f₃(w)] = f₁'(w) + f₂'(w) + f₃'(w)

    d/dw [Σᵢ fᵢ(w)] = Σᵢ [d/dw fᵢ(w)]

This means: to differentiate a sum, you just differentiate ONE term,
then sum up all those individual derivatives.

This is why we can focus on a SINGLE data point, find its derivative,
and then sum over all data points at the end.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULE 1: FOUR CALCULUS RULES YOU NEED (That's it!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Everything in ML gradient derivations uses just these four rules:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. POWER RULE:     d/dw [wⁿ] = n · wⁿ⁻¹                     │
│                                                                 │
│     Example: d/dw [w²] = 2w                                    │
│                                                                 │
│  2. CHAIN RULE:     d/dw [g(f(w))] = g'(f(w)) · f'(w)         │
│                                                                 │
│     "Derivative of outer × derivative of inner"                 │
│     Example: d/dw [(3w+1)²] = 2(3w+1) · 3 = 6(3w+1)          │
│                                                                 │
│  3. LOG RULE:       d/dw [ln(f(w))] = f'(w) / f(w)            │
│                                                                 │
│     Example: d/dw [ln(w²)] = 2w / w² = 2/w                    │
│                                                                 │
│  4. CONSTANT RULE:  d/dw [c · f(w)] = c · f'(w)               │
│                                                                 │
│     Constants just pass through the derivative.                 │
│     Example: d/dw [5w²] = 5 · 2w = 10w                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

That's ALL the calculus you need. Let's use these to derive everything.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WARM-UP: LINEAR REGRESSION GRADIENT (using the rules above)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Loss: L = (1/2n) · Σᵢ (w·xᵢ + b - yᵢ)²

Step 1: Constant rule — pull out 1/2n
    ∂L/∂w = (1/2n) · Σᵢ ∂/∂w [(w·xᵢ + b - yᵢ)²]

Step 2: Focus on ONE term: (w·xᵢ + b - yᵢ)²
    This is g(f(w)) where:
        f(w) = w·xᵢ + b - yᵢ       → f'(w) = xᵢ
        g(f) = f²                    → g'(f) = 2f

Step 3: Chain rule
    ∂/∂w [(w·xᵢ + b - yᵢ)²] = 2·(w·xᵢ + b - yᵢ) · xᵢ

Step 4: Put it back in the sum
    ∂L/∂w = (1/2n) · Σᵢ 2·(w·xᵢ + b - yᵢ) · xᵢ

Step 5: The 2 cancels with 1/2
    ∂L/∂w = (1/n) · Σᵢ (w·xᵢ + b - yᵢ) · xᵢ

Done! Same result as before. Now let's do logistic regression.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOGISTIC REGRESSION: BUILDING BLOCKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Before diving into the full loss, we need one key building block:
the derivative of the sigmoid function.


THE SIGMOID FUNCTION:

    σ(z) = 1 / (1 + e⁻ᶻ)

    This maps any real number to (0, 1):
        σ(-∞) = 0
        σ(0)  = 0.5
        σ(+∞) = 1


DERIVING σ'(z) — the derivative of sigmoid:

    σ(z) = 1 / (1 + e⁻ᶻ)
         = (1 + e⁻ᶻ)⁻¹

    Using the chain rule:
        outer: g(f) = f⁻¹         → g'(f) = -f⁻²     (power rule: n=-1)
        inner: f(z) = 1 + e⁻ᶻ     → f'(z) = -e⁻ᶻ     (chain rule again)

    σ'(z) = -1·(1 + e⁻ᶻ)⁻² · (-e⁻ᶻ)

    The two negatives cancel:

    σ'(z) = e⁻ᶻ / (1 + e⁻ᶻ)²

    Now the beautiful trick — rewrite this using σ itself:

    σ'(z) = e⁻ᶻ / (1 + e⁻ᶻ)²

           = [1 / (1 + e⁻ᶻ)] · [e⁻ᶻ / (1 + e⁻ᶻ)]
                ↑                    ↑
              = σ(z)            what is this?

    The second factor:
        e⁻ᶻ / (1 + e⁻ᶻ) = (1 + e⁻ᶻ - 1) / (1 + e⁻ᶻ)
                          = 1 - 1/(1 + e⁻ᶻ)
                          = 1 - σ(z)

    Therefore:

    ┌─────────────────────────────────────────────────┐
    │  σ'(z) = σ(z) · (1 - σ(z))                      │
    └─────────────────────────────────────────────────┘

    This is elegant and computationally convenient:
    once you have σ(z), the derivative is just σ(z)·(1-σ(z)).

    Example: if σ(z) = 0.7, then σ'(z) = 0.7 × 0.3 = 0.21
""")

import numpy as np

# Verify sigmoid derivative numerically
def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

z_test = 1.5
numerical_derivative = (sigmoid(z_test + 0.0001) - sigmoid(z_test - 0.0001)) / 0.0002
analytical_derivative = sigmoid(z_test) * (1 - sigmoid(z_test))

print(f"    NUMERICAL VERIFICATION at z = {z_test}:")
print(f"      σ({z_test}) = {sigmoid(z_test):.6f}")
print(f"      Numerical derivative  (finite difference): {numerical_derivative:.6f}")
print(f"      Analytical derivative (σ·(1-σ)):           {analytical_derivative:.6f}")
print(f"      Match: {abs(numerical_derivative - analytical_derivative) < 0.0001}")


print("""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOGISTIC REGRESSION: THE LOSS FUNCTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MODEL:
    z = w·x + b                 (linear part — same as linear regression)
    ŷ = σ(z) = σ(w·x + b)      (squeeze through sigmoid to get probability)

    ŷ = P(y=1|x) = probability that this sample is class 1


WHY NOT USE MSE FOR CLASSIFICATION?

    If we used MSE: L = (1/2n) · Σ(σ(w·x+b) - y)²

    Problem: this is NOT convex anymore! The sigmoid creates bumps
    in the loss surface → gradient descent can get stuck in local minima.

    We need a different loss function.


BINARY CROSS-ENTROPY (Log Loss):

    For a SINGLE data point (xᵢ, yᵢ) where yᵢ ∈ {0, 1}:

    ℓᵢ = -[yᵢ · ln(ŷᵢ) + (1 - yᵢ) · ln(1 - ŷᵢ)]

    where ŷᵢ = σ(w·xᵢ + b)


    WHY THIS FORMULA? Let's think about what it does:

    Case 1: yᵢ = 1 (actual class is 1)
        ℓᵢ = -[1 · ln(ŷᵢ) + 0 · ln(1 - ŷᵢ)]
           = -ln(ŷᵢ)

        If ŷᵢ = 0.99 (confident correct):  -ln(0.99) = 0.01  ← small loss ✓
        If ŷᵢ = 0.01 (confident WRONG):    -ln(0.01) = 4.6   ← huge loss ✓

    Case 2: yᵢ = 0 (actual class is 0)
        ℓᵢ = -[0 · ln(ŷᵢ) + 1 · ln(1 - ŷᵢ)]
           = -ln(1 - ŷᵢ)

        If ŷᵢ = 0.01 (confident correct):  -ln(0.99) = 0.01  ← small loss ✓
        If ŷᵢ = 0.99 (confident WRONG):    -ln(0.01) = 4.6   ← huge loss ✓

    Perfect: the loss is small when we're right, huge when we're wrong.
    And -ln(x) goes to ∞ as x→0, so confident wrong predictions are
    HEAVILY penalized.


    The FULL loss over all n data points:

    ┌───────────────────────────────────────────────────────────────┐
    │  L = -(1/n) · Σᵢ [yᵢ·ln(ŷᵢ) + (1-yᵢ)·ln(1-ŷᵢ)]          │
    │                                                               │
    │  where ŷᵢ = σ(w·xᵢ + b)                                     │
    └───────────────────────────────────────────────────────────────┘
""")

# Demonstrate loss values
print("    Numerical examples of per-sample loss:")
for y_true, y_pred in [(1, 0.99), (1, 0.5), (1, 0.01), (0, 0.01), (0, 0.5), (0, 0.99)]:
    y_pred_clip = np.clip(y_pred, 1e-15, 1-1e-15)
    loss_val = -(y_true * np.log(y_pred_clip) + (1-y_true) * np.log(1-y_pred_clip))
    print(f"      y={y_true}, ŷ={y_pred:.2f}  →  loss = {loss_val:.4f}"
          f"  {'(correct, confident)' if loss_val < 0.1 else '(uncertain)' if loss_val < 1 else '(WRONG!)'}")


print("""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOGISTIC REGRESSION: DERIVING THE GRADIENT ∂L/∂w
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is the main event. We'll go VERY slowly.

Full loss:
    L = -(1/n) · Σᵢ [yᵢ·ln(ŷᵢ) + (1-yᵢ)·ln(1-ŷᵢ)]

where ŷᵢ = σ(zᵢ) and zᵢ = w·xᵢ + b


STRATEGY: Same as before.
    1. Pull out constant -(1/n)
    2. Focus on ONE term in the sum
    3. Apply chain rule
    4. Sum up at the end


STEP 1: Pull out the constant and focus on one term.

    ∂L/∂w = -(1/n) · Σᵢ ∂/∂w [yᵢ·ln(ŷᵢ) + (1-yᵢ)·ln(1-ŷᵢ)]

    Focus on one term (drop the subscript i for clarity):

    ∂/∂w [y·ln(ŷ) + (1-y)·ln(1-ŷ)]


STEP 2: Split into two parts (sum rule: derivative of sum = sum of derivatives)

    Part A: ∂/∂w [y · ln(ŷ)]
    Part B: ∂/∂w [(1-y) · ln(1-ŷ)]


STEP 3: Solve Part A using chain rule.

    y is a constant (it's the label, not a function of w).

    ∂/∂w [y · ln(ŷ)] = y · ∂/∂w [ln(ŷ)]

    Now ŷ = σ(w·x + b), so we need chain rule TWICE:

    ∂/∂w [ln(ŷ)] = ∂/∂w [ln(σ(w·x + b))]

    Three nested functions:
        outermost: ln(·)           → derivative: 1/(·)
        middle:    σ(·)            → derivative: σ(·)·(1-σ(·))
        innermost: w·x + b         → derivative w.r.t. w: x

    Applying chain rule from outside in:

    ∂/∂w [ln(σ(w·x+b))]

        = [1/σ(w·x+b)] · σ(w·x+b)·(1-σ(w·x+b)) · x
           ↑ ln derivative   ↑ sigmoid derivative     ↑ linear derivative

    Simplify: the σ in numerator and denominator cancel!

        = (1-σ(w·x+b)) · x

        = (1 - ŷ) · x

    So Part A:
        ∂/∂w [y · ln(ŷ)] = y · (1 - ŷ) · x


STEP 4: Solve Part B using chain rule.

    ∂/∂w [(1-y) · ln(1-ŷ)]

    (1-y) is a constant:

    = (1-y) · ∂/∂w [ln(1 - σ(w·x + b))]

    Three nested functions again:
        outermost: ln(·)             → derivative: 1/(·)
        middle:    1 - σ(·)          → derivative: -σ(·)·(1-σ(·))
                                       (negative because of the "1 minus")
        innermost: w·x + b           → derivative: x

    ∂/∂w [ln(1 - σ(w·x+b))]

        = [1/(1-σ(w·x+b))] · [-σ(w·x+b)·(1-σ(w·x+b))] · x
           ↑ ln derivative      ↑ derivative of (1-σ)       ↑ linear

    Simplify: (1-σ) in numerator and denominator cancel!

        = -σ(w·x+b) · x

        = -ŷ · x

    So Part B:
        ∂/∂w [(1-y) · ln(1-ŷ)] = (1-y) · (-ŷ) · x = -(1-y)·ŷ·x


STEP 5: Combine Parts A and B.

    ∂/∂w [y·ln(ŷ) + (1-y)·ln(1-ŷ)]

    = y·(1-ŷ)·x + (-(1-y)·ŷ·x)

    = y·(1-ŷ)·x  -  (1-y)·ŷ·x

    Factor out x:

    = x · [y·(1-ŷ) - (1-y)·ŷ]

    Expand the bracket:

    = x · [y - y·ŷ - ŷ + y·ŷ]
                ↑         ↑
            these cancel!

    = x · [y - ŷ]

    = x · (y - ŷ)


    ┌──────────────────────────────────────────────────────────────┐
    │                                                              │
    │  For a single data point:                                    │
    │                                                              │
    │    ∂/∂w [yᵢ·ln(ŷᵢ) + (1-yᵢ)·ln(1-ŷᵢ)] = xᵢ · (yᵢ - ŷᵢ) │
    │                                                              │
    │  THIS IS REMARKABLY SIMPLE!                                  │
    │  All the sigmoid derivatives cancel out beautifully.         │
    │                                                              │
    └──────────────────────────────────────────────────────────────┘


STEP 6: Put it back into the full sum with the -(1/n) factor.

    ∂L/∂w = -(1/n) · Σᵢ xᵢ · (yᵢ - ŷᵢ)

    Distribute the negative sign:

    ∂L/∂w = (1/n) · Σᵢ xᵢ · (ŷᵢ - yᵢ)

    ┌───────────────────────────────────────────────────────────────┐
    │                                                               │
    │  ∂L/∂w = (1/n) · Σᵢ (ŷᵢ - yᵢ) · xᵢ                        │
    │                                                               │
    │  In matrix form:                                              │
    │  ∂L/∂w = (1/n) · Xᵀ · (ŷ - y)                               │
    │                                                               │
    │  where ŷ = σ(X·w + b)                                        │
    │                                                               │
    └───────────────────────────────────────────────────────────────┘


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE PUNCHLINE: Compare linear vs logistic regression gradients!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Linear regression:    ∂L/∂w = (1/n) · Xᵀ · (ŷ - y)   where ŷ = X·w + b
    Logistic regression:  ∂L/∂w = (1/n) · Xᵀ · (ŷ - y)   where ŷ = σ(X·w + b)

    THEY HAVE THE EXACT SAME FORM!

    The only difference: how ŷ is computed.
      Linear:   ŷ = X·w + b          (raw value)
      Logistic: ŷ = σ(X·w + b)       (squashed through sigmoid)

    This is NOT a coincidence. CS229 explains this through the
    "exponential family" framework — both are special cases of
    Generalized Linear Models (GLMs), and all GLMs have this
    gradient form.

    In code, the training loop is nearly identical:

        # Linear regression
        predictions = X @ w + b
        dw = (1/n) * X.T @ (predictions - y)

        # Logistic regression — only THIS LINE changes
        predictions = sigmoid(X @ w + b)
        dw = (1/n) * X.T @ (predictions - y)

    Same gradient formula. Different prediction function. That's it.
""")


print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NUMERICAL VERIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Let's verify our analytical gradient matches a numerical approximation.
If we derived it correctly, they should be (almost) identical.
""")

# Simple test: 3 data points, 1 feature
X = np.array([[1.0], [2.0], [3.0]])
y = np.array([0, 0, 1])
w = np.array([0.5])
b = 0.1
n = len(X)

# Analytical gradient
z = X @ w + b
y_hat = sigmoid(z.flatten())
dw_analytical = (1/n) * X.T @ (y_hat - y)
db_analytical = (1/n) * np.sum(y_hat - y)

# Numerical gradient (finite differences)
epsilon = 1e-5

def compute_loss(w_val, b_val):
    z = X @ w_val + b_val
    h = sigmoid(z.flatten())
    h = np.clip(h, 1e-15, 1-1e-15)
    return -(1/n) * np.sum(y * np.log(h) + (1-y) * np.log(1-h))

loss_current = compute_loss(w, b)
dw_numerical = (compute_loss(w + epsilon, b) - compute_loss(w - epsilon, b)) / (2*epsilon)
db_numerical = (compute_loss(w, b + epsilon) - compute_loss(w, b - epsilon)) / (2*epsilon)

print(f"    Test data: X = {X.flatten()}, y = {y}")
print(f"    Parameters: w = {w[0]}, b = {b}")
print(f"    Predictions ŷ = σ(Xw+b) = {np.round(y_hat, 4)}")
print(f"    Loss = {loss_current:.6f}")
print(f"")
print(f"    ∂L/∂w:")
print(f"      Analytical (our formula): {dw_analytical[0]:.8f}")
print(f"      Numerical  (finite diff): {dw_numerical:.8f}")
print(f"      Match: {abs(dw_analytical[0] - dw_numerical) < 1e-5}")
print(f"")
print(f"    ∂L/∂b:")
print(f"      Analytical (our formula): {db_analytical:.8f}")
print(f"      Numerical  (finite diff): {db_numerical:.8f}")
print(f"      Match: {abs(db_analytical - db_numerical) < 1e-5}")


print(f"""

    ✓ Analytical and numerical gradients match!
      This confirms our derivation is correct.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP-BY-STEP TRACE THROUGH THE NUMBERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Data point 1: x=1.0, y=0
      z = 0.5×1.0 + 0.1 = 0.6
      ŷ = σ(0.6) = {sigmoid(0.6):.4f}
      error = ŷ - y = {sigmoid(0.6):.4f} - 0 = {sigmoid(0.6):.4f}
      contribution to dw: error × x = {sigmoid(0.6):.4f} × 1.0 = {sigmoid(0.6)*1.0:.4f}

    Data point 2: x=2.0, y=0
      z = 0.5×2.0 + 0.1 = 1.1
      ŷ = σ(1.1) = {sigmoid(1.1):.4f}
      error = ŷ - y = {sigmoid(1.1):.4f} - 0 = {sigmoid(1.1):.4f}
      contribution to dw: error × x = {sigmoid(1.1):.4f} × 2.0 = {sigmoid(1.1)*2.0:.4f}

    Data point 3: x=3.0, y=1
      z = 0.5×3.0 + 0.1 = 1.6
      ŷ = σ(1.6) = {sigmoid(1.6):.4f}
      error = ŷ - y = {sigmoid(1.6):.4f} - 1 = {sigmoid(1.6)-1:.4f}
      contribution to dw: error × x = {(sigmoid(1.6)-1):.4f} × 3.0 = {(sigmoid(1.6)-1)*3.0:.4f}

    Sum of contributions: {sigmoid(0.6)*1.0:.4f} + {sigmoid(1.1)*2.0:.4f} + {(sigmoid(1.6)-1)*3.0:.4f} = {sigmoid(0.6)*1.0 + sigmoid(1.1)*2.0 + (sigmoid(1.6)-1)*3.0:.4f}

    ∂L/∂w = (1/{n}) × {sigmoid(0.6)*1.0 + sigmoid(1.1)*2.0 + (sigmoid(1.6)-1)*3.0:.4f} = {(1/n)*(sigmoid(0.6)*1.0 + sigmoid(1.1)*2.0 + (sigmoid(1.6)-1)*3.0):.4f}

    Matches our analytical result: {dw_analytical[0]:.4f} ✓


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY: THE DERIVATION RECIPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To differentiate ANY sum-based loss:

    1. Pull out the constant (1/n or 1/2n)
    2. Focus on ONE term in the sum
    3. Identify the nested functions (what's inside what)
    4. Apply chain rule from outside in:
         - ln(...)  →  1/(...) × derivative of inside
         - σ(...)   →  σ·(1-σ) × derivative of inside
         - (...)²   →  2·(...) × derivative of inside
         - w·x + b  →  x   (w.r.t. w)  or  1  (w.r.t. b)
    5. Simplify (things often cancel beautifully)
    6. Put back in the sum

    Key results to MEMORIZE for the interview:

    ┌────────────────────────────────────────────────────────────┐
    │  σ'(z) = σ(z) · (1 - σ(z))                                │
    │                                                            │
    │  Linear:   ∂L/∂w = (1/n) · Xᵀ · (Xw + b - y)            │
    │  Logistic: ∂L/∂w = (1/n) · Xᵀ · (σ(Xw + b) - y)         │
    │                                                            │
    │  Same form! Only difference is sigmoid in predictions.     │
    └────────────────────────────────────────────────────────────┘
""")