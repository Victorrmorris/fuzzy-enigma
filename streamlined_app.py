import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Placeholder data for spending categories
spending_data = [
    {"Category": "Groceries", "Amount": 1200},
    {"Category": "Rent", "Amount": 2500},
    {"Category": "Entertainment", "Amount": 600},
    {"Category": "Utilities", "Amount": 400},
    {"Category": "Transportation", "Amount": 300}
]

# Dataframe for accounts
df_accounts = pd.DataFrame(accounts_data)
df_spending = pd.DataFrame(spending_data)

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

# Bar chart for account balances
st.subheader("Account Balances Distribution")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="Account Name", y="Balance (USD)", data=df_accounts, palette="Blues_d", ax=ax)
ax.set_title("Distribution of Account Balances (USD)")
ax.set_ylabel("Balance (USD)")
ax.set_xlabel("Account Name")
plt.xticks(rotation=45)
st.pyplot(fig)

# Monthly spending distribution
st.subheader("Monthly Spending Distribution")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x="Category", y="Amount", data=df_spending, palette="Pastel1", ax=ax)
ax.set_title("Spending by Category")
ax.set_ylabel("Amount (USD)")
ax.set_xlabel("Category")
plt.xticks(rotation=45)
st.pyplot(fig)

# Budget alerts and progress
st.subheader("Budget Progress")
for _, row in df_spending.iterrows():
    category = row["Category"]
    amount = row["Amount"]
    st.progress(amount / 3000, text=f"{category}: ${amount:,.2f} spent out of $3000")

# Chatbot for spending and budgeting insights
st.subheader("Linked Account Insights")
def chatbot_response(account_name):
    account = df_accounts[df_accounts["Account Name"] == account_name]
    if account.empty:
        return "Sorry, I couldn't find any information for that account. Please try again."
    balance = account.iloc[0]["Balance (USD)"]
    if balance < 100:
        return f"Your balance in {account_name} is quite low (${balance:.2f}). Consider transferring funds to avoid overdraft."
    elif balance < 1000:
        return f"Your balance in {account_name} is below $1000. Monitor your spending carefully."
    else:
        return f"Your balance in {account_name} is healthy (${balance:.2f}). Keep up the good financial habits!"

selected_account = st.selectbox("Select an account to get insights:", df_accounts["Account Name"].tolist())
if st.button("Get Insights"):
    response = chatbot_response(selected_account)
    st.write(response)

# Enhanced chatbot for spending categories
st.subheader("Spending Insights")
def spending_chatbot_response(category_name):
    category = df_spending[df_spending["Category"] == category_name]
    if category.empty:
        return "Sorry, I couldn't find any information for that category. Please try again."
    amount = category.iloc[0]["Amount"]
    if amount > 2000:
        return f"You have spent a lot on {category_name} (${amount:.2f}). Consider reducing expenses in this category."
    elif amount > 1000:
        return f"Your spending on {category_name} (${amount:.2f}) is moderate. Keep an eye on it."
    else:
        return f"Your spending on {category_name} (${amount:.2f}) is within a healthy range. Good job!"

selected_category = st.selectbox("Select a spending category to get insights:", df_spending["Category"].tolist())
if st.button("Get Spending Insights"):
    category_response = spending_chatbot_response(selected_category)
    st.write(category_response)
