# E-commerce Customer Behavior Analytics

## 📌 Problem Statement
Analyze customer purchase behavior to segment customers into meaningful personas
based on purchase frequency, spending patterns, and product diversity.

## 🛠 Tech Stack
- Python
- MySQL
- SQLAlchemy
- Pandas
- dotenv

## 📂 Data Source
Relational MySQL database containing customers, orders, order_items, and products tables.

## 🔍 Key Analysis
- Total orders per customer
- Total revenue contribution
- Product variety per customer
- Average order value
- Average days between purchases

## 📊 Customer Personas
Customers were segmented into:
- Impulse Buyers
- Regular Buyers
- Occasional Buyers
- Rare Buyers

## 🚀 Results
- Identified dominant customer segments
- Generated CSV output for downstream analytics
- Enabled targeted marketing strategies

## ▶️ How to Run
```bash
python -m analysis.python.customer_purchase_behavious_analysis
