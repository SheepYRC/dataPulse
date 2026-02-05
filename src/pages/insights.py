import streamlit as st
import pandas as pd

def show():
    st.title("🔍 可视化探索 (Insights Engine)")
    st.write("快速生成图表并进行深度探索。")
    
    if 'last_query_result' not in st.session_state:
        st.warning("请先在 SQL 实验室执行查询以获取数据。")
        return

    df = st.session_state['last_query_result'].to_pandas()
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("配置")
        chart_type = st.selectbox("图表类型", ["折线图", "柱状图", "散点图", "区域图"])
        columns = df.columns.tolist()
        x_axis = st.selectbox("X 轴", columns)
        y_axis = st.multiselect("Y 轴", columns, default=columns[1] if len(columns) > 1 else columns[0])
    
    with col2:
        st.subheader("预览")
        if chart_type == "折线图":
            st.line_chart(df, x=x_axis, y=y_axis)
        elif chart_type == "柱状图":
            st.bar_chart(df, x=x_axis, y=y_axis)
        elif chart_type == "区域图":
            st.area_chart(df, x=x_axis, y=y_axis)
        elif chart_type == "散点图":
            st.scatter_chart(df, x=x_axis, y=y_axis)

    st.divider()
    if st.button("📤 导出为 HTML 报告"):
        st.info("导出功能开发中...")
