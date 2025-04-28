class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def fit(self, X, y):
        for name, step in self.steps[:-1]:
            X = step.fit_transform(X)
        self.steps[-1][1].fit(X, y)

    def predict(self, X):
        for name, step in self.steps[:-1]:
            X = step.transform(X)
        return self.steps[-1][1].predict(X)
