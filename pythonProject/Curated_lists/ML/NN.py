import numpy as np

x = np.array([[1.0, 0.0, 2.0], [-1.0, 2.0, -1.0]])
W = np.array([[0.5], [-1.5], [1.0]])
b = np.array([0.5])
y = np.array([[1.0], [0.0]])   # binary targets

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def feed_forward(x, W, b):
    z   = x @ W + b            # linear: (2,3)@(3,1) = (2,1)
    out = sigmoid(z)           # squash to [0,1]
    return out, z

def bce_loss(y_pred, y_true, W, lam=0.01):
    eps = 1e-9                 # avoid log(0)
    bce = -np.mean(y_true * np.log(y_pred + eps) +
                   (1 - y_true) * np.log(1 - y_pred + eps))
    l2  = lam * np.sum(W ** 2)
    return bce + l2

def backprop(x, y, W, b, lr=0.1, lam=0.01):
    n = x.shape[0]

    # forward
    out, z = feed_forward(x, W, b)
    loss   = bce_loss(out, y, W, lam)

    # backward
    # sigmoid + BCE gradient cancels cleanly to (out - y) / n
    d_z = (out - y) / n
    d_W = x.T @ d_z + 2 * lam * W   # + L2 grad
    d_b = np.sum(d_z, axis=0)        # no reg on bias

    # update
    W -= lr * d_W
    b -= lr * d_b

    return W, b, loss


if __name__ == "__main__":
    for epoch in range(1000):
        W, b, loss = backprop(x, y, W, b, lr=0.1, lam=0.01)
        if epoch % 100 == 0:
            out, _ = feed_forward(x, W, b)
            preds  = (out >= 0.5).astype(int)
            print(f'epoch {epoch:4d}  loss: {loss:.4f}  preds: {preds.T}')