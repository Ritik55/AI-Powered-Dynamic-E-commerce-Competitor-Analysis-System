import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

class PricePredictor:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, price_history):
        dates = [(datetime.strptime(p['timestamp'], "%Y-%m-%d %H:%M:%S") - datetime(1970, 1, 1)).days for p in price_history]
        prices = [p['price'] for p in price_history]
        
        X = np.array(dates).reshape(-1, 1)
        y = np.array(prices)
        
        self.model.fit(X, y)

    def predict_future_prices(self, days=30):
        last_date = max(self.model.predict(X))
        future_dates = np.array([(last_date + i).days for i in range(1, days+1)]).reshape(-1, 1)
        
        predicted_prices = self.model.predict(future_dates)
        
        return [
            {
                "date": (datetime(1970, 1, 1) + timedelta(days=int(date))).strftime("%Y-%m-%d"),
                "price": price
            }
            for date, price in zip(future_dates, predicted_prices)
        ]
