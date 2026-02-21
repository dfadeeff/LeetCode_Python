"""
RNN & LSTM — from scratch.

MLP/CNN process FIXED-SIZE inputs. But what about SEQUENCES?
  - Text: "I love ML" (3 words, variable length)
  - Time series: stock prices (daily, any length)
  - Audio: waveform samples

RNN's fix: process one element at a time, carry a HIDDEN STATE forward.

  MLP:   x → [W·x + b] → output          (no memory)
  RNN:   x₁ → [h₁] → x₂ → [h₂] → x₃ → [h₃] → output
              hidden state carries info from past steps

RNN EQUATION (just 1 line!):
  h_t = tanh(W_xh · x_t + W_hh · h_{t-1} + b)

  That's it. At each step:
    - Take current input x_t
    - Take previous hidden state h_{t-1}
    - Combine them → new hidden state h_t

PROBLEM: RNN forgets long-range dependencies (vanishing gradients).
  "I grew up in France ... I speak ___" → RNN forgets "France" by the end.

LSTM's fix: add a CELL STATE (long-term memory) with GATES that control
what to remember, what to forget, and what to output.
"""
import numpy as np

np.random.seed(42)


# ================================================================
# ACTIVATION FUNCTIONS
# ================================================================
def tanh(z):
    return np.tanh(z)


def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))


# ================================================================
# VANILLA RNN
# ================================================================
print("=" * 60)
print("VANILLA RNN — process sequences step by step")
print("=" * 60)


class SimpleRNN:
    """
    Simplest RNN: one hidden layer, processes sequence, outputs at last step.
    """

    def __init__(self, input_size, hidden_size, output_size):
        scale = 0.5
        self.W_xh = np.random.randn(input_size, hidden_size) * scale    # input → hidden
        self.W_hh = np.random.randn(hidden_size, hidden_size) * scale   # hidden → hidden
        self.b_h = np.zeros((1, hidden_size))                           # hidden bias

        self.W_hy = np.random.randn(hidden_size, output_size) * scale   # hidden → output
        self.b_y = np.zeros((1, output_size))                           # output bias

        self.hidden_size = hidden_size

    def forward(self, X, verbose=False):
        """
        X: (seq_len, input_size) — one sequence
        Returns: prediction from LAST hidden state
        """
        seq_len = X.shape[0]
        h = np.zeros((1, self.hidden_size))  # initial hidden state = zeros

        self.inputs = []
        self.hiddens = [h.copy()]  # store for backprop

        if verbose:
            print(f"\n    Initial h₀ = {h.flatten().round(3).tolist()}")

        for t in range(seq_len):
            x_t = X[t:t + 1]  # (1, input_size)

            # THE RNN EQUATION:
            # h_t = tanh(x_t @ W_xh + h_{t-1} @ W_hh + b_h)
            h = tanh(x_t @ self.W_xh + h @ self.W_hh + self.b_h)

            self.inputs.append(x_t)
            self.hiddens.append(h.copy())

            if verbose:
                print(f"    Step {t + 1}: x={x_t.flatten().round(2).tolist()} "
                      f"→ h={h.flatten().round(3).tolist()}")

        # Output from last hidden state
        y = sigmoid(h @ self.W_hy + self.b_y)

        if verbose:
            print(f"    Output: h_last @ W_hy + b_y → sigmoid → {y.flatten()[0]:.4f}")

        return y, h

    def backward(self, X, y_true, lr=0.1):
        """
        Backpropagation Through Time (BPTT):
        Unroll the RNN and backprop through all time steps.
        """
        seq_len = X.shape[0]

        # Forward pass (stores intermediates)
        y_pred, _ = self.forward(X)
        h_last = self.hiddens[-1]

        # Output layer gradient
        d_y = y_pred - y_true.reshape(1, -1)  # (1, output_size)
        d_W_hy = h_last.T @ d_y
        d_b_y = d_y

        # Gradient flowing into last hidden state
        d_h = d_y @ self.W_hy.T  # (1, hidden_size)

        # Accumulate gradients for shared weights
        d_W_xh = np.zeros_like(self.W_xh)
        d_W_hh = np.zeros_like(self.W_hh)
        d_b_h = np.zeros_like(self.b_h)

        # BPTT: go backwards through time
        for t in range(seq_len - 1, -1, -1):
            # tanh derivative: 1 - h²
            d_raw = d_h * (1 - self.hiddens[t + 1] ** 2)

            d_W_xh += self.inputs[t].T @ d_raw
            d_W_hh += self.hiddens[t].T @ d_raw
            d_b_h += d_raw

            # Propagate gradient to previous time step
            d_h = d_raw @ self.W_hh.T

        # Gradient clipping (prevent exploding gradients)
        for grad in [d_W_xh, d_W_hh, d_b_h, d_W_hy, d_b_y]:
            np.clip(grad, -5, 5, out=grad)

        # Update weights
        self.W_xh -= lr * d_W_xh
        self.W_hh -= lr * d_W_hh
        self.b_h -= lr * d_b_h
        self.W_hy -= lr * d_W_hy
        self.b_y -= lr * d_b_y

        return y_pred

    def train(self, sequences, labels, lr=0.1, epochs=100, verbose=True):
        for epoch in range(epochs):
            total_loss = 0
            correct = 0
            for seq, label in zip(sequences, labels):
                y_pred = self.backward(seq, np.array([label]), lr)
                eps = 1e-9
                loss = -(label * np.log(y_pred.flatten()[0] + eps) +
                         (1 - label) * np.log(1 - y_pred.flatten()[0] + eps))
                total_loss += loss
                pred_class = 1 if y_pred.flatten()[0] >= 0.5 else 0
                if pred_class == label:
                    correct += 1

            if verbose and (epoch < 3 or (epoch + 1) % 25 == 0):
                acc = correct / len(labels)
                print(f"    Epoch {epoch + 1:>3}: loss={total_loss / len(labels):.4f}  acc={acc:.0%}")


# ── Toy data: sequence classification ──
# Pattern: if sequence SUMS to > 0 → class 1, else → class 0
# Each sequence has 3 steps, 2 features per step

sequences = [
    np.array([[1.0, 0.5], [0.5, 1.0], [1.0, 0.5]]),   # sum=4.5  → 1
    np.array([[0.8, 0.3], [0.4, 0.9], [0.7, 0.6]]),    # sum=3.7  → 1
    np.array([[-1.0, -0.5], [-0.5, -1.0], [-0.8, -0.3]]),  # sum=-4.1 → 0
    np.array([[-0.7, -0.4], [-0.3, -0.8], [-0.6, -0.5]]),  # sum=-3.3 → 0
    np.array([[0.9, 0.6], [0.3, 0.7], [0.5, 0.4]]),    # sum=3.4  → 1
    np.array([[-0.6, -0.9], [-0.4, -0.7], [-0.5, -0.3]]),  # sum=-3.4 → 0
]
labels = [1, 1, 0, 0, 1, 0]

print(f"\n  Data: 6 sequences, each has 3 time steps, 2 features per step")
print(f"  Rule: sum > 0 → class 1, sum < 0 → class 0")
print(f"\n  Sequence 0 (class 1):")
for t, row in enumerate(sequences[0]):
    print(f"    t={t}: {row.tolist()}")
print(f"  Sequence 2 (class 0):")
for t, row in enumerate(sequences[2]):
    print(f"    t={t}: {row.tolist()}")

# Forward pass on one sequence (before training)
print(f"\n  --- Forward pass on sequence 0 (before training) ---")
rnn = SimpleRNN(input_size=2, hidden_size=4, output_size=1)
pred, _ = rnn.forward(sequences[0], verbose=True)

# Train
print(f"\n  --- Training RNN ---")
rnn = SimpleRNN(input_size=2, hidden_size=4, output_size=1)
rnn.train(sequences, labels, lr=0.1, epochs=100)

print(f"\n  --- Predictions after training ---")
for i, (seq, label) in enumerate(zip(sequences, labels)):
    pred, _ = rnn.forward(seq)
    p = pred.flatten()[0]
    print(f"    Seq {i}: pred={p:.4f} → {'1' if p >= 0.5 else '0'}  (actual: {label})")


# ================================================================
# RNN WALKTHROUGH: trace numbers through one step
# ================================================================
print(f"\n{'=' * 60}")
print("RNN WALKTHROUGH — one step with real numbers")
print("=" * 60)

np.random.seed(0)
mini_rnn = SimpleRNN(input_size=2, hidden_size=2, output_size=1)

x_t = np.array([[0.5, -0.3]])   # current input
h_prev = np.array([[0.1, 0.2]]) # previous hidden state

print(f"""
  Input:      x_t    = [0.5, -0.3]
  Prev state: h_prev = [0.1, 0.2]

  W_xh (2×2) = {mini_rnn.W_xh.round(3).tolist()}
  W_hh (2×2) = {mini_rnn.W_hh.round(3).tolist()}
  b_h        = {mini_rnn.b_h.round(3).tolist()}

  Step 1: x_t @ W_xh = {(x_t @ mini_rnn.W_xh).round(4).tolist()}
  Step 2: h_prev @ W_hh = {(h_prev @ mini_rnn.W_hh).round(4).tolist()}
  Step 3: sum + bias = {(x_t @ mini_rnn.W_xh + h_prev @ mini_rnn.W_hh + mini_rnn.b_h).round(4).tolist()}
  Step 4: tanh(sum) = {tanh(x_t @ mini_rnn.W_xh + h_prev @ mini_rnn.W_hh + mini_rnn.b_h).round(4).tolist()}

  That's h_t! One line: h_t = tanh(x_t @ W_xh + h_prev @ W_hh + b_h)
""")


# ================================================================
# LSTM
# ================================================================
print("=" * 60)
print("LSTM — Long Short-Term Memory")
print("=" * 60)
print("""
  RNN problem: gradients VANISH over long sequences.
    h_t depends on h_{t-1} which depends on h_{t-2} ...
    Multiply many small gradients → gradient → 0 → early steps don't learn.

  LSTM fix: add a CELL STATE (conveyor belt of memory) with 3 GATES:

    ┌─────────────────────────────────────────────────────────┐
    │                   CELL STATE (c_t)                      │
    │         ────────────────────────────────→                │
    │              ↑ forget    ↑ add new                      │
    │              │           │                              │
    │         ┌────┴───┐ ┌────┴───┐ ┌────────┐               │
    │         │ FORGET │ │ INPUT  │ │ OUTPUT │               │
    │         │  GATE  │ │  GATE  │ │  GATE  │               │
    │         │ f_t    │ │ i_t    │ │ o_t    │               │
    │         └────────┘ └────────┘ └────┬───┘               │
    │              ↑           ↑         ↓                    │
    │            [x_t, h_{t-1}]       h_t = o_t * tanh(c_t)  │
    └─────────────────────────────────────────────────────────┘

  FORGET gate: what to ERASE from memory?     f_t = σ(W_f · [h, x] + b_f)
  INPUT gate:  what to ADD to memory?         i_t = σ(W_i · [h, x] + b_i)
  OUTPUT gate: what to OUTPUT from memory?    o_t = σ(W_o · [h, x] + b_o)

  Cell update:  c_t = f_t * c_{t-1} + i_t * tanh(W_c · [h, x] + b_c)
  Hidden state: h_t = o_t * tanh(c_t)
""")


class SimpleLSTM:
    """
    LSTM: like RNN but with forget/input/output gates and a cell state.
    """

    def __init__(self, input_size, hidden_size, output_size):
        self.hidden_size = hidden_size
        concat_size = input_size + hidden_size
        scale = 0.3

        # 4 weight matrices: forget, input, cell candidate, output
        self.W_f = np.random.randn(concat_size, hidden_size) * scale
        self.b_f = np.zeros((1, hidden_size))

        self.W_i = np.random.randn(concat_size, hidden_size) * scale
        self.b_i = np.zeros((1, hidden_size))

        self.W_c = np.random.randn(concat_size, hidden_size) * scale
        self.b_c = np.zeros((1, hidden_size))

        self.W_o = np.random.randn(concat_size, hidden_size) * scale
        self.b_o = np.zeros((1, hidden_size))

        # Output layer
        self.W_y = np.random.randn(hidden_size, output_size) * scale
        self.b_y = np.zeros((1, output_size))

    def forward(self, X, verbose=False):
        """
        X: (seq_len, input_size)
        """
        seq_len = X.shape[0]
        h = np.zeros((1, self.hidden_size))
        c = np.zeros((1, self.hidden_size))

        # Store for backprop
        self.cache = []

        if verbose:
            print(f"\n    h₀ = {h.flatten().round(3).tolist()}")
            print(f"    c₀ = {c.flatten().round(3).tolist()}")

        for t in range(seq_len):
            x_t = X[t:t + 1]  # (1, input_size)

            # Concatenate input and previous hidden state
            concat = np.hstack([h, x_t])  # (1, hidden_size + input_size)

            # FORGET gate: what to erase from cell
            f_t = sigmoid(concat @ self.W_f + self.b_f)

            # INPUT gate: what to write to cell
            i_t = sigmoid(concat @ self.W_i + self.b_i)

            # Candidate values to add
            c_candidate = tanh(concat @ self.W_c + self.b_c)

            # UPDATE cell state
            c = f_t * c + i_t * c_candidate

            # OUTPUT gate: what to expose
            o_t = sigmoid(concat @ self.W_o + self.b_o)

            # Hidden state
            h = o_t * tanh(c)

            self.cache.append((concat, f_t, i_t, c_candidate, c.copy(), o_t, h.copy()))

            if verbose:
                print(f"    Step {t + 1}: x={x_t.flatten().round(2).tolist()}")
                print(f"      forget={f_t.flatten().round(3).tolist()} "
                      f"input={i_t.flatten().round(3).tolist()} "
                      f"output={o_t.flatten().round(3).tolist()}")
                print(f"      cell={c.flatten().round(3).tolist()} "
                      f"hidden={h.flatten().round(3).tolist()}")

        # Output from last hidden state
        y = sigmoid(h @ self.W_y + self.b_y)

        if verbose:
            print(f"    Prediction: {y.flatten()[0]:.4f}")

        self.last_h = h
        self.last_c = c
        return y

    def train(self, sequences, labels, lr=0.01, epochs=100, verbose=True):
        """Simplified training with numerical gradients."""
        eps_grad = 1e-5

        for epoch in range(epochs):
            total_loss = 0
            correct = 0

            for seq, label in zip(sequences, labels):
                # Forward
                y_pred = self.forward(seq).flatten()[0]
                eps = 1e-9
                loss = -(label * np.log(y_pred + eps) +
                         (1 - label) * np.log(1 - y_pred + eps))
                total_loss += loss
                if (y_pred >= 0.5) == (label == 1):
                    correct += 1

                # Numerical gradients (simpler than analytical LSTM backprop)
                all_params = [self.W_f, self.b_f, self.W_i, self.b_i,
                              self.W_c, self.b_c, self.W_o, self.b_o,
                              self.W_y, self.b_y]
                grads = []

                for param in all_params:
                    grad = np.zeros_like(param)
                    it = np.nditer(param, flags=['multi_index'])
                    while not it.finished:
                        idx = it.multi_index
                        old_val = param[idx]

                        param[idx] = old_val + eps_grad
                        y_plus = self.forward(seq).flatten()[0]
                        loss_plus = -(label * np.log(y_plus + eps) +
                                      (1 - label) * np.log(1 - y_plus + eps))

                        param[idx] = old_val - eps_grad
                        y_minus = self.forward(seq).flatten()[0]
                        loss_minus = -(label * np.log(y_minus + eps) +
                                       (1 - label) * np.log(1 - y_minus + eps))

                        grad[idx] = (loss_plus - loss_minus) / (2 * eps_grad)
                        param[idx] = old_val
                        it.iternext()

                    grads.append(grad)

                # Update
                for param, grad in zip(all_params, grads):
                    np.clip(grad, -5, 5, out=grad)
                    param -= lr * grad

            if verbose and (epoch < 3 or (epoch + 1) % 25 == 0):
                acc = correct / len(labels)
                print(f"    Epoch {epoch + 1:>3}: loss={total_loss / len(labels):.4f}  acc={acc:.0%}")


# ── Test LSTM ──
print(f"\n  Using same sequence data as RNN")
print(f"\n  --- LSTM forward pass on sequence 0 ---")

lstm = SimpleLSTM(input_size=2, hidden_size=3, output_size=1)
pred = lstm.forward(sequences[0], verbose=True)

# Train (small hidden size and numerical grads → slow but correct)
print(f"\n  --- Training LSTM (hidden_size=3, numerical gradients) ---")
print(f"  (Slow because numerical gradients, but shows it works)")
lstm = SimpleLSTM(input_size=2, hidden_size=3, output_size=1)
lstm.train(sequences, labels, lr=0.05, epochs=100)

print(f"\n  --- Predictions after training ---")
for i, (seq, label) in enumerate(zip(sequences, labels)):
    pred = lstm.forward(seq).flatten()[0]
    print(f"    Seq {i}: pred={pred:.4f} → {'1' if pred >= 0.5 else '0'}  (actual: {label})")


# ================================================================
# SUMMARY
# ================================================================
print(f"""
{'=' * 60}
RNN vs LSTM — COMPARISON
{'=' * 60}

  ┌──────────────────┬─────────────────────────┬─────────────────────────┐
  │                  │ RNN                     │ LSTM                    │
  ├──────────────────┼─────────────────────────┼─────────────────────────┤
  │ Equation         │ h = tanh(W·[h,x] + b)  │ 4 equations (3 gates +  │
  │                  │ (1 line!)               │ cell update)            │
  │ Memory           │ Short-term only         │ Short + long-term       │
  │ Parameters       │ Few                     │ ~4× more than RNN       │
  │ Long sequences   │ Forgets (vanishing grad)│ Remembers (cell state)  │
  │ Training         │ BPTT (fast)             │ BPTT + gates (slower)   │
  │ Use case         │ Short sequences         │ Long sequences, most    │
  │                  │                         │ real applications       │
  └──────────────────┴─────────────────────────┴─────────────────────────┘

  THE RECIPES:

  RNN (1 equation):
    h_t = tanh(x_t @ W_xh + h_{t-1} @ W_hh + b)

  LSTM (5 equations):
    concat = [h_{t-1}, x_t]
    f_t = sigmoid(concat @ W_f + b_f)           # forget gate
    i_t = sigmoid(concat @ W_i + b_i)           # input gate
    c_t = f_t * c_{t-1} + i_t * tanh(concat @ W_c + b_c)   # cell update
    o_t = sigmoid(concat @ W_o + b_o)           # output gate
    h_t = o_t * tanh(c_t)                       # hidden state

  KEY INTERVIEW POINTS:
    - RNN: simple but forgets → vanishing gradient problem
    - LSTM: solves vanishing gradient with cell state + gates
    - Forget gate near 0 → erase memory, near 1 → keep memory
    - Cell state = "conveyor belt" — gradients flow through unchanged
    - GRU = simplified LSTM (2 gates instead of 3, no cell state)
    - Modern alternative: Transformers (no recurrence, parallel!)
""")