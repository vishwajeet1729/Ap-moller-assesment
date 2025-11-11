from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path

DB_PATH = Path(__file__).parent / 'olist.db'
ENGINE = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

@contextmanager
def get_conn():
    conn = ENGINE.connect()
    try:
        yield conn
    finally:
        conn.close()

def run_readonly_sql(sql: str, limit: int = 1000):
    forbidden = ('insert', 'update', 'delete', 'drop', 'alter', 'create', 'replace', 'pragma')
    lowered = sql.lower()

    if any(x in lowered for x in forbidden):
        raise ValueError("Write / DDL statements are blocked.")

    if "limit" not in lowered:
        sql = sql.rstrip(";") + f" LIMIT {limit};"

    with get_conn() as conn:
        try:
            result = conn.execute(text(sql))
            cols = result.keys()
            rows = [dict(zip(cols, r)) for r in result.fetchall()]
            return {"columns": list(cols), "rows": rows}
        except SQLAlchemyError as e:
            raise ValueError(str(e))
