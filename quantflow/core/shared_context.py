import pandas as pd

class SharedContext:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SharedContext, cls).__new__(cls, *args, **kwargs)
            cls._instance.latest_price = pd.Series()
            cls._instance.orders = []
        return cls._instance

    def update_latest_price(self, price):
        self.latest_price = price

    def get_latest_price(self):
        return self.latest_price['Close']
    
    def add_stoploss_takeprofit_order(self, symbol, stoploss, takeprofit, quantity):
        self.orders.append({
            "symbol": symbol,
            "stoploss": stoploss,
            "takeprofit": takeprofit,
            "quantity": quantity
        })
    def get_stoploss_takeprofit_orders(self):
        return self.orders
    def remove_stoploss_takeprofit_order(self, order):
        self.orders.remove(order)