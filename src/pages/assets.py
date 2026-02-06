import streamlit as st
from src.core.database import db_manager
import pandas as pd

def show():
    st.title("📊 数据资产看板 (Data Assets)")
    
    duck_conn = db_manager.get_duckdb()
    
    # 1. Data Import Section
    with st.expander("📥 导入新数据", expanded=False):
        uploaded_file = st.file_uploader("选择 CSV, Excel 或 Parquet 文件", type=["csv", "xlsx", "parquet"])
        #print("uploaded_file",uploaded_file)
        table_name = st.text_input("目标表名", value="imported_table")
        
        # Validation logic
        import re
        valid_name_regex = r'^[a-zA-Z0-9_\-]+$' # Allow alphanumeric, dash, and underscore
        
        if uploaded_file and st.button("🚀 开始导入"):
            if not table_name:
                st.error("❌ 错误：表名不能为空。")
            elif not re.match(valid_name_regex, table_name):
                st.error(f"❌ 错误：表名 '{table_name}' 包含非法字符。建议仅使用字母、数字、下划线或连字符。")
            else:
                import tempfile
                import os
                from src.utils.io_handler import import_to_duckdb
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                with st.spinner("正在导入百万级引擎..."):
                    success = import_to_duckdb(tmp_path, table_name, duck_conn)
                    os.unlink(tmp_path)
                if success:
                    st.success(f"成功导入: {table_name}")
                    st.rerun()
                else:
                    st.error("导入失败，详见系统日志。")

    st.divider()

    # 2. Overview Metrics
    st.subheader("📦 存储概览")
    try:
        storage_info = duck_conn.execute("PRAGMA database_size").df()
        db_size = storage_info['database_size'].iloc[0]
        st.metric("分析数据库体积", db_size)
    except:
        st.info("无法获取详细存储指标，数据库可能为空。")

    st.divider()

    # 3. Table List & Schema
    st.subheader("📂 数据表清单")
    tables = duck_conn.execute("SHOW TABLES").df()
    
    if tables.empty:
        st.warning("当前没有已导入的数据表。")
    else:
        selected_table = st.selectbox("选择表以查看详情", tables['name'].tolist())
        
        if selected_table:
            # Metadata
            quoted_table = f'"{selected_table}"'
            schema = duck_conn.execute(f"DESCRIBE {quoted_table}").df()
            row_count = duck_conn.execute(f"SELECT COUNT(*) FROM {quoted_table}").fetchone()[0]
            
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
                        quoted_table = f'"{selected_table}"'
                        c = duck_conn.execute(f"SELECT COUNT(*) FROM {quoted_table} WHERE {col} IS NULL").fetchone()[0]
                        null_counts[col] = c
                    
                    st.write("**空值审计:**")
                    st.bar_chart(pd.Series(null_counts))
