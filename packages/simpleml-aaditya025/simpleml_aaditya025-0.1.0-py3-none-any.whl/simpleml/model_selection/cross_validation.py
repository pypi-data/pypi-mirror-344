from simpleml.utils.train_test_split import train_test_split

def cross_val_score(model, X, y, cv=3):
    fold_size = len(X) // cv
    scores = []
    for i in range(cv):
        start = i * fold_size
        end = start + fold_size
        X_val = X[start:end]
        y_val = y[start:end]
        X_train = X[:start] + X[end:]
        y_train = y[:start] + y[end:]

        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        score = sum(y_val[j] == preds[j] for j in range(len(y_val))) / len(y_val)
        scores.append(score)
    return scores
