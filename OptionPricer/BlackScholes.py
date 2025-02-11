from SimulationStrategy import SimulationStrategy
import numpy as np
from scipy.stats import norm


class BlackScholes(SimulationStrategy):
    def __init__(self):
        super().__init__()

    def calculate(self, option_type, underlying_price, strike, time_to_maturity, risk_free_rate, volatility):
        S = underlying_price
        K = strike
        T = time_to_maturity
        r = risk_free_rate
        sigma = volatility

        # Compute intermediary values for Black-Scholes formula
        numerator = np.log(S / K) + (r + 0.5 * sigma ** 2) * T
        denominator = sigma * np.sqrt(T)
        standardized_return = numerator / denominator
        adjusted_return = standardized_return - sigma * np.sqrt(T)

        # Compute option price
        if option_type == "CALL":
            return S * norm.cdf(standardized_return) - K * np.exp(-r * T) * norm.cdf(adjusted_return)
        elif option_type == "PUT":
            return K * np.exp(-r * T) * norm.cdf(-adjusted_return) - S * norm.cdf(-standardized_return)
        else:
            raise ValueError("option_type must be 'call' or 'put'")