import streamlit as st
from src.pages import home, assets, workbench, history, insights
from src.ui.status_bar import show_status_bar

# Page Configuration
st.set_page_config(
    page_title="DataPulse",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Navigation
pg = st.navigation({
    "任务": [
        st.Page(home.show, title="首页", icon="🏠", url_path="home"),
    ],
    "数据": [
        st.Page(assets.show, title="数据资产", icon="📊", url_path="assets"),
        st.Page(workbench.show, title="SQL 实验室", icon="🧪", url_path="workbench"),
        st.Page(history.show, title="历史与快照", icon="📜", url_path="history"),
    ],
    "洞察": [
        st.Page(insights.show, title="可视化探索", icon="🔍", url_path="insights"),
    ]
})

# Sidebar branding
st.sidebar.markdown("# 📡 DataPulse")
st.sidebar.caption("本地数据处理黑科技")

# Show Sidebar Status
show_status_bar()

# Run Navigation
pg.run()
