import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ─── Page config ───
st.set_page_config(
    page_title="The Opportunity Cost Calculator",
    page_icon="💰",
    layout="wide",
)

# ─── Theme colours (matching group spec) ───
BG_DARK = "#2b2d42"
GREY = "#8d99ae"
CRIMSON = "#ef233c"
OFF_WHITE = "#edf2f4"
CARD_BG = "#3a3d56"

# ─── Country flag emoji map ───
FLAGS = {
    "United States": "🇺🇸", "China": "🇨🇳", "Russia": "🇷🇺",
    "India": "🇮🇳", "Germany": "🇩🇪", "United Kingdom": "🇬🇧",
    "Saudi Arabia": "🇸🇦", "France": "🇫🇷", "Ukraine": "🇺🇦",
    "Japan": "🇯🇵", "South Korea": "🇰🇷", "Israel": "🇮🇱",
    "Poland": "🇵🇱", "Italy": "🇮🇹", "Australia": "🇦🇺",
    "Canada": "🇨🇦", "Türkiye": "🇹🇷", "Spain": "🇪🇸",
    "Netherlands": "🇳🇱", "Algeria": "🇩🇿", "Brazil": "🇧🇷",
    "Mexico": "🇲🇽", "Rest of World": "🌍",
}

# ─── Custom CSS ───
st.markdown(f"""
<style>
    .stApp {{
        background-color: {BG_DARK};
        color: {OFF_WHITE};
    }}
    section[data-testid="stSidebar"] {{
        background-color: #1f2033;
    }}
    section[data-testid="stSidebar"] .stMarkdown {{
        color: {OFF_WHITE};
    }}

    /* ── Header ── */
    .page-title {{
        font-size: 3.5vw;
        font-weight: 900;
        color: {OFF_WHITE};
        line-height: 1.1;
        letter-spacing: -2px;
        margin: 0;
        padding-top: 0.5rem;
    }}
    .page-title .hl {{
        color: {CRIMSON};
    }}
    .page-subtitle {{
        font-size: 1.3rem;
        color: {GREY};
        margin-top: 0.6rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }}

    /* ── Section headers ── */
    .section-label {{
        font-size: 1rem;
        font-weight: 700;
        color: {OFF_WHITE};
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.8rem;
    }}

    /* ── Country info ── */
    .country-info {{
        background: {CARD_BG};
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
        border-left: 4px solid {CRIMSON};
    }}
    .country-name {{
        font-size: 1.4rem;
        font-weight: 700;
        color: {OFF_WHITE};
    }}
    .country-spend {{
        font-size: 0.95rem;
        color: {GREY};
    }}

    /* ── Calculator header ── */
    .calc-header {{
        font-size: 1.4rem;
        font-weight: 800;
        color: {OFF_WHITE};
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        margin-bottom: 0.5rem;
    }}
    .slider-label {{
        font-size: 1rem;
        color: {GREY};
        margin-bottom: 0.3rem;
    }}

    /* ── Budget display ── */
    .budget-display {{
        background: linear-gradient(135deg, {CRIMSON}22, {CRIMSON}08);
        border: 1px solid {CRIMSON}44;
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        margin: 1rem 0 1.5rem 0;
    }}
    .budget-amount {{
        font-size: 2.4rem;
        font-weight: 800;
        color: {CRIMSON};
    }}
    .budget-label {{
        font-size: 0.8rem;
        color: {GREY};
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* ── Metric cards ── */
    .metric-card {{
        background: {CARD_BG};
        border-radius: 16px;
        padding: 1.5rem 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }}
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }}
    .card-icon {{ font-size: 2.8rem; margin-bottom: 0.5rem; }}
    .card-title {{
        font-size: 0.8rem;
        color: {GREY};
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }}
    .card-value {{
        font-size: 3rem;
        font-weight: 800;
        color: {CRIMSON};
        line-height: 1.1;
    }}
    .card-unit {{
        font-size: 0.9rem;
        color: {OFF_WHITE};
        opacity: 0.85;
        margin-top: 0.4rem;
        font-weight: 600;
    }}
    .card-sub {{
        font-size: 0.75rem;
        color: {GREY};
        margin-top: 0.6rem;
        line-height: 1.4;
    }}

    .section-divider {{
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 1rem 0;
    }}

    .stSelectbox label, .stSlider label {{
        color: {OFF_WHITE} !important;
        font-weight: 600 !important;
    }}
    div[data-baseweb="select"] {{
        background-color: {CARD_BG};
    }}

    .source-footer {{
        font-size: 0.7rem;
        color: {GREY};
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.06);
    }}
    .source-footer a {{ color: {GREY}; }}
</style>
""", unsafe_allow_html=True)

# ─── Load data ───
@st.cache_data
def load_data():
    mil = pd.read_csv("data/military_spending.csv")
    realloc = pd.read_csv("data/reallocation_costs.csv")
    return mil, realloc

mil_df, realloc_df = load_data()

# ━━━ HEADER ━━━
st.markdown("""
<p class="page-title"><span class="hl">Page 1:</span> The Opportunity Cost Calculator</p>
<p class="page-subtitle">What is the re-allocation impact? Translating military budgets into tangible global development metrics.</p>
""", unsafe_allow_html=True)

# ━━━ LAYOUT ━━━
left_col, right_col = st.columns([1.1, 1.4], gap="large")

# ─── LEFT PANEL ───
with left_col:
    st.markdown('<p class="section-label">Global Military Expenditure 2024</p>', unsafe_allow_html=True)

    country_list = mil_df["country"].tolist()
    selected_country = st.selectbox(
        "Select a country",
        country_list,
        index=0,
        help="Choose a country to explore its military spending",
    )

    row = mil_df[mil_df["country"] == selected_country].iloc[0]
    spend_total = row["total"]
    spend_label = row["label"]
    flag = FLAGS.get(selected_country, "")

    st.markdown(f"""
    <div class="country-info">
        <div class="country-name">{flag} {selected_country}</div>
        <div class="country-spend">Military Spending: <strong>{spend_label}</strong> (2024, constant USD)</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Treemap (packed-bubble style) ──
    labels_tree = []
    values_tree = []
    colors_tree = []
    text_tree = []

    for _, r in mil_df.iterrows():
        c = r["country"]
        f = FLAGS.get(c, "")
        labels_tree.append(c)
        values_tree.append(r["total"])
        text_tree.append(f"{f}<br><b>{c}</b><br>{r['label']}")
        colors_tree.append(CRIMSON if c == selected_country else GREY)

    fig = go.Figure(go.Treemap(
        labels=labels_tree,
        parents=[""] * len(labels_tree),
        values=values_tree,
        text=text_tree,
        textinfo="text",
        textfont=dict(size=13, color=OFF_WHITE),
        marker=dict(
            colors=colors_tree,
            line=dict(width=2, color=BG_DARK),
        ),
        hovertemplate="<b>%{label}</b><br>%{value:$,.0f}<extra></extra>",
    ))
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=480,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ─── RIGHT PANEL ───
with right_col:
    st.markdown('<p class="calc-header">Interactive Calculator: Re-Allocation Impact</p>', unsafe_allow_html=True)

    st.markdown('<p class="slider-label">Select a percentage of the defence budget to re-allocate:</p>', unsafe_allow_html=True)
    pct = st.slider(
        "Budget %",
        min_value=0,
        max_value=20,
        value=5,
        step=1,
        format="%d%%",
        label_visibility="collapsed",
    )

    reallocated = spend_total * (pct / 100)

    if reallocated >= 1e9:
        realloc_display = f"${reallocated / 1e9:.1f}B"
    elif reallocated >= 1e6:
        realloc_display = f"${reallocated / 1e6:.0f}M"
    else:
        realloc_display = f"${reallocated:,.0f}"

    st.markdown(f"""
    <div class="budget-display">
        <div class="budget-label">Re-allocated Budget ({pct}% of {spend_label})</div>
        <div class="budget-amount">{realloc_display}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ── Initiative cards ──
    initiatives = [
        {
            "name": "NASA Artemis Missions",
            "icon": "🚀",
            "cost": 93_000_000_000,
            "unit_label": "Full Artemis Programs",
            "sub": "Complete lunar exploration programme ($93B)",
        },
        {
            "name": "Global Internet Connection",
            "icon": "🌐",
            "cost": 428_000_000_000,
            "unit_label": "of Global Coverage",
            "sub": "Connecting unserved populations worldwide ($428B)",
        },
        {
            "name": "Global WASH Infrastructure",
            "icon": "💧",
            "cost": 114_000_000_000,
            "unit_label": "of WASH Programs",
            "sub": "Universal clean water & sanitation ($114B)",
        },
        {
            "name": "Global AI Investment",
            "icon": "🧠",
            "cost": 252_000_000_000,
            "unit_label": "of Global AI Investment",
            "sub": "New AI data centers & research ($252B)",
        },
    ]

    row1_cols = st.columns(2)
    row2_cols = st.columns(2)
    card_cols = [row1_cols[0], row1_cols[1], row2_cols[0], row2_cols[1]]

    for idx, init in enumerate(initiatives):
        with card_cols[idx]:
            if reallocated > 0:
                times = reallocated / init["cost"]
                pct_funded = (reallocated / init["cost"]) * 100

                if times >= 1:
                    value_display = f"{times:.1f}×"
                    unit_display = init["unit_label"]
                else:
                    value_display = f"{pct_funded:.0f}%"
                    unit_display = init["unit_label"]
            else:
                value_display = "—"
                unit_display = "Move the slider"

            st.markdown(f"""
            <div class="metric-card">
                <div class="card-icon">{init["icon"]}</div>
                <div class="card-title">{init["name"]}</div>
                <div class="card-value">{value_display}</div>
                <div class="card-unit">{unit_display}</div>
                <div class="card-sub">{init["sub"]}</div>
            </div>
            """, unsafe_allow_html=True)

# ━━━ FOOTER ━━━
st.markdown("""
<div class="source-footer">
    Data: <a href="https://www.sipri.org/databases/milex" target="_blank">SIPRI Military Expenditure Database</a> (2023 constant USD) &nbsp;|&nbsp;
    <a href="https://oig.nasa.gov/docs/IG-22-003.pdf" target="_blank">NASA OIG</a> &nbsp;|&nbsp;
    <a href="https://www.itu.int" target="_blank">ITU</a> &nbsp;|&nbsp;
    <a href="https://www.unicef.org/wash" target="_blank">UNICEF WASH</a> &nbsp;|&nbsp;
    <a href="https://aiindex.stanford.edu/report/" target="_blank">Stanford HAI</a>
</div>
""", unsafe_allow_html=True)