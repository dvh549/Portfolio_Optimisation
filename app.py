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

# import PyPortfolioOpt
from pypfopt import expected_returns
from pypfopt import risk_models
from pypfopt import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

app = Flask(__name__)
CORS(app)

@app.route("/getPredictions/<ticker>/<int:days_to_forecast>")
def get_predictions(ticker, days_to_forecast):
    data = get_data(ticker, (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d"), datetime.today().strftime("%Y-%m-%d"), "Close")
    config_dict = {"ticker": ticker, "n_steps": 24, "n_features": 1, "forecast_period": days_to_forecast, "df": data}
    if data.empty:
        return jsonify(
            {
                "code": 404,
                "message": f"{ticker} not found."
            }
        )
    
    predictions = initialise_model_and_predict(config_dict)
    timestamps = [(datetime.today() + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(1, days_to_forecast+1)]
    return jsonify(
        {
            "code": 200,
            "timestamps": timestamps,
            "predictions": predictions
        }
    )

@app.route("/getOptimisedPortfolio/<tickers>/<int:portfolio_size>")
def get_optimised_portfolio(tickers, portfolio_size):
    tickers_splitted = tickers.split(",")
    if len(tickers_splitted) <= 1:
        return jsonify(
            {
                "code": 500,
                "message": "Please select more than one ticker."
            }
        )   
    historical_prices = get_data(tickers_splitted, (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d"), datetime.today().strftime("%Y-%m-%d"), "Adj Close")
    if historical_prices.empty:
        return jsonify(
            {
                "code": 404,
                "message": f"{tickers} not found."
            }
        )  
    for column in historical_prices:
        if historical_prices[column].isnull().sum() == len(historical_prices[column]):
            return jsonify(
                {
                    "code": 404,
                    "message": f"{column} not found."
                }
            )     

    mu = expected_returns.mean_historical_return(historical_prices)
    S = risk_models.sample_cov(historical_prices)
    ef = EfficientFrontier(mu, S)
    ef.max_sharpe()
    w = ef.clean_weights()
    ar, vol, sharpe = ef.portfolio_performance()

    latest_prices = get_latest_prices(historical_prices)
    da = DiscreteAllocation(w, latest_prices, total_portfolio_value=portfolio_size)
    allocation, leftover = da.lp_portfolio()
    for key in allocation:
        allocation[key] = int(allocation[key])
    return jsonify(
        {
            "code": 200,
            "allocations": allocation,
            "expected_annual_return": "{:.1f}%".format(100 * ar),
            "annual_volatility": "{:.1f}%".format(100 * vol),
            "sharpe_ratio": "{:.2f}".format(sharpe),
            "funds_remaining": "${:.2f}".format(leftover)
        }
    )

def get_data(tickers, start, end, key):
    data = pdr.get_data_yahoo(tickers, start=start, end=end)[key]
    return data

def initialise_model_and_predict(config_dict):
    model = Deep(config_dict)
    model.load_config()
    model.load_model()
    return model.predict()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)