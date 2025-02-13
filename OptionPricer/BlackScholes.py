import datetime

from SimulationStrategy import SimulationStrategy
import numpy as np
from scipy.stats import norm


class BlackScholes(SimulationStrategy):
    def __init__(self):
        super().__init__()

    def calculate(self, option_type, underlying_price, strike, maturity_date, risk_free_rate, volatility, exercise_ratio):
        time_to_maturity_years = (maturity_date - datetime.date.today()).days / 365.0

        ratio_underlying_price_strike = underlying_price/strike
        variance = pow(volatility,2)
        discount_factor = np.exp(-risk_free_rate*time_to_maturity_years)



        d1 = (np.log(ratio_underlying_price_strike) + (risk_free_rate+variance/2)*time_to_maturity_years)/(volatility*np.sqrt(time_to_maturity_years))
        d2 = (np.log(ratio_underlying_price_strike) + (risk_free_rate-variance/2)*time_to_maturity_years)/(volatility*np.sqrt(time_to_maturity_years))

        if option_type == "CALL":
            return (underlying_price*norm.cdf(d1)-strike*discount_factor*norm.cdf(d2))*exercise_ratio
        else:
            return (-underlying_price*norm.cdf(-d1)+strike*discount_factor*norm.cdf(-d2))*exercise_ratio
