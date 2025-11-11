import os, sqlite3, pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / 'olist.db'
SCHEMA = ROOT / 'schema.sql'

CSV_DIR = ROOT / 'csv'
CUSTOMERS = CSV_DIR / 'olist_customers_dataset.csv'
ORDERS = CSV_DIR / 'olist_orders_dataset.csv'
ORDER_ITEMS = CSV_DIR / 'olist_order_items_dataset.csv'
PRODUCTS = CSV_DIR / 'olist_products_dataset.csv'

CSV_REQUIRED = [CUSTOMERS, ORDERS, ORDER_ITEMS, PRODUCTS]

if not all(p.exists() for p in CSV_REQUIRED):
    raise SystemExit(
        "Place CSVs inside backend/csv/ directory:\n"
        "- olist_customers_dataset.csv\n"
        "- olist_orders_dataset.csv\n"
        "- olist_order_items_dataset.csv\n"
        "- olist_products_dataset.csv"
    )

# Build DB
con = sqlite3.connect(DB)
with open(SCHEMA, 'r') as f:
    con.executescript(f.read())

pd.read_csv(CUSTOMERS).to_sql('customers', con, if_exists='replace', index=False)
pd.read_csv(ORDERS).to_sql('orders', con, if_exists='replace', index=False)
pd.read_csv(ORDER_ITEMS).to_sql('order_items', con, if_exists='replace', index=False)
pd.read_csv(PRODUCTS).to_sql('products', con, if_exists='replace', index=False)

# Build view
con.executescript('''
DROP VIEW IF EXISTS v_order_lines;
CREATE VIEW v_order_lines AS
SELECT oi.order_id,
       o.order_purchase_timestamp AS purchased_at,
       c.customer_state,
       p.product_category_name,
       oi.price,
       oi.freight_value
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN customers c ON c.customer_id = o.customer_id
LEFT JOIN products p ON p.product_id = oi.product_id;
''')

con.commit()
con.close()
print("DB Ready:", DB)
