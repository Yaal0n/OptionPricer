import datetime

from SimulationStrategy import SimulationStrategy
import numpy as np
from scipy.stats import norm


class BlackScholes(SimulationStrategy):
    def __init__(self):
        super().__init__()

    def calculate(self, underlying_price, strike, maturity_date, risk_free_rate, volatility, exercise_ratio):
        time_to_maturity_years = (maturity_date - datetime.date.today()).days / 365.0

        ratio_underlying_price_strike = underlying_price/strike
        variance = pow(volatility,2)
        discount_factor = np.exp(-risk_free_rate*time_to_maturity_years)



        d1 = (np.log(ratio_underlying_price_strike) + (risk_free_rate+variance/2)*time_to_maturity_years)/(volatility*np.sqrt(time_to_maturity_years))
        d2 = (np.log(ratio_underlying_price_strike) + (risk_free_rate-variance/2)*time_to_maturity_years)/(volatility*np.sqrt(time_to_maturity_years))

        call_price = (underlying_price*norm.cdf(d1)-strike*discount_factor*norm.cdf(d2))*exercise_ratio
        put_price = (-underlying_price*norm.cdf(-d1)+strike*discount_factor*norm.cdf(-d2))*exercise_ratio

        greeks = self.calculate_greeks(underlying_price, strike, maturity_date, risk_free_rate, volatility, exercise_ratio, d1, d2)

        return call_price, put_price, greeks


    def calculate_greeks(self, underlying_price, strike, maturity_date, risk_free_rate, volatility, exercise_ratio, d1, d2):
            """
            Calculates all Greeks (Delta, Gamma, Theta, Vega, Rho) for the Black-Scholes model.

            Returns:
            - Dictionary containing Delta, Gamma, Theta, Vega, and Rho for Call and Put options
            """
            time_to_maturity_years = (maturity_date - datetime.date.today()).days / 365.0

            if time_to_maturity_years <= 0:
                return None  # No Greeks for expired options

            n_prime_d1 = norm.pdf(d1)  # Standard normal PDF for Gamma & Vega

            # Delta
            delta_call = norm.cdf(d1) * exercise_ratio
            delta_put = (norm.cdf(d1) - 1) * exercise_ratio

            # Gamma (Same for Calls & Puts)
            gamma = (n_prime_d1 / (underlying_price * volatility * np.sqrt(time_to_maturity_years))) * exercise_ratio

            # Vega (Same for Calls & Puts)
            vega = (underlying_price * n_prime_d1 * np.sqrt(
                time_to_maturity_years)) * 0.01 * exercise_ratio  # Adjusted for 1% change in volatility

            # Theta
            theta_call = (- (underlying_price * n_prime_d1 * volatility) / (
                        2 * np.sqrt(time_to_maturity_years)) - risk_free_rate * strike * np.exp(
                -risk_free_rate * time_to_maturity_years) * norm.cdf(d2)) * (exercise_ratio / 365)
            theta_put = (- (underlying_price * n_prime_d1 * volatility) / (
                        2 * np.sqrt(time_to_maturity_years)) + risk_free_rate * strike * np.exp(
                -risk_free_rate * time_to_maturity_years) * norm.cdf(-d2)) * (exercise_ratio / 365)

            # Rho
            rho_call = (strike * time_to_maturity_years * np.exp(-risk_free_rate * time_to_maturity_years) * norm.cdf(
                d2)) * 0.01 * exercise_ratio  # Adjusted for 1% change in rates
            rho_put = (-strike * time_to_maturity_years * np.exp(-risk_free_rate * time_to_maturity_years) * norm.cdf(
                -d2)) * 0.01 * exercise_ratio

            # Store Greeks in a dictionary
            greeks = {
                "delta_call": delta_call,
                "delta_put": delta_put,
                "gamma": gamma,
                "theta_call": theta_call,
                "theta_put": theta_put,
                "vega": vega,
                "rho_call": rho_call,
                "rho_put": rho_put
            }

            return greeks
