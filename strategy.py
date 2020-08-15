

class Strategy:
    def __init__(self, data):
        self.data = data
        self.stop_loss_value = None
        self.take_profit_value = None
        self.statistic = {'profit_deals_number': 0,
                          'loss_deals_number': 0,
                          'bank': 0
                          }

    # условие старта сделки --> покупки
    def buy_condition(self):
        pass

    # условие старта сделки --> продажи
    def sell_condition(self):
        pass

    # условие продажи по тейк-профиту
    def take_profit_buy(self):
        pass

    # условие продажи по стоплоссу
    def stop_loss_buy(self):
        pass

    # условие покупки по тейк-профиту
    def take_profit_sell(self):
        pass

    # условие покупки по стоплоссу
    def stop_loss_sell(self):
        pass

    def run(self):
        is_in_deal: bool = False
        start_price: float = 0.0
        end_price: float = 0.0
        deal_type = ''  # buy/sell
        profit = 0.0

        for i, row in enumerate(self.data):

            # старт сделки - buy
            if not is_in_deal:
                if self.buy_condition():
                    deal_type = 'buy'
                    start_price = row['open']
                    is_in_deal = True
                if self.sell_condition():
                    deal_type = 'sell'
                    start_price = row['open']
                    is_in_deal = True

            # завершение сделки - по стоп-лоссу или тейк-профиту
            if is_in_deal:
                if deal_type == 'buy':
                    if self.take_profit_buy():
                        profit = self.take_profit_value - start_price
                        self.statistic['profit_deals_number'] += 1
                        self.statistic['bank'] += profit
                    if self.stop_loss_buy():
                        profit = start_price - self.stop_loss_value
                        self.statistic['loss_deals_number'] += 1
                        self.statistic['bank'] += profit

                if deal_type == 'sell':
                    if self.take_profit_sell():
                        profit = start_price - self.take_profit_value
                        self.statistic['profit_deals_number'] += 1
                        self.statistic['bank'] += profit
                    if self.stop_loss_buy():
                        profit = start_price - self.stop_loss_value
                        self.statistic['loss_deals_number'] += 1
                        self.statistic['bank'] += profit

            pass
