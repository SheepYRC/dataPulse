import polars as pl
import pandas as pd

class CalculationEngine:
    def __init__(self):
        pass

    def run_query_polars(self, sql_query, duckdb_conn):
        """Execute query and return results as Polars DataFrame."""
        return duckdb_conn.execute(sql_query).pl()

    def run_query_pandas(self, sql_query, duckdb_conn):
        """Execute query and return results as Pandas DataFrame (fallback)."""
        return duckdb_conn.execute(sql_query).df()

engine = CalculationEngine()
