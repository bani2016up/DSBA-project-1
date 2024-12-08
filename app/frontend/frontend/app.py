import os
import streamlit as st
import requests
from PIL import Image
import io
import base64
from datetime import datetime, timedelta

st.set_page_config(page_title="Transaction Analysis Dashboard", layout="wide")


API_URL = os.getenv('API_URL', 'http://localhost:6969')

def get_date_range():
    response = requests.get(f"{API_URL}/dates_range")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch date range from the API")
        return None

def get_image_from_api(endpoint, start_date, end_date_str):
    params = {}
    if start_date and end_date:
        params['start_date'] = start_date
        params['end_date'] = end_date
    response = requests.get(f"{API_URL}/{endpoint}", params=params)
    if response.status_code == 200:
        img_data = base64.b64decode(response.json()["image"])
        return Image.open(io.BytesIO(img_data))
    else:
        st.error(f"Failed to fetch image from {endpoint}")
        return None

date_range = get_date_range()
if not date_range:
    st.error("Failed to fetch date range from the API")
    st.stop()

min_date = datetime.strptime(date_range['min_date'], '%Y-%m-%d').date()
max_date = datetime.strptime(date_range['max_date'], '%Y-%m-%d').date()

# Add date range selector to sidebar
st.sidebar.header("Date Range Filter")
start_date = st.sidebar.date_input("Start date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End date", max_date, min_value=min_date, max_value=max_date)

st.sidebar.header("Currency Converter")
amount = st.sidebar.number_input("Amount", min_value=0.001, value=1.0, step=0.01)
from_currency = st.sidebar.text_input("From Currency (e.g., EUR, GBP)", max_chars=3).upper()
if st.sidebar.button("Convert to USD"):
    if from_currency:
        try:
            response = requests.post(f"{API_URL}/convert_to_usd",
                                     json={"amount": amount, "from_currency": from_currency})
            if response.status_code == 200:
                result = response.json()
                st.sidebar.success(f"{amount} {from_currency} = {result['amount_usd']} USD")
            else:
                st.sidebar.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.sidebar.error(f"Error: {str(e)}")
    else:
        st.sidebar.warning("Please enter a valid currency code.")

# Convert dates to string format
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

st.title("Transaction Analysis Dashboard")

st.markdown(
    "[View on GitHub](https://github.com/bani2016up/DSBA-project-1)",
    unsafe_allow_html=True
)

st.header("Objectives")
st.write("""
1. Country Spending Analysis: Analyze the data to determine if some countries spend more money in USD than others.
2. Category Popularity Analysis: Analyze which merchant categories are more popular in some countries compared to others.
""")

st.header("Hypotheses")
hypotheses = [
    {
        "statement": "USA and Europe regions are expected to spend more money in USD than other regions.",
        "result": "Hypothesis incorrect. In fact, the most spending country was Mexico, Brazil, and Russia, respectively."
    },
    {
        "statement": "Most popular merchant categories in top spending counties are expected to be different from other regions that spend less money.",
        "result": "Hypothesis incorrect. Most popular merchant categories in top spending countries were the same as in regions that spent less money. However, the amount of money spent on each category was larger."
    },
    {
        "statement": "Transaction count should be higher in countries that spend more money.",
        "result": "Hypothesis incorrect. The most spending countries were the ones that covered most amount of regions, such as Europe. However, it is important to note that originally Europe was expected to be a 'country that spends more money'."
    }
]

for idx, hypothesis in enumerate(hypotheses, 1):
    st.subheader(f"Hypothesis {idx}")
    st.write(f"**Statement:** {hypothesis['statement']}")
    st.write(f"**Result:** {hypothesis['result']}")

st.header("Analysis Results")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Transactions per Country")
    transactions_map = get_image_from_api("transactions_per_country", start_date_str, end_date_str)
    if transactions_map:
        st.image(transactions_map, use_container_width=True)
    st.write("This map shows the distribution of transactions across different countries.")

with col2:
    st.subheader("Total Spending per Country")
    country_spending = get_image_from_api("country_spending", start_date_str, end_date_str)
    if country_spending:
        st.image(country_spending, use_container_width=True)
    st.write("This bar chart displays the total spending in USD for each country.")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Top 5 Merchant Categories by Country")
    category_popularity = get_image_from_api("category_popularity", start_date_str, end_date_str)
    if category_popularity:
        st.image(category_popularity, use_container_width=True)
    st.write("This stacked bar chart shows the top 5 merchant categories by total amount spent in USD for each country.")

with col4:
    st.subheader("Average Transaction Amount by Country")
    avg_transaction = get_image_from_api("avg_transaction", start_date_str, end_date_str)
    if avg_transaction:
        st.image(avg_transaction, use_container_width=True)
    st.write("This scatter plot illustrates the average transaction amount in USD for each country.")

col5, col6 = st.columns(2)

with col5:
    st.subheader("Transaction Count by Currency")
    currency_distribution = get_image_from_api("currency_distribution", start_date_str, end_date_str)
    if currency_distribution:
        st.image(currency_distribution, use_container_width=True)
    st.write("This pie chart shows the distribution of transactions across different currencies.")

with col6:
    st.subheader("Top Currencies by Transaction Count")
    top_currencies = get_image_from_api("top_currencies", start_date_str, end_date_str)
    if top_currencies:
        st.image(top_currencies, use_container_width=True)
    st.write("This bar chart displays the most frequently used currencies in transactions.")

col7, col8 = st.columns(2)

with col7:
    st.subheader("Heatmap of Transaction Counts by Country and Merchant Category")
    category_heatmap = get_image_from_api("category_heatmap", start_date_str, end_date_str)
    if category_heatmap:
        st.image(category_heatmap, use_container_width=True)
    st.write("This heatmap visualizes the transaction counts for each combination of country and merchant category.")

st.header("Conclusions")
st.write("""
Based on our analysis, we can draw the following conclusions:

1. Contrary to our initial hypothesis, the countries with the highest spending were Mexico, Brazil, and Russia, not the USA or European countries.
2. The most popular merchant categories were similar across both high-spending and low-spending countries, but the amount spent in each category was larger in high-spending countries.
3. Transaction count was not directly correlated with total spending. Some countries with fewer transactions had higher total spending due to larger transaction amounts.
4. The distribution of transactions and spending across countries and categories provides valuable insights for businesses looking to expand or focus their operations in specific regions or markets.
5. Currency usage varied significantly across transactions, which could have implications for currency exchange and international business strategies.

These findings challenge some common assumptions about global spending patterns and highlight the importance of data-driven decision-making in international business and finance.
""")

st.header("Future Work")
st.write("""
To further enhance our analysis and insights, we propose the following future work:

1. Implement more advanced statistical analysis techniques to uncover deeper patterns and correlations in the data.
2. Develop a machine learning model for fraud detection based on the insights gained from this analysis.
3. Create an interactive dashboard that allows users to explore the data in real-time and customize visualizations based on specific criteria.
4. Integrate additional data sources, such as economic indicators or demographic information, to provide more context to the transaction patterns.
5. Conduct a time-series analysis to identify trends and seasonality in spending patterns across different countries and categories.
6. Investigate the factors contributing to the unexpected high spending in countries like Mexico, Brazil, and Russia.
7. Analyze the relationship between currency exchange rates and spending patterns in different countries.
8. Develop predictive models to forecast future spending trends based on historical data and external factors.
""")
