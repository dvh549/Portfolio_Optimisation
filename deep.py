# import DL required libs
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Bidirectional, Dropout

class Deep:
    def __init__(self, config_dict):
        self.config = config_dict

    def load(self):
        self.df = self.config["df"]
        self.n_steps = self.config["n_steps"]
        self.n_features = self.config["n_features"]
        self.forecast_period = self.config["forecast_period"]

    def _preprocess_data(self):
        sequence = self.df.tolist()
        X, Y = list(), list()
  
        for i in range(len(sequence)):
            sam = i + self.n_steps
            if sam > len(sequence)-1:
                break
            x, y = sequence[i:sam], sequence[sam]
            X.append(x)
            Y.append(y)

        X, self.y = np.array(X), np.array(Y)
        self.X = X.reshape((X.shape[0], X.shape[1], 1))

    def build(self):
        model = Sequential()
        model.add(Bidirectional(LSTM(50, activation='relu', return_sequences=True), input_shape=(self.n_steps, self.n_features)))
        model.add(Dropout(0.1))
        model.add(Bidirectional(LSTM(50, activation="relu")))
        model.add(Dropout(0.1))
        model.add(Dense(1))
        model.compile(optimizer="adam", loss="mae")
        self.model = model

    def train(self):
        self.model.fit(self.X, self.y, epochs=10, verbose=0)

    def predict(self):
        predictions = []
        x_input = np.array([[price] for price in self.df.iloc[-self.n_steps:]])
        for _ in range(self.forecast_period):
            temp = x_input.reshape((1, self.n_steps, self.n_features))
            yhat = self.model.predict(temp, verbose=0)[0][0]
            predictions.append(float(yhat))
            x_input = x_input[1:]
            x_input = np.append(x_input, [yhat])
        return predictions