# Transaction Analysis Project

## Overview

This project analyzes a synthetic fraud dataset to gain insights into transaction patterns across different countries and merchant categories. The main objectives of this research are:

1. Currency Conversion: Convert all transaction amounts to USD.
2. Country Spending Analysis: Determine if some countries spend more money in USD than others.
3. Category Popularity Analysis: Analyze which merchant categories are more popular in different countries.
4. Visualizations: Create modern-looking graphs to visualize the results.

### [Dataset](https://www.kaggle.com/datasets/ismetsemedov/transactions)

or use -> https://www.kaggle.com/datasets/ismetsemedov/transactions

## Technologies Used

- Python 3.x

### Backend (FastAPI)

- pandas: Data manipulation and analysis
- unicorn: HTTP web server
- functools: For caching function results

### Frontend (SPA)

- Jupyter Notebook: Interactive development environment
- Matplotlib: Basic plotting library
- Seaborn: Statistical data visualization
- Plotly: Interactive and publication-quality graphs

## How to Run the Notebook Code

1. Ensure you have Python 3.x installed on your system.
2. Clone this repository to your local machine.
3. Navigate to ipynb.
4. Open the `main.ipynb` file in Jupyter Notebook or JupyterLab.
5. Run all cells in the notebook sequentially.

## How to Run Web App.

### Option 1: use docker.

1. Ensure you have Python 3.x installed on your system.
2. On mac os you may need to add start.sh to allowed commands list.

   ```
   chmod +x ./start.sh
   ```
3. Execute start script

   ```
   ./start.sh
   ```

### Option 2: manually.

#### Frontend

1. Open new terminal.
2. Navigate to dir
   ```
   cd app/frontend
   ```
3. Start web server
   ```
   poetry run streamlit run  frontend/app.py
   ```

#### Backend

1. Open new terminal.
2. Navigate to dir
   ```
   cd app/backend
   ```
3. Start web server
   ```
   poetry run python backend
   ```

## Analysis Results

## Objectives were:

1. Country Spending Analysis: Analyze the data to determine if some countries spend more money in USD than others. (Completed ✅)
2. Category Popularity Analysis: Analyze which merchant categories are more popular in some countries compared to others. (Completed ✅)

## Hypothesis were:

1. USA and Europe regions are expected to spend more money in USD than other regions.

   Hypothesis incorrect. In fact, the most spending country was Mexico, Brazil, and Russia, respectively.
2. Most popular merchant categories in top spending counties are expected to be different from other regions that spend less money.

   Hypothesis incorrect. Most popular merchant categories in top spending countries were the same as in regions that spent less money. However, the amount of money spend on each category was larger.
3. Transaction count should be higher in countries that spend more money.

   Hypothesis incorrect. The most spending country were the ones, that covered most amount of regions, such as Europe. However, it is important to note that
   originally Europe was expected to be "country that spend more money".

## Future Work

- Implement more advanced statistical analysis techniques.
- Develop a machine learning model for fraud detection based on the insights gained.
- Create an interactive dashboard for real-time analysis of transaction data.
- Create open API to upload and download datasets.
- Use GenAI to find relative column and create graphs.
