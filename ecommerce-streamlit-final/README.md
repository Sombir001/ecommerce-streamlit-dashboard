# E-Commerce Analytics Web App

An interactive analytics application built using Python, Pandas,
Plotly, and Streamlit.

## Project Overview

This project extends an independently developed Power BI
e-commerce dashboard into a browser-based analytics application.

It analyzes approximately 600,000 sales transactions across
2021–2024.

## Key Features

- Executive sales, profit, order, and margin KPIs
- Interactive Year, Region, Category, and Segment filters
- Monthly and annual performance trends
- Product sales and profitability analysis
- Customer segment and category analysis
- Regional performance analysis
- Filtered data explorer and CSV downloads

## Validated Business Metrics

| Metric | Value |
|---|---:|
| Total Sales | 1,531,256,652.62 |
| Total Profit | 299,889,886.78 |
| Total Orders | 600,000 |
| Profit Margin | 19.58% |

These baseline metrics were validated against the Power BI project.

## Technology Stack

- Python
- Pandas
- Plotly
- Streamlit
- GitHub

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Place the five required CSV files in the `data/` directory.

Launch the app:

```bash
streamlit run app.py
```

## Data Requirements

Required files:

- `fact_sales.csv`
- `dim_customers.csv`
- `dim_products.csv`
- `dim_stores.csv`
- `dim_promotions.csv`

Only share data publicly if you have permission to do so.

## Related Project

[Power BI E-Commerce Dashboard](https://github.com/Sombir001/ecommerce-powerbi-dashboard)

## Author

Sombir

[GitHub Portfolio](https://github.com/Sombir001)
