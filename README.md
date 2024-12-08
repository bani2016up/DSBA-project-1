# Transaction Analysis Project

## Overview

This project analyzes a synthetic fraud dataset to gain insights into transaction patterns across different countries and merchant categories. The main objectives of this research are:

1. Currency Conversion: Convert all transaction amounts to USD.
2. Country Spending Analysis: Determine if some countries spend more money in USD than others.
3. Category Popularity Analysis: Analyze which merchant categories are more popular in different countries.
4. Visualizations: Create modern-looking graphs to visualize the results.

## Technologies Used

- Python 3.x

### Backend (FastAPI)

- pandas: Data manipulation and analysis
- requests: HTTP library for API calls
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

1. Ensure you have Python 3.x installed on your system.
2. On mac os you may need to add start.sh to allowed commands list.

   ```
   chmod +x ./start.sh
   ```
3. Execute start script

   ```
   ./start.sh
   ```

## Analysis Results

The analysis revealed several interesting insights:

1. Currency Conversion: All transaction amounts were successfully converted to USD using real-time exchange rates.
2. Country Spending Analysis:

- The analysis showed significant variations in total spending across different countries.
- A bar chart and an interactive Plotly visualization were created to illustrate these differences.

3. Category Popularity Analysis:

- The top 5 merchant categories for each country were identified and visualized.
- A stacked bar chart was created to show the distribution of popular categories across countries.

4. Additional Visualizations:

- Average Transaction Amount by Country: A scatter plot showing the average transaction amount for each country.
- Transaction Count by Currency: A pie chart illustrating the distribution of transactions across different currencies.
- Heatmap of Transaction Counts: A complex visualization showing the relationship between countries, merchant categories, and transaction counts.
- Top Currencies by Transaction Count: A bar chart displaying the most frequently used currencies in the dataset.

These visualizations provide valuable insights into spending patterns, popular merchant categories, and currency usage across different countries, which can be useful for fraud detection and business strategy development.

## Future Work

- Implement more advanced statistical analysis techniques.
- Develop a machine learning model for fraud detection based on the insights gained.
- Create an interactive dashboard for real-time analysis of transaction data.
- Create open API to upload and download datasets.
- Use GenAI to find relative column and create graphs.
