import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


class DWHRepository:
    def __init__(self, db_uri: str, timeout_seconds: int = 10):
        self._engine: Engine = create_engine(db_uri, pool_pre_ping=True)
        self._timeout_seconds = timeout_seconds

    def execute_read_query(self, sql_query: str) -> pd.DataFrame:
        with self._engine.connect() as connection:
            connection.execute(text(f"SET SESSION max_statement_time = {self._timeout_seconds}"))
            return pd.read_sql(text(sql_query), connection)
