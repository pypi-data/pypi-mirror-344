def accuracy_score(y_true, y_pred):
    return sum(y_true_i == y_pred_i for y_true_i, y_pred_i in zip(y_true, y_pred)) / len(y_true)

def precision_score(y_true, y_pred):
    tp = sum((yt == 1) and (yp == 1) for yt, yp in zip(y_true, y_pred))
    fp = sum((yt == 0) and (yp == 1) for yt, yp in zip(y_true, y_pred))
    return tp / (tp + fp) if (tp + fp) != 0 else 0

def recall_score(y_true, y_pred):
    tp = sum((yt == 1) and (yp == 1) for yt, yp in zip(y_true, y_pred))
    fn = sum((yt == 1) and (yp == 0) for yt, yp in zip(y_true, y_pred))
    return tp / (tp + fn) if (tp + fn) != 0 else 0
