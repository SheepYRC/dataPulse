import streamlit as st
from src.core.database import db_manager
import pandas as pd

def show():
    st.title("📊 数据资产看板 (Data Assets)")
    
    duck_conn = db_manager.get_duckdb()
    
    # 1. Overview Metrics
    st.subheader("📦 存储概览")
    # DuckDB specific storage info (experimental)
    try:
        storage_info = duck_conn.execute("PRAGMA database_size").df()
        db_size = storage_info['database_size'].iloc[0]
        st.metric("分析数据库体积", db_size)
    except:
        st.info("无法获取详细存储指标，数据库可能为空。")

    st.divider()

    # 2. Table List & Schema
    st.subheader("📂 数据表清单")
    tables = duck_conn.execute("SHOW TABLES").df()
    
    if tables.empty:
        st.warning("当前没有已导入的数据表。")
    else:
        selected_table = st.selectbox("选择表以查看详情", tables['name'].tolist())
        
        if selected_table:
            # Metadata
            schema = duck_conn.execute(f"DESCRIBE {selected_table}").df()
            row_count = duck_conn.execute(f"SELECT COUNT(*) FROM {selected_table}").fetchone()[0]
            
            col1, col2 = st.columns(2)
            col1.write(f"**行数:** {row_count}")
            col2.write(f"**字段数:** {len(schema)}")
            
            st.write("**字段定义:**")
            st.dataframe(schema, width='content')
            
            # Health Check (Simple version)
            if st.button(f"🔍 运行 {selected_table} 健康评估"):
                with st.spinner("正在扫描数据量与空值..."):
                    # Scan for nulls in each column
                    null_counts = {}
                    for col in schema['column_name']:
                        c = duck_conn.execute(f"SELECT COUNT(*) FROM {selected_table} WHERE {col} IS NULL").fetchone()[0]
                        null_counts[col] = c
                    
                    st.write("**空值审计:**")
                    st.bar_chart(pd.Series(null_counts))
