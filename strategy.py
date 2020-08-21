from dataclasses import dataclass


# дата класс для ТЕКУЩИХ параметров
@dataclass
class Price:
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    index: int = 0


class Strategy:
    def __init__(self, data, start_index):
        self.data = data
        self.start_index = start_index
        self.stop_loss_value = None
        self.take_profit_value = None
        self.statistic = {'profit_deals_number': 0,
                          'loss_deals_number': 0,
                          'bank': 0
                          }
        self.price = Price()

    # условие старта сделки --> покупки/продажи
    # is_buy -> True=buy, False=sell
    def start_deal(self, is_buy):
        pass

    # условие по тейк-профиту - возвращает True/False
    def take_profit(self, is_buy, start_price):
        pass

    # условие по стоп-лоссу - возвращает True/False
    def stop_loss(self, is_buy, start_price):
        pass

    def run(self):
        is_in_deal: bool = False
        start_price: float = 0.0
        deal_type = ''  # buy/sell

        for i, row in enumerate(self.data):
            self.price.open = row['open']
            self.price.high = row['high']
            self.price.low = row['low']
            self.price.close = row['close']
            self.price.index = i

            # старт сделки - buy
            if not is_in_deal:
                if self.start_deal(is_buy=True) or self.start_deal(is_buy=False):
                    deal_type = 'buy' if self.start_deal(is_buy=True) else 'sell'
                    start_price = self.price.open
                    is_in_deal = True
                    print('start', self.price, row['date'], deal_type)
            # завершение сделки - по стоп-лоссу или тейк-профиту
            else:
                if deal_type == 'buy':
                    if self.take_profit(is_buy=True, start_price=start_price):
                        profit = self.take_profit_value - start_price
                        self.statistic['profit_deals_number'] += 1
                        self.statistic['bank'] += profit
                        is_in_deal = False
                        continue
                    if self.stop_loss(is_buy=True, start_price=start_price):
                        profit = start_price - self.stop_loss_value
                        self.statistic['loss_deals_number'] += 1
                        self.statistic['bank'] += profit
                        is_in_deal = False
                        continue
                else:  # deal_type='sell'
                    if self.take_profit(is_buy=False, start_price=start_price):
                        profit = start_price - self.take_profit_value
                        self.statistic['profit_deals_number'] += 1
                        self.statistic['bank'] += profit
                        is_in_deal = False
                        continue
                    if self.stop_loss(is_buy=False, start_price=start_price):
                        profit = start_price - self.stop_loss_value
                        self.statistic['loss_deals_number'] += 1
                        self.statistic['bank'] += profit
                        is_in_deal = False
