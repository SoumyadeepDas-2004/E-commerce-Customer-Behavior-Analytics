import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter


def product_performance_analysis(df):
    """
    Analyze product performance including revenue contribution,
    Pareto analysis, and frequently bought together products.
    """

    # Revenue column
    df['Revenue'] = df['Quantity'] * df['UnitPrice']

    # -------------------------------
    # 1️⃣ Top 20 Products by Revenue
    # -------------------------------
    product_revenue = (
        df.groupby(['StockCode', 'Description'])['Revenue']
        .sum()
        .reset_index()
        .sort_values(by='Revenue', ascending=False)
    )

    top_20_products = product_revenue.head(20)

    # -------------------------------
    # 2️⃣ Pareto Analysis (80/20)
    # -------------------------------
    product_revenue['Revenue_Share'] = (
        product_revenue['Revenue'] / product_revenue['Revenue'].sum()
    )

    product_revenue['Cumulative_Revenue'] = (
        product_revenue['Revenue_Share'].cumsum()
    )

    pareto_products = product_revenue[
        product_revenue['Cumulative_Revenue'] <= 0.80
    ]

    # -------------------------------
    # 3️⃣ High Revenue but Low Quantity
    # -------------------------------
    product_quantity = (
        df.groupby(['StockCode', 'Description'])['Quantity']
        .sum()
        .reset_index()
    )

    product_summary = product_revenue.merge(
        product_quantity,
        on=['StockCode', 'Description']
    )

    high_revenue_low_quantity = product_summary[
        (product_summary['Revenue'] > product_summary['Revenue'].quantile(0.75)) &
        (product_summary['Quantity'] < product_summary['Quantity'].quantile(0.25))
    ]

    # -------------------------------
    # 4️⃣ Frequently Bought Together
    # -------------------------------
    basket = (
        df.groupby('InvoiceNo')['StockCode']
        .apply(list)
    )

    product_pairs = Counter()

    for items in basket:
        unique_items = set(items)
        for pair in combinations(unique_items, 2):
            product_pairs[pair] += 1

    frequent_pairs = pd.DataFrame(
        product_pairs.most_common(10),
        columns=['Product_Pair', 'Frequency']
    )

    return (
        top_20_products,
        pareto_products,
        high_revenue_low_quantity,
        frequent_pairs
    )


if __name__ == "__main__":
    # Load cleaned dataset
    df = pd.read_csv(
        "data/cleaned_dataset.csv",
        parse_dates=['InvoiceDate']
    )

    # Remove negative quantities (returns)
    df = df[df['Quantity'] > 0]

    (
        top_20_products,
        pareto_products,
        high_revenue_low_quantity,
        frequent_pairs
    ) = product_performance_analysis(df)

    # -------------------------------
    # SAVE OUTPUTS
    # -------------------------------
    top_20_products.to_csv(
        "analysis/python/product_performance_analysis/top_20_products_by_revenue.csv",
        index=False
    )

    pareto_products.to_csv(
        "analysis/python/product_performance_analysis/pareto_80_20_products.csv",
        index=False
    )

    high_revenue_low_quantity.to_csv(
        "analysis/python/product_performance_analysis/high_revenue_low_quantity_products.csv",
        index=False
    )

    frequent_pairs.to_csv(
        "analysis/python/product_performance_analysis/frequently_bought_together.csv",
        index=False
    )

    # -------------------------------
    # PARETO VISUALIZATION
    # -------------------------------
    plt.figure(figsize=(8, 5))
    plt.plot(
        product_performance := (
            pareto_products.reset_index().index + 1
        ),
        pareto_products['Cumulative_Revenue'] * 100
    )

    plt.axhline(80, color='red', linestyle='--')
    plt.title("Pareto Analysis – Revenue Contribution")
    plt.xlabel("Number of Products")
    plt.ylabel("Cumulative Revenue (%)")
    plt.tight_layout()
    plt.savefig("analysis/python/product_performance_analysis/pareto_80_20.png")
    plt.show()

    print("✅ Product performance analysis completed")
