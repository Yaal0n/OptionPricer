from SimulationStrategy import SimulationStrategy


class MonteCarlo(SimulationStrategy):
    def __init__(self):
        super().__init__()
        self.amount_simulations = 1000

    def calculate(self, underlying_price, strike, maturity_date, risk_free_rate, volatility, exercise_ratio):
        return 99999