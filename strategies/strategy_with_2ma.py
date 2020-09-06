from strategies.strategy import Strategy


class StrategyWith2MA(Strategy):
    def __init__(self, data, start_index, take_profit, stop_loss, delta_limit, main_time_frame, ticker):
        super().__init__(data=data, start_index=start_index, take_profit=take_profit, stop_loss=stop_loss,
                         main_time_frame=main_time_frame, ticker=ticker)
        self.ma_short = None
        self.ma_long = None
        self.delta_limit = delta_limit

    def set_ma(self, ma_short, ma_long):
        self.ma_short = ma_short
        self.ma_long = ma_long

    def is_start_deal(self, is_buy):
        # условие - пересечение длинной и медленной MA
        if (self.price.index + 1) >= self.start_index:
            i = self.price.index
            delta = abs(self.price.close - self.ma_long[i])
            self.delta_limit = 100
            # покупка
            if is_buy and self.bull_ma_cross():
                if delta < self.delta_limit:
                    if self.is_print:
                        print('start_deal->  buy|', 'delta=', delta,  'ma_long=', self.ma_long[i], 'ma_short=', self.ma_short[i])
                    return True
            # продажа
            if not is_buy and self.bear_ma_cross():
                if delta < self.delta_limit:
                    if self.is_print:
                        print('start_deal-> sell|', 'delta=', delta, 'ma_long=', self.ma_long[i], 'ma_short=', self.ma_short[i])
                    return True
            return False
        else:
            return False

    def is_take_profit(self, is_buy, take_profit_price):
        if is_buy:
            return True if self.price.high >= take_profit_price else False
        else:
            return True if self.price.low <= take_profit_price else False

    def is_stop_loss(self, is_buy, stop_loss_price):
        if is_buy:
            return True if self.price.low <= stop_loss_price else False
        else:
            return True if self.price.high >= stop_loss_price else False

    # по перечению МА
    def is_end_deal(self, is_buy, start_price):
        if is_buy:
            if self.bear_ma_cross():
                self.end_deal_price = self.price.close
                if self.is_print:
                    print('stop_loss->  by cross_ma', 'ma_long=', self.ma_long[self.price.index],
                          'ma_short=', self.ma_short[self.price.index])
                return True
        else:
            if self.bull_ma_cross():
                self.end_deal_price = self.price.close
                if self.is_print:
                    print('stop_loss-> by cross_ma', 'ma_long=', self.ma_long[self.price.index],
                          'ma_short=', self.ma_short[self.price.index])
                return True
        return False

    # бычье перечение - короткая МА снизу длинной (обычно это сигнал на покупку)
    def bull_ma_cross(self):
        i = self.price.index
        return True if self.ma_short[i] > self.ma_long[i] and self.ma_short[i-1] < self.ma_long[i-1] else False

    # медвежье перечение - короткая МА сверху длинной (обычно это сигнал на продажу)
    def bear_ma_cross(self):
        i = self.price.index
        return True if self.ma_long[i] > self.ma_short[i] and self.ma_long[i-1] < self.ma_short[i-1] else False
