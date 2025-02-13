from abc import ABC, abstractmethod

class SimulationStrategy(ABC):
    @abstractmethod
    def calculate(self, option_type, underlying_price, strike, maturity_date, risk_free_rate, volatility, exercise_ratio):
        pass