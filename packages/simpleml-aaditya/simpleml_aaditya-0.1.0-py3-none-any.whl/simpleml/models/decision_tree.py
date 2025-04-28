class DecisionTree:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.tree = None

    def fit(self, X, y):
        self.tree = {'predict': max(set(y), key=y.count)}

    def predict(self, X):
        return [self.tree['predict']] * len(X)
