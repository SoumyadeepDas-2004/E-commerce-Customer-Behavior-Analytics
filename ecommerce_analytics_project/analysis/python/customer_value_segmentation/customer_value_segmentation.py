import pandas as pd
from config.database import engine


def load_customer_value_segments(engine):
    """
    Segment customers based on total spending into Low, Mid, and High value groups.
    """
    query = """
    SELECT 
        c.customer_id,
        c.name,
        SUM(p.amount) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN payments p ON o.order_id = p.order_id
    GROUP BY c.customer_id, c.name
    """

    df = pd.read_sql(query, engine)

    df['segment'] = pd.qcut(
        df['total_spent'],
        q=3,
        labels=['Low Value', 'Mid Value', 'High Value']
    )

    return df


if __name__ == "__main__":
    df = load_customer_value_segments(engine)
    df.to_csv("analysis/python/customer_value_segmentation/customer_value_segments.csv", index=False)
    print(df['segment'].value_counts())
