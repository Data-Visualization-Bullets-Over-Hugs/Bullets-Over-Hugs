import streamlit as st
import pandas as pd
import pydeck as pdk
import time
import math

@st.cache_data
def load_data():
    return pd.read_csv("data/nuke_blast_effects.csv")

# Initialize Session State Variables
if "detonated" not in st.session_state:
    st.session_state.detonated = False
if "animating" not in st.session_state:
    st.session_state.animating = False
if "selected_bomb_idx" not in st.session_state:
    st.session_state.selected_bomb_idx = 0

df = load_data().sort_values("display_order").reset_index(drop=True)

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #08152f 0%, #050b18 45%, #040812 100%);
        color: #edf2f4;
    }

    .block-container {
        padding-top: 1.1rem;
        padding-bottom: 1rem;
        max-width: 1400px;
    }

    h1, h2, h3 {
        color: #edf2f4 !important;
        letter-spacing: -0.02em;
    }

    .page-subtitle {
        color: #cbd5e1;
        font-size: 1.02rem;
        margin-top: -0.45rem;
        margin-bottom: 1rem;
    }

    /* Unifying panels by removing harsh borders and tightening padding */
    .panel {
        background: rgba(8, 15, 30, 0.82);
        border-radius: 18px;
        padding: 10px 12px 10px 12px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.18);
    }

    .control-panel {
        background: linear-gradient(180deg, rgba(8, 15, 30, 0.95) 0%, rgba(12, 22, 40, 0.92) 100%);
        border-radius: 16px;
        padding: 10px 12px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.20);
        height: 100%;
    }

    .small-note {
        color: #94a3b8;
        font-size: 0.84rem;
        line-height: 1.5;
        margin-top: 1rem;
        text-align: center;
    }

    /* Metric Cards */
    .metric-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.045) 0%, rgba(255,255,255,0.015) 100%);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 16px 20px 12px 20px;
        box-shadow: 0 10px 26px rgba(0,0,0,0.25);
        margin-bottom: 16px;
    }

    .metric-label {
        font-size: 0.85rem;
        color: #cbd5e1;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #edf2f4;
        line-height: 1.05;
    }

    .metric-note {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 6px;
    }

    /* Radius Summary Cards - Adjusted for horizontal flex layout */
    .radius-card {
        display: flex;
        align-items: center;
        border: 1px solid;
        border-radius: 12px;
        padding: 10px 12px;
        transition: transform 0.2s;
        flex: 1; /* Forces them to stretch horizontally equally */
        min-width: 140px; /* Prevents them from crushing too tight */
    }
    .radius-card:hover {
        transform: translateY(-2px);
    }
    .radius-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 10px;
        flex-shrink: 0;
        border: 1px solid rgba(255,255,255,0.4);
    }
    .radius-details {
        flex-grow: 1;
    }
    .radius-title {
        font-size: 0.75rem;
        color: #cbd5e1;
        font-weight: 600;
        line-height: 1.2;
    }
    .radius-value {
        font-size: 1rem;
        color: #edf2f4;
        font-weight: 700;
        margin-top: 2px;
    }

    /* Context Card */
    .context-card {
        background: rgba(15, 25, 45, 0.4);
        border-radius: 12px;
        padding: 16px;
        margin-top: 10px;
    }
    .context-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #edf2f4;
        margin-bottom: 8px;
    }
    .context-text {
        font-size: 0.88rem;
        color: #cbd5e1;
        line-height: 1.5;
    }

    .method-box {
        background: linear-gradient(90deg, rgba(217,4,41,0.18), rgba(239,35,60,0.08));
        border-left: 4px solid #ef233c;
        border-radius: 12px;
        padding: 14px 16px;
        color: #edf2f4;
        font-size: 0.92rem;
        line-height: 1.55;
        margin-top: 1rem;
    }

    /* Standardized Selectbox Styles */
    div[data-testid="stSelectbox"] label {
        color: #edf2f4 !important;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.02em;
    }
    
    div[data-testid="stSelectbox"] > div[data-baseweb="select"] {
        background: linear-gradient(180deg, rgba(15, 25, 45, 0.9) 0%, rgba(8, 15, 30, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        cursor: pointer;
    }

    /* Remove Streamlit's default column gap padding visually */
    [data-testid="column"] {
        padding: 0 8px !important; 
    }

    /* Buttons */
    div.stButton button[kind="primary"] {
        background: linear-gradient(180deg, #ef233c 0%, #d90429 100%);
        color: white;
        font-weight: 800;
        letter-spacing: 0.05em;
        font-size: 1.05rem;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1rem;
        width: 100%;
        box-shadow: 0 6px 15px rgba(217, 4, 41, 0.3);
        height: 100%;
    }
    div.stButton button[kind="primary"]:hover {
        background: linear-gradient(180deg, #ff3b54 0%, #ef233c 100%);
        transform: translateY(-1px);
    }

    div.stButton button[kind="secondary"] {
        background: rgba(255,255,255,0.05);
        color: #edf2f4;
        font-weight: 800;
        letter-spacing: 0.05em;
        font-size: 1.05rem;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 0.7rem 1rem;
        width: 100%;
        height: 100%;
    }
    div.stButton button[kind="secondary"]:hover {
        background: rgba(255,255,255,0.1);
        color: white;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

def fmt_num(x):
    return f"{int(x):,}" if pd.notna(x) else "0"

def metric_card(label, value, note=""):
    html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """
    return "".join(line.strip() for line in html.split('\n'))

def build_rings(row):
    rings = [
        {
            "ring_label": "Fireball / total destruction zone",
            "radius_km": row["fireball_km"],
            "fill_color": [220, 38, 38, 160],   # Red
            "line_color": [255, 80, 80, 255]
        },
        {
            "ring_label": "Heavy damage zone (5 psi blast)",
            "radius_km": row["heavy_5psi_km"],
            "fill_color": [249, 115, 22, 100],  # Orange
            "line_color": [255, 150, 50, 255]
        },
        {
            "ring_label": "Moderate damage zone (1 psi blast)",
            "radius_km": row["moderate_1psi_km"],
            "fill_color": [234, 179, 8, 80],    # Yellow
            "line_color": [255, 215, 50, 255]
        },
        {
            "ring_label": "Thermal radiation zone",
            "radius_km": row["thermal_3rd_km"],
            "fill_color": [14, 165, 233, 60],   # Cyan
            "line_color": [50, 200, 255, 255]
        }
    ]

    rings = [r for r in rings if pd.notna(r["radius_km"]) and r["radius_km"] > 0]
    rings = sorted(rings, key=lambda x: x["radius_km"], reverse=True)

    return pd.DataFrame([
        {
            "lat": row["centroid_lat"],
            "lon": row["centroid_lon"],
            "radius_m": r["radius_km"] * 1000,
            "ring_label": r["ring_label"],
            "radius_km": round(r["radius_km"], 2),
            "fill_color": r["fill_color"],
            "line_color": r["line_color"],
        }
        for r in rings
    ])

def get_target_zoom(max_radius_km, lat):
    if pd.isna(max_radius_km) or max_radius_km <= 0: 
        return 11.2
    target_width_km = max_radius_km * 2 * 1.35
    target_width_deg = target_width_km / (111.32 * abs(math.cos(math.radians(lat))))
    if target_width_deg <= 0: 
        return 11.2
    zoom = math.log2(360 / target_width_deg)
    return max(4.0, min(zoom, 12.5)) 

st.title("Localized Impact Simulator (Sydney)")
st.markdown(
    '<div class="page-subtitle">How would a nuclear detonation translate into real geographic impact?</div>',
    unsafe_allow_html=True
)

# --- TOP ROW: Dropdown (Left) and Buttons (Right) ---
top_col1, top_col2, top_col3 = st.columns([3.5, 1, 1])

with top_col1:
    options = df.index.tolist()
    
    def format_dropdown_label(idx):
        r = df.iloc[idx]
        return f"{r['bomb_name']}  |  Yield: {r['yield_display']}  |  {r['country']} ({int(r['year'])})"

    selected_idx = st.selectbox(
        "Select Weapon Profile",
        options,
        format_func=format_dropdown_label
    )
    
    radius_summary_placeholder = st.empty()

with top_col2:
    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    if st.button("DETONATE", type="primary", width="stretch"):
        st.session_state.animating = True
        st.session_state.detonated = True

with top_col3:
    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    if st.button("RESET", type="secondary", width="stretch"):
        st.session_state.detonated = False
        st.session_state.animating = False

selected_row = df.iloc[selected_idx]
rings_df = build_rings(selected_row)
base_lat = float(selected_row["centroid_lat"])
base_lon = float(selected_row["centroid_lon"])

if st.session_state.selected_bomb_idx != selected_idx:
    st.session_state.selected_bomb_idx = selected_idx
    st.session_state.detonated = False
    st.session_state.animating = False

# --- MIDDLE ROW: Map (Left) and Metrics (Right) ---
left_col, right_col = st.columns([2.3, 1])

with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    map_placeholder = st.empty()
    
    desc = str(selected_row['description']).strip() if pd.notna(selected_row['description']) else ""
    notes = str(selected_row['notes']).strip() if pd.notna(selected_row['notes']) else ""
    context_html = f"""
    <div class="context-card">
        <div class="context-title">Weapon Context: {selected_row['bomb_name']}</div>
        <div class="context-text">{desc}</div>
        <div class="context-text" style="margin-top: 6px; color: #94a3b8; font-style: italic;">{notes}</div>
    </div>
    """
    st.markdown("".join(line.strip() for line in context_html.split('\n')), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    metrics_placeholder = st.empty()
    st.markdown('</div>', unsafe_allow_html=True)


# --- RENDER FUNCTIONS ---
def get_val(col, progress):
    val = selected_row[col]
    return 0 if pd.isna(val) else int(val * progress)

def render_metrics(progress):
    if not st.session_state.detonated:
        f_val, i_val, c_val = 0, 0, 0
    else:
        f_val = get_val("fatalities", progress)
        i_val = get_val("injuries", progress)
        c_val = get_val("total_casualties", progress)

    html = f"""
    {metric_card("Estimated fatalities", fmt_num(f_val), "Direct-effect estimate")}
    {metric_card("Estimated injuries", fmt_num(i_val), "Direct-effect estimate")}
    {metric_card("Total casualties", fmt_num(c_val), "Fatalities + injuries")}
    """
    metrics_placeholder.markdown(html, unsafe_allow_html=True)

def render_radius_summary():
    if not st.session_state.detonated:
        radius_summary_placeholder.empty()
        return

    html = "<div style='display: flex; gap: 12px; margin-top: 12px; margin-bottom: 8px; flex-wrap: wrap;'>"
    
    for _, ring in rings_df.iterrows():
        r, g, b, _ = ring["line_color"]
        dot_color = f"rgba({r},{g},{b},1)"
        bg_color = f"rgba({r},{g},{b},0.08)"
        border_color = f"rgba({r},{g},{b},0.25)"
        
        card_html = f"""
        <div class="radius-card" style="background: {bg_color}; border-color: {border_color};">
            <div class="radius-dot" style="background-color: {dot_color}; box-shadow: 0 0 8px {dot_color};"></div>
            <div class="radius-details">
                <div class="radius-title">{ring['ring_label']}</div>
                <div class="radius-value">{ring['radius_km']} km</div>
            </div>
        </div>
        """
        html += "".join(line.strip() for line in card_html.split('\n'))
        
    html += "</div>"
    radius_summary_placeholder.markdown(html, unsafe_allow_html=True)

def render_map(progress):
    layers = []
    
    max_radius = rings_df["radius_km"].max() if not rings_df.empty else 0
    target_zoom = get_target_zoom(max_radius, base_lat)
    start_zoom = 11.2 
    
    if st.session_state.detonated:
        current_zoom = start_zoom + (target_zoom - start_zoom) * progress
        for _, ring in rings_df.iterrows():
            layers.append(
                pdk.Layer(
                    "ScatterplotLayer",
                    data=pd.DataFrame([{
                        "lat": ring["lat"],
                        "lon": ring["lon"],
                        "radius_m": ring["radius_m"] * progress,
                        # FIX: Pre-format the HTML string in the DataFrame
                        "tooltip_html": f"<b>{ring['ring_label']}</b><br/>Radius: {ring['radius_km']} km"
                    }]),
                    get_position='[lon, lat]',
                    get_radius='radius_m',
                    get_fill_color=ring["fill_color"],
                    get_line_color=ring["line_color"],
                    stroked=True,
                    filled=True,
                    line_width_min_pixels=2,
                    pickable=True
                )
            )
    else:
        current_zoom = start_zoom

    layers.append(
        pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame([{
                "lat": base_lat,
                "lon": base_lon,
                # FIX: Add a tooltip string specifically for Ground Zero
                "tooltip_html": "<b>Ground Zero</b><br/>Target Center"
            }]),
            get_position='[lon, lat]',
            get_radius=150,
            get_fill_color=[170, 0, 0, 255],
            pickable=True
        )
    )

    deck = pdk.Deck(
        map_style=pdk.map_styles.CARTO_DARK,
        initial_view_state=pdk.ViewState(
            latitude=base_lat,
            longitude=base_lon,
            zoom=current_zoom,
            pitch=0
        ),
        layers=layers,
        # FIX: Tell PyDeck to simply render our dynamically built string
        tooltip={
            "html": "{tooltip_html}",
            "style": {
                "backgroundColor": "rgba(5,11,24,0.94)",
                "color": "white",
                "fontSize": "12px",
                "borderRadius": "8px",
                "padding": "10px"
            }
        }
    )
    map_placeholder.pydeck_chart(deck, width="stretch")


# --- ANIMATION EXECUTION LOGIC ---
if st.session_state.animating:
    num_frames = 25
    for i in range(1, num_frames + 1):
        progress = math.sin((i / num_frames) * (math.pi / 2))
        render_metrics(progress)
        render_radius_summary()
        render_map(progress)
        time.sleep(0.03) 
    
    st.session_state.animating = False 
else:
    current_progress = 1.0 if st.session_state.detonated else 0.0
    render_metrics(current_progress)
    render_radius_summary()
    render_map(current_progress)


# --- BOTTOM UI ROW ---
st.markdown(
    """
    <div class="method-box">
        <b>Methodology note:</b> These estimates should be treated as evocative rather than definitive.
        They reflect direct blast, thermal, and prompt-radiation effects only, and do not include fallout.
        Casualty estimates are based on NUKEMAP's server-side model using 24-hour average population data,
        so real-world outcomes could vary substantially by time of day and scenario.
    </div>
    """,
    unsafe_allow_html=True
)