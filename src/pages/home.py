import streamlit as st
from src.core.database import db_manager
import assets
import pandas as pd

def show():
    st.title("🏠 工作看板 (Workboard)")
    st.write("欢迎来到 DataPulse。从这里开始你的数据处理流程。")
    
    # 1. Quick Action Cards
    st.subheader("⚡ 快捷动作")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🧼 清理临时缓存", use_container_width=True):
            st.info("缓存已清理（模拟）")
    with col2:
        if st.button("🎒 备份当前数据库", use_container_width=True):
            st.info("数据库已备份至 backup 目录（模拟）")
    with col3:
        if st.button("📊 查看数据分布", use_container_width=True):
            st.info("未配置"),

    st.divider()

    # 2. Recent Activity
    st.subheader("📜 最近活动")
    history = db_manager.get_history(limit=5)
    if not history:
        st.info("暂无活动，快去 SQL 实验室执行查询吧！")
    else:
        for ts, sql, tag in history:
            with st.container(border=True):
                st.markdown(f"**{ts}**")
                st.code(sql, language="sql")
