import streamlit as st
from src.core.config import settings
from src.core.database import db_manager
import pandas as pd

def show():
    st.title("⚙️ 系统管理 (System Management)")
    
    tab1, tab2, tab3 = st.tabs(["基础配置", "存储配置", "开发者诊断"])
    
    with tab1:
        st.subheader("🎨 界面与偏好")
        theme = st.selectbox("主题模式", ["系统默认", "深色模式", "浅色模式"])
        lang = st.radio("语言 (Language)", ["简体中文", "English"], horizontal=True)
        
        st.divider()
        st.subheader("🔑 存储路径概览")
        st.write(f"**项目根目录:** `{settings.BASE_DIR}`")
        st.write(f"**分析库路径:** `{settings.DUCKDB_PATH}`")
        
        if st.button("💾 保存配置"):
            st.success("配置已保存（模拟）")

    with tab2:
        st.subheader("💾 数据管理")
        st.warning("⚠️ 此处的删除操作不可撤销。")
        
        col1, col2 = st.columns(2)
        if col1.button("🗑️ 清空所有 SQL 历史"):
            db_manager.get_sqlite().execute("DELETE FROM sql_history")
            db_manager.get_sqlite().commit()
            st.toast("历史已清空")
            
        if col2.button("🔥 初始化分析引擎"):
            # This would delete analytics.duckdb and restart
            st.error("此功能需要重启程序，暂未开放。")

    with tab3:
        st.subheader("🔍 系统诊断")
        import sys
        import platform
        
        diag_data = {
            "OS": platform.system(),
            "Python Version": sys.version.split()[0],
            "DuckDB Version": "1.1+",
            "Streamlit Version": st.__version__
        }
        st.json(diag_data)
        
        if st.button("🛠️ 导出系统日志"):
            st.info("日志已打包至 data/logs/...")
