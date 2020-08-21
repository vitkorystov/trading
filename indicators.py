

class Indicators:
    def __init__(self, data):
        self.data = data
        self.closes = list(map(lambda x: x['close'], self.data))

    # расчет простой скользящей средней
    # матчасть: https://allfi.biz/Forex/TechnicalAnalysis/Trend-Indicators/prostoe-skolzjashhee-srednee.php
    def sma(self, n, round_digit=1):
        sma_res = []
        for i, row in enumerate(self.closes):
            index_from = i - n + 1
            index_to = i + 1
            sma_value = sum(self.closes[index_from: index_to])/n if i >= (n - 1) else -1
            sma_res.append(round(sma_value, round_digit))
            # print(self.data[i], sma_value)
        return sma_res

    #  расчет экспоненциального скользящего среднего
    # матчасть: https://www.youtube.com/watch?v=sjIjhfuu2go
    def ema(self, n, round_digit=1):
        ema_res = []
        alpha = 2/(n + 1)  # весовой коэффициент
        last_ema_value = -1
        for i, row in enumerate(self.closes):
            if i < (n - 1):
                ema_value = -1
            elif i == (n - 1):  # первое значение - SMA
                index_from = i - n + 1
                index_to = i + 1
                ema_value = sum(self.closes[index_from: index_to])/n
                last_ema_value = ema_value
            else:
                ema_value = alpha * self.closes[i] + (1 - alpha)*last_ema_value
                last_ema_value = ema_value
            # print(self.data[i], ema_value)
            ema_res.append(round(ema_value, round_digit))
        return ema_res
