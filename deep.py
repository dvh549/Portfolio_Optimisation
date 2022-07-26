# import pdr required libs
from pandas_datareader import data as pdr
from datetime import datetime, timedelta
import yfinance as yf
yf.pdr_override()

# import DL required libs
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense

class Deep:
    def __init__(self, config_dict):
        self.config = config_dict

    def load_config(self):
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

    def save_model(self):
        self.model.save("saved_models/model.h5")

    def load_model(self):
        self.model = load_model("saved_models/model.h5")

    def build(self):
        model = Sequential()
        model.add(LSTM(20, activation='relu', input_shape=(self.n_steps, self.n_features)))
        model.add(Dense(1))
        model.compile(optimizer="adam", loss="mae")
        self.model = model

    def train(self):
        self.model.fit(self.X, self.y, epochs=150, batch_size=32, verbose=0)

    def predict(self):
        predictions = []
        x_input = np.array([[price] for price in self.df.iloc[-self.n_steps:]])
        for _ in range(self.forecast_period):
            temp = x_input.reshape((1, self.n_steps, self.n_features))
            yhat = self.model.predict(temp, verbose=0)[0][0]
            predictions.append(float(yhat))
            x_input = np.append(x_input[1:], [yhat])
        return predictions

    def run_steps_to_get_predictions(self):
        self.load_config()
        self._preprocess_data()
        self.build()
        self.train()
        return self.predict()

if __name__ == "__main__":
    ticker = input("Which ticker would you like to predict for? ")
    start, end = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d"), datetime.today().strftime("%Y-%m-%d")
    data = pdr.get_data_yahoo(ticker, start=start, end=end)
    close = data["Close"]
    forecast_period = input("How many days would you like to predict for? ")
    config_dict = {"df": close, "n_steps": 24, "n_features": 1, "forecast_period": int(forecast_period)}
    model = Deep(config_dict)
    predictions = model.run_steps_to_get_predictions()
    print(predictions)