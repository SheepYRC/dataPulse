import streamlit as st
from streamlit_searchbox import st_searchbox
from src.core.database import db_manager
import pandas as pd

def show():
    st.title("⌨️ 全局搜索 (Command Palette)")
    st.markdown("输入表名、任务或 SQL 关键词快速定位。")

    def search_all(searchterm: str):
        if not searchterm:
            return []
        
        results = []
        
        # 1. Search Tables in DuckDB
        duck_conn = db_manager.get_duckdb()
        tables = duck_conn.execute(f"SHOW TABLES").df()
        if not tables.empty:
            for t in tables['name']:
                if searchterm.lower() in t.lower():
                    results.append((f"📄 表: {t}", f"table:{t}"))
        
        # 2. Search SQL History in SQLite
        history = db_manager.get_history(limit=50)
        for _, sql, tag in history:
            if searchterm.lower() in sql.lower():
                results.append((f"📜 SQL: {sql[:30]}...", f"sql:{sql}"))
        
        # 3. Search Tasks
        sqlite_conn = db_manager.get_sqlite()
        tasks = pd.read_sql(f"SELECT name FROM tasks WHERE name LIKE '%{searchterm}%'", sqlite_conn)
        for t in tasks['name']:
            results.append((f"🚀 任务: {t}", f"task:{t}"))
            
        # 4. Action commands
        actions = [
            ("> export", "page:assets"),
            ("> system", "page:system"),
            ("> help", "page:dashboard")
        ]
        for label, val in actions:
            if searchterm.lower() in label.lower():
                results.append((f"⚡ 命令: {label}", val))

        return results

    selected_value = st_searchbox(
        search_all,
        key="global_search_box",
        placeholder="输入并搜索..."
    )

    if selected_value:
        st.divider()
        st.subheader("🎯 搜索跳轉")
        
        if selected_value.startswith("table:"):
            st.info(f"正在跳转至表 {selected_value.split(':')[1]} 的资产管理页...")
            # Here we could set some session state to highlight this table in assets.py
        elif selected_value.startswith("sql:"):
            st.code(selected_value.split(":", 1)[1])
        elif selected_value.startswith("page:"):
            page = selected_value.split(":")[1]
            st.write(f"建议跳转至: {page}")
        else:
            st.write(f"选定结果: {selected_value}")
