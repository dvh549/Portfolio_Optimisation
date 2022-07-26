# Share Price Prediction

1. Share price information retrieved from Yahoo Finance.
2. A deep learning model is used to predict the specified periods ("forecast_period").
3. Running **deep.py** will prompt the user for the ticker and periods to forecast for.
4. Once inputs are processed, it will return a list of predictions.

## To notes
1. Forecasted period is inclusive of the current day **IF** the market has not closed.
2. **app.py** serves just as a template to integrate the model for a web application.