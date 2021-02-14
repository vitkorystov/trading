from dataclasses import dataclass


@dataclass
class Candles:
    """Дата класс для анализа свечей"""
    open: float
    close: float
    high: float
    low: float

    def is_bull(self) -> bool:
        return self.close > self.open

    def is_bear(self) -> bool:
        return self.close < self.open

    def is_dodge(self, tolerance=0):
        """проверка на додж. tolerance - в пунктах"""
        return abs(self.close - self.open) <= tolerance

    def is_long_body(self, body_size=None) -> bool:
        """проверка на длину свечи. body_size - в пунктах"""
        if body_size is not None:
            return self.body() >= body_size

    def body(self) -> float:
        return abs(self.open - self.close)
