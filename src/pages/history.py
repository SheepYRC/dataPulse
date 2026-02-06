import streamlit as st
from src.core.database import db_manager
import pandas as pd
from src.core.config import settings

def show():
    st.title("📜 历史与快照 (History & Snapshots)")
    
    tab1, tab2 = st.tabs(["SQL 历史", "结果快照"])
    
    with tab1:
        st.subheader("🕒 最近执行的 SQL")
        history = db_manager.get_history(limit=100)
        
        if not history:
            st.info("暂无查询历史。")
        else:
            df_history = pd.DataFrame(history, columns=["时间", "SQL 语句", "标签"])
            st.dataframe(df_history, width='content')
            
            if st.button("🗑️ 清空历史"):
                db_manager.get_sqlite().execute("DELETE FROM sql_history")
                db_manager.get_sqlite().commit()
                st.rerun()

    with tab2:
        st.subheader("📁 已保存的 Parquet 快照")
        snapshot_files = list(settings.SNAPSHOT_DIR.glob("*.parquet"))
        
        if not snapshot_files:
            st.info("暂无快照文件。快照可以在 SQL 实验室中生成（实现中）。")
        else:
            for file in snapshot_files:
                col1, col2 = st.columns([3, 1])
                col1.write(f"📄 {file.name}")
                if col2.button(f"删除", key=str(file)):
                    file.unlink()
                    st.rerun()
