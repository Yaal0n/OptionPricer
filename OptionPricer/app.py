import streamlit as st
import datetime
import numpy as np
import matplotlib.pyplot as plt
from BlackScholes import BlackScholes
from MonteCarlo import MonteCarlo
import logging

# Set page layout
st.set_page_config(page_title="Option Pricing Calculator", layout="wide")

st.title("Option Pricing Calculator")

# Initialize session state for menu selection
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = None

# Initialize session state for input values
for key in ["underlying_price", "strike", "maturity_date", "r", "volatility", "exercise_ratio",
            "call_price", "put_price", "is_calculated", "greeks"]:
    if key not in st.session_state:
        st.session_state[key] = None

# --- LAYOUT: SIDEBAR FOR FIXED INPUTS, PRICES & GREEKS ---
with st.sidebar:
    st.title("Made by Yaal0n")

    st.markdown(
        """
        <a href="https://www.linkedin.com/in/yungpinchen/" target="_blank">
            <button style="color: white; padding: 10px 15px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; width: 100%;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="20" style="vertical-align: middle; margin-right: 5px;">
                Connect on LinkedIn
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

    # Portfolio button
    st.markdown(
        """
        <a href="https://yaal0n.github.io/" target="_blank">
            <button style="color: white; padding: 10px 15px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; width: 100%;">
                🌍 Visit My Portfolio
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

    # GitHub repository button with GitHub logo
    # st.markdown(
    #     """
    #     <a href="https://github.com/Yaal0n" target="_blank">
    #         <button style="color: white; padding: 10px 15px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; width: 100%;">
    #             <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="20" style="vertical-align: middle; margin-right: 5px;">
    #             GitHub Repository
    #         </button>
    #     </a>
    #     """,
    #     unsafe_allow_html=True
    # )


    st.markdown("## 📋 Input Parameters")

    st.session_state.underlying_price = st.number_input("Underlying Price", value=100.0, step=0.01)
    st.session_state.strike = st.number_input("Strike Price", value=100.0, step=0.001)
    st.session_state.maturity_date = st.date_input("Maturity Date", min_value=datetime.date.today())

    st.session_state.r = st.number_input("Risk-Free Rate", value=0.05, step=0.0001, format="%.4f")
    st.session_state.volatility = st.number_input("Volatility (σ)", value=0.2, step=0.0001, format="%.4f")
    st.session_state.exercise_ratio = st.number_input("Exercise Ratio", value=0.1, step=0.001)

    sim_strategy_type = st.selectbox("Calculation Method", ["BlackScholes", "MonteCarlo"])

    # Select strategy
    sim_strategy = MonteCarlo() if sim_strategy_type == "MonteCarlo" else BlackScholes()

    # --- CALCULATE OPTION PRICE BUTTON ---
    if st.button("Calculate Option Price"):
        if sim_strategy_type == "MonteCarlo":
            st.warning("Calculation using MonteCarlo simulation has not been implemented yet!")

        st.session_state.call_price, st.session_state.put_price, st.session_state.greeks = sim_strategy.calculate(
            st.session_state.underlying_price,
            st.session_state.strike,
            st.session_state.maturity_date,
            st.session_state.r,
            st.session_state.volatility,
            st.session_state.exercise_ratio,
        )
        st.session_state.is_calculated = True

    # --- DISPLAY CALL & PUT PRICES ---
    if st.session_state.is_calculated:
        st.markdown("## 📈 Option Prices")
        st.success(f"CALL Price: ${st.session_state.call_price:.4f}")
        st.error(f"PUT Price: ${st.session_state.put_price:.4f}")

        # --- DISPLAY GREEKS ---
        st.markdown("## 📊 Greeks")
        st.metric(label="Delta (CALL)", value=f"{st.session_state.greeks['delta_call']:.4f}")
        st.metric(label="Delta (PUT)", value=f"{st.session_state.greeks['delta_put']:.4f}")
        st.metric(label="Gamma", value=f"{st.session_state.greeks['gamma']:.4f}")
        st.metric(label="Vega", value=f"{st.session_state.greeks['vega']:.4f}")
        st.metric(label="Daily-Theta (CALL)", value=f"{st.session_state.greeks['theta_call']:.4f}")
        st.metric(label="Daily-Theta (PUT)", value=f"{st.session_state.greeks['theta_put']:.4f}")
        st.metric(label="Rho (CALL)", value=f"{st.session_state.greeks['rho_call']:.4f}")
        st.metric(label="Rho (PUT)", value=f"{st.session_state.greeks['rho_put']:.4f}")

# --- TOP MENU BAR (DYNAMIC CONTENT IN MAIN AREA) ---
st.markdown("## Navigation")

menu_items = {
    "Payoff Diagram": "💰 Payoff Diagram",
    "Sensitivity Analysis": "📉 Sensitivity Analysis",
    "Market Data": "📰 Market Data",
    "Settings": "⚙️ Settings"
}

menu_cols = st.columns(len(menu_items))  # Create columns for buttons

for key, label in menu_items.items():
    with menu_cols[list(menu_items.keys()).index(key)]:  # Correct indexing
        st.markdown(
            f"""
            <style>
                div[data-testid="stButton"] > button {{
                    width: 100%;
                    padding: 10px;
                    font-size: 16px;
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
        if st.button(label, key=key):
            st.session_state.selected_menu = key  # Store plain text only
            st.rerun()  # Force UI update


if st.session_state.selected_menu == "Payoff Diagram":
    st.subheader("💰 Payoff Diagram")

    if st.session_state.is_calculated:
        price_range = np.linspace(st.session_state.underlying_price * 0.5, st.session_state.underlying_price * 1.5, 100)
        payoff = [max(p - st.session_state.strike, 0) for p in price_range]

        fig, ax = plt.subplots()
        ax.plot(price_range, payoff, label="Option Payoff", color="blue")
        ax.axhline(y=0, color='black', linestyle='--')
        ax.set_xlabel("Underlying Price")
        ax.set_ylabel("Profit / Loss")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("⚠️ Calculate the option price first to view the payoff diagram.")

elif st.session_state.selected_menu == "Sensitivity Analysis":
    st.subheader("📉 Sensitivity Analysis")
    st.write("Sensitivity Analysis will be displayed here.")

elif st.session_state.selected_menu == "Market Data":
    st.subheader("📈 Market Data")
    st.write("Market Data will be displayed here.")

elif st.session_state.selected_menu == "Settings":
    st.subheader("⚙️ Settings")
    st.write("Settings will be displayed here.")
