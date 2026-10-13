from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent / "data"

FILES = {
    "sales": "fact_sales.csv",
    "customers": "dim_customers.csv",
    "products": "dim_products.csv",
    "stores": "dim_stores.csv",
    "promotions": "dim_promotions.csv",
}


def read_table(name: str) -> pd.DataFrame:
    path = DATA_DIR / FILES[name]

    if not path.is_file():
        raise FileNotFoundError(f"Missing data file: {path}")

    df = pd.read_csv(path, low_memory=False)
    df.columns = df.columns.str.strip()
    return df


def require_columns(df, columns, table_name):
    missing = set(columns) - set(df.columns)
    if missing:
        raise ValueError(
            f"{table_name} missing columns: {sorted(missing)}"
        )


def build_dataset() -> pd.DataFrame:
    sales = read_table("sales")
    customers = read_table("customers")
    products = read_table("products")
    stores = read_table("stores")

    require_columns(
        sales,
        [
            "Order_ID", "Order_Date", "Customer_ID",
            "Product_ID", "Store_ID", "Sales_Amount",
            "Profit",
        ],
        "FactSales",
    )
    require_columns(
        customers, ["Customer_ID", "Segment"], "DimCustomers"
    )
    require_columns(
        products,
        ["Product_ID", "Product_Name", "Category", "Sub_Category"],
        "DimProducts",
    )
    require_columns(stores, ["Store_ID"], "DimStores")

    sales["Sales_Amount"] = pd.to_numeric(
        sales["Sales_Amount"], errors="coerce"
    )
    sales["Profit"] = pd.to_numeric(
        sales["Profit"], errors="coerce"
    )
    sales["Order_Date"] = pd.to_datetime(
        sales["Order_Date"], errors="coerce"
    , format="%d-%m-%Y")

    if sales[["Sales_Amount", "Profit", "Order_Date"]].isna().any().any():
        raise ValueError(
            "Invalid sales, profit, or order date values found."
        )

    if sales["Order_ID"].isna().any():
        raise ValueError("Missing Order_ID values found.")

    customer_cols = ["Customer_ID", "Segment"]
    product_cols = [
        "Product_ID", "Product_Name", "Category", "Sub_Category"
    ]

    # FactSales already contains Region in the validated dataset.
    # Prefer that field to avoid Region_x / Region_y collisions.
    store_cols = ["Store_ID"]
    if "Store_Name" in stores.columns:
        store_cols.append("Store_Name")
    if "Region" not in sales.columns and "Region" in stores.columns:
        store_cols.append("Region")

    df = (
        sales.merge(
            customers[customer_cols],
            on="Customer_ID",
            how="left",
            validate="many_to_one",
        )
        .merge(
            products[product_cols],
            on="Product_ID",
            how="left",
            validate="many_to_one",
        )
        .merge(
            stores[store_cols],
            on="Store_ID",
            how="left",
            validate="many_to_one",
        )
    )

    if len(df) != len(sales):
        raise ValueError("Joining tables changed the row count.")

    for key, column in [
        ("Customer_ID", "Segment"),
        ("Product_ID", "Category"),
    ]:
        if df.loc[df[key].notna(), column].isna().any():
            raise ValueError(f"Missing dimension matches for {key}")

    if "Region" not in df.columns:
        df["Region"] = "Unknown"

    df["Year"] = df["Order_Date"].dt.year.astype("int64")
    df["Year_Month"] = df["Order_Date"].dt.strftime("%Y-%m")

    for col in [
        "Segment", "Category", "Sub_Category",
        "Product_Name", "Region",
    ]:
        df[col] = df[col].fillna("Unknown").astype("category")

    return df
