from src.utils.metrics import get_system_metrics
import streamlit as st

def show_status_bar():
    """Display system metrics in the sidebar or bottom."""
    with st.sidebar:
        st.divider()
        st.subheader("💻 系统状态")
        
        metrics = get_system_metrics()
        cpu_usage = metrics["cpu"]
        ram_percent = metrics["memory"]
        
        col1, col2 = st.columns(2)
        col1.metric("CPU", f"{cpu_usage}%")
        col2.metric("内存", f"{ram_percent}%")
        
        if ram_percent > 80:
            st.warning("⚠️ 内存占用过高")
        
        # Disk I/O monitoring
        st.progress(metrics["disk"] / 100, text=f"磁盘占用: {metrics['disk']}%")
