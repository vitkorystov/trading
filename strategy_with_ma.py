from strategy import Strategy


class StrategyWithMA(Strategy):
    def __init__(self, data, start_index):
        super().__init__(data=data, start_index=start_index)
        self.ma_short = None
        self.ma_long = None
        self.take_profit_range = 50

    def set_ma(self, ma_short, ma_long):
        self.ma_short = ma_short
        self.ma_long = ma_long

    def start_deal(self, is_buy):
        # условие - пересечение длинной и медленной MA
        if (self.price.index + 1) >= self.start_index:
            return self.bull_ma_cross() if is_buy else self.bear_ma_cross()
        else:
            return False

    def take_profit(self, is_buy, start_price):
        if is_buy:
            if self.price.high >= (start_price + self.take_profit_range):
                # определим take_profit_value
                self.take_profit_value = start_price + self.take_profit_range
                return True
            else:
                return False
        else:
            if self.price.low <= (start_price - self.take_profit_range):
                # определим take_profit_value
                self.take_profit_value = start_price - self.take_profit_range
                return True
            else:
                return False

    # условие по стоп-лоссу
    def stop_loss(self, is_buy, start_price):
        if is_buy:
            if self.bear_ma_cross():
                # определим stop_loss_value
                self.stop_loss_value = self.price.close
                return True
            else:
                return False
        else:
            if self.bull_ma_cross():
                # определим stop_loss_value
                self.stop_loss_value = self.price.close
                return True
            else:
                return False

    # бычье перечение - короткая МА снизу длинной
    def bull_ma_cross(self):
        if self.ma_short[self.price.index] > self.ma_long[self.price.index] and \
                self.ma_short[self.price.index - 1] < self.ma_long[self.price.index - 1]:
            return True
        else:
            return False

    # бычье перечение - короткая МА снизу длинной
    def bear_ma_cross(self):
        if self.ma_long[self.price.index] > self.ma_short[self.price.index] and \
                self.ma_long[self.price.index - 1] < self.ma_short[self.price.index - 1]:
            return True
        else:
            return False
