from SimulationStrategy import SimulationStrategy


class MonteCarlo(SimulationStrategy):
    def __init__(self):
        super().__init__()
        self.amount_simulations = 1000

    def calculate(self, underlying_price, strike, maturity_date, risk_free_rate, volatility, exercise_ratio):
        greeks = {
            "delta_call": 0,
            "delta_put": 0,
            "gamma": 0,
            "theta_call": 0,
            "theta_put": 0,
            "vega": 0,
            "rho_call": 0,
            "rho_put": 0
        }

        return 99999, 99999, greeks