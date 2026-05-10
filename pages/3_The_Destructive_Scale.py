import streamlit as st
import pandas as pd
import math

# ─── Page config ───
st.set_page_config(
    page_title="The Destructive Scale",
    page_icon="☢️",
    layout="wide",
)

# ─── Theme colours (matching group spec) ───
BG_DARK = "#2b2d42"
GREY = "#8d99ae"
CRIMSON = "#ef233c"
OFF_WHITE = "#edf2f4"
CARD_BG = "#3a3d56"
BOMB_RED = "#d90429"

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

    /* ── Section labels ── */
    .section-label {{
        font-size: 1rem;
        font-weight: 700;
        color: {OFF_WHITE};
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.8rem;
    }}

    /* ── Bomb info card ── */
    .bomb-card {{
        background: {CARD_BG};
        border-radius: 14px;
        padding: 1.5rem;
        border-left: 4px solid {CRIMSON};
        margin-bottom: 1.5rem;
    }}
    .bomb-card h2 {{
        color: {OFF_WHITE};
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0 0 1rem 0;
    }}
    .bomb-detail {{
        font-size: 1rem;
        color: {GREY};
        margin-bottom: 0.4rem;
        line-height: 1.5;
    }}
    .bomb-detail strong {{
        color: {OFF_WHITE};
    }}
    .bomb-description {{
        font-size: 0.85rem;
        color: {GREY};
        margin-top: 1rem;
        font-style: italic;
        line-height: 1.5;
    }}

    /* ── Equivalent yield header ── */
    .equiv-header {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {OFF_WHITE};
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        text-align: center;
    }}

    /* ── Big number display ── */
    .big-number {{
        text-align: center;
        margin: 1rem 0;
    }}
    .big-number .value {{
        font-size: 5rem;
        font-weight: 900;
        color: {CRIMSON};
        line-height: 1;
    }}
    .big-number .label {{
        font-size: 1.1rem;
        color: {OFF_WHITE};
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.3rem;
        font-weight: 600;
    }}
    .big-number .sublabel {{
        font-size: 0.85rem;
        color: {GREY};
        margin-top: 0.3rem;
    }}

    /* ── Bomb grid ── */
    .bomb-grid-container {{
        background: rgba(0,0,0,0.25);
        border-radius: 14px;
        padding: 1.5rem;
        margin-top: 1rem;
        text-align: center;
    }}
    .bomb-grid {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1px;
        max-height: 400px;
        overflow-y: auto;
    }}
    .bomb-dot {{
        width: 6px;
        height: 6px;
        background: {CRIMSON};
        border-radius: 1px;
        opacity: 0.85;
    }}
    .bomb-block {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: {CRIMSON};
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        margin: 4px;
        font-size: 0.85rem;
        font-weight: 700;
        color: {OFF_WHITE};
    }}
    .grid-legend {{
        font-size: 0.8rem;
        color: {GREY};
        margin-top: 0.8rem;
        text-align: center;
    }}

    /* ── Casualty cards ── */
    .casualty-row {{
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
    }}
    .casualty-card {{
        background: {CARD_BG};
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        flex: 1;
        border: 1px solid rgba(255,255,255,0.06);
    }}
    .casualty-card .card-label {{
        font-size: 0.75rem;
        color: {GREY};
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }}
    .casualty-card .card-value {{
        font-size: 2rem;
        font-weight: 800;
        color: {CRIMSON};
        line-height: 1.1;
    }}
    .casualty-card .card-sub {{
        font-size: 0.75rem;
        color: {GREY};
        margin-top: 0.3rem;
    }}

    /* ── Explosive force banner ── */
    .force-banner {{
        background: linear-gradient(135deg, {CRIMSON}22, {CRIMSON}08);
        border: 1px solid {CRIMSON}44;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        margin-top: 1.5rem;
    }}
    .force-banner .force-label {{
        font-size: 0.8rem;
        color: {GREY};
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }}
    .force-banner .force-value {{
        font-size: 2.5rem;
        font-weight: 900;
        color: {CRIMSON};
    }}

    /* ── Disclaimer ── */
    .disclaimer {{
        font-size: 0.75rem;
        color: {GREY};
        margin-top: 2rem;
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px;
        background: rgba(0,0,0,0.15);
        line-height: 1.5;
    }}

    /* ── Streamlit overrides ── */
    .stSelectbox label {{
        color: {OFF_WHITE} !important;
        font-weight: 600 !important;
    }}
    div[data-baseweb="select"] {{
        background-color: {CARD_BG};
    }}

    /* ── Source footer ── */
    .source-footer {{
        font-size: 0.7rem;
        color: {GREY};
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.06);
    }}
    .source-footer a {{ color: {GREY}; }}
</style>
""", unsafe_allow_html=True)

# ─── Load data ───
@st.cache_data
def load_data():
    df = pd.read_csv("data/nuke_blast_effects.csv")
    df = df.sort_values("display_order")
    return df

df = load_data()

# ━━━ HEADER ━━━
st.markdown("""
<p class="page-title"><span class="hl">Page 3:</span> The Destructive Scale (Hiroshima Baseline)</p>
<p class="page-subtitle">Which is the destructive scale of the current nuclear arsenals?</p>
""", unsafe_allow_html=True)

# ━━━ LAYOUT ━━━
left_col, right_col = st.columns([1, 1.5], gap="large")

# ─── LEFT PANEL ───
with left_col:
    st.markdown('<p class="section-label">Baseline: Little Boy (15 kt)</p>', unsafe_allow_html=True)

    # Dropdown
    dropdown_options = df["dropdown_label"].tolist()
    selected_label = st.selectbox(
        "Select bomb",
        dropdown_options,
        index=0,
        help="Choose a weapon to compare against the Hiroshima baseline",
    )

    bomb = df[df["dropdown_label"] == selected_label].iloc[0]

    # Bomb silhouette SVG (stylised)
    bomb_svg = f"""
    <svg viewBox="0 0 200 500" xmlns="http://www.w3.org/2000/svg" style="max-height:280px; display:block; margin:0 auto;">
        <!-- Nose cone -->
        <ellipse cx="100" cy="80" rx="30" ry="60" fill="{GREY}" opacity="0.7"/>
        <!-- Body -->
        <rect x="70" y="80" width="60" height="220" rx="8" fill="{GREY}" opacity="0.6"/>
        <!-- Fins -->
        <polygon points="70,300 40,360 70,340" fill="{CRIMSON}" opacity="0.6"/>
        <polygon points="130,300 160,360 130,340" fill="{CRIMSON}" opacity="0.6"/>
        <!-- Tail -->
        <rect x="80" y="300" width="40" height="50" rx="4" fill="{GREY}" opacity="0.5"/>
        <!-- Ring details -->
        <line x1="70" y1="120" x2="130" y2="120" stroke="{CRIMSON}" stroke-width="2" opacity="0.5"/>
        <line x1="70" y1="200" x2="130" y2="200" stroke="{CRIMSON}" stroke-width="2" opacity="0.5"/>
        <line x1="70" y1="260" x2="130" y2="260" stroke="{CRIMSON}" stroke-width="2" opacity="0.5"/>
        <!-- Label -->
        <text x="100" y="420" text-anchor="middle" fill="{OFF_WHITE}" font-size="16" font-weight="800">{bomb["bomb_name"]}</text>
        <text x="100" y="445" text-anchor="middle" fill="{GREY}" font-size="12">{bomb["yield_display"]}</text>
    </svg>
    """
    st.markdown(bomb_svg, unsafe_allow_html=True)

    # Bomb info card
    st.markdown(f"""
    <div class="bomb-card">
        <h2>{bomb["bomb_name"]}</h2>
        <div class="bomb-detail"><strong>Country:</strong> {bomb["country"]}</div>
        <div class="bomb-detail"><strong>Year:</strong> {bomb["year"]}</div>
        <div class="bomb-detail"><strong>Yield:</strong> {bomb["yield_display"]}</div>
        <div class="bomb-detail"><strong>Burst type:</strong> {bomb["burst_type"]}</div>
        <div class="bomb-description">{bomb["description"]}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── RIGHT PANEL ───
with right_col:
    hiroshima_ratio = int(bomb["hiroshima_ratio"])

    st.markdown(f"""
    <p class="equiv-header">Equivalent Yield: {bomb["bomb_name"]} ({bomb["yield_display"]})</p>
    """, unsafe_allow_html=True)

    # Big number
    st.markdown(f"""
    <div class="big-number">
        <div class="value">{hiroshima_ratio:,}×</div>
        <div class="label">Little Boy Equivalent</div>
        <div class="sublabel">in raw explosive yield</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Bomb grid visualization using st.components.v1.html ──
    import streamlit.components.v1 as components

    grid_html = f"""
    <html>
    <body style="margin:0;padding:0;background:transparent;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
    <div style="background:rgba(0,0,0,0.3);border-radius:14px;padding:20px;">
        <!-- Top labels -->
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
            <div>
                <div style="color:{CRIMSON};font-size:1.4rem;font-weight:900;">{hiroshima_ratio:,}×</div>
                <div style="color:{OFF_WHITE};font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;">LITTLE BOY<br>EQUIVALENT</div>
            </div>
            <div style="text-align:right;">
                <div style="color:{CRIMSON};font-size:1.4rem;font-weight:900;">{hiroshima_ratio:,}×</div>
                <div style="color:{OFF_WHITE};font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;">LITTLE BOY<br>EQUIVALENT</div>
            </div>
        </div>
        <canvas id="bombGrid" style="display:block;margin:0 auto;width:100%;"></canvas>
        <!-- Bottom section: 1000 blocks + force label -->
        <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:16px;">
            <div style="display:flex;flex-wrap:wrap;gap:6px;">
                {"".join([f'<div style="background:{CRIMSON};border-radius:4px;padding:10px 18px;font-size:0.8rem;font-weight:700;color:{OFF_WHITE};text-align:center;">1,000<br>BOMBS</div>' for _ in range(int(hiroshima_ratio) // 1000)])}
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.7rem;font-weight:600;color:{OFF_WHITE};text-transform:uppercase;letter-spacing:1px;">OVER</div>
                <div style="font-size:2.2rem;font-weight:900;color:{CRIMSON};line-height:1;">{hiroshima_ratio:,}×</div>
                <div style="font-size:0.7rem;font-weight:700;color:{OFF_WHITE};letter-spacing:1px;">EXPLOSIVE FORCE</div>
            </div>
        </div>
    </div>
    <script>
    (function() {{
        const canvas = document.getElementById('bombGrid');
        const ctx = canvas.getContext('2d');

        // Fixed dimensions — fit in one frame
        const containerWidth = canvas.parentElement.clientWidth - 40;
        const targetHeight = 380;  // fixed height, no scroll

        const totalBombs = {hiroshima_ratio};
        const maxBombs = Math.max(totalBombs, 3333);

        // Auto-calculate bomb size to fit all in targetHeight
        // Start with a guess and shrink until it fits
        let bombW = 6, bombH = 10, gap = 2;
        let stepX, stepY, cols, rows;

        for (let size = 10; size >= 2; size--) {{
            bombH = size;
            bombW = Math.max(Math.round(size * 0.6), 2);
            gap = Math.max(Math.round(size * 0.2), 1);
            stepX = bombW + gap;
            stepY = bombH + gap;
            cols = Math.floor(containerWidth / stepX);
            rows = Math.ceil(maxBombs / cols);
            if (rows * stepY <= targetHeight) break;
        }}

        canvas.width = cols * stepX;
        canvas.height = rows * stepY;
        canvas.style.width = '100%';
        canvas.style.height = canvas.height + 'px';

        let count = 0;
        for (let r = 0; r < rows; r++) {{
            for (let c = 0; c < cols; c++) {{
                if (count >= maxBombs) break;
                const x = c * stepX;
                const y = r * stepY;
                const filled = count < totalBombs;

                if (filled) {{
                    ctx.fillStyle = '{CRIMSON}';
                    ctx.globalAlpha = 0.9;
                }} else {{
                    ctx.fillStyle = 'rgba(141,153,174,0.15)';
                    ctx.globalAlpha = 1;
                }}

                // Draw bomb shape: nose (triangle) + body (rect) + fins
                const noseH = bombH * 0.25;
                const bodyH = bombH * 0.55;
                const finH = bombH * 0.2;
                const bodyW = bombW * 0.6;
                const cx = x + bombW / 2;

                ctx.beginPath();
                ctx.moveTo(cx, y);
                ctx.lineTo(cx - bodyW/2, y + noseH);
                ctx.lineTo(cx + bodyW/2, y + noseH);
                ctx.closePath();
                ctx.fill();

                ctx.fillRect(cx - bodyW/2, y + noseH, bodyW, bodyH);

                ctx.beginPath();
                ctx.moveTo(cx - bombW/2, y + noseH + bodyH + finH);
                ctx.lineTo(cx - bodyW/2, y + noseH + bodyH);
                ctx.lineTo(cx + bodyW/2, y + noseH + bodyH);
                ctx.lineTo(cx + bombW/2, y + noseH + bodyH + finH);
                ctx.closePath();
                ctx.fill();

                count++;
            }}
        }}
        ctx.globalAlpha = 1;
    }})();
    </script>
    </body>
    </html>
    """
    components.html(grid_html, height=560, scrolling=False)

    # Explosive force banner
    st.markdown(f"""
    <div class="force-banner">
        <div class="force-label">Total Explosive Force</div>
        <div class="force-value">OVER {hiroshima_ratio:,}×</div>
        <div class="force-label">the bomb that destroyed Hiroshima</div>
    </div>
    """, unsafe_allow_html=True)

# ━━━ CASUALTY STATS (full width below) ━━━
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="section-label">Estimated Impact on Sydney CBD</p>', unsafe_allow_html=True)

st.markdown(f"""
<div class="casualty-row">
    <div class="casualty-card">
        <div class="card-label">Estimated Fatalities</div>
        <div class="card-value">{bomb["fatalities"]:,}</div>
        <div class="card-sub">Direct blast & thermal</div>
    </div>
    <div class="casualty-card">
        <div class="card-label">Estimated Injuries</div>
        <div class="card-value">{bomb["injuries"]:,}</div>
        <div class="card-sub">Within blast radius</div>
    </div>
    <div class="casualty-card">
        <div class="card-label">Total Casualties</div>
        <div class="card-value">{bomb["total_casualties"]:,}</div>
        <div class="card-sub">Fatalities + injuries</div>
    </div>
    <div class="casualty-card">
        <div class="card-label">Fireball Radius</div>
        <div class="card-value">{bomb["fireball_km"]:.1f} km</div>
        <div class="card-sub">Complete vaporisation zone</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ━━━ DISCLAIMER ━━━
st.markdown(f"""
<div class="disclaimer">
    ⚠️ <strong>Disclaimer:</strong> Casualty estimates from NUKEMAP are "evocative, not definitive" (Wellerstein, 2012–2026).
    Figures represent direct effects only — blast, thermal, and prompt radiation. Radioactive fallout (which would
    significantly increase casualties for surface bursts) is deliberately excluded. Population data uses 24-hour
    ambient averages; daytime CBD figures would be substantially higher. Yields above 20 Mt are extrapolated.
</div>
""", unsafe_allow_html=True)

# ━━━ FOOTER ━━━
st.markdown("""
<div class="source-footer">
    Data: <a href="https://nuclearsecrecy.com/nukemap/" target="_blank">NUKEMAP</a> (Alex Wellerstein) &nbsp;|&nbsp;
    Physics: Glasstone & Dolan, <em>The Effects of Nuclear Weapons</em> (1977) &nbsp;|&nbsp;
    Population: LandScan 24-hour ambient
</div>
""", unsafe_allow_html=True)