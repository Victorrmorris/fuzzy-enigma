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

# Placeholder data for spending categories
spending_data = [
    {"Category": "Groceries", "Amount": 1200},
    {"Category": "Rent", "Amount": 2500},
    {"Category": "Entertainment", "Amount": 600},
    {"Category": "Utilities", "Amount": 400},
    {"Category": "Transportation", "Amount": 300}
]

# Placeholder data for credit cards
credit_card_data = [
    {"Credit Card": "Star Card", "Balance": 1645.98, "Credit Limit": 3000.00},
    {"Credit Card": "USAA", "Balance": 3774.12, "Credit Limit": 5000.00}
]

# Placeholder data for spending trends
spending_trend_data = {
    "Date": pd.date_range(start="2023-01-01", periods=12, freq="M"),
    "Spending": np.random.randint(500, 3000, 12)
}

# Dataframe for accounts
df_accounts = pd.DataFrame(accounts_data)
df_spending = pd.DataFrame(spending_data)
df_credit_cards = pd.DataFrame(credit_card_data)
df_spending_trend = pd.DataFrame(spending_trend_data)

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

# Cumulative Spending Trend
st.subheader("Cumulative Spending Trend")
fig, ax = plt.subplots(figsize=(10, 5))
df_spending_trend["Cumulative Spending"] = df_spending_trend["Spending"].cumsum()
sns.lineplot(x="Date", y="Cumulative Spending", data=df_spending_trend, marker="o", ax=ax)
ax.set_title("Cumulative Spending Over Time")
ax.set_ylabel("Cumulative Spending (USD)")
ax.set_xlabel("Date")
plt.xticks(rotation=45)
st.pyplot(fig)

# Budget progress section
st.subheader("Budget Management")
total_spent = df_spending["Amount"].sum()
st.write(f"**Total Spent:** ${total_spent:,.2f}")

for _, row in df_spending.iterrows():
    category = row["Category"]
    amount = row["Amount"]
    progress = min(amount / 3000, 1.0)  # Limit to 100%
    st.text(f"{category}: ${amount:,.2f} spent out of $3000")
    st.progress(progress)

# Credit Card Section
st.subheader("Credit Card Overview")
def calculate_utilization(balance, credit_limit):
    return (balance / credit_limit) * 100

df_credit_cards["Utilization (%)"] = df_credit_cards.apply(lambda row: calculate_utilization(row["Balance"], row["Credit Limit"]), axis=1)
st.dataframe(df_credit_cards)

# Credit Card Insights
st.subheader("Credit Card Insights")
def credit_card_insights(card_name):
    card = df_credit_cards[df_credit_cards["Credit Card"] == card_name]
    if card.empty:
        return "We couldn't find any information for this credit card. Please try again."
    balance = card.iloc[0]["Balance"]
    credit_limit = card.iloc[0]["Credit Limit"]
    utilization = card.iloc[0]["Utilization (%)"]
    if utilization > 30:
        return (f"The utilization on your {card_name} is high at {utilization:.2f}%. To improve your credit score, try to pay down "
                f"your balance from ${balance:,.2f} to below ${0.3 * credit_limit:,.2f}. Maintaining a utilization below 30% is recommended.")
    else:
        return (f"Your utilization on {card_name} is excellent at {utilization:.2f}%. You're effectively managing your credit "
                f"with a balance of ${balance:,.2f} and a credit limit of ${credit_limit:,.2f}. Keep it up!")

selected_card = st.selectbox("Select a credit card to get insights:", df_credit_cards["Credit Card"].tolist())
if st.button("Get Credit Card Insights"):
    card_response = credit_card_insights(selected_card)
    st.write(card_response)

# Spending Heatmap
st.subheader("Spending Heatmap")
heatmap_data = np.random.randint(100, 500, size=(5, 7))  # Random weekly data
heatmap_df = pd.DataFrame(heatmap_data, columns=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                          index=["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"])
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(heatmap_df, annot=True, fmt="d", cmap="coolwarm", ax=ax)
ax.set_title("Weekly Spending Heatmap")
st.pyplot(fig)

# Chatbot for spending and budgeting insights
st.subheader("Spending and Budgeting Insights Chatbot")
def chatbot_response(account_name):
    account = df_accounts[df_accounts["Account Name"] == account_name]
    if account.empty:
        return "We couldn't find any information for this account. Please check the name and try again."
    balance = account.iloc[0]["Balance (USD)"]
    if balance < 500:
        return (f"Your balance in {account_name} is low (${balance:.2f}). Consider reviewing your spending or transferring funds. "
                "Use DECC tools to plan reimbursements or manage unexpected expenses.")
    elif 500 <= balance < 5000:
        return (f"Your balance in {account_name} (${balance:.2f}) is stable. Monitor your spending to ensure it aligns with your "
                "budget. Consider leveraging DECC's real-time tracking tools for better control.")
    else:
        return (f"Your balance in {account_name} (${balance:.2f}) is healthy. Great job managing your finances! "
                "Explore DECC's investment insights to make your money work for you.")

selected_account = st.selectbox("Select an account to get insights:", df_accounts["Account Name"].tolist())
if st.button("Get Insights"):
    response = chatbot_response(selected_account)
    st.write(response)

# Enhanced chatbot for spending categories
st.subheader("Spending Insights Chatbot")
def spending_chatbot_response(category_name):
    category = df_spending[df_spending["Category"] == category_name]
    if category.empty:
        return "We couldn't find any information for this spending category. Please try another one."
    amount = category.iloc[0]["Amount"]
    if amount > 2000:
        return (f"You've spent a significant amount on {category_name} (${amount:.2f}). Consider reducing spending "
                "in this category if it's not essential. Use DECC's budgeting tools to plan more effectively.")
    elif 1000 <= amount <= 2000:
        return (f"Your spending on {category_name} (${amount:.2f}) is moderate. Keep track of upcoming expenses "
                "to ensure you stay within budget. DECC can help you create custom visuals to analyze trends.")
    else:
        return (f"Your spending on {category_name} (${amount:.2f}) is within a healthy range. Good financial management! "
                "Use DECC's tools to continue optimizing your spending.")

selected_category = st.selectbox("Select a spending category to get insights:", df_spending["Category"].tolist())
if st.button("Get Spending Insights"):
    category_response = spending_chatbot_response(selected_category)
    st.write(category_response)
