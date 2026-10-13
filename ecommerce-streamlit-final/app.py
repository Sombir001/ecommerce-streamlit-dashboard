import io

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from analytics import (
    apply_filters,
    calculate_kpis,
    dimension_performance,
    format_compact,
    monthly_performance,
    product_performance,
    yearly_performance,
)
from data_loader import build_dataset


NAVY = "#142D4E"
TEAL = "#168C91"
GOLD = "#E6A23C"
SLATE = "#526579"
BACKGROUND = "#F4F7FB"

st.set_page_config(
    page_title="E-Commerce Analytics | Python",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F4F7FB;
    }
    [data-testid="stSidebar"] {
        background-color: #142D4E;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #142D4E;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3 {
        color: #142D4E;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF;
    }

    /* Sidebar navigation and filter labels */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #FFFFFF !important;
    }

    /* Keep text readable inside light-colored filter inputs */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        color: #142D4E;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] input {
        color: #142D4E !important;
    }

    .hero {
        background: linear-gradient(110deg, #142D4E, #245478);
        color: white;
        padding: 26px 30px;
        border-radius: 16px;
        margin-bottom: 20px;
    }
    .hero h1 {
        color: white;
        font-size: 2rem;
        margin: 0 0 6px 0;
    }
    .hero p {
        color: #D8E7F2;
        margin: 0;
    }
    .metric-card {
        background: white;
        border: 1px solid #E5EBF2;
        border-radius: 14px;
        padding: 20px;
        min-height: 115px;
        box-shadow: 0 3px 12px rgba(20, 45, 78, 0.04);
    }
    .metric-label {
        color: #526579;
        font-size: 0.85rem;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #142D4E;
        font-size: 1.7rem;
        font-weight: 750;
    }
    .section-title {
        color: #142D4E;
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Loading sales data...")
def load_data():
    return build_dataset()


@st.cache_data(show_spinner=False)
def csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def style_chart(fig, height=380):
    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=NAVY),
        margin=dict(l=20, r=20, t=40, b=30),
        legend_title_text="",
        hovermode="closest",
    )
    return fig


def show_kpi(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_no_data():
    st.warning(
        "No records match the selected filters. "
        "Change one or more sidebar selections."
    )


try:
    data = load_data()
except (FileNotFoundError, ValueError, pd.errors.ParserError) as exc:
    st.error(f"Unable to load dashboard data: {exc}")
    st.stop()


# Sidebar navigation and filters
with st.sidebar:
    st.title("📊 E-Commerce")
    st.caption("Analytics Control Center")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Product Intelligence",
            "Customer & Category",
            "Data Explorer",
        ],
    )

    st.divider()
    st.subheader("Filters")

    def options_for(column):
        return sorted(data[column].dropna().unique().tolist())

    years = st.multiselect(
        "Year",
        options=options_for("Year"),
        default=options_for("Year"),
    )
    regions = st.multiselect(
        "Region",
        options=options_for("Region"),
        default=options_for("Region"),
    )
    categories = st.multiselect(
        "Category",
        options=options_for("Category"),
        default=options_for("Category"),
    )
    segments = st.multiselect(
        "Customer Segment",
        options=options_for("Segment"),
        default=options_for("Segment"),
    )

    st.divider()
    st.caption("Built with Python · Pandas · Plotly · Streamlit")


filtered = apply_filters(
    data,
    years=years,
    regions=regions,
    categories=categories,
    segments=segments,
)

st.markdown(
    """
    <div class="hero">
        <h1>E-Commerce Sales Analytics</h1>
        <p>Interactive Business Intelligence | 2021–2024</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if filtered.empty:
    show_no_data()
    st.stop()

kpis = calculate_kpis(filtered)

col1, col2, col3, col4 = st.columns(4)

with col1:
    show_kpi("TOTAL SALES", format_compact(kpis["sales"]))
with col2:
    show_kpi("TOTAL PROFIT", format_compact(kpis["profit"]))
with col3:
    show_kpi("TOTAL ORDERS", f'{kpis["orders"]:,}')
with col4:
    show_kpi("PROFIT MARGIN", f'{kpis["margin"]:.2f}%')

st.write("")
st.caption(
    f"Showing {len(filtered):,} sales records "
    f"across {kpis['orders']:,} distinct orders."
)


if page == "Executive Overview":
    st.markdown(
        '<div class="section-title">Sales Performance</div>',
        unsafe_allow_html=True,
    )

    monthly = monthly_performance(filtered)
    yearly = yearly_performance(filtered)

    left, right = st.columns([1.5, 1])

    with left:
        fig = px.line(
            monthly,
            x="Year_Month",
            y="Sales",
            markers=True,
            title="Monthly Sales Trend",
            color_discrete_sequence=[TEAL],
        )
        fig.update_xaxes(
            title=None,
            type="category",
            categoryorder="array",
            categoryarray=monthly["Year_Month"].tolist(),
            nticks=12,
        )
        fig.update_yaxes(title="Sales")
        st.plotly_chart(style_chart(fig), use_container_width=True)

    with right:
        fig = px.bar(
            yearly,
            x="Year",
            y=["Sales", "Profit"],
            barmode="group",
            title="Sales vs Profit by Year",
            color_discrete_map={"Sales": TEAL, "Profit": GOLD},
        )
        fig.update_xaxes(type="category", title=None)
        fig.update_yaxes(title="Amount")
        st.plotly_chart(style_chart(fig), use_container_width=True)

    left, right = st.columns(2)

    with left:
        category = dimension_performance(filtered, "Category")
        fig = px.bar(
            category.sort_values("Sales"),
            x="Sales",
            y="Category",
            orientation="h",
            title="Sales by Category",
            color_discrete_sequence=[TEAL],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

    with right:
        segment = dimension_performance(filtered, "Segment")
        fig = px.pie(
            segment,
            names="Segment",
            values="Sales",
            hole=0.62,
            title="Sales by Customer Segment",
            color_discrete_sequence=[TEAL, GOLD, NAVY],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

    st.subheader("Top 15 Products")
    top15 = product_performance(filtered).head(15)

    st.dataframe(
        top15[
            ["Product_Name", "Sales", "Profit", "Orders", "Margin %"]
        ],
        hide_index=True,
        use_container_width=True,
        column_config={
            "Sales": st.column_config.NumberColumn(
                "Sales", format="%.2f"
            ),
            "Profit": st.column_config.NumberColumn(
                "Profit", format="%.2f"
            ),
            "Margin %": st.column_config.NumberColumn(
                "Margin %", format="%.2f%%"
            ),
        },
    )


elif page == "Product Intelligence":
    st.subheader("Product Performance & Profitability")

    products = product_performance(filtered)
    top_n = st.slider(
        "Number of products to display",
        min_value=5,
        max_value=30,
        value=15,
        step=5,
    )

    left, right = st.columns(2)

    with left:
        top = products.head(top_n).sort_values("Sales")
        fig = px.bar(
            top,
            x="Sales",
            y="Product_Name",
            orientation="h",
            title=f"Top {top_n} Products by Sales",
            color_discrete_sequence=[TEAL],
        )
        st.plotly_chart(
            style_chart(fig, height=520),
            use_container_width=True,
        )

    with right:
        fig = px.scatter(
            products,
            x="Sales",
            y="Profit",
            hover_name="Product_Name",
            color="Margin %",
            color_continuous_scale="Teal",
            title="Product Sales vs Profit",
        )
        st.plotly_chart(
            style_chart(fig, height=520),
            use_container_width=True,
        )

    st.subheader("Detailed Product Rankings")
    st.dataframe(
        products,
        hide_index=True,
        use_container_width=True,
    )

    st.download_button(
        "Download Product Analysis",
        data=csv_bytes(products),
        file_name="product_performance.csv",
        mime="text/csv",
    )


elif page == "Customer & Category":
    st.subheader("Customer Segments & Business Categories")

    left, right = st.columns(2)

    with left:
        segment = dimension_performance(filtered, "Segment")
        fig = px.bar(
            segment,
            x="Segment",
            y="Sales",
            color="Segment",
            title="Revenue by Customer Segment",
            color_discrete_sequence=[TEAL, GOLD, NAVY],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.dataframe(
            segment,
            hide_index=True,
            use_container_width=True,
        )

    with right:
        category = dimension_performance(filtered, "Category")
        fig = px.bar(
            category,
            x="Category",
            y="Profit",
            color="Category",
            title="Profit by Product Category",
            color_discrete_sequence=[TEAL, GOLD, NAVY],
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.dataframe(
            category,
            hide_index=True,
            use_container_width=True,
        )

    st.subheader("Regional Performance")
    region = dimension_performance(filtered, "Region")

    fig = px.bar(
        region.sort_values("Sales"),
        x="Sales",
        y="Region",
        orientation="h",
        title="Sales by Region",
        color_discrete_sequence=[TEAL],
    )
    st.plotly_chart(style_chart(fig), use_container_width=True)

    st.dataframe(
        region,
        hide_index=True,
        use_container_width=True,
    )


elif page == "Data Explorer":
    st.subheader("Explore Filtered Sales Records")
    st.info(
        "Use the sidebar filters to explore transactions. "
        "The table preview is limited for browser performance."
    )

    visible_columns = [
        column
        for column in [
            "Order_ID",
            "Order_Date",
            "Year",
            "Region",
            "Segment",
            "Category",
            "Product_Name",
            "Sales_Amount",
            "Profit",
        ]
        if column in filtered.columns
    ]

    preview_size = st.select_slider(
        "Rows to preview",
        options=[25, 50, 100, 250, 500],
        value=100,
    )

    st.dataframe(
        filtered[visible_columns].head(preview_size),
        hide_index=True,
        use_container_width=True,
    )

    st.subheader("Download Analysis")

    summary = product_performance(filtered)

    st.download_button(
        "Download Filtered Product Summary",
        data=csv_bytes(summary),
        file_name="filtered_product_summary.csv",
        mime="text/csv",
    )

    # Prepare a smaller transaction export to reduce memory use
    # and prevent large browser downloads.
    export_limit = 100_000
    export_df = filtered[visible_columns].head(export_limit)

    st.download_button(
        f"Download Transactions (up to {export_limit:,} rows)",
        data=csv_bytes(export_df),
        file_name="filtered_transactions.csv",
        mime="text/csv",
    )

    if len(filtered) > export_limit:
        st.caption(
            "The transaction export is limited to the first "
            f"{export_limit:,} matching rows."
        )


st.divider()
st.caption(
    "E-Commerce Analytics Portfolio | "
    "Python · Pandas · Streamlit · Plotly | "
    "Metrics validated against Power BI"
)
