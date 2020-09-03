from strategies.strategy import Strategy


class StrategyWith2MA(Strategy):
    def __init__(self, data, start_index, take_profit_range, stop_loss_range, delta_limit):
        super().__init__(data=data, start_index=start_index)
        self.ma_short = None
        self.ma_long = None
        self.take_profit_range = take_profit_range
        self.stop_loss_range = stop_loss_range
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
                    #print('start_deal->  buy|', 'delta=', delta,  'ma_long=', self.ma_long[i], 'ma_short=', self.ma_short[i])
                    return True
                else:
                    return False
            # продажа
            if not is_buy and self.bear_ma_cross():
                if delta < self.delta_limit:
                    #print('start_deal-> sell|', 'delta=', delta, 'ma_long=', self.ma_long[i], 'ma_short=', self.ma_short[i])
                    return True
                else:
                    return False
        else:
            return False

    def is_take_profit(self, is_buy, start_price):
        if is_buy:
            if self.price.high >= (start_price + self.take_profit_range):
                # определим take_profit_value
                self.take_profit_price = start_price + self.take_profit_range
                return True
            else:
                return False
        else:
            if self.price.low <= (start_price - self.take_profit_range):
                # определим take_profit_value
                self.take_profit_price = start_price - self.take_profit_range
                return True
            else:
                return False

    # условие по стоп-лоссу
    def is_stop_loss(self, is_buy, start_price):
        # при покупке
        if is_buy:
            # по заданному значению stop_loss_range
            if self.price.low <= (start_price - self.stop_loss_range):
                # определим stop_loss_value
                # print('stop_loss->', ' by value')
                self.stop_loss_price = start_price - self.stop_loss_range
                return True

            # по перечению МА
            if self.bear_ma_cross():
                self.stop_loss_price = self.price.close
                if self.is_print:
                    print('stop_loss->  by cross_ma', 'ma_long=', self.ma_long[self.price.index],
                          'ma_short=', self.ma_short[self.price.index])
                return True

            return False


        # при продаже
        else:
            # по заданному значению stop_loss_range
            if self.price.high >= (start_price + self.stop_loss_range):
                # определим stop_loss_value
                #print('stop_loss->', ' by value')
                self.stop_loss_price = start_price + self.stop_loss_range
                return True

            # по перечению МА
            if self.bull_ma_cross():
                self.stop_loss_price = self.price.close
                if self.is_print:
                    print('stop_loss-> by cross_ma', 'ma_long=', self.ma_long[self.price.index],
                          'ma_short=', self.ma_short[self.price.index])

                return True

            return False

    # бычье перечение - короткая МА снизу длинной
    # сигнал на покупку
    def bull_ma_cross(self):
        i = self.price.index
        return True if self.ma_short[i] > self.ma_long[i] and self.ma_short[i-1] < self.ma_long[i-1] else False

    # медвежье перечение - короткая МА сверху длинной
    # сигнал на продажу
    def bear_ma_cross(self):
        i = self.price.index
        return True if self.ma_long[i] > self.ma_short[i] and self.ma_long[i-1] < self.ma_short[i-1] else False
