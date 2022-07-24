# import pdr required libs
from distutils.command.config import config
from pandas_datareader import data as pdr
from datetime import datetime, timedelta
import yfinance as yf
yf.pdr_override()

# import deep learning model
from deep import Deep

# import required libs for flask
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/getPredictions")
def get_predictions():
    predictions = model.predict()
    return jsonify(
        {
            "code": 200,
            "predictions": predictions
        }
    )

if __name__ == "__main__":
    config_dict = {"ticker": "O39.SI", "n_steps": 7, "n_features": 1, "forecast_period": 2}
    start, end = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d"), datetime.today().strftime("%Y-%m-%d")
    data = pdr.get_data_yahoo(config_dict["ticker"], start=start, end=end)
    close = data["Close"]
    config_dict["df"] = close
    model = Deep(config_dict)
    model.load()
    model._preprocess_data()
    model.build()
    model.train()
    app.run(host="0.0.0.0", port=5000)