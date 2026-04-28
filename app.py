import streamlit as st

st.set_page_config(
    page_title="Bullets Over Hugs",
    page_icon="🔫",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Bullets Over Hugs")
st.subheader("Data Visualization — Assignment 3")

st.markdown(
    """
    Welcome to **Bullets Over Hugs**, an interactive data visualization dashboard
    exploring patterns in global gun violence and social indicators.

    Use the sidebar to navigate between pages.
    """
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Countries Covered", value="195")

with col2:
    st.metric(label="Years of Data", value="20+")

with col3:
    st.metric(label="Indicators Tracked", value="50+")

st.divider()
st.caption("UTS — Data Visualization | Semester 2, 2026")
