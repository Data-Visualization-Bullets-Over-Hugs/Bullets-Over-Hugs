import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(
    page_title="Localized Impact Simulator",
    page_icon="☢️",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/nuke_blast_effects.csv")

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

    .panel {
        background: rgba(8, 15, 30, 0.82);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 14px 16px 12px 16px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.18);
    }

    .control-panel {
        background: linear-gradient(180deg, rgba(8, 15, 30, 0.95) 0%, rgba(12, 22, 40, 0.92) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 14px 14px 10px 14px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.20);
    }

    .small-note {
        color: #94a3b8;
        font-size: 0.84rem;
        line-height: 1.5;
        margin-top: 0.35rem;
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.035) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 14px 16px 10px 16px;
        box-shadow: 0 10px 26px rgba(0,0,0,0.20);
        min-height: 108px;
    }

    .metric-label {
        font-size: 0.84rem;
        color: #b8c1cc;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #edf2f4;
        line-height: 1.05;
    }

    .metric-note {
        font-size: 0.80rem;
        color: #94a3b8;
        margin-top: 7px;
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

    .bomb-title {
        font-size: 1.08rem;
        font-weight: 700;
        color: #edf2f4;
        margin-bottom: 0.35rem;
    }

    .bomb-meta {
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.55;
    }

    div[data-testid="stSelectbox"] label {
        color: #edf2f4 !important;
        font-weight: 600;
    }

    div.stButton > button {
        background: linear-gradient(180deg, #ef233c 0%, #d90429 100%);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1rem;
        width: 100%;
    }

    div.stButton > button:hover {
        background: linear-gradient(180deg, #ff3b54 0%, #ef233c 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

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

def build_rings(row):
    rings = [
        {
            "ring_label": "Fireball / total destruction zone",
            "radius_km": row["fireball_km"],
            "fill_color": [180, 0, 0, 180],
            "line_color": [255, 255, 255, 180]
        },
        {
            "ring_label": "Heavy damage zone (5 psi blast)",
            "radius_km": row["heavy_5psi_km"],
            "fill_color": [239, 35, 60, 95],
            "line_color": [239, 35, 60, 220]
        },
        {
            "ring_label": "Moderate damage zone (1 psi blast)",
            "radius_km": row["moderate_1psi_km"],
            "fill_color": [239, 35, 60, 65],
            "line_color": [239, 35, 60, 200]
        },
        {
            "ring_label": "Thermal radiation zone",
            "radius_km": row["thermal_3rd_km"],
            "fill_color": [255, 90, 95, 45],
            "line_color": [255, 120, 120, 180]
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

st.title("Page 4: Localized Impact Simulator (Sydney)")
st.markdown(
    '<div class="page-subtitle">How would a nuclear detonation translate into real geographic impact?</div>',
    unsafe_allow_html=True
)

selected_label = st.selectbox(
    "Select bomb",
    df["dropdown_label"].tolist()
)

selected_row = df[df["dropdown_label"] == selected_label].iloc[0]
rings_df = build_rings(selected_row)

if "detonated" not in st.session_state:
    st.session_state.detonated = False

if "selected_bomb_label" not in st.session_state:
    st.session_state.selected_bomb_label = selected_label

if st.session_state.selected_bomb_label != selected_label:
    st.session_state.selected_bomb_label = selected_label
    st.session_state.detonated = False

left_col, right_col = st.columns([0.78, 2.22], gap="large")

with left_col:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)

    st.markdown(f'<div class="bomb-title">{selected_row["bomb_name"]}</div>', unsafe_allow_html=True)
    st.markdown(
        f'''
        <div class="bomb-meta">
            <b>Location:</b> Sydney CBD<br>
            <b>Country:</b> {selected_row["country"]}<br>
            <b>Year:</b> {int(selected_row["year"])}<br>
            <b>Yield:</b> {selected_row["yield_display"]}<br>
            <b>Burst type:</b> {selected_row["burst_type"]}
        </div>
        ''',
        unsafe_allow_html=True
    )

    if st.button("DETONATE"):
        st.session_state.detonated = True

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    st.markdown(
        metric_card(
            "Estimated fatalities",
            fmt_num(selected_row["fatalities"]),
            "Direct-effect estimate"
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        metric_card(
            "Estimated injuries",
            fmt_num(selected_row["injuries"]),
            "Direct-effect estimate"
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        metric_card(
            "Total casualties",
            fmt_num(selected_row["total_casualties"]),
            "Fatalities + injuries"
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="small-note">The simulation overlays the selected weapon’s direct blast and thermal radii over Sydney CBD. Ring order is based on actual radius size, not a fixed visual order.</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Sydney CBD Impact Map")

    base_lat = float(selected_row["centroid_lat"])
    base_lon = float(selected_row["centroid_lon"])

    layers = []

    if st.session_state.detonated:
        for _, ring in rings_df.iterrows():
            layers.append(
                pdk.Layer(
                    "ScatterplotLayer",
                    data=pd.DataFrame([{
                        "lat": ring["lat"],
                        "lon": ring["lon"],
                        "radius_m": ring["radius_m"],
                        "ring_label": ring["ring_label"],
                        "radius_km": ring["radius_km"]
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

    layers.append(
        pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame([{
                "lat": base_lat,
                "lon": base_lon,
                "label": "Sydney CBD Ground Zero"
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
            zoom=11.2,
            pitch=0
        ),
        layers=layers,
        tooltip={
            "html": "<b>{ring_label}</b><br/>Radius: {radius_km} km",
            "style": {
                "backgroundColor": "rgba(5,11,24,0.94)",
                "color": "white",
                "fontSize": "12px"
            }
        }
    )

    st.pydeck_chart(deck, use_container_width=True)

    if not st.session_state.detonated:
        st.info("Select a bomb and click DETONATE to overlay the blast and thermal zones over Sydney CBD.")

    st.markdown('</div>', unsafe_allow_html=True)

m1, m2 = st.columns([1.15, 1], gap="large")

with m1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Effect Radius Summary")

    display_rings = rings_df[["ring_label", "radius_km"]].copy()
    display_rings.columns = ["Effect zone", "Radius (km)"]

    st.dataframe(display_rings, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with m2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Bomb Context")
    st.write(selected_row["description"])
    if pd.notna(selected_row["notes"]) and str(selected_row["notes"]).strip():
        st.caption(selected_row["notes"])
    st.markdown('</div>', unsafe_allow_html=True)

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