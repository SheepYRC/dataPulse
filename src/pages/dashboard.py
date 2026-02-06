import streamlit as st
from src.core.database import db_manager
import pandas as pd

def show():
    st.title("📡 DataPulse 工作看板")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 任务流水线")
        # Fetch tasks from SQLite
        sqlite_conn = db_manager.get_sqlite()
        tasks_df = pd.read_sql("SELECT * FROM tasks ORDER BY created_at DESC", sqlite_conn)
        
        if tasks_df.empty:
            st.info("尚无处理任务。在下方创建一个吧！")
        else:
            for _, task in tasks_df.iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1])
                    c1.markdown(f"**{task['name']}**")
                    c1.caption(f"状态: {task['status']} | 创建于: {task['created_at']}")
                    if c2.button("执行", key=f"run_{task['id']}"):
                        st.write(f"正在执行: {task['name']}...")
                        # Here we would actually run the SQL script
        
        with st.expander("➕ 创建新任务"):
            new_name = st.text_input("任务名称", placeholder="例如：2月销售报表清洗")
            new_sql = st.text_area("SQL 脚本", placeholder="SELECT * FROM ...")
            if st.button("保存任务"):
                cursor = sqlite_conn.cursor()
                cursor.execute("INSERT INTO tasks (name, sql_script) VALUES (?, ?)", (new_name, new_sql))
                sqlite_conn.commit()
                st.success("任务已创建！")
                st.rerun()

    with col2:
        st.subheader("🕒 最近访问")
        duck_conn = db_manager.get_duckdb()
        try:
            tables = duck_conn.execute("SHOW TABLES").df()
            if not tables.empty:
                for t in tables['name'].head(5):
                    if st.button(f"📄 {t}", key=f"recent_{t}", use_container_width=True):
                        # Navigation hack or just show info
                        st.info(f"跳转到 {t} 的查看页面...")
            else:
                st.write("暂无数据表")
        except:
            st.write("无法连接到分析引擎")
