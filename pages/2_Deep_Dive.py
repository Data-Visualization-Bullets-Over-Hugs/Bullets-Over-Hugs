import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Deep Dive", page_icon="🔍", layout="wide")

st.title("🔍 Deep Dive")
st.markdown("Drill down into individual countries and correlations.")

st.divider()

# Placeholder data — replace with real dataset
np.random.seed(7)
years = list(range(2000, 2024))
countries = ["USA", "Brazil", "Australia", "Germany", "India", "Mexico"]
indicators = ["Gun Deaths per 100k", "Homicide Rate", "GDP per Capita", "Happiness Index", "Gini Coefficient"]

records = []
for country in countries:
    for year in years:
        row = {"Country": country, "Year": year}
        for ind in indicators:
            row[ind] = round(np.random.uniform(1, 100), 2)
        records.append(row)

df = pd.DataFrame(records)

# Sidebar
st.sidebar.header("Configuration")
country = st.sidebar.selectbox("Country", options=countries)
x_axis = st.sidebar.selectbox("X axis", options=indicators, index=3)
y_axis = st.sidebar.selectbox("Y axis", options=indicators, index=0)

country_df = df[df["Country"] == country]

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        country_df,
        x="Year",
        y=y_axis,
        title=f"{y_axis} — {country}",
        color=y_axis,
        color_continuous_scale="Reds",
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.scatter(
        country_df,
        x=x_axis,
        y=y_axis,
        trendline="ols",
        title=f"{x_axis} vs {y_axis} — {country}",
        hover_data=["Year"],
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("Correlation Matrix")
numeric_df = country_df[indicators]
corr = numeric_df.corr().round(2)

fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title=f"Correlation Matrix — {country}",
    zmin=-1,
    zmax=1,
)
st.plotly_chart(fig_corr, use_container_width=True)
