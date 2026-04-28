import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

st.title("📊 Overview")
st.markdown("High-level summary of the dataset.")

st.divider()

# Placeholder data — replace with real dataset
np.random.seed(42)
years = list(range(2000, 2024))
countries = ["USA", "Brazil", "Australia", "Germany", "India", "Mexico"]

records = []
for country in countries:
    for year in years:
        records.append(
            {
                "Country": country,
                "Year": year,
                "Gun Deaths per 100k": round(np.random.uniform(0.5, 15), 2),
                "Happiness Index": round(np.random.uniform(3, 8), 2),
            }
        )

df = pd.DataFrame(records)

# Sidebar filters
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Select countries", options=countries, default=countries[:3]
)
year_range = st.sidebar.slider("Year range", 2000, 2023, (2005, 2023))

filtered = df[
    (df["Country"].isin(selected_countries))
    & (df["Year"].between(*year_range))
]

# Charts
col1, col2 = st.columns(2)

with col1:
    fig = px.line(
        filtered,
        x="Year",
        y="Gun Deaths per 100k",
        color="Country",
        title="Gun Deaths per 100k Over Time",
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.scatter(
        filtered,
        x="Happiness Index",
        y="Gun Deaths per 100k",
        color="Country",
        size="Gun Deaths per 100k",
        hover_data=["Year"],
        title="Gun Deaths vs Happiness Index",
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.dataframe(filtered, use_container_width=True, hide_index=True)
