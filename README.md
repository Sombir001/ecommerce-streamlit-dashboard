# 📊 E-Commerce Sales Analytics Dashboard

### Python | Pandas | Plotly | Streamlit | Data Analytics

An interactive, end-to-end e-commerce analytics web application developed using **Python, Pandas, Plotly, and Streamlit**.

The project analyzes **600,000 sales transactions from 2021 to 2024**, transforming raw transactional data into actionable business insights through interactive visualizations, validated KPIs, and dynamic filtering.

This application builds upon my independently developed [Power BI E-Commerce Dashboard](https://github.com/Sombir001/ecommerce-powerbi-dashboard), extending the analysis into a Python-powered web application.

## 🚀 Live Interactive Dashboard

### [▶ Click Here to Explore the Live Dashboard](https://sombir-ecommerce-analytics.streamlit.app/)

**Live URL:** https://sombir-ecommerce-analytics.streamlit.app/

Explore sales trends, profitability, product performance, customer segments, and regional insights directly in your browser.

**No installation, Google Colab, or manual dataset extraction required.**

## 🎯 Project Objectives

- Analyze overall e-commerce sales and profitability.
- Monitor key business performance indicators.
- Identify sales trends across months and years.
- Evaluate product and category performance.
- Understand customer segment contributions.
- Compare regional business performance.
- Build a user-friendly interactive analytics application.
- Demonstrate a reproducible Python analytics workflow.

## 📈 Validated Business KPIs

| Business Metric | Value |
|---|---:|
| Total Sales | 1,531,256,652.62 |
| Total Profit | 299,889,886.78 |
| Total Orders | 600,000 |
| Profit Margin | 19.58% |
| Analysis Period | 2021–2024 |
| Monthly Periods | 48 |

These baseline metrics were validated against the corresponding Power BI analysis.

## 🖥️ Dashboard Features

### 1. Executive Overview

- Total Sales, Total Profit, Total Orders, and Profit Margin KPI cards
- Monthly sales performance trends
- Yearly sales versus profit comparisons
- Sales distribution by product category
- Customer segment contribution analysis

### 2. Product Intelligence

- Top-performing products by sales
- Product profitability comparisons
- Sales and profit relationships
- Product-level performance analysis

### 3. Customer & Category Analysis

- Customer segment performance
- Product category comparisons
- Regional sales and profitability insights
- Interactive business performance visualizations

### 4. Data Explorer

- Filtered transactional data preview
- Interactive data exploration
- Downloadable CSV results

### Interactive Filters

Users can dynamically filter dashboard results by:

- Year
- Region
- Product Category
- Customer Segment

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data loading, cleaning, transformation, and aggregation |
| Plotly | Interactive business visualizations |
| Streamlit | Dashboard interface and web application |
| GitHub | Source code hosting and version control |
| Streamlit Community Cloud | Live application deployment |

## 📁 Project Structure

```text
ecommerce-streamlit-dashboard/
│
├── app.py
├── analytics.py
├── data_loader.py
├── launcher.py
├── requirements.txt
├── README.md
├── data.zip
│
└── .streamlit/
    └── config.toml
```

### File Descriptions

| File | Description |
|---|---|
| `app.py` | Main Streamlit dashboard, navigation, filters, and visualizations |
| `analytics.py` | KPI calculations, aggregation functions, and analytical logic |
| `data_loader.py` | Data loading, validation, and preparation |
| `launcher.py` | Automatically prepares compressed datasets and launches the dashboard |
| `data.zip` | Compressed source CSV datasets |
| `requirements.txt` | Required Python dependencies |
| `.streamlit/config.toml` | Streamlit dashboard theme configuration |

## 📂 Dataset Information

The project uses five related datasets:

| Dataset | Purpose |
|---|---|
| `fact_sales.csv` | Transaction-level sales and profit records |
| `dim_customers.csv` | Customer attributes and segments |
| `dim_products.csv` | Product names and categories |
| `dim_stores.csv` | Store and regional information |
| `dim_promotions.csv` | Promotion-related information |

The sales dataset contains approximately **600,000 transaction records**.

Because the original sales CSV exceeds GitHub's browser upload limit for individual files, the datasets are packaged inside `data.zip`.

The `launcher.py` file automatically extracts the required CSV files into the appropriate directory before starting the dashboard.

**Visitors do not need to manually extract the ZIP file.**

## ▶️ How to Run the Project Locally

### Step 1 — Clone the GitHub repository

```bash
git clone https://github.com/Sombir001/ecommerce-streamlit-dashboard.git
cd ecommerce-streamlit-dashboard
```

### Step 2 — Install Python dependencies

Python and pip must be installed on your system.

```bash
python -m pip install -r requirements.txt
```

### Step 3 — Launch the dashboard

```bash
streamlit run launcher.py
```

The launcher will:

1. Locate the compressed dataset (`data.zip`).
2. Extract the required CSV files into the `data/` directory.
3. Start the existing Streamlit dashboard.

### Step 4 — Open the dashboard

Streamlit will display a local URL, typically:

`http://localhost:8501`

Open this URL in your browser to explore the dashboard.

**Alternatively, use the [Live Dashboard](https://sombir-ecommerce-analytics.streamlit.app/) without any local setup.**

## 🔍 Data Validation and Analytical Workflow

### Phase 1 — Data Preparation and Validation

- Loaded sales and dimension datasets using Pandas.
- Validated required columns and relationships.
- Checked customer, product, and store keys.
- Converted transaction dates using the `DD-MM-YYYY` format.
- Prepared the analytical dataset for downstream analysis.

### Phase 2 — Business Analytics

- Calculated total sales, profit, order count, and profit margin.
- Aggregated monthly and yearly business performance.
- Analyzed product, category, customer segment, and regional performance.
- Developed reusable analytical functions.
- Validated baseline metrics against the Power BI project.

### Phase 3 — Interactive Dashboard Development

- Developed the Streamlit application.
- Created interactive Plotly visualizations.
- Implemented dynamic sidebar filters.
- Added multiple dashboard sections.
- Enabled filtered data exploration and CSV downloads.

### Phase 4 — Deployment

- Organized the project into reusable Python modules.
- Packaged large CSV datasets into a compressed archive.
- Added automatic dataset preparation through `launcher.py`.
- Hosted the source code on GitHub.
- Deployed the application using Streamlit Community Cloud.

## 💡 Skills Demonstrated

- Python programming
- Data cleaning and transformation
- Relational data modeling
- Data validation
- Exploratory data analysis
- Business KPI development
- Interactive data visualization
- Dashboard development
- Modular Python project organization
- GitHub project documentation
- Web application deployment

## 🔗 Related Project

### [Power BI E-Commerce Dashboard](https://github.com/Sombir001/ecommerce-powerbi-dashboard)

The Power BI project explores the same e-commerce business domain through interactive reporting and KPI analysis.

This Streamlit application demonstrates how similar business analytics can be implemented using Python and deployed as a browser-based application.

## 👤 Author

**Sombir**

- [GitHub Profile](https://github.com/Sombir001)
- [Live E-Commerce Analytics Dashboard](https://sombir-ecommerce-analytics.streamlit.app/)

---

**If you find this project useful, consider giving the repository a star!**
