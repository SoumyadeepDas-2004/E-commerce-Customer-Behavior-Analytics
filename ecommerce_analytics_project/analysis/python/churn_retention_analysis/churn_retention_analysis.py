import os
import pandas as pd
import matplotlib.pyplot as plt


def churn_retention_analysis(df, churn_days=90):
    """
    Perform churn and retention analysis.
    A customer is considered churned if they have not
    made a purchase in the last `churn_days`.
    """

    # Remove returns
    df = df[df['Quantity'] > 0]

    # Reference date (end of dataset)
    reference_date = df['InvoiceDate'].max()

    # Customer-level aggregation
    customer_activity = (
        df.groupby('CustomerID')
        .agg(
            Last_Purchase_Date=('InvoiceDate', 'max'),
            First_Purchase_Date=('InvoiceDate', 'min'),
            Total_Orders=('InvoiceNo', 'nunique')
        )
        .reset_index()
    )

    # Days since last purchase
    customer_activity['Days_Since_Last_Purchase'] = (
        reference_date - customer_activity['Last_Purchase_Date']
    ).dt.days

    # Churn flag
    customer_activity['Churned'] = (
        customer_activity['Days_Since_Last_Purchase'] > churn_days
    )

    # Retention & churn rates
    total_customers = len(customer_activity)
    churned_customers = customer_activity['Churned'].sum()
    retained_customers = total_customers - churned_customers

    churn_rate = churned_customers / total_customers * 100
    retention_rate = retained_customers / total_customers * 100

    return (
        customer_activity,
        churn_rate,
        retention_rate
    )


if __name__ == "__main__":
    # Load cleaned dataset
    df = pd.read_csv(
        "data/cleaned_dataset.csv",
        parse_dates=['InvoiceDate']
    )

    customer_activity, churn_rate, retention_rate = churn_retention_analysis(
        df, churn_days=90
    )


    # ----------------------------
    # SAVE DATA
    # ----------------------------
    customer_activity.to_csv(
        "analysis/python/churn_retention_analysis/customer_churn_status.csv",
        index=False
    )

    # ----------------------------
    # SAVE INSIGHTS
    # ----------------------------
    with open("analysis/python/churn_retention_analysis/churn_retention_insights.txt", "w") as f:
        f.write("CHURN & RETENTION ANALYSIS\n\n")
        f.write(f"Churn Definition: No purchase in last 90 days\n\n")
        f.write(f"Total Customers: {len(customer_activity)}\n")
        f.write(f"Churn Rate: {churn_rate:.2f}%\n")
        f.write(f"Retention Rate: {retention_rate:.2f}%\n")

    print("🔁 Churn & Retention Summary\n")
    print(f"Churn Rate: {churn_rate:.2f}%")
    print(f"Retention Rate: {retention_rate:.2f}%")

    # ----------------------------
    # TIME-TO-CHURN DISTRIBUTION
    # ----------------------------
    plt.figure(figsize=(8, 5))
    plt.hist(
        customer_activity['Days_Since_Last_Purchase'],
        bins=30
    )

    plt.axvline(90, color='red', linestyle='--', label='Churn Threshold')
    plt.title("Time-to-Churn Distribution")
    plt.xlabel("Days Since Last Purchase")
    plt.ylabel("Number of Customers")
    plt.legend()
    plt.tight_layout()

    plt.savefig("analysis/python/churn_retention_analysis/time_to_churn_distribution.png")
    plt.show()
