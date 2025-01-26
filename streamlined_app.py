import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

# Placeholder data for Germany and US budgets
germany_budget_data = [
    {"Category": "Transportation", "Amount": 62.80},
    {"Category": "Rent", "Amount": 1800.00},
    {"Category": "Entertainment", "Amount": 154.67},
    {"Category": "Education", "Amount": 123.54},
    {"Category": "Utilities", "Amount": 179.20},
    {"Category": "Groceries", "Amount": 845.98}
]

us_budget_data = [
    {"Category": "Transportation", "Amount": 113.67},
    {"Category": "Mortgage", "Amount": 1502.16},
    {"Category": "Home Maintenance", "Amount": 312.43},
    {"Category": "Utilities", "Amount": 416.82},
    {"Category": "Groceries", "Amount": 456.89}
]

# Dataframe for budgets
df_germany_budget = pd.DataFrame(germany_budget_data)
df_us_budget = pd.DataFrame(us_budget_data)

# Account dataframes
df_accounts = pd.DataFrame(accounts_data)

# Spending data
spending_data = [
    {"Category": "Groceries", "Amount": 1200},
    {"Category": "Rent", "Amount": 2500},
    {"Category": "Entertainment", "Amount": 600},
    {"Category": "Utilities", "Amount": 400},
    {"Category": "Transportation", "Amount": 300}
]
df_spending = pd.DataFrame(spending_data)

# Account insights chatbot
st.subheader("Linked Accounts Insights")
def account_insights(account_name):
    account = df_accounts[df_accounts["Account Name"] == account_name]
    if account.empty:
        return "We couldn't find any information for this account. Please try again."
    balance = account.iloc[0]["Balance"]
    if balance < 500:
        return f"Your balance in {account_name} is low (${balance:.2f}). Consider transferring funds."
    elif 500 <= balance < 5000:
        return f"Your balance in {account_name} (${balance:.2f}) is stable. Keep monitoring your spending."
    else:
        return f"Your balance in {account_name} (${balance:.2f}) is healthy. Great financial management!"

selected_account = st.selectbox("Select an account to get insights:", df_accounts["Account Name"].tolist())
if st.button("Get Account Insights"):
    account_response = account_insights(selected_account)
    st.write(account_response)

# Spending insights chatbot
st.subheader("Spending Insights")
def spending_insights(category_name):
    category = df_spending[df_spending["Category"] == category_name]
    if category.empty:
        return "We couldn't find any information for this spending category. Please try again."
    amount = category.iloc[0]["Amount"]
    if amount > 2000:
        return f"Your spending on {category_name} (${amount:.2f}) is high. Consider reducing expenses in this category."
    elif 1000 <= amount <= 2000:
        return f"Your spending on {category_name} (${amount:.2f}) is moderate. Track upcoming expenses carefully."
    else:
        return f"Your spending on {category_name} (${amount:.2f}) is well within your budget."

selected_category = st.selectbox("Select a spending category to get insights:", df_spending["Category"].tolist())
if st.button("Get Spending Insights"):
    spending_response = spending_insights(selected_category)
    st.write(spending_response)

# Lifestyle Event Planning
st.subheader("Lifestyle Event Support")
def lifestyle_event_response(prompt):
    if "move" in prompt.lower():
        return "For frequent moves, consider consolidating accounts and using DECC's budgeting tools to track relocation expenses."
    elif "deployment" in prompt.lower():
        return "For deployments, use DECC's multi-currency tracking and reimbursement tools to stay on top of international expenses."
    elif "retirement" in prompt.lower():
        return "For retirement planning, explore DECC's investment insights and long-term budgeting features to maximize savings."
    else:
        return "We’re here to help! Please ask about moving, deployments, or retirement-related financial advice."

lifestyle_prompts = ["I’m preparing for a move.", "How can I manage finances during a deployment?", "What tools does DECC offer for retirement planning?"]
selected_prompt = st.selectbox("Choose a lifestyle event question:", lifestyle_prompts)
if st.button("Get Lifestyle Event Insights"):
    lifestyle_response = lifestyle_event_response(selected_prompt)
    st.write(lifestyle_response)
