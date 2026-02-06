import streamlit as st
import pandas as pd
import polars as pl
from src.core.database import db_manager
from src.core.config import settings
import datetime

def show():
    st.title("🧪 数据查询 (Data Query)")
    
    duck_conn = db_manager.get_duckdb()
    
    # 1. Query Mode Selection
    mode = st.radio("查询模式", ["SQL 模式", "GUI 交互模式"], horizontal=True)
    
    if mode == "SQL 模式":
        sql_input = st.text_area("SQL 编辑器", value="SELECT * FROM imported_table LIMIT 100", height=200)
        
        col1, col2, col3 = st.columns([1, 1, 3])
        run_btn = col1.button("▶ 运行查询")
        save_btn = col2.button("💾 存为快照")
        engine_choice = col3.selectbox("计算引擎", ["Polars (推荐)", "Pandas", "DuckDB Native"])

        if run_btn:
            try:
                with st.spinner("正在高速运算..."):
                    db_manager.log_query(sql_input)
                    
                    if engine_choice == "Polars (推荐)":
                        df = duck_conn.execute(sql_input).pl()
                    elif engine_choice == "Pandas":
                        df = duck_conn.execute(sql_input).df()
                    else:
                        df = duck_conn.execute(sql_input).arrow() # Arrow is close to native/efficient
                    
                    st.session_state['query_result'] = df
                    st.success(f"查询成功！")
            except Exception as e:
                st.error(f"SQL 执行失败: {e}")

    else:
        # GUI Mode
        tables = duck_conn.execute("SHOW TABLES").df()
        if tables.empty:
            st.warning("请先在'数据资产'模块导入数据。")
        else:
            selected_table = st.selectbox("选择目标表", tables['name'].tolist())
            limit = st.number_input("展示行数", value=100, step=100)
            
            if st.button("🔍 加载预览"):
                quoted_table = f'"{selected_table}"'
                df = duck_conn.execute(f"SELECT * FROM {quoted_table} LIMIT {limit}").pl()
                st.session_state['query_result'] = df

    # Display Results
    if 'query_result' in st.session_state:
        df = st.session_state['query_result']
        st.divider()
        st.subheader("📋 查询结果")
        st.dataframe(df, use_container_width=True)
        
        # Download/Snapshot
        if st.download_button(
            label="📥 导出为 CSV",
            data=df.to_pandas().to_csv(index=False).encode('utf-8'),
            file_name=f"query_result_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime='text/csv',
        ):
            st.toast("文件准备就绪")

        if 'save_btn' in locals() and save_btn:
             # Save as parquet snapshot
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snapshot_{ts}.parquet"
            save_path = settings.SNAPSHOT_DIR / filename
            try:
                if isinstance(df, pl.DataFrame):
                    df.write_parquet(save_path)
                else: # pandas or arrow
                    pd.DataFrame(df).to_parquet(save_path)
                st.success(f"结果已保存为快照: {filename}")
            except Exception as e:
                st.error(f"快照保存失败: {e}")
