"""
TRANSFORMER — from scratch.

RNN processes tokens ONE BY ONE (sequential → slow, forgets long range).
Transformer processes ALL tokens AT ONCE using ATTENTION.

THE KEY IDEA — SELF-ATTENTION:
  For each word, ask: "which OTHER words should I pay attention to?"

  "The cat sat on the mat because it was tired"
   → For "it": attend most to "cat" (that's what "it" refers to)
   → For "tired": attend most to "cat" and "it"

  RNN would need to carry "cat" through many steps to connect it to "it".
  Transformer connects them DIRECTLY in one step.

HOW ATTENTION WORKS (3 vectors per token):
  Q = Query  ("what am I looking for?")
  K = Key    ("what do I contain?")
  V = Value  ("what do I actually say?")

  Attention = softmax(Q · K^T / √d) · V

  That's the whole thing. The rest is just stacking this operation.

TRANSFORMER ARCHITECTURE:
  Input → [Embedding + Position] → [Self-Attention → FFN] × N → Output
                                    └── encoder block ──┘
"""
import numpy as np

np.random.seed(42)


# ================================================================
# HELPER FUNCTIONS
# ================================================================
def softmax(x):
    """Softmax along last axis."""
    e = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def relu(z):
    return np.maximum(0, z)


def layer_norm(x, eps=1e-6):
    """Normalize each token's features to mean=0, var=1."""
    mean = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return (x - mean) / np.sqrt(var + eps)


# ================================================================
# STEP 1: SCALED DOT-PRODUCT ATTENTION
# ================================================================
print("=" * 60)
print("STEP 1: SELF-ATTENTION — the core of Transformers")
print("=" * 60)

print("""
  Each token gets 3 vectors:
    Q (Query): "what am I looking for?"
    K (Key):   "what do I contain?"
    V (Value): "what information do I carry?"

  Attention(Q, K, V) = softmax(Q · K^T / √d_k) · V

  Q · K^T  = how much each token should attend to every other token
  / √d_k   = scale down so softmax doesn't become too sharp
  softmax  = normalize to probabilities (attention weights)
  · V      = weighted sum of values
""")


def attention(Q, K, V, verbose=False):
    """
    Scaled dot-product attention.
    Q, K, V: (seq_len, d_k)
    Returns: (seq_len, d_k)
    """
    d_k = Q.shape[-1]

    # Step 1: Q · K^T → attention scores
    scores = Q @ K.T  # (seq_len, seq_len)

    if verbose:
        print(f"    Q @ K^T (raw scores):")
        for row in scores:
            print(f"      {row.round(3).tolist()}")

    # Step 2: Scale by √d_k
    scores = scores / np.sqrt(d_k)

    if verbose:
        print(f"    After scaling by √{d_k}={np.sqrt(d_k):.2f}:")
        for row in scores:
            print(f"      {row.round(3).tolist()}")

    # Step 3: Softmax → attention weights
    weights = softmax(scores)

    if verbose:
        print(f"    After softmax (attention weights):")
        for row in weights:
            print(f"      {row.round(3).tolist()}")
        print(f"    Each row sums to 1: {weights.sum(axis=1).round(3).tolist()}")

    # Step 4: Weighted sum of values
    output = weights @ V  # (seq_len, d_k)

    return output, weights


# ── Demo with 3 tokens, dimension 4 ──
print(f"  --- Example: 3 tokens, d_k=4 ---\n")
print(f"  Imagine: ['I', 'love', 'ML']")
print(f"  Each token → Q, K, V vectors (d_k=4)\n")

# Simulated Q, K, V (in practice, these come from linear projections)
Q = np.array([
    [1.0, 0.0, 1.0, 0.0],   # "I" query
    [0.0, 1.0, 0.0, 1.0],   # "love" query
    [1.0, 1.0, 0.0, 0.0],   # "ML" query
])
K = np.array([
    [1.0, 0.0, 0.0, 1.0],   # "I" key
    [0.0, 1.0, 1.0, 0.0],   # "love" key
    [1.0, 1.0, 0.0, 0.0],   # "ML" key
])
V = np.array([
    [0.1, 0.2, 0.3, 0.4],   # "I" value
    [0.5, 0.6, 0.7, 0.8],   # "love" value
    [0.9, 1.0, 1.1, 1.2],   # "ML" value
])

print(f"  Q (queries):  {Q.tolist()}")
print(f"  K (keys):     {K.tolist()}")
print(f"  V (values):   {V.tolist()}")
print()

output, weights = attention(Q, K, V, verbose=True)

print(f"\n    Output (weighted sum of V):")
for i, (row, label) in enumerate(zip(output, ["I", "love", "ML"])):
    print(f"      '{label}': {row.round(3).tolist()}")

print(f"""
  Reading the attention weights:
    'I'    attends to: I={weights[0,0]:.2f}, love={weights[0,1]:.2f}, ML={weights[0,2]:.2f}
    'love' attends to: I={weights[1,0]:.2f}, love={weights[1,1]:.2f}, ML={weights[1,2]:.2f}
    'ML'   attends to: I={weights[2,0]:.2f}, love={weights[2,1]:.2f}, ML={weights[2,2]:.2f}

  Each token's output = weighted mix of ALL values, where weights
  are determined by how well its Query matches each Key.
""")


# ================================================================
# STEP 2: MULTI-HEAD ATTENTION
# ================================================================
print("=" * 60)
print("STEP 2: MULTI-HEAD ATTENTION — attend in different ways")
print("=" * 60)

print("""
  One attention head might focus on SYNTAX ("subject-verb agreement").
  Another might focus on MEANING ("what does 'it' refer to?").

  Multi-head = run several attention heads in PARALLEL,
  each with its own W_Q, W_K, W_V, then concatenate results.

  MultiHead(X) = Concat(head_1, head_2, ..., head_h) @ W_O

  where head_i = Attention(X @ W_Qi, X @ W_Ki, X @ W_Vi)
""")


class MultiHeadAttention:
    def __init__(self, d_model, n_heads):
        """
        d_model: total dimension (e.g. 8)
        n_heads: number of attention heads (e.g. 2)
        d_k = d_model / n_heads (e.g. 4 per head)
        """
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.d_model = d_model

        scale = np.sqrt(2.0 / d_model)
        # Each head gets its own Q, K, V projection
        self.W_Q = np.random.randn(d_model, d_model) * scale
        self.W_K = np.random.randn(d_model, d_model) * scale
        self.W_V = np.random.randn(d_model, d_model) * scale
        # Output projection
        self.W_O = np.random.randn(d_model, d_model) * scale

    def forward(self, X, verbose=False):
        """
        X: (seq_len, d_model)
        Returns: (seq_len, d_model)
        """
        seq_len = X.shape[0]

        # Project to Q, K, V
        Q = X @ self.W_Q  # (seq_len, d_model)
        K = X @ self.W_K
        V = X @ self.W_V

        if verbose:
            print(f"    Projected Q shape: {Q.shape}")
            print(f"    Projected K shape: {K.shape}")
            print(f"    Projected V shape: {V.shape}")

        # Split into heads
        # Reshape: (seq_len, d_model) → (seq_len, n_heads, d_k)
        Q_heads = Q.reshape(seq_len, self.n_heads, self.d_k)
        K_heads = K.reshape(seq_len, self.n_heads, self.d_k)
        V_heads = V.reshape(seq_len, self.n_heads, self.d_k)

        # Run attention for each head
        head_outputs = []
        all_weights = []
        for h in range(self.n_heads):
            Q_h = Q_heads[:, h, :]  # (seq_len, d_k)
            K_h = K_heads[:, h, :]
            V_h = V_heads[:, h, :]

            out_h, w_h = attention(Q_h, K_h, V_h)
            head_outputs.append(out_h)
            all_weights.append(w_h)

            if verbose:
                print(f"    Head {h + 1} attention weights:")
                for row in w_h:
                    print(f"      {row.round(3).tolist()}")

        # Concatenate heads: (seq_len, n_heads * d_k) = (seq_len, d_model)
        concat = np.hstack(head_outputs)

        # Final projection
        output = concat @ self.W_O

        if verbose:
            print(f"    Concat shape: {concat.shape} → Output shape: {output.shape}")

        return output, all_weights


# Demo
print(f"\n  --- Example: 3 tokens, d_model=8, 2 heads (d_k=4 each) ---\n")
X_demo = np.random.randn(3, 8) * 0.5

mha = MultiHeadAttention(d_model=8, n_heads=2)
output_mha, weights_mha = mha.forward(X_demo, verbose=True)

print(f"\n  Head 1 and Head 2 learn DIFFERENT attention patterns!")
print(f"  That's the power of multi-head — different 'perspectives'.\n")


# ================================================================
# STEP 3: POSITIONAL ENCODING
# ================================================================
print("=" * 60)
print("STEP 3: POSITIONAL ENCODING — where is each token?")
print("=" * 60)

print("""
  Attention has NO notion of order! "I love ML" = "ML love I" to it.
  Fix: ADD position information to each token's embedding.

  PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
  PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

  Each position gets a unique pattern of sines and cosines.
  Why sin/cos? They let the model learn RELATIVE positions easily:
    PE(pos+k) can be expressed as a linear function of PE(pos).
""")


def positional_encoding(seq_len, d_model):
    """Generate positional encodings."""
    PE = np.zeros((seq_len, d_model))
    for pos in range(seq_len):
        for i in range(0, d_model, 2):
            denom = 10000 ** (i / d_model)
            PE[pos, i] = np.sin(pos / denom)
            if i + 1 < d_model:
                PE[pos, i + 1] = np.cos(pos / denom)
    return PE


PE = positional_encoding(seq_len=5, d_model=8)
print(f"\n  Positional encoding for 5 positions, d_model=8:")
for pos in range(5):
    print(f"    pos {pos}: {PE[pos].round(3).tolist()}")
print(f"\n  Each position has a unique pattern.")
print(f"  Added to token embeddings: X_input = embedding + PE")


# ================================================================
# STEP 4: FEED-FORWARD NETWORK
# ================================================================
print(f"\n{'=' * 60}")
print("STEP 4: FEED-FORWARD NETWORK — process each token independently")
print("=" * 60)

print("""
  After attention mixes information BETWEEN tokens,
  FFN processes each token INDEPENDENTLY:

    FFN(x) = ReLU(x @ W1 + b1) @ W2 + b2

  Typically d_ff = 4 × d_model (expand then compress).
  This is where the model "thinks" about each token.
""")


class FeedForward:
    def __init__(self, d_model, d_ff):
        scale = np.sqrt(2.0 / d_model)
        self.W1 = np.random.randn(d_model, d_ff) * scale
        self.b1 = np.zeros((1, d_ff))
        self.W2 = np.random.randn(d_ff, d_model) * scale
        self.b2 = np.zeros((1, d_model))

    def forward(self, x):
        """x: (seq_len, d_model) → (seq_len, d_model)"""
        hidden = relu(x @ self.W1 + self.b1)  # expand
        return hidden @ self.W2 + self.b2       # compress back


# ================================================================
# STEP 5: FULL TRANSFORMER ENCODER BLOCK
# ================================================================
print(f"\n{'=' * 60}")
print("STEP 5: TRANSFORMER ENCODER BLOCK — putting it all together")
print("=" * 60)

print("""
  One encoder block:
    1. Multi-Head Attention + Residual + LayerNorm
    2. Feed-Forward Network + Residual + LayerNorm

    x → [Multi-Head Attention] → + x → [LayerNorm] →
      → [Feed-Forward]        → + x → [LayerNorm] → output

  Residual connection (+ x): helps gradients flow, prevents degradation.
  LayerNorm: stabilizes training.
  Stack 6-12 of these blocks → full Transformer encoder.
""")


class TransformerBlock:
    def __init__(self, d_model, n_heads, d_ff):
        self.attention = MultiHeadAttention(d_model, n_heads)
        self.ffn = FeedForward(d_model, d_ff)

    def forward(self, x, verbose=False):
        # 1. Multi-head attention + residual + norm
        attn_out, weights = self.attention.forward(x, verbose=verbose)
        x = layer_norm(x + attn_out)  # residual + norm

        # 2. Feed-forward + residual + norm
        ffn_out = self.ffn.forward(x)
        x = layer_norm(x + ffn_out)  # residual + norm

        return x, weights


# ================================================================
# STEP 6: FULL TRANSFORMER for sequence classification
# ================================================================
print(f"\n{'=' * 60}")
print("STEP 6: FULL TRANSFORMER — sequence classification")
print("=" * 60)


class SimpleTransformer:
    """
    Transformer encoder for binary sequence classification.
    Input → Embedding + PE → N × EncoderBlock → Pool → Dense → Sigmoid
    """

    def __init__(self, vocab_size, d_model, n_heads, d_ff, n_layers, max_len):
        self.d_model = d_model

        # Token embedding: vocab_size → d_model
        self.embedding = np.random.randn(vocab_size, d_model) * 0.3

        # Positional encoding
        self.PE = positional_encoding(max_len, d_model)

        # Transformer blocks
        self.blocks = [TransformerBlock(d_model, n_heads, d_ff)
                       for _ in range(n_layers)]

        # Classification head
        self.W_out = np.random.randn(d_model, 1) * 0.3
        self.b_out = np.zeros((1, 1))

    def forward(self, token_ids, verbose=False):
        """
        token_ids: list of ints (token indices)
        Returns: probability (scalar)
        """
        seq_len = len(token_ids)

        # 1. Embed tokens
        x = self.embedding[token_ids]  # (seq_len, d_model)

        if verbose:
            print(f"\n    1. Embeddings shape: {x.shape}")

        # 2. Add positional encoding
        x = x + self.PE[:seq_len]

        if verbose:
            print(f"    2. After adding positional encoding: {x.shape}")

        # 3. Pass through transformer blocks
        for i, block in enumerate(self.blocks):
            x, weights = block.forward(x, verbose=(verbose and i == 0))
            if verbose:
                print(f"    3. After block {i + 1}: {x.shape}")

        # 4. Pool: average all token representations
        pooled = x.mean(axis=0, keepdims=True)  # (1, d_model)

        if verbose:
            print(f"    4. Pooled (mean of all tokens): {pooled.shape}")

        # 5. Classify
        logit = pooled @ self.W_out + self.b_out
        prob = 1 / (1 + np.exp(-np.clip(logit, -500, 500)))

        if verbose:
            print(f"    5. Output probability: {prob.flatten()[0]:.4f}")

        return prob.flatten()[0]

    def train(self, data, labels, lr=0.01, epochs=50, verbose=True):
        """Train with numerical gradients (simplified)."""
        eps_num = 1e-5
        eps_log = 1e-9

        # Collect all parameters
        params = [self.embedding, self.W_out, self.b_out]
        for block in self.blocks:
            params.extend([block.attention.W_Q, block.attention.W_K,
                           block.attention.W_V, block.attention.W_O])
            params.extend([block.ffn.W1, block.ffn.b1,
                           block.ffn.W2, block.ffn.b2])

        for epoch in range(epochs):
            total_loss = 0
            correct = 0

            for tokens, label in zip(data, labels):
                pred = self.forward(tokens)
                loss = -(label * np.log(pred + eps_log) +
                         (1 - label) * np.log(1 - pred + eps_log))
                total_loss += loss
                if (pred >= 0.5) == (label == 1):
                    correct += 1

                # Numerical gradients for all parameters
                for param in params:
                    grad = np.zeros_like(param)
                    it = np.nditer(param, flags=['multi_index'])
                    while not it.finished:
                        idx = it.multi_index
                        old = param[idx]

                        param[idx] = old + eps_num
                        p_plus = self.forward(tokens)
                        l_plus = -(label * np.log(p_plus + eps_log) +
                                   (1 - label) * np.log(1 - p_plus + eps_log))

                        param[idx] = old - eps_num
                        p_minus = self.forward(tokens)
                        l_minus = -(label * np.log(p_minus + eps_log) +
                                    (1 - label) * np.log(1 - p_minus + eps_log))

                        grad[idx] = (l_plus - l_minus) / (2 * eps_num)
                        param[idx] = old
                        it.iternext()

                    np.clip(grad, -1, 1, out=grad)
                    param -= lr * grad

            if verbose and (epoch < 3 or (epoch + 1) % 10 == 0):
                acc = correct / len(labels)
                print(f"    Epoch {epoch + 1:>3}: loss={total_loss / len(labels):.4f}  acc={acc:.0%}")


# ── Tiny vocabulary and data ──
# vocab: 0=pad, 1=good, 2=bad, 3=great, 4=terrible, 5=ok
# Task: positive (good/great) vs negative (bad/terrible) sentiment

print(f"""
  Toy sentiment classification:
    Vocab: 0=pad, 1=good, 2=bad, 3=great, 4=terrible, 5=ok

    Sequences (token IDs):
      [1, 3, 5] = "good great ok"    → positive (1)
      [2, 4, 5] = "bad terrible ok"  → negative (0)
      [3, 1, 1] = "great good good"  → positive (1)
      [4, 2, 2] = "terrible bad bad" → negative (0)
""")

data = [
    [1, 3, 5],  # good great ok → positive
    [2, 4, 5],  # bad terrible ok → negative
    [3, 1, 1],  # great good good → positive
    [4, 2, 2],  # terrible bad bad → negative
]
labels = [1, 0, 1, 0]

# Forward pass demo
print(f"  --- Forward pass on 'good great ok' ---")
transformer = SimpleTransformer(
    vocab_size=6, d_model=8, n_heads=2, d_ff=16,
    n_layers=1, max_len=10
)
pred = transformer.forward(data[0], verbose=True)

# Train
print(f"\n  --- Training (d_model=8, 1 layer, 2 heads) ---")
print(f"  (Numerical gradients → slow, but shows concept)\n")
transformer = SimpleTransformer(
    vocab_size=6, d_model=8, n_heads=2, d_ff=16,
    n_layers=1, max_len=10
)
transformer.train(data, labels, lr=0.05, epochs=50)

print(f"\n  --- Predictions after training ---")
names = ["good great ok", "bad terrible ok", "great good good", "terrible bad bad"]
for tokens, label, name in zip(data, labels, names):
    pred = transformer.forward(tokens)
    print(f"    '{name}' → {pred:.4f} → {'pos' if pred >= 0.5 else 'neg'}  (actual: {'pos' if label else 'neg'})")


# ================================================================
# CAUSAL (DECODER) ATTENTION MASK
# ================================================================
print(f"\n{'=' * 60}")
print("BONUS: CAUSAL MASK — for decoder / GPT-style models")
print("=" * 60)

print("""
  Encoder (BERT): each token sees ALL other tokens (bidirectional).
  Decoder (GPT):  each token sees only PREVIOUS tokens (causal).

  Causal mask: set future positions to -infinity before softmax.

  Scores before mask:         After mask:
  ┌──────────────────┐       ┌──────────────────┐
  │ 0.5  0.3  0.8    │       │ 0.5  -∞   -∞     │
  │ 0.2  0.7  0.4    │  →    │ 0.2  0.7  -∞     │
  │ 0.9  0.1  0.6    │       │ 0.9  0.1  0.6    │
  └──────────────────┘       └──────────────────┘

  Token 1 can only see token 1.
  Token 2 can see tokens 1-2.
  Token 3 can see tokens 1-3.
""")


def causal_attention(Q, K, V, verbose=False):
    """Attention with causal mask (decoder-style)."""
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)

    # Create causal mask: upper triangle = -inf
    seq_len = Q.shape[0]
    mask = np.triu(np.ones((seq_len, seq_len)) * (-1e9), k=1)
    scores = scores + mask

    if verbose:
        print(f"    Scores after causal mask:")
        for row in scores:
            print(f"      {['  -inf' if v < -1e8 else f'{v:6.3f}' for v in row]}")

    weights = softmax(scores)

    if verbose:
        print(f"    Causal attention weights:")
        for row in weights:
            print(f"      {row.round(3).tolist()}")

    output = weights @ V
    return output, weights


print(f"\n  --- Causal attention on 3 tokens ---\n")
causal_out, causal_w = causal_attention(Q, K, V, verbose=True)
print(f"\n  Token 1 only attends to itself: {causal_w[0].round(3).tolist()}")
print(f"  Token 3 attends to all 3:       {causal_w[2].round(3).tolist()}")


# ================================================================
# SUMMARY
# ================================================================
print(f"""
{'=' * 60}
TRANSFORMER SUMMARY
{'=' * 60}

  THE RECIPE:

  1. Embed tokens + add positional encoding
  2. For each encoder block:
       a. Multi-Head Self-Attention + residual + LayerNorm
       b. Feed-Forward Network + residual + LayerNorm
  3. Pool (or use [CLS] token) → classification head

  ATTENTION IN 1 LINE:
    Attention(Q, K, V) = softmax(Q @ K.T / √d_k) @ V

  MULTI-HEAD:
    Split Q, K, V into h heads → attention each → concat → project

{'=' * 60}
ENCODER vs DECODER vs ENCODER-DECODER
{'=' * 60}

  ┌──────────────────┬──────────────────┬──────────────────────────┐
  │ Encoder-only     │ Decoder-only     │ Encoder-Decoder          │
  │ (BERT)           │ (GPT)            │ (T5, original Transformer│
  ├──────────────────┼──────────────────┼──────────────────────────┤
  │ Sees ALL tokens  │ Sees only PAST   │ Encoder sees all,        │
  │ (bidirectional)  │ tokens (causal)  │ decoder sees past +      │
  │                  │                  │ attends to encoder       │
  │ Classification,  │ Text generation, │ Translation,             │
  │ NER, embeddings  │ chat, code gen   │ summarization            │
  └──────────────────┴──────────────────┴──────────────────────────┘

{'=' * 60}
RNN vs TRANSFORMER — WHY TRANSFORMERS WON
{'=' * 60}

  ┌──────────────────┬─────────────────────┬─────────────────────────┐
  │                  │ RNN/LSTM            │ Transformer             │
  ├──────────────────┼─────────────────────┼─────────────────────────┤
  │ Processing       │ Sequential (slow)   │ Parallel (fast on GPU)  │
  │ Long-range deps  │ Hard (vanishing     │ Direct (attention       │
  │                  │ gradient)           │ connects any 2 tokens)  │
  │ Training speed   │ Slow (can't         │ Fast (fully parallel)   │
  │                  │ parallelize)        │                         │
  │ Memory of past   │ Compressed into     │ Full access to all      │
  │                  │ hidden state        │ previous tokens         │
  │ Position info    │ Built-in (order)    │ Must add (PE)           │
  │ Complexity       │ O(n·d²)             │ O(n²·d) per layer       │
  └──────────────────┴─────────────────────┴─────────────────────────┘

  KEY INTERVIEW POINTS:
    - Self-attention: each token attends to every other token
    - Q, K, V: query/key for matching, value for content
    - Multi-head: different heads learn different patterns
    - Positional encoding: sin/cos to encode position
    - Residual + LayerNorm: stable training
    - Encoder (BERT) = bidirectional, Decoder (GPT) = causal
    - O(n²) in sequence length → expensive for very long sequences
    - Transformers replaced RNNs for almost all NLP tasks
""")