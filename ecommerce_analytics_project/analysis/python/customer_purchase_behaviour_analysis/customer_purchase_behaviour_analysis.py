import pandas as pd
from config.database import engine


def generate_customer_personas(engine):
    """
    Analyze customer purchase behavior and segment customers into personas
    based on average time between orders.
    """
    query = """
    SELECT
        c.customer_id,
        COUNT(DISTINCT o.order_id) AS orders,
        SUM(oi.quantity * p.price) AS total_spent,
        COUNT(DISTINCT oi.product_id) AS product_variety,
        AVG(oi.quantity * p.price) AS avg_order_value,
        DATEDIFF(MAX(o.order_date), MIN(o.order_date)) / COUNT(DISTINCT o.order_id) 
            AS avg_days_between_orders
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY c.customer_id;
    """

    df = pd.read_sql(query, engine)

    df['persona'] = pd.cut(
        df['avg_days_between_orders'],
        bins=[0, 7, 30, 90, 9999],
        labels=['Impulse Buyer', 'Regular Buyer', 'Occasional Buyer', 'Rare Buyer']
    )

    return df


if __name__ == "__main__":
    df = generate_customer_personas(engine)
    df.to_csv("analysis/python/customer_purchase_behaviour_analysis/customer_personas.csv", index=False)
    print(df['persona'].value_counts())
