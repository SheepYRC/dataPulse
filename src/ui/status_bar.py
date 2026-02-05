import streamlit as st
from src.utils.metrics import get_system_metrics


@st.fragment(run_every="5s")
def show_status_bar():
    """只负责渲染指标内容"""
    # 注意：这里不再写 with st.sidebar
    st.divider()
    st.subheader("💻 系统状态")

    metrics = get_system_metrics()
    cpu_usage = metrics["cpu"]
    ram_percent = metrics["memory"]
    disk_usage = metrics["disk"]

    col1, col2 = st.columns(2)
    col1.metric("CPU", f"{cpu_usage}%")
    col2.metric("内存", f"{ram_percent}%")

    if ram_percent > 80:
        st.warning(f"⚠️ 内存占用过高: {ram_percent}%")

    st.progress(disk_usage / 100, text=f"磁盘占用: {disk_usage}%")
    st.caption("数据每 5 秒自动更新")