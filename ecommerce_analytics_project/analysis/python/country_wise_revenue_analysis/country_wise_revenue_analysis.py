import os
import pandas as pd
import matplotlib.pyplot as plt


def country_wise_analysis(df):
    """
    Analyze country-wise revenue, customer distribution,
    and average order value (AOV).
    """

    # Revenue column
    df['Revenue'] = df['Quantity'] * df['UnitPrice']

    # ----------------------------
    # Country-wise Aggregation
    # ----------------------------
    country_metrics = (
        df.groupby('Country')
        .agg(
            Total_Revenue=('Revenue', 'sum'),
            Total_Orders=('InvoiceNo', 'nunique'),
            Total_Customers=('CustomerID', 'nunique')
        )
        .reset_index()
    )

    # Average Order Value
    country_metrics['AOV'] = (
        country_metrics['Total_Revenue'] /
        country_metrics['Total_Orders']
    )

    return country_metrics


if __name__ == "__main__":
    # Load cleaned dataset
    df = pd.read_csv(
        "data/cleaned_dataset.csv",
        parse_dates=['InvoiceDate']
    )

    # Remove returns
    df = df[df['Quantity'] > 0]

    country_metrics = country_wise_analysis(df)

    # ----------------------------
    # SAVE DATA
    # ----------------------------
    country_metrics.to_csv(
        "analysis/python/country_wise_revenue_analysis/country_wise_metrics.csv",
        index=False
    )

    # ----------------------------
    # TOP COUNTRIES BY REVENUE
    # ----------------------------
    top_revenue_countries = country_metrics.sort_values(
        by='Total_Revenue', ascending=False
    ).head(10)

    # ----------------------------
    # TOP COUNTRIES BY AOV
    # ----------------------------
    top_aov_countries = country_metrics.sort_values(
        by='AOV', ascending=False
    ).head(10)

    # ----------------------------
    # UNTAPPED MARKETS
    # High customers but low revenue
    # ----------------------------
    untapped_markets = country_metrics[
        (country_metrics['Total_Customers'] >
         country_metrics['Total_Customers'].quantile(0.75)) &
        (country_metrics['Total_Revenue'] <
         country_metrics['Total_Revenue'].quantile(0.25))
    ]

    # ----------------------------
    # SAVE INSIGHTS
    # ----------------------------
    with open("analysis/python/country_wise_revenue_analysis/country_wise_insights.txt", "w") as f:
        f.write("COUNTRY-WISE BUSINESS INSIGHTS\n\n")

        f.write("Top 10 Countries by Revenue:\n")
        f.write(top_revenue_countries.to_string(index=False))
        f.write("\n\n")

        f.write("Top 10 Countries by AOV:\n")
        f.write(top_aov_countries.to_string(index=False))
        f.write("\n\n")

        f.write("Untapped Markets (High Customers, Low Revenue):\n")
        if untapped_markets.empty:
            f.write("No clear untapped markets detected.\n")
        else:
            f.write(untapped_markets.to_string(index=False))

    print("✅ Country-wise analysis saved")

    # ----------------------------
    # VISUALIZATION
    # ----------------------------
    plt.figure(figsize=(10, 5))
    plt.bar(
        top_revenue_countries['Country'],
        top_revenue_countries['Total_Revenue']
    )

    plt.title("Top 10 Countries by Revenue")
    plt.xlabel("Country")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("analysis/python/country_wise_revenue_analysis/top_countries_by_revenue.png")
    plt.show()
