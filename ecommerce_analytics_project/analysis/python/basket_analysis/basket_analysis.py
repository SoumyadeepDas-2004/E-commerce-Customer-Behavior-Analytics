import os
import pandas as pd
from itertools import combinations
from collections import Counter


def basket_analysis(df, top_n=20):
    """
    Perform basket analysis to identify
    frequently bought product combinations.
    """

    # Keep only positive quantities
    df = df[df['Quantity'] > 0]

    # Group products by invoice (basket)
    baskets = (
        df.groupby('InvoiceNo')['Description']
        .apply(list)
    )

    pair_counter = Counter()

    for items in baskets:
        unique_items = set(items)
        if len(unique_items) > 1:
            for pair in combinations(unique_items, 2):
                pair_counter[pair] += 1

    # Convert to DataFrame
    frequent_pairs = pd.DataFrame(
        pair_counter.most_common(top_n),
        columns=['Product_Pair', 'Frequency']
    )

    return frequent_pairs


if __name__ == "__main__":
    # Load cleaned dataset
    df = pd.read_csv(
        "data/cleaned_dataset.csv",
        parse_dates=['InvoiceDate']
    )

    frequent_pairs = basket_analysis(df, top_n=20)


    # Save results
    frequent_pairs.to_csv(
        "analysis/python/basket_analysis/frequently_bought_together_products.csv",
        index=False
    )

    print("🧺 Top Frequently Bought Together Products:\n")
    print(frequent_pairs)
