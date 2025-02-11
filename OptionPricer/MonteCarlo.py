from SimulationStrategy import SimulationStrategy


class MonteCarlo(SimulationStrategy):
    def __init__(self):
        super().__init__()
        self.amount_simulations = 1000

    def calculate(self, option_type, underlying_price, strike, time_to_maturity, risk_free_rate, volatility):
        return 99999