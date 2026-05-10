import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# Data loading
# =========================================================
@st.cache_data
def load_data():
    # Ensuring data is loaded from the relative 'data/' directory
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

    .metric-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.035) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 12px 14px 8px 14px;
        box-shadow: 0 10px 26px rgba(0,0,0,0.20);
        min-height: 100px;
    }

    /* Fixed Panel Styling using Streamlit native containers to avoid the 'long rounded square' issue */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.025) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 18px !important;
        padding: 1.2rem !important;
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
        margin-top: 1.5rem;
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

def fmt_num(x):
    return f"{int(x):,}" if pd.notna(x) else "0"

def metric_card(label, value, note=""):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note" style="font-size: 0.75rem; color: #94a3b8; margin-top: 6px;">{note}</div>
    </div>
    """

# =========================================================
# Header & Controls
# =========================================================
st.title("Modern Conflicts and Casualties (2015–2024)")
st.markdown('<div class="page-subtitle">Which is the human cost of the modern arms race?</div>', unsafe_allow_html=True)

years = sorted(country_year_df["year"].unique().tolist())
c1, c2, c3, c4 = st.columns([1.1, 1.1, 1.1, 1.0])

with c1:
    selected_year = st.slider("Timeline", min_value=min(years), max_value=max(years), value=max(years), step=1)
with c2:
    selected_metric_label = st.selectbox("Death metric", list(METRIC_OPTIONS.keys()), index=0)
    selected_metric = METRIC_OPTIONS[selected_metric_label]
with c3:
    type_options = ["All"] + sorted(by_type_df["conflict_type_label"].dropna().unique().tolist())
    selected_type = st.selectbox("Conflict type", type_options, index=0)
with c4:
    top_n_options = [5, 8, 10, 12, 15, "All"]
    top_n = st.selectbox("Top countries to highlight", top_n_options, index=2)

# =========================================================
# Data Integration
# =========================================================
if selected_type == "All":
    base_df = country_year_df.copy()
else:
    type_data = by_type_df[by_type_df["conflict_type_label"] == selected_type].copy()
    demographics = country_year_df[["country", "year", "civilian_deaths", "combatant_deaths", "unclear_deaths"]]
    base_df = type_data.merge(demographics, on=["country", "year"], how="left")
    base_df["total_deaths"] = base_df["deaths"].fillna(0)
    
    for col in ["latitude", "longitude", "civilian_deaths", "combatant_deaths", "unclear_deaths"]:
        base_df[col] = base_df[col].fillna(0) if col in base_df.columns else 0
    if selected_metric not in base_df.columns:
        base_df[selected_metric] = base_df["total_deaths"]

filtered_year = base_df[base_df["year"] == selected_year].copy()
filtered_year["metric_value"] = filtered_year[selected_metric].fillna(0)

# Full map data for global totals
map_df_full = filtered_year[(filtered_year["metric_value"] > 0) & (filtered_year["latitude"] != 0)].copy()

# Filter specific map data based on Top N selection
if top_n == "All":
    map_df_display = map_df_full.copy()
else:
    map_df_display = map_df_full.sort_values("metric_value", ascending=False).head(top_n).copy()

# =========================================================
# KPI Row
# =========================================================
year_total = int(filtered_year["metric_value"].sum())
countries_with_conflict = int((filtered_year["metric_value"] > 0).sum())

if not map_df_full.empty:
    deadliest_row = map_df_full.sort_values("metric_value", ascending=False).iloc[0]
    deadliest_country, deadliest_value = deadliest_row["country"], int(deadliest_row["metric_value"])
else:
    deadliest_country, deadliest_value = "N/A", 0

k1, k2, k3 = st.columns(3)
with k1: st.markdown(metric_card(f"{selected_metric_label} ({selected_year})", fmt_num(year_total), "Conflict-related deaths"), unsafe_allow_html=True)
with k2: st.markdown(metric_card("Conflict Zones", fmt_num(countries_with_conflict), "Unique countries with deaths"), unsafe_allow_html=True)
with k3: st.markdown(metric_card("Deadliest Country", deadliest_country, f"{fmt_num(deadliest_value)} {selected_metric_label.lower()}"), unsafe_allow_html=True)

st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

# =========================================================
# Map Section (Bubbles and labels filtered to Top N)
# =========================================================
with st.container(border=True):
    st.subheader("Global Conflict Deaths Map")
    if not map_df_display.empty:
        fig = go.Figure()
        
        # Trace 1: Bubbles (Circles) - ONLY for Top N
        fig.add_trace(go.Scattergeo(
            lon=map_df_display["longitude"], lat=map_df_display["latitude"], text=map_df_display["country"],
            customdata=map_df_display[["country", "year", "total_deaths", "civilian_deaths", "combatant_deaths", "unclear_deaths"]],
            mode="markers",
            marker=dict(
                size=(map_df_display["metric_value"] ** 0.35).clip(lower=3) * 1.2, 
                color="rgba(239,35,60,0.72)", 
                line=dict(color="rgba(217,4,41,0.95)", width=1)
            ),
            hovertemplate=(
                "<b style='font-size:15px;color:#edf2f4;'>%{customdata[0]}</b>"
                "&nbsp;&nbsp;<span style='font-size:10px;color:#64748b;'>%{customdata[1]}</span>"
                "<br><span style='color:#2a3550;'>━━━━━━━━━━━━━━━━━━━━━━</span>"
                "<br><span style='font-size:10px;color:#94a3b8;'>TOTAL DEATHS</span>"
                "<br><span style='font-size:4px;'>​</span>"
                "<br><b style='font-size:22px;color:#ff2447;'>%{customdata[2]:,}</b>"
                "<br><span style='color:#2a3550;'>━━━━━━━━━━━━━━━━━━━━━━</span>"
                "<br><span style='font-size:11px;color:#94a3b8;'>👥 Civilian: </span>"
                "<b style='font-size:11px;color:#cbd5e1;'>%{customdata[3]:,}</b>"
                "<br><span style='font-size:11px;color:#94a3b8;'>⚔️ Combatant: </span>"
                "<b style='font-size:11px;color:#cbd5e1;'>%{customdata[4]:,}</b>"
                "<br><span style='font-size:11px;color:#94a3b8;'>❓ Unclear: </span>"
                "<b style='font-size:11px;color:#cbd5e1;'>%{customdata[5]:,}</b>"
                "<extra></extra>"
            ),
            hoverlabel=dict(
                bgcolor="rgba(4,9,20,0.97)",
                bordercolor="rgba(239,35,60,0.5)",
                font=dict(color="#edf2f4", size=12, family="system-ui, -apple-system, sans-serif"),
                namelength=0,
                align="left",
            ),
            showlegend=False
        ))
        
        # Trace 2: Labels (Names) - ONLY for Top N
        fig.add_trace(go.Scattergeo(
            lon=map_df_display["longitude"], lat=map_df_display["latitude"], text=map_df_display["country"],
            mode="text",
            textfont=dict(color="#edf2f4", size=10),
            textposition="top center",
            hoverinfo="skip",
            showlegend=False
        ))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=10, b=0), height=550,
            geo=dict(
                projection_type="natural earth", 
                bgcolor="rgba(0,0,0,0)", 
                showland=True, landcolor="#aab4c5", 
                showocean=True, oceancolor="#030d24", 
                countrycolor="#3b4658"
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No recorded conflict data for this selection.")

# =========================================================
# Lower Charts Row
# =========================================================
trend_df = base_df[base_df["total_deaths"] > 0].groupby("year", as_index=False).agg({"total_deaths": "sum", "country": "nunique"})
trend_df.rename(columns={"country": "active_countries_count"}, inplace=True)

left_col, right_col = st.columns([1.3, 1.0], gap="medium")

with left_col:
    # 1. Total Deaths Timeline
    with st.container(border=True):
        st.subheader("Timeline of Total Conflict Deaths")
        t_fig = px.line(trend_df, x="year", y="total_deaths", markers=True,
                        labels={"year": "Year", "total_deaths": "Total Deaths"})
        t_fig.update_traces(
            line_color="#ff2447",
            marker=dict(size=8, color="#ff2447", line=dict(color="rgba(217,4,41,0.95)", width=1)),
            hovertemplate=(
                "<span style='font-size:10px;color:#94a3b8;'>TOTAL DEATHS</span>"
                "<br><span style='font-size:4px;'>​</span>"
                "<br><b style='font-size:22px;color:#ff2447;'>%{y:,}</b>"
                "<br><span style='color:#2a3550;'>━━━━━━━━━━━━━━━━</span>"
                "<br><span style='font-size:10px;color:#64748b;'>Year: %{x}</span>"
                "<extra></extra>"
            ),
            hoverlabel=dict(
                bgcolor="rgba(4,9,20,0.97)",
                bordercolor="rgba(239,35,60,0.5)",
                font=dict(color="#edf2f4", size=12, family="system-ui, sans-serif"),
                namelength=0,
                align="left",
            ),
        )
        t_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                            height=280, font=dict(color="#edf2f4"), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(t_fig, use_container_width=True)

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # 2. Unique Countries Timeline
    with st.container(border=True):
        st.subheader("Timeline of Unique Countries in Conflict")
        c_fig = px.line(trend_df, x="year", y="active_countries_count", markers=True,
                        labels={"year": "Year", "active_countries_count": "Active Countries"})
        c_fig.update_traces(
            line_color="#ff2447",
            marker=dict(size=8, color="#ff2447", line=dict(color="rgba(217,4,41,0.95)", width=1)),
            hovertemplate=(
                "<span style='font-size:10px;color:#94a3b8;'>ACTIVE CONFLICT ZONES</span>"
                "<br><span style='font-size:4px;'>​</span>"
                "<br><b style='font-size:22px;color:#ff2447;'>%{y}</b>"
                "<span style='font-size:13px;color:#94a3b8;'> countries</span>"
                "<br><span style='color:#2a3550;'>━━━━━━━━━━━━━━━━</span>"
                "<br><span style='font-size:10px;color:#64748b;'>Year: %{x}</span>"
                "<extra></extra>"
            ),
            hoverlabel=dict(
                bgcolor="rgba(4,9,20,0.97)",
                bordercolor="rgba(239,35,60,0.5)",
                font=dict(color="#edf2f4", size=12, family="system-ui, sans-serif"),
                namelength=0,
                align="left",
            ),
        )
        c_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                            height=280, font=dict(color="#edf2f4"), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(c_fig, use_container_width=True)

with right_col:
    # 3. Country Ranking Bar Chart
    with st.container(border=True):
        st.subheader(f"Country Ranking ({selected_year})")
        # Ranking also reflects Top N for consistency
        rank_n = len(map_df_full) if top_n == "All" else top_n
        top_df = map_df_full.sort_values("metric_value", ascending=False).head(rank_n)
        
        r_fig = px.bar(top_df, x="metric_value", y="country", orientation="h",
                       labels={"metric_value": selected_metric_label, "country": "Country"},
                       text_auto=',.0f')
        r_fig.update_traces(
            marker_color="#ff2447",
            hovertemplate=(
                "<b style='font-size:14px;color:#edf2f4;'>%{y}</b>"
                "<br><span style='color:#2a3550;'>━━━━━━━━━━━━━━━━━━━━</span>"
                "<br><span style='font-size:10px;color:#94a3b8;'>" + selected_metric_label.upper() + "</span>"
                "<br><span style='font-size:4px;'>​</span>"
                "<br><b style='font-size:22px;color:#ff2447;'>%{x:,}</b>"
                "<extra></extra>"
            ),
            hoverlabel=dict(
                bgcolor="rgba(4,9,20,0.97)",
                bordercolor="rgba(239,35,60,0.5)",
                font=dict(color="#edf2f4", size=12, family="system-ui, sans-serif"),
                namelength=0,
                align="left",
            ),
        )
        r_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                            height=605, font=dict(color="#edf2f4"), 
                            margin=dict(l=10, r=40, t=30, b=10), yaxis=dict(autorange="reversed"))
        st.plotly_chart(r_fig, use_container_width=True)

st.markdown('<div class="method-box"><b>Methodology note:</b> Data reflects direct battle-related deaths only and excludes indirect casualties.</div>', unsafe_allow_html=True)