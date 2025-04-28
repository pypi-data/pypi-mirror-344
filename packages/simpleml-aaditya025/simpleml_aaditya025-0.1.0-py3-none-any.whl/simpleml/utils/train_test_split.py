import numpy as np

def train_test_split(X, y, test_size=0.2, random_state=None):
    np.random.seed(random_state)
    idx = np.arange(len(X))
    np.random.shuffle(idx)
    split = int(len(X) * (1 - test_size))
    train_idx, test_idx = idx[:split], idx[split:]
    X_train, X_test = [X[i] for i in train_idx], [X[i] for i in test_idx]
    y_train, y_test = [y[i] for i in train_idx], [y[i] for i in test_idx]
    return X_train, X_test, y_train, y_test
