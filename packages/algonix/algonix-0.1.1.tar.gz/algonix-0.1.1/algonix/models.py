# import numpy as np

# class SimpleLinearRegression:
#     def __init__(self):
#         self.slope = None
#         self.intercept = None

#     def fit(self, X, y):
#         X = np.array(X).flatten()
#         y = np.array(y)
#         x_mean = np.mean(X)
#         y_mean = np.mean(y)

#         self.slope = np.sum((X - x_mean) * (y - y_mean)) / np.sum((X - x_mean) ** 2)
#         self.intercept = y_mean - self.slope * x_mean

#     def predict(self, X):
#         X = np.array(X).flatten()
#         return self.slope * X + self.intercept

# class MultipleLinearRegression:
#     def __init__(self):
#         self.coefficients = None

#     def fit(self, X, y):
#         X = np.column_stack((np.ones(X.shape[0]), X))
#         self.coefficients = np.linalg.inv(X.T @ X) @ X.T @ y

#     def predict(self, X):
#         X = np.column_stack((np.ones(X.shape[0]), X))
#         return X @ self.coefficients

# class LogisticRegression:
#     def __init__(self, learning_rate=0.01, iterations=1000):
#         self.learning_rate = learning_rate
#         self.iterations = iterations
#         self.weights = None
#         self.bias = None

#     def sigmoid(self, z):
#         return 1 / (1 + np.exp(-z))

#     def fit(self, X, y):
#         n_samples, n_features = X.shape
#         self.weights = np.zeros(n_features)
#         self.bias = 0

#         for _ in range(self.iterations):
#             linear_model = np.dot(X, self.weights) + self.bias
#             predictions = self.sigmoid(linear_model)

#             dw = (1 / n_samples) * np.dot(X.T, (predictions - y))
#             db = (1 / n_samples) * np.sum(predictions - y)

#             self.weights -= self.learning_rate * dw
#             self.bias -= self.learning_rate * db

#     def predict(self, X):
#         linear_model = np.dot(X, self.weights) + self.bias
#         predictions = self.sigmoid(linear_model)
#         return np.round(predictions)



# class RidgeRegression:
#     def __init__(self, alpha=1.0):
#         self.alpha = alpha
#         self.coefficients = None

#     def fit(self, X, y):
#         X = np.column_stack((np.ones(X.shape[0]), X))
#         n_features = X.shape[1]
#         identity = np.eye(n_features)
#         identity[0, 0] = 0  # Don't regularize the bias term
#         self.coefficients = np.linalg.inv(X.T @ X + self.alpha * identity) @ X.T @ y

#     def predict(self, X):
#         X = np.column_stack((np.ones(X.shape[0]), X))
#         return X @ self.coefficients

# class LassoRegression:
#     def __init__(self, alpha=1.0, iterations=1000, learning_rate=0.01):
#         self.alpha = alpha
#         self.iterations = iterations
#         self.learning_rate = learning_rate
#         self.coefficients = None

#     def fit(self, X, y):
#         X = np.column_stack((np.ones(X.shape[0]), X))
#         n_samples, n_features = X.shape
#         self.coefficients = np.zeros(n_features)

#         for _ in range(self.iterations):
#             y_pred = X @ self.coefficients
#             error = y_pred - y
#             gradient = (X.T @ error) / n_samples
#             self.coefficients -= self.learning_rate * gradient
#             self.coefficients[1:] -= self.learning_rate * self.alpha * np.sign(self.coefficients[1:])

#     def predict(self, X):
#         X = np.column_stack((np.ones(X.shape[0]), X))
#         return X @ self.coefficients
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import Counter
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score, mean_squared_error

# Simple Linear Regression
class SimpleLinearRegression:
    def __init__(self):
        self.slope = None
        self.intercept = None

    def fit(self, X, y):
        X = np.array(X).flatten()
        y = np.array(y)
        x_mean = np.mean(X)
        y_mean = np.mean(y)

        self.slope = np.sum((X - x_mean) * (y - y_mean)) / np.sum((X - x_mean) ** 2)
        self.intercept = y_mean - self.slope * x_mean

    def predict(self, X):
        X = np.array(X).flatten()
        return self.slope * X + self.intercept

# Multiple Linear Regression
class MultipleLinearRegression:
    def __init__(self):
        self.coefficients = None

    def fit(self, X, y):
        X = np.column_stack((np.ones(X.shape[0]), X))
        self.coefficients = np.linalg.inv(X.T @ X) @ X.T @ y

    def predict(self, X):
        X = np.column_stack((np.ones(X.shape[0]), X))
        return X @ self.coefficients

# Logistic Regression
class LogisticRegression:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.weights = None
        self.bias = None

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.iterations):
            linear_model = np.dot(X, self.weights) + self.bias
            predictions = self.sigmoid(linear_model)

            dw = (1 / n_samples) * np.dot(X.T, (predictions - y))
            db = (1 / n_samples) * np.sum(predictions - y)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        predictions = self.sigmoid(linear_model)
        return np.round(predictions)

# Ridge Regression
class RidgeRegression:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.coefficients = None

    def fit(self, X, y):
        X = np.column_stack((np.ones(X.shape[0]), X))
        I = np.identity(X.shape[1])
        I[0, 0] = 0  # Do not regularize bias
        self.coefficients = np.linalg.inv(X.T @ X + self.alpha * I) @ X.T @ y

    def predict(self, X):
        X = np.column_stack((np.ones(X.shape[0]), X))
        return X @ self.coefficients

# Lasso Regression (simple implementation using coordinate descent)
class LassoRegression:
    def __init__(self, alpha=1.0, max_iter=1000):
        self.alpha = alpha
        self.max_iter = max_iter
        self.coefficients = None

    def fit(self, X, y):
        X = np.column_stack((np.ones(X.shape[0]), X))
        n_samples, n_features = X.shape
        self.coefficients = np.zeros(n_features)

        for _ in range(self.max_iter):
            for j in range(n_features):
                residual = y - X @ self.coefficients + self.coefficients[j] * X[:, j]
                rho = X[:, j] @ residual
                if j == 0:
                    self.coefficients[j] = rho / (X[:, j] @ X[:, j])
                else:
                    self.coefficients[j] = np.sign(rho) * max(0, abs(rho) - self.alpha) / (X[:, j] @ X[:, j])

    def predict(self, X):
        X = np.column_stack((np.ones(X.shape[0]), X))
        return X @ self.coefficients

# Decision Tree Regressor
class DecisionTreeRegressorCustom:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.tree = None

    def fit(self, X, y):
        self.tree = self._build_tree(X, y, depth=0)

    def predict(self, X):
        return np.array([self._predict_single(x, self.tree) for x in X])

    def _build_tree(self, X, y, depth):
        if self.max_depth is not None and depth >= self.max_depth:
            return np.mean(y)

        if len(y) == 1 or len(np.unique(y)) == 1:
            return np.mean(y)

        best_split = self._find_best_split(X, y)
        if best_split is None:
            return np.mean(y)

        feature_index, threshold = best_split
        left_indices = X[:, feature_index] <= threshold
        right_indices = X[:, feature_index] > threshold

        left_subtree = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right_subtree = self._build_tree(X[right_indices], y[right_indices], depth + 1)

        return {"feature_index": feature_index, "threshold": threshold,
                "left": left_subtree, "right": right_subtree}

    def _find_best_split(self, X, y):
        best_split = None
        min_error = float('inf')

        for feature_index in range(X.shape[1]):
            thresholds = np.unique(X[:, feature_index])
            for threshold in thresholds:
                left_indices = X[:, feature_index] <= threshold
                right_indices = X[:, feature_index] > threshold

                if len(y[left_indices]) == 0 or len(y[right_indices]) == 0:
                    continue

                error = self._calculate_error(y[left_indices], y[right_indices])
                if error < min_error:
                    min_error = error
                    best_split = (feature_index, threshold)

        return best_split

    def _calculate_error(self, left_y, right_y):
        left_mean = np.mean(left_y)
        right_mean = np.mean(right_y)
        error = np.sum((left_y - left_mean) ** 2) + np.sum((right_y - right_mean) ** 2)
        return error

    def _predict_single(self, x, tree):
        if isinstance(tree, float):
            return tree

        if x[tree["feature_index"]] <= tree["threshold"]:
            return self._predict_single(x, tree["left"])
        else:
            return self._predict_single(x, tree["right"])

# KNN Classifier
class KNNClassifier:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def predict(self, X):
        predictions = []
        X = np.array(X)
        for x in X:
            distances = [np.linalg.norm(x - x_train) for x_train in self.X_train]
            k_indices = np.argsort(distances)[:self.k]
            k_nearest_labels = [self.y_train[i] for i in k_indices]
            most_common = Counter(k_nearest_labels).most_common(1)[0][0]
            predictions.append(most_common)
        return np.array(predictions)

    def plot_k_vs_accuracy(self, X_test, y_test, max_k=20):
        accuracies = []
        for k in range(1, max_k + 1):
            self.k = k
            y_pred = self.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            accuracies.append(acc)

        plt.figure(figsize=(10, 5))
        plt.plot(range(1, max_k + 1), accuracies, marker='o', color='blue')
        plt.title("Accuracy for different values of K")
        plt.xlabel("K value")
        plt.ylabel("Accuracy")
        plt.grid(True)
        plt.xticks(range(1, max_k + 1))
        plt.show()

        best_k = np.argmax(accuracies) + 1
        print(f"Best K is {best_k} with accuracy = {accuracies[best_k - 1]:.4f}")
        return best_k

# KMeans Clustering
class KMeansNew:
    def __init__(self, n_clusters=2, max_iter=100):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.centroids = None

    def fit_predict(self, X):
        random_index = random.sample(range(0, X.shape[0]), self.n_clusters)
        self.centroids = X[random_index]

        for _ in range(self.max_iter):
            cluster_group = self.assign_clusters(X)
            old_centroids = self.centroids
            self.centroids = self.move_centroids(X, cluster_group)
            if (old_centroids == self.centroids).all():
                break

        return cluster_group

    def assign_clusters(self, X):
        cluster_group = []
        distances = []

        for row in X:
            for centroid in self.centroids:
                distances.append(np.sqrt(np.dot(row - centroid, row - centroid)))
            min_distance = min(distances)
            index_pos = distances.index(min_distance)
            cluster_group.append(index_pos)
            distances.clear()

        return np.array(cluster_group)

    def move_centroids(self, X, cluster_group):
        new_centroids = []
        cluster_type = np.unique(cluster_group)

        for type in cluster_type:
            new_centroids.append(X[cluster_group == type].mean(axis=0))

        return np.array(new_centroids)

    @staticmethod
    def find_optimal_k(X, max_k=10):
        distortions = []
        for k in range(1, max_k + 1):
            model = KMeansNew(n_clusters=k)
            clusters = model.fit_predict(X)
            distortion = 0
            for i, point in enumerate(X):
                centroid = model.centroids[clusters[i]]
                distortion += np.linalg.norm(point - centroid) ** 2
            distortions.append(distortion)

        plt.figure()
        plt.plot(range(1, max_k + 1), distortions, marker='o')
        plt.xlabel('Number of clusters')
        plt.ylabel('Distortion')
        plt.title('Elbow Method for Optimal k')
        plt.grid(True)
        plt.show()

        deltas = np.diff(distortions)
        sec_deltas = np.diff(deltas)
        elbow_point = np.argmax(sec_deltas) + 2

        return elbow_point

# Gradient Boosting Regressor
class GradientBoostingRegressorCustom:
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=3):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.models = []

    def fit(self, X, y, verbose=True):
        self.models = []
        self.y_pred = np.zeros_like(y, dtype=np.float64)

        for i in range(self.n_estimators):
            residual = y - self.y_pred
            tree = DecisionTreeRegressor(max_depth=self.max_depth, random_state=42)
            tree.fit(X, residual)
            update = self.learning_rate * tree.predict(X)
            self.y_pred += update
            self.models.append(tree)

            if verbose and i % 10 == 0:
                mse = mean_squared_error(y, self.y_pred)
                print(f"Iteration {i+1}/{self.n_estimators} - MSE: {mse:.4f}")

    def predict(self, X):
        y_pred = np.zeros(X.shape[0], dtype=np.float64)
        for tree in self.models:
            y_pred += self.learning_rate * tree.predict(X)
        return y_pred

    def plot_learning_curve(self, X, y):
        errors = []
        y_pred = np.zeros_like(y, dtype=np.float64)

        for tree in self.models:
            update = self.learning_rate * tree.predict(X)
            y_pred += update
            mse = mean_squared_error(y, y_pred)
            errors.append(mse)

        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(errors) + 1), errors, marker='o', color='green')
        plt.title("Gradient Boosting - Learning Curve")
        plt.xlabel("Number of Estimators")
        plt.ylabel("Mean Squared Error")
        plt.grid(True)
        plt.show()

# Gradient Boosting Classifier
class GradientBoostingClassifier:
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=3):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.trees = []

    def fit(self, X, y):
        y = np.where(y == 1, 1.0, -1.0)
        self.initial_pred = 0.0
        residuals = y.astype(float)

        for _ in range(self.n_estimators):
            tree = DecisionTreeRegressor(max_depth=self.max_depth)
            tree.fit(X, residuals)
            predictions = tree.predict(X)
            residuals -= self.learning_rate * predictions
            self.trees.append(tree)

    def predict_proba(self, X):
        pred = np.full(X.shape[0], self.initial_pred, dtype=float)
        for tree in self.trees:
            pred += self.learning_rate * tree.predict(X)
        return self._sigmoid(pred)

    def predict(self, X):
        return (self.predict_proba(X) > 0.5).astype(int)

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
