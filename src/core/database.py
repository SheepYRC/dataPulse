import duckdb
import sqlite3
import streamlit as st
from src.core.config import settings

class DatabaseManager:
    def __init__(self):
        self.sqlite_conn = None
        self.duckdb_conn = None
        self._init_db()

    def _init_db(self):
        """Initialize connections to SQLite and DuckDB."""
        # SQLite for OLTP (Configs, Logs)
        self.sqlite_conn = sqlite3.connect(settings.SQLITE_DB_PATH, check_same_thread=False)
        self._setup_sqlite()

        # DuckDB for OLAP (Analytics)
        self.duckdb_conn = duckdb.connect(str(settings.DUCKDB_PATH))

    def _setup_sqlite(self):
        """Setup basic tables in SQLite if they don't exist."""
        cursor = self.sqlite_conn.cursor()
        # SQL History
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sql_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                sql_query TEXT,
                tag TEXT DEFAULT '-'
            )
        """)
        # Task Cards (M0)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                sql_script TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        """)
        self.sqlite_conn.commit()

    def log_query(self, sql_query, tag='-'):
        """Log a SQL query to the history table."""
        cursor = self.sqlite_conn.cursor()
        cursor.execute("INSERT INTO sql_history (sql_query, tag) VALUES (?, ?)", (sql_query, tag))
        self.sqlite_conn.commit()

    def get_history(self, limit=50):
        """Fetch the latest SQL history from SQLite."""
        cursor = self.sqlite_conn.cursor()
        cursor.execute("SELECT timestamp, sql_query, tag FROM sql_history ORDER BY timestamp DESC LIMIT ?", (limit,))
        return cursor.fetchall()

    def get_duckdb(self):
        return self.duckdb_conn

    def get_sqlite(self):
        return self.sqlite_conn

    def execute_duckdb(self, sql_query):
        """Execute a query on DuckDB and return as a Polars DataFrame."""
        return self.duckdb_conn.execute(sql_query).pl()

# Singleton instance
db_manager = DatabaseManager()
