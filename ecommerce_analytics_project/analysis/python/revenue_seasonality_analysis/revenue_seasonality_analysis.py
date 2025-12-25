import os
import pandas as pd
import matplotlib.pyplot as plt


def revenue_seasonality_analysis(df):
    """
    Analyze monthly revenue trends, seasonality,
    peak sales months, and MoM growth.
    """

    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')

    monthly_revenue = (
        df.groupby('YearMonth')['Revenue']
        .sum()
        .reset_index()
    )

    monthly_revenue['YearMonth'] = monthly_revenue['YearMonth'].dt.to_timestamp()

    monthly_revenue['MoM_Growth_%'] = (
        monthly_revenue['Revenue'].pct_change() * 100
    )

    return monthly_revenue


if __name__ == "__main__":
    df = pd.read_csv(
        "data/cleaned_dataset.csv",
        parse_dates=['InvoiceDate']
    )

    monthly_revenue = revenue_seasonality_analysis(df)

    # Output folders
    os.makedirs("outputs/figures", exist_ok=True)
    os.makedirs("outputs/reports", exist_ok=True)

    # ----------------------------
    # SAVE DATA
    # ----------------------------
    monthly_revenue.to_csv(
        "outputs/monthly_revenue_seasonality.csv",
        index=False
    )

    # ----------------------------
    # BUSINESS INSIGHTS
    # ----------------------------
    top_months = monthly_revenue.sort_values(
        by='Revenue', ascending=False
    ).head(3)

    low_months = monthly_revenue.sort_values(
        by='Revenue'
    ).head(3)

    holiday_months = monthly_revenue[
        monthly_revenue['YearMonth'].dt.month.isin([11, 12])
    ]

    best_growth = monthly_revenue.loc[
        monthly_revenue['MoM_Growth_%'].idxmax()
    ]

    # Save insights to text file
    with open("analysis/python/revenue_seasonality_analysis/revenue_seasonality_insights.txt", "w") as f:
        f.write("REVENUE & SEASONALITY INSIGHTS\n\n")

        f.write("Top 3 Peak Sales Months:\n")
        f.write(top_months.to_string(index=False))
        f.write("\n\n")

        f.write("Lowest 3 Sales Months:\n")
        f.write(low_months.to_string(index=False))
        f.write("\n\n")

        f.write("Holiday Season Performance (Nov–Dec):\n")
        f.write(holiday_months.to_string(index=False))
        f.write("\n\n")

        f.write("Highest Month-over-Month Growth:\n")
        f.write(best_growth.to_string())
        f.write("\n")

    print("✅ Revenue seasonality insights saved")

    # ----------------------------
    # VISUALIZATION
    # ----------------------------
    plt.figure(figsize=(10, 5))
    plt.plot(
        monthly_revenue['YearMonth'],
        monthly_revenue['Revenue'],
        marker='o'
    )

    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("analysis/python/revenue_seasonality_analysis/monthly_revenue_trend.png")
    plt.show()
