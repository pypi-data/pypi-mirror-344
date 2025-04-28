import numpy as np

class KNNClassifier:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def predict(self, X):
        X = np.array(X)
        preds = []
        for point in X:
            distances = np.linalg.norm(self.X_train - point, axis=1)
            neighbors_idx = np.argsort(distances)[:self.k]
            neighbor_labels = self.y_train[neighbors_idx]
            preds.append(np.bincount(neighbor_labels).argmax())
        return preds
