import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

df: pd.DataFrame = pd.read_csv("processed_data.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601', errors='coerce')
print("Dataset loaded successfully")

def filter_df_by_date(df, start_date, end_date):
    try:
        start_date = pd.to_datetime(start_date).tz_localize(None)
        end_date = pd.to_datetime(end_date).tz_localize(None)
        df['timestamp'] = df['timestamp'].dt.tz_localize(None)
        return df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
    except Exception as e:
        raise ValueError(f"Error filtering data: {str(e)}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Transaction Analysis API"}

@app.get("/dates_range")
async def get_dates_range():
    try:
        min_date = df['timestamp'].min().strftime('%Y-%m-%d')
        max_date = df['timestamp'].max().strftime('%Y-%m-%d')
        return {"min_date": min_date, "max_date": max_date}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/transactions_per_country")
async def get_transactions_per_country(start_date: str, end_date: str):
    try:
        filtered_df = filter_df_by_date(df, start_date, end_date)
        transactions_per_country = filtered_df['country'].value_counts().reset_index()
        transactions_per_country.columns = ['country', 'transaction_count']

        fig = px.choropleth(transactions_per_country,
                            locations="country",
                            locationmode="country names",
                            color="transaction_count",
                            hover_name="country",
                            color_continuous_scale=px.colors.sequential.Plasma,
                            title="Number of Transactions per Country",
                            labels={'transaction_count': 'Number of Transactions'})

        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            ),
            height=600,
            margin={"r":0,"t":40,"l":0,"b":0}
        )

        img_bytes = fig.to_image(format="png")
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return {"image": img_base64}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/country_spending")
async def get_country_spending(start_date: str, end_date: str):
    try:
        filtered_df = filter_df_by_date(df, start_date, end_date)
        country_spending = filtered_df.groupby('country')['amount_usd'].sum().reset_index().sort_values(by='amount_usd', ascending=False)
        fig = px.bar(country_spending, x='country', y='amount_usd',
                     title=f'Total Spending per Country in USD ({start_date} to {end_date})',
                     labels={'country': 'Country', 'amount_usd': 'Total Spending (USD)'},
                     color='amount_usd', color_continuous_scale=px.colors.sequential.Viridis)
        fig.update_layout(xaxis_tickangle=-45)

        img_bytes = fig.to_image(format="png")
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return {"image": img_base64}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/category_popularity")
async def get_category_popularity(start_date: str, end_date: str):
    try:
        filtered_df = filter_df_by_date(df, start_date, end_date)
        category_spending = filtered_df.groupby(['country', 'merchant_category'])['amount_usd'].sum().reset_index()
        category_spending = category_spending.sort_values(['country', 'amount_usd'], ascending=[True, False])
        top_categories = category_spending.groupby('country').head(5)

        fig = px.bar(top_categories, x='country', y='amount_usd', color='merchant_category',
                     title=f'Top 5 Merchant Categories by Country ({start_date} to {end_date})',
                     labels={'amount_usd': 'Total Amount (USD)', 'country': 'Country', 'merchant_category': 'Merchant Category'},
                     height=500)
        fig.update_layout(xaxis_tickangle=-45, barmode='stack')

        img_bytes = fig.to_image(format="png")
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return {"image": img_base64}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/avg_transaction")
async def get_avg_transaction(start_date: str, end_date: str):
    try:
        filtered_df = filter_df_by_date(df, start_date, end_date)
        avg_transaction = filtered_df.groupby('country')['amount_usd'].mean().reset_index()
        fig = px.scatter(avg_transaction, x='country', y='amount_usd', size='amount_usd', color='amount_usd',
                         title=f'Average Transaction Amount by Country ({start_date} to {end_date})',
                         labels={'country': 'Country', 'amount_usd': 'Average Transaction Amount (USD)'},
                         color_continuous_scale=px.colors.sequential.Plasma)
        fig.update_layout(xaxis_tickangle=-45)

        img_bytes = fig.to_image(format="png")
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return {"image": img_base64}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/currency_distribution")
async def get_currency_distribution(start_date: str, end_date: str):
    try:
        filtered_df = filter_df_by_date(df, start_date, end_date)
        currency_count = filtered_df['currency'].value_counts().reset_index()
        currency_count.columns = ['currency', 'count']
        fig = px.pie(currency_count, values='count', names='currency',
                     title=f'Transaction Count by Currency ({start_date} to {end_date})')

        img_bytes = fig.to_image(format="png")
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return {"image": img_base64}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/category_heatmap")
async def get_category_heatmap(start_date: str, end_date: str):
    try:
        filtered_df = filter_df_by_date(df, start_date, end_date)
        heatmap_data = filtered_df.groupby(['country', 'merchant_category']).size().reset_index(name='count')
        heatmap_pivot = heatmap_data.pivot(index='country', columns='merchant_category', values='count').fillna(0)

        fig = px.imshow(heatmap_pivot,
                        labels=dict(x="Merchant Category", y="Country", color="Transaction Count"),
                        x=heatmap_pivot.columns,
                        y=heatmap_pivot.index,
                        aspect="auto",
                        title=f"Heatmap of Transaction Counts by Country and Merchant Category ({start_date} to {end_date})")
        fig.update_xaxes(side="top")

        img_bytes = fig.to_image(format="png")
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return {"image": img_base64}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/top_currencies")
async def get_top_currencies(start_date: str, end_date: str):
    try:
        filtered_df = filter_df_by_date(df, start_date, end_date)
        currency_counts = filtered_df['currency'].value_counts()

        fig = go.Figure(data=[go.Bar(x=currency_counts.index, y=currency_counts.values)])
        fig.update_layout(
            title=f'Top Currencies by Transaction Count ({start_date} to {end_date})',
            xaxis_title='Currency',
            yaxis_title='Number of Transactions',
            height=400
        )

        img_bytes = fig.to_image(format="png")
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return {"image": img_base64}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=6969)
