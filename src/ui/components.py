import streamlit as st

def custom_card(title, content, icon="default"):
    """Placeholder for custom UI components."""
    with st.container(border=True):
        st.markdown(f"### {title}")
        st.write(content)
