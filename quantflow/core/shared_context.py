class SharedContext:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SharedContext, cls).__new__(cls, *args, **kwargs)
            cls._instance.latest_price = 0.0
        return cls._instance

    def update_latest_price(self, price):
        self.latest_price = price

    def get_latest_price(self):
        return self.latest_price
