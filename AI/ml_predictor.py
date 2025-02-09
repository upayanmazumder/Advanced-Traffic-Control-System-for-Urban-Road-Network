import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

class MLModel:
    def __init__(self):
        self.model = LinearRegression()
        self.trained = False

    def train_model(self):
        # Simulate historical data.
        np.random.seed(42)
        X = np.zeros((100, 2))  # Features: [effective_count, hour]
        y = np.zeros(100)       # Target: optimal green time (sec)
        for i in range(100):
            effective_count = np.random.randint(0, 30)  # between 0 and 30
            hour = np.random.uniform(0, 24)
            noise = np.random.normal(0, 2)
            optimal_green = 10 + 0.5 * effective_count + 2 * (hour/24) + noise
            X[i, :] = [effective_count, hour]
            y[i] = optimal_green
        self.model.fit(X, y)
        self.trained = True

    def predict_optimal_green(self, effective_count, current_time):
        if not self.trained:
            self.train_model()
        hour = current_time.hour + current_time.minute / 60.0
        X_new = np.array([[effective_count, hour]])
        prediction = self.model.predict(X_new)[0]
        prediction = max(10, min(120, prediction))
        return prediction
