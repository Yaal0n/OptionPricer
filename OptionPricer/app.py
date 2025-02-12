import streamlit as st

from BlackScholes import BlackScholes
from MonteCarlo import MonteCarlo

st.title("Option Pricing Calculator")

sim_strategy = None

option_type = st.selectbox("Option Type", ["CALL", "PUT"])
underlying_price = st.number_input("Underlying Price", value=100.0, step=0.01)
strike = st.number_input("Strike Price", value=100.0, step=0.001)
time_to_maturity = st.number_input("Time to Maturity in years", value=1.0, step=0.01)
r = st.number_input("Risk-Free Rate", value=0.05, step=0.001)
volatility = st.number_input("Volatility (σ)", value=0.2, step=0.01)
sim_strategy_type = st.selectbox("Calculation method", ["BlackScholes","MonteCarlo"])

if sim_strategy_type == "MonteCarlo":
    sim_strategy = MonteCarlo()
elif sim_strategy_type == "BlackScholes":
    sim_strategy = BlackScholes()


if st.button("Start Calculation"):
    price = sim_strategy.calculate(option_type, underlying_price, strike, time_to_maturity, r, volatility)
    st.text(f"Calculated price: {price}")

# Compute Option Price
# if st.button("Calculate Price"):
#     strategy = BlackScholes() if strategy_name == "Black-Scholes" else MonteCarlo()
#     price = strategy.calculate(S=S, K=K, T=T, r=r, sigma=sigma, option_type=option_type)
#
#     st.success(f"Calculated Option Price: {price:.4f}")