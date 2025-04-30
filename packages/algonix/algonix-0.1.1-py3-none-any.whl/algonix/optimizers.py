import numpy as np

class GradientDescent:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations

    def optimize(self, X, y, weights, bias):
        n_samples = X.shape[0]

        for _ in range(self.iterations):
            predictions = np.dot(X, weights) + bias
            error = predictions - y

            dw = (1 / n_samples) * np.dot(X.T, error)
            db = (1 / n_samples) * np.sum(error)

            weights -= self.learning_rate * dw
            bias -= self.learning_rate * db

        return weights, bias

class StochasticGradientDescent:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations

    def optimize(self, X, y, weights, bias):
        n_samples = X.shape[0]

        for _ in range(self.iterations):
            for i in range(n_samples):
                xi = X[i].reshape(1, -1)
                yi = y[i]

                prediction = np.dot(xi, weights) + bias
                error = prediction - yi

                dw = np.dot(xi.T, error)
                db = error

                weights -= self.learning_rate * dw.flatten()
                bias -= self.learning_rate * db

        return weights, bias
