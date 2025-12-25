import os
import pandas as pd
from config.database import engine


def perform_rfm_analysis(engine):
    """
    Perform RFM (Recency, Frequency, Monetary) analysis
    using normalized e-commerce transaction tables.
    """

    # Load transaction-level data
    query = """
    SELECT
        o.customer_id AS CustomerID,
        o.order_id AS InvoiceNo,
        o.order_date AS InvoiceDate,
        p.amount AS Revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    WHERE p.amount > 0
    """

    df = pd.read_sql(query, engine)

    # Reference date = one day after the most recent transaction
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

    # Calculate RFM metrics
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
        'InvoiceNo': 'nunique',                                   # Frequency
        'Revenue': 'sum'                                          # Monetary
    }).reset_index()

    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

    # -----------------------------
    # ROBUST RFM SCORING (NO ERRORS)
    # -----------------------------

    rfm['R_Score'] = pd.qcut(rfm['Recency'], q=5, duplicates='drop')
    rfm['F_Score'] = pd.qcut(rfm['Frequency'], q=5, duplicates='drop')
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], q=5, duplicates='drop')

    # Convert bins to numeric scores (1 = lowest, higher = better)
    rfm['R_Score'] = rfm['R_Score'].cat.codes + 1
    rfm['F_Score'] = rfm['F_Score'].cat.codes + 1
    rfm['M_Score'] = rfm['M_Score'].cat.codes + 1

    # Combined RFM score
    rfm['RFM_Score'] = (
        rfm['R_Score'].astype(str)
        + rfm['F_Score'].astype(str)
        + rfm['M_Score'].astype(str)
    )

    # -----------------------------
    # BUSINESS SEGMENTATION
    # -----------------------------
    def segment(row):
        if row['R_Score'] >= 4 and row['F_Score'] >= 4 and row['M_Score'] >= 4:
            return 'Champions'
        elif row['F_Score'] >= 4:
            return 'Loyal Customers'
        elif row['R_Score'] >= 4:
            return 'Recent Customers'
        elif row['R_Score'] <= 2 and row['F_Score'] <= 2:
            return 'At Risk'
        else:
            return 'Others'

    rfm['Segment'] = rfm.apply(segment, axis=1)

    return rfm


if __name__ == "__main__":
    rfm_df = perform_rfm_analysis(engine)
    rfm_df.to_csv("analysis/python/RFM_analysis/customer_rfm_segments.csv", index=False)
    print(rfm_df['Segment'].value_counts())
