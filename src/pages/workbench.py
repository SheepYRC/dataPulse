import streamlit as st
import pandas as pd
import polars as pl
from src.core.database import db_manager
from src.utils.io_handler import import_to_duckdb
import tempfile
import os

def show():
    st.title("🧪 数据实验室 (SQL Workbench)")
    
    # 1. File Upload Section
    with st.expander("📂 导入本地数据 (CSV/Excel/Parquet)", expanded=False):
        uploaded_file = st.file_uploader("选择文件", type=["csv", "xlsx", "parquet"])
        table_name = st.text_input("预设表名", value="imported_data")
        
        if uploaded_file and st.button("开始导入"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            with st.spinner("正在高速导入..."):
                success = import_to_duckdb(tmp_path, table_name, db_manager.get_duckdb())
                os.unlink(tmp_path)
                if success:
                    st.success(f"成功导入至表: {table_name}")
                else:
                    st.error("导入失败，请检查文件格式。")

    st.divider()

    # 2. SQL Editor Section
    sql_input = st.text_area("SQL 编辑器", value="SELECT * FROM imported_data LIMIT 100", height=150)
    
    col1, col2 = st.columns([1, 5])
    run_btn = col1.button("▶ 运行查询", width='content')
    save_btn = col2.button("💾 保存为结果快照", width='stretch')

    if run_btn:
        try:
            with st.spinner("正在计算..."):
                # Register the query in history
                db_manager.log_query(sql_input)
                
                # Execute
                df = db_manager.execute_duckdb(sql_input)
                
                if df is not None:
                    st.session_state['last_query_result'] = df
                    st.success(f"查询完成，返回 {len(df)} 行数据。")
                else:
                    st.warning("查询执行成功，但未返回数据。")
        except Exception as e:
            st.error(f"SQL 错误: {e}")

    if 'last_query_result' in st.session_state:
        df = st.session_state['last_query_result']
        
        # Streamlit's st.dataframe is efficient for large datasets (lazy loading)
        st.dataframe(df, width='content')
        
        if save_btn:
            # Generate a filename based on timestamp
            import datetime
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snapshot_{ts}.parquet"
            save_path = settings.SNAPSHOT_DIR / filename
            
            try:
                # Save as parquet
                df.write_parquet(save_path)
                st.success(f"结果已保存为快照: {filename}")
            except Exception as e:
                st.error(f"保存快照失败: {e}")
