import streamlit as st
from src.pages import (
    dashboard, statistics, assets, query, 
    process, insights, history, system, search
)
from src.ui.status_bar import show_status_bar

# Page Configuration
st.set_page_config(
    page_title="DataPulse",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 在 main 中指定渲染到 sidebar
with st.sidebar:
    show_status_bar()


pages = {
    "工作台": [
        st.Page(dashboard.show, title="工作看板", icon="🏠", url_path="dashboard"),
        st.Page(statistics.show, title="概况统计", icon="📊", url_path="statistics"),
        st.Page(search.show, title="全局搜索", icon="⌨️", url_path="search"),
    ],
    "数据中心": [
        st.Page(assets.show, title="数据资产", icon="📂", url_path="assets"),
        st.Page(query.show, title="数据查询", icon="🧪", url_path="query"),
        st.Page(process.show, title="数据处理", icon="🛠️", url_path="process"),
    ],
    "洞察与历史": [
        st.Page(insights.show, title="可视化引擎", icon="🔍", url_path="insights"),
        st.Page(history.show, title="历史与快照", icon="📜", url_path="history"),
    ],
    "系统": [
        st.Page(system.show, title="系统管理", icon="⚙️", url_path="system"),
    ]
}

# Navigation Structure (0-8 Modules)
pg = st.navigation(pages)


# Run Navigation
pg.run()
