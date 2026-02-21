"""
CNN (Convolutional Neural Network) — from scratch.

MLP connects EVERY input to EVERY neuron. For images, that's insane:
  28×28 image = 784 pixels → 784 × hidden_size weights PER neuron.
  No spatial awareness. Pixel [0,0] treated same as pixel [27,27].

CNN's fix: use FILTERS (small windows) that SLIDE across the image.

  MLP:  flatten image → one big vector → fully connected layers
  CNN:  keep image as 2D → slide small filters → detect LOCAL patterns

THREE KEY OPERATIONS:
  1. CONVOLUTION: slide a small filter (e.g. 3×3) across image,
     compute dot product at each position → feature map
  2. POOLING: shrink feature maps (e.g. 2×2 → 1 value) → reduce size
  3. FLATTEN + DENSE: flatten to vector → MLP for classification

WHY IT WORKS:
  - Layer 1 filters detect EDGES (horizontal, vertical, diagonal)
  - Layer 2 filters combine edges → SHAPES (corners, curves)
  - Layer 3 filters combine shapes → OBJECTS (eyes, wheels)
  Each layer detects more complex patterns.

PARAMETER SHARING:
  Same filter is used at EVERY position → way fewer parameters than MLP.
  A 3×3 filter = 9 parameters, regardless of image size!
"""
import numpy as np

np.random.seed(42)


# ================================================================
# CONVOLUTION — the core operation
# ================================================================
def convolve2d(image, kernel):
    """
    Slide kernel across image, compute dot product at each position.

    image: (H, W)
    kernel: (kH, kW)
    output: (H - kH + 1, W - kW + 1)
    """
    H, W = image.shape
    kH, kW = kernel.shape
    out_H = H - kH + 1
    out_W = W - kW + 1

    output = np.zeros((out_H, out_W))

    for i in range(out_H):
        for j in range(out_W):
            # Extract the patch under the kernel
            patch = image[i:i + kH, j:j + kW]
            # Dot product (element-wise multiply, then sum)
            output[i, j] = np.sum(patch * kernel)

    return output


# ================================================================
# MAX POOLING — shrink feature maps
# ================================================================
def max_pool2d(feature_map, pool_size=2):
    """
    Take max value in each pool_size × pool_size window.
    Reduces spatial dimensions by pool_size.
    """
    H, W = feature_map.shape
    out_H = H // pool_size
    out_W = W // pool_size

    output = np.zeros((out_H, out_W))

    for i in range(out_H):
        for j in range(out_W):
            patch = feature_map[i * pool_size:(i + 1) * pool_size,
                                j * pool_size:(j + 1) * pool_size]
            output[i, j] = np.max(patch)

    return output


# ================================================================
# ACTIVATION FUNCTIONS
# ================================================================
def relu(z):
    return np.maximum(0, z)


def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))


# ================================================================
# DEMO 1: Convolution on a tiny image
# ================================================================
print("=" * 60)
print("STEP 1: CONVOLUTION — how a filter detects patterns")
print("=" * 60)

# 6×6 image with a vertical edge
image = np.array([
    [0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 1],
], dtype=float)

# Vertical edge detector
edge_filter = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1],
], dtype=float)

print(f"\n  Image (6×6) — has a vertical edge in the middle:")
for row in image:
    print(f"    {row.astype(int).tolist()}")

print(f"\n  Filter (3×3) — vertical edge detector:")
for row in edge_filter:
    print(f"    {row.astype(int).tolist()}")

# Show one convolution step manually
print(f"\n  --- Manual convolution at position (0,0) ---")
patch = image[0:3, 0:3]
print(f"  Patch under filter:")
for row in patch:
    print(f"    {row.astype(int).tolist()}")
print(f"  Element-wise multiply:")
result = patch * edge_filter
for row in result:
    print(f"    {row.astype(int).tolist()}")
print(f"  Sum = {np.sum(result):.0f}")

print(f"\n  --- Manual convolution at position (0,1) ---")
patch = image[0:3, 1:4]
print(f"  Patch under filter:")
for row in patch:
    print(f"    {row.astype(int).tolist()}")
result = patch * edge_filter
print(f"  Element-wise multiply, sum = {np.sum(result):.0f}")

print(f"\n  --- Manual convolution at position (0,2) ---")
patch = image[0:3, 2:5]
print(f"  Patch under filter:")
for row in patch:
    print(f"    {row.astype(int).tolist()}")
result = patch * edge_filter
print(f"  Element-wise multiply, sum = {np.sum(result):.0f}")

# Full convolution
feature_map = convolve2d(image, edge_filter)
print(f"\n  Full convolution result (4×4 feature map):")
for row in feature_map:
    print(f"    {row.astype(int).tolist()}")
print(f"\n  The 3's in the middle = where the edge is!")
print(f"  The filter FOUND the vertical edge.")


# ================================================================
# DEMO 2: Max Pooling
# ================================================================
print(f"\n{'=' * 60}")
print("STEP 2: MAX POOLING — shrink while keeping important features")
print("=" * 60)

print(f"\n  Feature map (4×4):")
for row in feature_map:
    print(f"    {row.astype(int).tolist()}")

pooled = max_pool2d(feature_map, pool_size=2)
print(f"\n  After 2×2 max pooling (2×2):")
for row in pooled:
    print(f"    {row.astype(int).tolist()}")

print(f"""
  How pooling works:
    [0, 3]  → max = 3     [3, 0]  → max = 3
    [0, 3]                 [3, 0]

    [0, 3]  → max = 3     [3, 0]  → max = 3
    [0, 3]                 [3, 0]

  4×4 → 2×2.  Keeps the "3" (edge detected!), discards zeros.
""")


# ================================================================
# DEMO 3: Full CNN forward pass on tiny "images"
# ================================================================
print("=" * 60)
print("STEP 3: FULL CNN — convolution → ReLU → pool → flatten → dense")
print("=" * 60)


class SimpleCNN:
    """
    Minimal CNN: 1 conv filter → ReLU → max pool → flatten → 1 dense layer.
    For binary classification on tiny grayscale images.
    """

    def __init__(self, filter_size=3, image_size=6):
        # Conv layer: one 3×3 filter
        self.conv_filter = np.random.randn(filter_size, filter_size) * 0.5
        self.conv_bias = 0.0

        # After conv: (image_size - filter_size + 1) × (image_size - filter_size + 1)
        conv_out_size = image_size - filter_size + 1  # 4×4

        # After pool: conv_out_size // 2
        pool_out_size = conv_out_size // 2  # 2×2

        # Dense layer: flattened pool output → 1 output
        flat_size = pool_out_size * pool_out_size  # 4
        self.dense_w = np.random.randn(flat_size) * 0.5
        self.dense_b = 0.0

    def forward(self, image, verbose=False):
        """
        image (H, W) → conv → relu → pool → flatten → dense → sigmoid → prediction
        """
        # 1. Convolution
        self.z_conv = convolve2d(image, self.conv_filter) + self.conv_bias
        if verbose:
            print(f"\n    1. Conv output (4×4):")
            for row in self.z_conv:
                print(f"       {np.round(row, 2).tolist()}")

        # 2. ReLU
        self.a_conv = relu(self.z_conv)
        if verbose:
            print(f"    2. After ReLU (negatives → 0):")
            for row in self.a_conv:
                print(f"       {np.round(row, 2).tolist()}")

        # 3. Max pooling
        self.a_pool = max_pool2d(self.a_conv, pool_size=2)
        if verbose:
            print(f"    3. After 2×2 max pool (2×2):")
            for row in self.a_pool:
                print(f"       {np.round(row, 2).tolist()}")

        # 4. Flatten
        self.flat = self.a_pool.flatten()
        if verbose:
            print(f"    4. Flatten: {np.round(self.flat, 2).tolist()}")

        # 5. Dense layer
        z_out = np.dot(self.flat, self.dense_w) + self.dense_b
        self.output = sigmoid(z_out)
        if verbose:
            print(f"    5. Dense: dot product + bias → {z_out:.4f}")
            print(f"    6. Sigmoid → {self.output:.4f}")

        return self.output

    def train(self, images, labels, lr=0.01, epochs=100, verbose=True):
        """
        Train with gradient descent. Simplified: numerical gradients.
        (Analytical backprop through conv is complex — interview usually
        only asks you to explain it, not implement it.)
        """
        for epoch in range(epochs):
            total_loss = 0
            for img, label in zip(images, labels):
                # Forward
                pred = self.forward(img)
                eps = 1e-9
                loss = -(label * np.log(pred + eps) + (1 - label) * np.log(1 - pred + eps))
                total_loss += loss

                # Gradient of loss w.r.t. output
                error = pred - label  # dL/d(output)

                # --- Dense layer gradients (same as MLP) ---
                d_dense_w = error * self.flat
                d_dense_b = error

                # --- Backprop through pool + conv (simplified) ---
                # Gradient flows back: dense → flatten → pool → relu → conv
                d_flat = error * self.dense_w  # (flat_size,)

                # Un-flatten back to pool shape
                d_pool = d_flat.reshape(self.a_pool.shape)

                # Backprop through max pool: gradient goes to the max element
                d_relu = np.zeros_like(self.a_conv)
                pool_size = 2
                for pi in range(d_pool.shape[0]):
                    for pj in range(d_pool.shape[1]):
                        patch = self.a_conv[pi * pool_size:(pi + 1) * pool_size,
                                            pj * pool_size:(pj + 1) * pool_size]
                        max_idx = np.unravel_index(np.argmax(patch), patch.shape)
                        d_relu[pi * pool_size + max_idx[0],
                               pj * pool_size + max_idx[1]] = d_pool[pi, pj]

                # Backprop through ReLU
                d_conv = d_relu * (self.z_conv > 0).astype(float)

                # Backprop through convolution → filter gradients
                d_filter = np.zeros_like(self.conv_filter)
                kH, kW = self.conv_filter.shape
                for i in range(d_conv.shape[0]):
                    for j in range(d_conv.shape[1]):
                        d_filter += d_conv[i, j] * img[i:i + kH, j:j + kW]
                d_conv_bias = np.sum(d_conv)

                # Update all parameters
                self.dense_w -= lr * d_dense_w
                self.dense_b -= lr * d_dense_b
                self.conv_filter -= lr * d_filter
                self.conv_bias -= lr * d_conv_bias

            if verbose and (epoch < 3 or (epoch + 1) % 25 == 0):
                avg_loss = total_loss / len(images)
                preds = [1 if self.forward(img) >= 0.5 else 0 for img in images]
                acc = np.mean(np.array(preds) == labels)
                print(f"    Epoch {epoch + 1:>3}: loss={avg_loss:.4f}  acc={acc:.0%}")


# ── Create tiny 6×6 "images" ──
# Class 0: vertical edge on the LEFT
# Class 1: vertical edge on the RIGHT
images = []
labels = []

# 4 images with edge on LEFT (class 0)
for _ in range(4):
    img = np.zeros((6, 6))
    img[:, :2] = 1  # bright on left
    img += np.random.randn(6, 6) * 0.1  # small noise
    images.append(img)
    labels.append(0)

# 4 images with edge on RIGHT (class 1)
for _ in range(4):
    img = np.zeros((6, 6))
    img[:, 4:] = 1  # bright on right
    img += np.random.randn(6, 6) * 0.1
    images.append(img)
    labels.append(1)

labels = np.array(labels)

print(f"\n  Data: 8 tiny images (6×6), 2 classes")
print(f"    Class 0: bright on LEFT  (4 images)")
print(f"    Class 1: bright on RIGHT (4 images)")
print(f"\n  Example class 0 image:")
for row in (images[0] > 0.5).astype(int):
    print(f"    {row.tolist()}")
print(f"\n  Example class 1 image:")
for row in (images[4] > 0.5).astype(int):
    print(f"    {row.tolist()}")

# Show forward pass on one image
print(f"\n  --- Forward pass on image 0 (class 0) ---")
cnn = SimpleCNN(filter_size=3, image_size=6)
pred = cnn.forward(images[0], verbose=True)
print(f"\n  Prediction: {pred:.4f}  (before training — random)")

# Train
print(f"\n  --- Training ---")
cnn.train(images, labels, lr=0.05, epochs=100)

# Test
print(f"\n  --- After training ---")
for i in range(len(images)):
    pred = cnn.forward(images[i])
    pred_class = 1 if pred >= 0.5 else 0
    print(f"    Image {i}: pred={pred:.4f} → class {pred_class}  (actual: {labels[i]})")

# Show learned filter
print(f"\n  Learned conv filter:")
for row in cnn.conv_filter:
    print(f"    {np.round(row, 3).tolist()}")


# ================================================================
# CNN BACKPROP WALKTHROUGH
# ================================================================
print(f"""
{'=' * 60}
CNN BACKPROP — layer by layer
{'=' * 60}

  Forward:
    image (6×6) → [conv 3×3] → (4×4) → [ReLU] → (4×4) → [pool 2×2] → (2×2)
                                                                          ↓
                                                                      flatten
                                                                          ↓
                                                                   [dense] → sigmoid → prediction

  Backward (chain rule, right to left):

    1. Dense layer:  same as MLP
       d_dense_w = error * flat_input
       d_dense_b = error

    2. Flatten:  just reshape gradient back to 2D

    3. Max pool:  gradient goes ONLY to the position that was the max
       ┌───┬───┐
       │ 1 │ 3 │ → max = 3 → gradient goes to position (0,1)
       │ 2 │ 0 │
       └───┴───┘

    4. ReLU:  same as MLP (pass gradient if z > 0, block if z ≤ 0)

    5. Conv filter:  at each position, gradient × input patch
       d_filter += d_conv[i,j] * image_patch[i:i+3, j:j+3]
       (Same idea as dense: gradient × input = weight update)

{'=' * 60}
CNN vs MLP — WHY CNN WINS FOR IMAGES
{'=' * 60}

  ┌──────────────────┬─────────────────────────┬─────────────────────────┐
  │                  │ MLP                     │ CNN                     │
  ├──────────────────┼─────────────────────────┼─────────────────────────┤
  │ Input            │ Flatten image to vector │ Keep 2D structure       │
  │ Connections      │ Every pixel → every     │ Small filter → local    │
  │                  │ neuron (FULL)           │ patch only (SPARSE)     │
  │ Parameters       │ 784 × 128 = 100K       │ 3×3 × 32 = 288         │
  │                  │ (for 28×28 image)       │ (32 filters)            │
  │ Spatial info     │ LOST (flattened)        │ PRESERVED               │
  │ Translation      │ Not invariant           │ Invariant (same filter  │
  │ invariance       │                         │ everywhere)             │
  │ Works for        │ Tabular data, small     │ Images, spatial data    │
  │                  │ inputs                  │                         │
  └──────────────────┴─────────────────────────┴─────────────────────────┘

  KEY CNN CONCEPTS FOR INTERVIEWS:
    - Filter/kernel: small matrix (3×3, 5×5) that slides across image
    - Feature map: output of applying one filter (detects one pattern)
    - Stride: how many pixels to skip between positions (default 1)
    - Padding: add zeros around border to keep output same size
    - Channels: RGB image has 3 channels, each filter works across all
    - Multiple filters: each learns a different pattern → stack feature maps

  TYPICAL CNN ARCHITECTURE:
    Input (28×28×1)
    → Conv(32 filters, 3×3) → ReLU → MaxPool(2×2)   → (13×13×32)
    → Conv(64 filters, 3×3) → ReLU → MaxPool(2×2)   → (5×5×64)
    → Flatten                                          → (1600)
    → Dense(128) → ReLU                               → (128)
    → Dense(10) → Softmax                             → (10 classes)
""")