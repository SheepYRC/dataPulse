import streamlit as st
from src.core.database import db_manager
from src.core.config import settings
import pandas as pd
import os

def show():
    st.title("📊 概况统计 (Summary Statistics)")
    
    duck_conn = db_manager.get_duckdb()
    
    # 1. High-level Audit
    st.subheader("📋 数据库审计")
    
    col1, col2, col3 = st.columns(3)
    
    try:
        tables = duck_conn.execute("SHOW TABLES").df()
        table_count = len(tables)
    except:
        table_count = 0
        
    snapshot_count = len(list(settings.SNAPSHOT_DIR.glob("*.parquet")))
    
    col1.metric("已导入数据表", table_count)
    col2.metric("结果快照数量", snapshot_count)
    
    # Disk Usage for data folder
    data_size = sum(f.stat().st_size for f in settings.DATA_DIR.rglob('*') if f.is_file())
    col3.metric("本地存储占用", f"{data_size / (1024*1024):.2f} MB")

    st.divider()
    
    # 2. Activity / Snapshot Details
    st.subheader("📜 快照清单")
    snapshots = []
    for f in settings.SNAPSHOT_DIR.glob("*.parquet"):
        snapshots.append({
            "文件名": f.name,
            "大小 (KB)": f.stat().st_size // 1024,
            "创建时间": pd.to_datetime(f.stat().st_mtime, unit='s')
        })
    
    if snapshots:
        st.table(pd.DataFrame(snapshots))
    else:
        st.info("尚未创建任何快照。")

    st.divider()
    
    # 3. Heatmap Placeholder
    st.subheader("🔥 活跃度画像")
    st.info("模块开发中：将展示对各数据表的操作频率热力图。")
    import numpy as np
    # Fake data for demonstration
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['查询', '处理', '导出'])
    st.line_chart(chart_data)
