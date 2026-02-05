import polars as pl
import os
from src.utils.logger import logger

def smart_read_csv(file_path):
    """Robust CSV reading with separator and encoding detection."""
    try:
        # Polars often handles encoding and separators automatically
        df = pl.read_csv(file_path, try_parse_dates=True, ignore_errors=True)
        return df
    except Exception as e:
        logger.error(f"Error reading CSV {file_path}: {e}")
        return None

def smart_read_excel(file_path):
    """Read Excel files using Polars (requires fsspec and openpyxl/xlsx2csv)."""
    try:
        df = pl.read_excel(file_path)
        return df
    except Exception as e:
        logger.error(f"Error reading Excel {file_path}: {e}")
        return None

def import_to_duckdb(file_path, table_name, db_conn):
    """Fast import of a file to DuckDB."""
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.csv':
            db_conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file_path}')")
        elif ext == '.parquet':
            db_conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_parquet('{file_path}')")
        elif ext in ['.xlsx', '.xls']:
            df = smart_read_excel(file_path)
            if df is not None:
                db_conn.register("temp_df", df)
                db_conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM temp_df")
                db_conn.unregister("temp_df")
        return True
    except Exception as e:
        logger.error(f"Import failed for {file_path}: {e}")
        return False
