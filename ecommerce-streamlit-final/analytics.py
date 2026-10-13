import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict:
    sales = float(df["Sales_Amount"].sum())
    profit = float(df["Profit"].sum())
    orders = int(df["Order_ID"].nunique())

    return {
        "sales": sales,
        "profit": profit,
        "orders": orders,
        "margin": profit / sales * 100 if sales else 0.0,
    }


def apply_filters(
    df: pd.DataFrame,
    years=None,
    regions=None,
    categories=None,
    segments=None,
) -> pd.DataFrame:
    mask = pd.Series(True, index=df.index)

    filters = {
        "Year": years,
        "Region": regions,
        "Category": categories,
        "Segment": segments,
    }

    for column, selected in filters.items():
        if selected is not None:
            mask &= df[column].isin(selected)

    return df.loc[mask]


def monthly_performance(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby("Year_Month", observed=True)
        .agg(
            Sales=("Sales_Amount", "sum"),
            Profit=("Profit", "sum"),
        )
        .reset_index()
        .sort_values("Year_Month")
    )
    return result


def yearly_performance(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Year", observed=True)
        .agg(
            Sales=("Sales_Amount", "sum"),
            Profit=("Profit", "sum"),
        )
        .reset_index()
        .sort_values("Year")
    )


def dimension_performance(
    df: pd.DataFrame, dimension: str
) -> pd.DataFrame:
    if dimension not in {"Category", "Segment", "Region"}:
        raise ValueError(f"Unsupported dimension: {dimension}")

    result = (
        df.groupby(dimension, observed=True)
        .agg(
            Sales=("Sales_Amount", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
        )
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    result["Margin %"] = (
        result["Profit"]
        .div(result["Sales"].replace(0, float("nan")))
        .mul(100)
        .fillna(0)
    )
    return result


def product_performance(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.groupby(
            ["Product_ID", "Product_Name"], observed=True
        )
        .agg(
            Sales=("Sales_Amount", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
        )
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    result["Margin %"] = (
        result["Profit"]
        .div(result["Sales"].replace(0, float("nan")))
        .mul(100)
        .fillna(0)
    )
    return result


def format_compact(value: float) -> str:
    magnitude = abs(value)

    if magnitude >= 1_000_000_000:
        return f"{value / 1_000_000_000:,.2f}B"
    if magnitude >= 1_000_000:
        return f"{value / 1_000_000:,.2f}M"
    if magnitude >= 1_000:
        return f"{value / 1_000:,.1f}K"
    return f"{value:,.2f}"
