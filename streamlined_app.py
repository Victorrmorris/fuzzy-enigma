import streamlit as st
import pandas as pd

# Initialize the app
st.set_page_config(page_title="Total Balance and Linked Accounts", layout="wide", initial_sidebar_state="expanded")
st.title("Total Balance and Linked Accounts")

# Placeholder data for accounts
accounts_data = [
    {"Account Name": "USAA Checking", "Balance": 4500.13, "Currency": "USD"},
    {"Account Name": "AMEX Savings", "Balance": 20348.05, "Currency": "USD"},
    {"Account Name": "SCU Checking (Local)", "Balance": 233.81, "Currency": "USD"},
    {"Account Name": "Wise", "Balance": 198.76, "Currency": "EUR"},
    {"Account Name": "Greenlight (Kids)", "Balance": 300.00, "Currency": "USD"}
]

# Dataframe for accounts
df_accounts = pd.DataFrame(accounts_data)

# Calculate total balance
currency_conversion_rates = {"USD": 1, "EUR": 1.09}  # Example conversion rates

def convert_to_usd(balance, currency):
    return balance * currency_conversion_rates.get(currency, 1)

df_accounts["Balance (USD)"] = df_accounts.apply(lambda row: convert_to_usd(row["Balance"], row["Currency"]), axis=1)
total_balance = df_accounts["Balance (USD)"].sum()

# Display total balance
st.subheader("Total Balance")
st.metric(label="Total Balance (USD)", value=f"${total_balance:,.2f}")

# Display linked accounts
def format_currency(value, currency):
    return f"{value:,.2f} {currency}"

df_accounts["Formatted Balance"] = df_accounts.apply(lambda row: format_currency(row["Balance"], row["Currency"]), axis=1)
st.subheader("Linked Accounts")
st.dataframe(df_accounts[["Account Name", "Formatted Balance"]])
