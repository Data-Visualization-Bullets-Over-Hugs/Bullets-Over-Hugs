import streamlit as st
import pandas as pd

# ─── Import the safe wrapper component ───
from voronoi_wrapper import render_voronoi

# ─── Page Config ───
st.set_page_config(page_title="Opportunity Cost Calculator", layout="wide")

# ─── Session State ───
if "selected_country" not in st.session_state:
    st.session_state.selected_country = "United States"

# ─── Custom CSS & Icon Script ───
st.markdown("""
<script src="https://unpkg.com/lucide@latest"></script>
<style>
    /* 1. Global Layout Adjustments */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }

    /* 2. Typography */
    h1 { 
        margin-bottom: 0px !important; 
        padding-bottom: 0px !important;
    }
    .page-subtitle { 
        color: #cbd5e1; 
        font-size: 1.02rem; 
        margin-top: 0px !important; 
        margin-bottom: 2rem; 
    }

    /* 3. Panel Styling */
    .panel { 
        background: transparent !important; 
        border: none !important; 
        box-shadow: none !important; 
        padding: 0px !important; 
    }

    /* Theme Colors */
    .stApp { 
        background: radial-gradient(circle at top, #08152f 0%, #050b18 45%, #040812 100%); 
        color: #edf2f4; 
    }
    h1, h2, h3 { color: #edf2f4 !important; letter-spacing: -0.02em; }
    
    /* Re-allocation Header */
    .budget-display { 
        background: linear-gradient(180deg, rgba(239,35,60,0.15) 0%, rgba(217,4,41,0.05) 100%); 
        border: 1px solid rgba(239,35,60,0.3); 
        border-radius: 16px; 
        padding: 1.2rem; 
        text-align: center; 
        margin: 1.5rem 0; 
    }
    .budget-label { font-size: 0.85rem; color: #ef233c; font-weight: 700; letter-spacing: 1px; margin-bottom: 5px; }
    .budget-amount  { font-size: 2.8rem; font-weight: 800; color: #ef233c; line-height: 1.1; }
    
    /* Metric Card Design */
    .metric-card { 
        background: linear-gradient(180deg, rgba(255,255,255,0.035) 0%, rgba(255,255,255,0.02) 100%); 
        border: 1px solid rgba(255,255,255,0.08); 
        border-radius: 16px; 
        padding: 16px; 
        text-align: center; 
        min-height: 170px; 
        margin-bottom: 10px; 
        transition: border 0.3s ease;
    }
    .metric-card:hover {
        border: 1px solid rgba(239,35,60,0.4);
    }
    
    /* Lucide Icon Styling */
    .metric-icon {
        color: #ef233c;
        margin-bottom: 12px;
        display: flex;
        justify-content: center;
    }
    .metric-icon svg {
        width: 32px;
        height: 32px;
        stroke-width: 1.5px;
    }

    .metric-label { font-size: 0.82rem; color: #b8c1cc; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #edf2f4; margin: 4px 0; }
    .metric-note  { font-size: 0.78rem; color: #94a3b8; line-height: 1.3; }
    
    .instruction-text { font-size: 0.85rem; color: #94a3b8; font-style: italic; margin-bottom: 8px; }
    .source-footer { text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 30px; }
</style>
<script>
    // MutationObserver ensures icons are parsed every time Streamlit updates the DOM
    const observer = new MutationObserver(() => {
        if (window.lucide) {
            lucide.createIcons();
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

# ─── Load Data ───
@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/military_spending.csv")
    if "flag_url" not in df.columns:
        df["flag_url"] = None
    return df

mil_df = load_data()

# ─── Build Hierarchical Data ───
hierarchy = {"name": "Global Spending", "children": []}
for continent, group in mil_df.groupby("continent"):
    continent_children = []
    for _, row in group.iterrows():
        continent_children.append({
            "name": row["country"],
            "value": int(row["total"]),
            "label": row["label"],
            "flag_url": row["flag_url"] if pd.notna(row["flag_url"]) and row["flag_url"] else None,
        })
    hierarchy["children"].append({"name": str(continent).upper(), "children": continent_children})

# ─── Pre-compute Logic ───
country_rows = mil_df[mil_df["country"] == st.session_state.selected_country]
spend_total = country_rows.iloc[0]["total"] if not country_rows.empty else 0

# ━━━ HEADER ━━━
st.title("The Opportunity Cost Calculator")
st.markdown('<div class="page-subtitle">Translating global defence spending into sustainable development.</div>', unsafe_allow_html=True)

# ━━━ LAYOUT ━━━
left_col, right_col = st.columns([1.6, 1.0])

# ─── LEFT PANEL ───
with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Global Military Expenditure by Nation (2024)")
    st.markdown('<p class="instruction-text">Click any country to update the calculator.</p>', unsafe_allow_html=True)

    clicked = render_voronoi(
        chart_data=hierarchy, 
        selected_country=st.session_state.selected_country,
        key="voronoi_chart"
    )

    if clicked and clicked != st.session_state.selected_country:
        st.session_state.selected_country = clicked
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ─── RIGHT PANEL ───
with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader(f"Re-Allocation Impact: {st.session_state.selected_country}")

    pct = st.slider("Percentage to re-allocate:", min_value=0, max_value=20, value=5, step=1, format="%d%%")

    if spend_total > 0:
        reallocated = spend_total * (pct / 100)
        
        if reallocated >= 1e9:   r_disp = f"${reallocated / 1e9:.1f}B"
        elif reallocated >= 1e6: r_disp = f"${reallocated / 1e6:.0f}M"
        else:                    r_disp = f"${reallocated:,.0f}"

        st.markdown(
            f'<div class="budget-display">'
            f'<div class="budget-label">RE-ALLOCATED AMOUNT ({pct}% OF BUDGET)</div>'
            f'<div class="budget-amount">{r_disp}</div>'
            f'</div>', 
            unsafe_allow_html=True
        )

        # ─── Representative Icons for Metrics ───
        initiatives = [
            {"name": "NASA ARTEMIS",    "icon": "rocket",           "cost": 93e9,  "sub": "Lunar exploration funding ($93B)"},
            {"name": "GLOBAL INTERNET", "icon": "satellite-dish",   "cost": 428e9, "sub": "High-speed orbital coverage ($428B)"},
            {"name": "GLOBAL WASH",     "icon": "droplets",         "cost": 114e9, "sub": "Clean water & sanitation ($114B)"},
            {"name": "AI INVESTMENT",   "icon": "brain-circuit",    "cost": 252e9, "sub": "GenAI research & data centers ($252B)"},
        ]

        c1, c2 = st.columns(2)
        cols = [c1, c2, c1, c2]

        for idx, init in enumerate(initiatives):
            with cols[idx]:
                times = reallocated / init["cost"] if reallocated > 0 else 0
                val = "0%" if reallocated == 0 else (f"{times:.1f}×" if times >= 1 else f"{times * 100:.0f}%")
                
                st.markdown(
                    f'''
                    <div class="metric-card">
                        <div class="metric-icon">
                            <i data-lucide="{init['icon']}"></i>
                        </div>
                        <div class="metric-label">{init["name"]}</div>
                        <div class="metric-value">{val}</div>
                        <div class="metric-note">{init["sub"]}</div>
                    </div>
                    ''', 
                    unsafe_allow_html=True
                )
    st.markdown('</div>', unsafe_allow_html=True)

# ━━━ FOOTER ━━━
st.markdown('<div class="source-footer">Data: SIPRI Military Expenditure Database</div>', unsafe_allow_html=True)