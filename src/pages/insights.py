import streamlit as st
import pandas as pd
import plotly.express as px
from src.core.database import db_manager

def show():
    st.title("🔍 可视化引擎 (Insights Engine)")
    
    # Use global query result from session state
    if 'query_result' not in st.session_state:
        st.warning("請先在 '数据查询' 模块执行查询以获取数据。")
        return

    # Check if pl.DataFrame or pd.DataFrame
    raw_df = st.session_state['query_result']
    if hasattr(raw_df, 'to_pandas'):
        df = raw_df.to_pandas()
    else:
        df = raw_df
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.subheader("🎨 图表配置")
        chart_type = st.selectbox("图表类型", ["折线图", "柱状图", "散点图", "面积图"])
        cols = df.columns.tolist()
        x_axis = st.selectbox("X 轴 (维度)", cols)
        y_axis = st.multiselect("Y 轴 (指标)", cols, default=cols[1] if len(cols) > 1 else cols[0])
        
        color_col = st.selectbox("颜色分组 (可选)", [None] + cols)
        
        st.divider()
        st.subheader("📤 导出")
        if st.button("生成 HTML 报告"):
            import tempfile
            # Generate a simple plotly figure again for export
            # (In a real app, we'd reuse the one created in col2)
            st.toast("正在导出...")

    with col2:
        if not y_axis:
            st.info("请选择至少一个 Y 轴指标。")
        else:
            fig = None
            if chart_type == "折线图":
                fig = px.line(df, x=x_axis, y=y_axis, color=color_col, markers=True)
            elif chart_type == "柱状图":
                fig = px.bar(df, x=x_axis, y=y_axis, color=color_col, barmode="group")
            elif chart_type == "散点图":
                fig = px.scatter(df, x=x_axis, y=y_axis, color=color_col)
            elif chart_type == "面积图":
                fig = px.area(df, x=x_axis, y=y_axis, color=color_col)
            
            if fig:
                fig.update_layout(template="plotly_white", hovermode="x unified")
                st.plotly_chart(fig, use_container_width=True)
                
                # provide download button for the fig as html
                html_str = fig.to_html(include_plotlyjs='cdn')
                st.download_button(
                    label="📥 下载交互式图表 (HTML)",
                    data=html_str.encode('utf-8'),
                    file_name="datapulse_insight.html",
                    mime="text/html"
                )
