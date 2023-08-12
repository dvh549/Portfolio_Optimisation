# import pdr required libs
from pandas_datareader import data as pdr
from datetime import datetime, timedelta
import yfinance as yf
yf.pdr_override()

# import deep learning model
from deep import Deep

# import flask required libs
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/getPredictions/<ticker>/<int:days_to_forecast>")
def get_predictions(ticker, days_to_forecast):
    config_dict = {"ticker": ticker, "n_steps": 24, "n_features": 1, "forecast_period": days_to_forecast}
    start, end = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d"), datetime.today().strftime("%Y-%m-%d")
    data = pdr.get_data_yahoo(config_dict["ticker"], start=start, end=end)
    if data.empty:
        return jsonify(
            {
                "code": 404,
                "message": f"{ticker} not found."
            }
        )
    else:
        config_dict["df"] = data["Close"]
        predictions = initialise_model_and_predict(config_dict)
        return jsonify(
            {
                "code": 200,
                "predictions": predictions
            }
        )

def initialise_model_and_predict(config_dict):
    model = Deep(config_dict)
    model.load_config()
    model.load_model()
    return model.predict()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)