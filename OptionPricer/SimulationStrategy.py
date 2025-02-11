from abc import ABC, abstractmethod

class SimulationStrategy(ABC):
    @abstractmethod
    def calculate(self, option_type, underlying_price, strike, time_to_maturity, risk_free_rate, volatility):
        pass