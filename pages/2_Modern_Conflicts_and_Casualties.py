import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Modern Conflicts and Casualties",
    page_icon="🌍",
    layout="wide"
)

# =========================================================
# Data loading
# =========================================================
@st.cache_data
def load_data():
    country_year = pd.read_csv("data/conflict_deaths_country_year.csv")
    by_type = pd.read_csv("data/conflict_deaths_by_type.csv")
    summary = pd.read_csv("data/conflict_deaths_summary.csv")
    return country_year, by_type, summary

country_year_df, by_type_df, summary_df = load_data()

# =========================================================
# Styling
# =========================================================
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #08152f 0%, #050b18 45%, #040812 100%);
        color: #edf2f4;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        max-width: 1380px;
    }

    h1, h2, h3 {
        color: #edf2f4 !important;
        letter-spacing: -0.02em;
    }

    .page-subtitle {
        color: #cbd5e1;
        font-size: 1.05rem;
        margin-top: -0.45rem;
        margin-bottom: 1.1rem;
    }

    .section-intro {
        color: #b8c1cc;
        font-size: 0.95rem;
        margin-bottom: 0.8rem;
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.035) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 14px 16px 10px 16px;
        box-shadow: 0 10px 26px rgba(0,0,0,0.20);
        min-height: 112px;
    }

    .metric-label {
        font-size: 0.84rem;
        color: #b8c1cc;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 1.95rem;
        font-weight: 700;
        color: #edf2f4;
        line-height: 1.05;
    }

    .metric-note {
        font-size: 0.80rem;
        color: #94a3b8;
        margin-top: 7px;
    }

    .panel {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        padding: 14px 16px 8px 16px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.14);
    }

    .method-box {
        background: linear-gradient(90deg, rgba(217,4,41,0.18), rgba(239,35,60,0.08));
        border-left: 4px solid #ef233c;
        border-radius: 12px;
        padding: 14px 16px;
        color: #edf2f4;
        font-size: 0.92rem;
        line-height: 1.55;
        margin-top: 0.5rem;
    }

    .small-note {
        color: #94a3b8;
        font-size: 0.82rem;
        margin-top: -0.15rem;
        margin-bottom: 0.75rem;
    }

    div[data-testid="stSlider"] label,
    div[data-testid="stSelectbox"] label {
        color: #edf2f4 !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# Helpers
# =========================================================
METRIC_OPTIONS = {
    "Total deaths": "total_deaths",
    "Civilian deaths": "civilian_deaths",
    "Combatant deaths": "combatant_deaths",
    "Unclear deaths": "unclear_deaths"
}

TYPE_COLOR_MAP = {
    "Interstate": "#ff4d6d",
    "Intrastate": "#ef233c",
    "Non-state": "#ff8fa3",
    "One-sided violence": "#ffc2d1"
}

def fmt_num(x):
    return f"{int(x):,}" if pd.notna(x) else "0"

def metric_card(label, value, note=""):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """

# =========================================================
# Title
# =========================================================
st.title("Page 2: Modern Conflicts and Casualties (2015–2024)")
st.markdown(
    '<div class="page-subtitle">Which is the human cost of the modern arms race?</div>',
    unsafe_allow_html=True
)

# =========================================================
# Controls
# =========================================================
years = sorted(country_year_df["year"].unique().tolist())

c1, c2, c3 = st.columns([1.15, 1.1, 1.0])

with c1:
    selected_year = st.slider(
        "Timeline",
        min_value=min(years),
        max_value=max(years),
        value=max(years),
        step=1
    )

with c2:
    selected_metric_label = st.selectbox(
        "Death metric",
        list(METRIC_OPTIONS.keys()),
        index=0
    )
    selected_metric = METRIC_OPTIONS[selected_metric_label]

with c3:
    top_n = st.selectbox(
        "Top countries to highlight",
        [5, 8, 10, 12, 15],
        index=2
    )

filtered_year = country_year_df[country_year_df["year"] == selected_year].copy()
filtered_year["metric_value"] = filtered_year[selected_metric].fillna(0)

map_df = filtered_year[filtered_year["metric_value"] > 0].copy()

# =========================================================
# KPI calculations
# =========================================================
year_total = int(filtered_year["metric_value"].sum())
countries_with_conflict = int((filtered_year["metric_value"] > 0).sum())

if not map_df.empty:
    deadliest_row = map_df.sort_values("metric_value", ascending=False).iloc[0]
    deadliest_country = deadliest_row["country"]
    deadliest_value = int(deadliest_row["metric_value"])
else:
    deadliest_country = "N/A"
    deadliest_value = 0

trend_df = country_year_df.groupby("year", as_index=False)["total_deaths"].sum()
worst_year_row = trend_df.sort_values("total_deaths", ascending=False).iloc[0]
worst_year = int(worst_year_row["year"])
worst_year_total = int(worst_year_row["total_deaths"])

# =========================================================
# KPI row
# =========================================================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        metric_card(
            f"{selected_metric_label} in {selected_year}",
            fmt_num(year_total),
            "Direct conflict-related deaths"
        ),
        unsafe_allow_html=True
    )
with k2:
    st.markdown(
        metric_card(
            "Countries with recorded conflict",
            fmt_num(countries_with_conflict),
            f"Countries with >0 {selected_metric_label.lower()}"
        ),
        unsafe_allow_html=True
    )
with k3:
    st.markdown(
        metric_card(
            "Deadliest country this year",
            deadliest_country,
            f"{fmt_num(deadliest_value)} {selected_metric_label.lower()}"
        ),
        unsafe_allow_html=True
    )
with k4:
    st.markdown(
        metric_card(
            "Deadliest year overall",
            str(worst_year),
            f"{fmt_num(worst_year_total)} total deaths"
        ),
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# =========================================================
# Main map panel
# =========================================================
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.subheader("Global Conflict Deaths Map")
st.markdown(
    '<div class="section-intro">The map shows where direct conflict deaths were concentrated in the selected year, with bubble size indicating the scale of human loss.</div>',
    unsafe_allow_html=True
)

if map_df.empty:
    st.warning("No non-zero values are available for the selected year and selected metric.")
else:
    top_labels_df = (
        map_df.sort_values("metric_value", ascending=False)
        .head(min(top_n, len(map_df)))
        .copy()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scattergeo(
            lon=map_df["longitude"],
            lat=map_df["latitude"],
            text=map_df["country"],
            customdata=map_df[[
                "country", "year", "total_deaths",
                "civilian_deaths", "combatant_deaths", "unclear_deaths",
                "metric_value"
            ]],
            mode="markers",
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Year: %{customdata[1]}<br>"
                + selected_metric_label + ": %{customdata[6]:,.0f}<br>"
                + "Total deaths: %{customdata[2]:,.0f}<br>"
                + "Civilian deaths: %{customdata[3]:,.0f}<br>"
                + "Combatant deaths: %{customdata[4]:,.0f}<br>"
                + "Unclear deaths: %{customdata[5]:,.0f}"
                + "<extra></extra>"
            ),
            marker=dict(
                size=(map_df["metric_value"] ** 0.35).clip(lower=3) * 1.2,
                color="rgba(239,35,60,0.72)",
                line=dict(color="rgba(217,4,41,0.95)", width=1),
                sizemode="diameter"
            ),
            showlegend=False
        )
    )

    fig.add_trace(
        go.Scattergeo(
            lon=top_labels_df["longitude"],
            lat=top_labels_df["latitude"],
            text=top_labels_df["country"],
            mode="text",
            textfont=dict(color="#edf2f4", size=11),
            textposition="top center",
            hoverinfo="skip",
            showlegend=False
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=670,
        geo=dict(
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)",
            showframe=False,
            showcoastlines=False,
            showland=True,
            landcolor="#aab4c5",
            showocean=True,
            oceancolor="#030d24",
            showcountries=True,
            countrycolor="#3b4658",
            lakecolor="#030d24"
        ),
        font=dict(color="#edf2f4")
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# =========================================================
# Lower row: timeline + ranking
# =========================================================
left_col, right_col = st.columns([1.35, 0.95], gap="large")

with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Timeline of Total Conflict Deaths")
    st.markdown(
        '<div class="small-note">The dashed marker shows the currently selected year.</div>',
        unsafe_allow_html=True
    )

    timeline_fig = go.Figure()
    timeline_fig.add_trace(
        go.Scatter(
            x=trend_df["year"],
            y=trend_df["total_deaths"],
            mode="lines+markers",
            line=dict(color="#ff2447", width=3),
            marker=dict(size=8, color="#ff2447"),
            hovertemplate="<b>Year %{x}</b><br>Total deaths: %{y:,}<extra></extra>"
        )
    )

    timeline_fig.add_vline(
        x=selected_year,
        line_width=2,
        line_dash="dash",
        line_color="#e2e8f0"
    )

    timeline_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350,
        margin=dict(l=10, r=10, t=10, b=5),
        font=dict(color="#edf2f4"),
        xaxis=dict(
            title="Year",
            showgrid=False,
            tickmode="linear"
        ),
        yaxis=dict(
            title="Total deaths",
            gridcolor="rgba(255,255,255,0.09)",
            zeroline=False
        )
    )

    st.plotly_chart(timeline_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader(f"Top {top_n} Countries in {selected_year}")

    top_df = (
        filtered_year[filtered_year["metric_value"] > 0]
        .sort_values("metric_value", ascending=False)
        .head(top_n)
        .sort_values("metric_value", ascending=True)
        .copy()
    )

    if top_df.empty:
        st.info("No countries to display for the selected year.")
    else:
        top_bar = px.bar(
            top_df,
            x="metric_value",
            y="country",
            orientation="h",
            text="metric_value"
        )

        top_bar.update_traces(
            marker_color="#ff2447",
            texttemplate="%{text:,}",
            textposition="outside",
            cliponaxis=False
        )

        top_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=10, r=45, t=10, b=5),
            font=dict(color="#edf2f4"),
            xaxis=dict(
                title=selected_metric_label,
                gridcolor="rgba(255,255,255,0.09)",
                zeroline=False
            ),
            yaxis=dict(title=None)
        )

        st.plotly_chart(top_bar, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# =========================================================
# Conflict-type breakdown
# =========================================================
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.subheader("Conflict-Type Breakdown")
st.markdown(
    '<div class="section-intro">This view shows which kinds of conflict drove deaths in the selected country and year.</div>',
    unsafe_allow_html=True
)

available_countries = sorted(by_type_df["country"].unique().tolist())
default_country = deadliest_country if deadliest_country in available_countries else available_countries[0]

selected_country = st.selectbox(
    "Select a country to inspect conflict composition",
    available_countries,
    index=available_countries.index(default_country)
)

country_type_df = by_type_df[
    (by_type_df["country"] == selected_country) &
    (by_type_df["year"] == selected_year)
].copy()

if country_type_df.empty or country_type_df["deaths"].sum() == 0:
    st.info(f"No conflict-type deaths recorded for {selected_country} in {selected_year}.")
else:
    country_type_df = country_type_df.sort_values("deaths", ascending=True)

    type_fig = px.bar(
        country_type_df,
        x="deaths",
        y="conflict_type_label",
        orientation="h",
        text="deaths",
        color="conflict_type_label",
        color_discrete_map=TYPE_COLOR_MAP
    )

    type_fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False
    )

    type_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        margin=dict(l=10, r=40, t=10, b=10),
        font=dict(color="#edf2f4"),
        xaxis=dict(
            title="Deaths",
            gridcolor="rgba(255,255,255,0.09)",
            zeroline=False
        ),
        yaxis=dict(title=None),
        legend_title="Conflict type",
        showlegend=True
    )

    st.plotly_chart(type_fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# Method note
# =========================================================
st.markdown(
    """
    <div class="method-box">
        <b>Methodology note:</b> This page uses direct battle-related deaths only. It does not include
        broader indirect deaths from famine, disease, or displacement. Civilian-share interpretation
        should also be treated carefully for some countries, especially where many deaths are classified
        as unclear rather than civilian or combatant.
    </div>
    """,
    unsafe_allow_html=True
)