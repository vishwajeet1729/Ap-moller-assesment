import re
from datetime import datetime, timedelta

def _months_ago(months: int) -> str:
    return (datetime.utcnow() - timedelta(days=30 * months)).strftime('%Y-%m-%d')

RULES = [
    {
        'pattern': r'(top|highest).*category.*(last|past)\s*(\d+)\s*month',
        'to_sql': lambda m: f"""
            SELECT product_category_name AS category,
                   ROUND(SUM(price), 2) AS gross_revenue
            FROM v_order_lines
            WHERE purchased_at >= '{_months_ago(int(m.group(3)))}'
            GROUP BY 1
            ORDER BY 2 DESC
            LIMIT 10;
        """
    },
    {
        'pattern': r'average order value|aov',
        'to_sql': lambda m: """
            WITH order_totals AS (
                SELECT order_id, SUM(price) AS order_value
                FROM order_items
                GROUP BY order_id
            )
            SELECT ROUND(AVG(order_value), 2) AS avg_order_value
            FROM order_totals;
        """
    }
]

FALLBACK = """
SELECT order_status, COUNT(*) AS orders
FROM orders
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;
"""

def question_to_sql(q: str) -> str:
    q = q.lower().strip()
    for rule in RULES:
        match = re.search(rule['pattern'], q)
        if match:
            return rule['to_sql'](match)
    return FALLBACK
