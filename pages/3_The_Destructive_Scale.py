import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ─── Page Config ───
st.set_page_config(page_title="The Destructive Scale", page_icon="☢️", layout="wide")

# ─── Theme Colours ───
CRIMSON = "#ef233c"
OFF_WHITE = "#edf2f4"
GREY_TEXT = "#94a3b8"
GREY_LABEL = "#b8c1cc"
GREY_MID = "#cbd5e1"

# ─── Custom CSS & Lucide Icons ───
st.markdown("""
<script src="https://unpkg.com/lucide@latest"></script>
<style>
    /* 1. Global */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }
    .stApp {
        background: radial-gradient(circle at top, #08152f 0%, #050b18 45%, #040812 100%);
        color: #edf2f4;
    }

    /* 2. Typography */
    h1 {
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
        color: #edf2f4 !important;
        letter-spacing: -0.02em;
    }
    h2, h3 {
        color: #edf2f4 !important;
        letter-spacing: -0.02em;
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

    /* 4. Section Labels */
    .section-label {
        font-size: 0.85rem;
        font-weight: 700;
        color: #b8c1cc;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.8rem;
    }

    /* 5. Bomb Info Card — glass morphism */
    .bomb-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.035) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-left: 4px solid #ef233c;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: border 0.3s ease;
    }
    .bomb-card:hover {
        border: 1px solid rgba(239,35,60,0.4);
        border-left: 4px solid #ef233c;
    }
    .bomb-card h2 {
        color: #edf2f4;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0 0 1rem 0;
        letter-spacing: -0.02em;
    }
    .bomb-detail {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-bottom: 0.4rem;
        line-height: 1.5;
    }
    .bomb-detail strong {
        color: #edf2f4;
        font-weight: 600;
    }
    .bomb-description {
        font-size: 0.82rem;
        color: #94a3b8;
        margin-top: 1rem;
        font-style: italic;
        line-height: 1.4;
    }

    /* 6. Big Number Display */
    .big-number {
        text-align: center;
        margin: 1.5rem 0 1rem 0;
    }
    .big-number .value {
        font-size: 5rem;
        font-weight: 900;
        color: #ef233c;
        line-height: 1;
    }
    .big-number .label {
        font-size: 1rem;
        color: #edf2f4;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.3rem;
        font-weight: 700;
    }
    .big-number .sublabel {
        font-size: 0.82rem;
        color: #94a3b8;
        margin-top: 0.3rem;
    }

    /* 7. Casualty Cards — glass morphism matching metric-card */
    .casualty-row {
        display: flex;
        gap: 12px;
        margin-top: 1.5rem;
    }
    .casualty-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.035) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        flex: 1;
        min-height: 140px;
        transition: border 0.3s ease;
    }
    .casualty-card:hover {
        border: 1px solid rgba(239,35,60,0.4);
    }
    .casualty-card .card-icon {
        color: #ef233c;
        margin-bottom: 10px;
        display: flex;
        justify-content: center;
    }
    .casualty-card .card-icon svg {
        width: 28px;
        height: 28px;
        stroke-width: 1.5px;
    }
    .casualty-card .card-label {
        font-size: 0.82rem;
        color: #b8c1cc;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .casualty-card .card-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #edf2f4;
        line-height: 1.1;
        margin: 4px 0;
    }
    .casualty-card .card-sub {
        font-size: 0.78rem;
        color: #94a3b8;
        margin-top: 0.3rem;
        line-height: 1.3;
    }

    /* 8. Force Banner — gradient like budget-display */
    .force-banner {
        background: linear-gradient(180deg, rgba(239,35,60,0.15) 0%, rgba(217,4,41,0.05) 100%);
        border: 1px solid rgba(239,35,60,0.3);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        margin-top: 1.5rem;
    }
    .force-banner .force-label {
        font-size: 0.85rem;
        color: #ef233c;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .force-banner .force-value {
        font-size: 2.8rem;
        font-weight: 800;
        color: #ef233c;
        line-height: 1.1;
    }

    /* 9. Disclaimer */
    .disclaimer {
        font-size: 0.78rem;
        color: #94a3b8;
        margin-top: 2rem;
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        background: linear-gradient(180deg, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0.01) 100%);
        line-height: 1.5;
    }

    /* 10. Instruction text */
    .instruction-text {
        font-size: 0.85rem;
        color: #94a3b8;
        font-style: italic;
        margin-bottom: 8px;
    }

    /* 11. Source Footer */
    .source-footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 30px;
    }
    .source-footer a {
        color: #94a3b8;
    }

    /* 12. Streamlit overrides */
    .stSelectbox label {
        color: #edf2f4 !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] {
        background-color: rgba(255,255,255,0.04);
    }
</style>
<script>
    const observer = new MutationObserver(() => {
        if (window.lucide) { lucide.createIcons(); }
    });
    observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

# ─── Load Data ───
@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv("data/nuke_blast_effects.csv")
    df = df.sort_values("display_order")
    return df

df = load_data()

# ━━━ HEADER ━━━
st.title("The Destructive Scale (Hiroshima Baseline)")
st.markdown('<div class="page-subtitle">Which is the destructive scale of the current nuclear arsenals?</div>', unsafe_allow_html=True)

# ━━━ LAYOUT ━━━
left_col, right_col = st.columns([1, 1.5], gap="large")

# ─── LEFT PANEL ───
with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Select a Weapon")
    st.markdown('<p class="instruction-text">Choose any nuclear weapon to see how it compares to the Hiroshima baseline.</p>', unsafe_allow_html=True)

    dropdown_options = df["dropdown_label"].tolist()
    selected_label = st.selectbox(
        "Select bomb",
        dropdown_options,
        index=0,
        help="Choose a weapon to compare against the Hiroshima baseline",
    )

    bomb = df[df["dropdown_label"] == selected_label].iloc[0]

    # Bomb silhouette SVG
    bomb_svg = f"""
    <svg viewBox="0 0 200 500" xmlns="http://www.w3.org/2000/svg" style="max-height:260px; display:block; margin:0 auto;">
        <ellipse cx="100" cy="80" rx="30" ry="60" fill="#94a3b8" opacity="0.5"/>
        <rect x="70" y="80" width="60" height="220" rx="8" fill="#94a3b8" opacity="0.4"/>
        <polygon points="70,300 40,360 70,340" fill="#ef233c" opacity="0.5"/>
        <polygon points="130,300 160,360 130,340" fill="#ef233c" opacity="0.5"/>
        <rect x="80" y="300" width="40" height="50" rx="4" fill="#94a3b8" opacity="0.35"/>
        <line x1="70" y1="120" x2="130" y2="120" stroke="#ef233c" stroke-width="2" opacity="0.35"/>
        <line x1="70" y1="200" x2="130" y2="200" stroke="#ef233c" stroke-width="2" opacity="0.35"/>
        <line x1="70" y1="260" x2="130" y2="260" stroke="#ef233c" stroke-width="2" opacity="0.35"/>
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
    st.markdown('</div>', unsafe_allow_html=True)

# ─── RIGHT PANEL ───
with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    hiroshima_ratio = int(bomb["hiroshima_ratio"])

    st.subheader("Hiroshima Equivalent Yield")

    # Big number
    st.markdown(f"""
    <div class="big-number">
        <div class="value">{hiroshima_ratio:,}×</div>
        <div class="label">Little Boy Equivalent</div>
        <div class="sublabel">in raw explosive yield</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Bomb grid visualization ──
    grid_html = f"""
    <html>
    <body style="margin:0;padding:0;background:transparent;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">

    <!-- Hover tooltip -->
    <div id="tooltip" style="
        display:none;
        position:fixed;
        background:linear-gradient(180deg,rgba(8,21,47,0.97) 0%,rgba(5,11,24,0.97) 100%);
        border:1px solid rgba(239,35,60,0.45);
        border-radius:12px;
        padding:12px 16px;
        pointer-events:none;
        z-index:9999;
        min-width:210px;
        box-shadow:0 8px 32px rgba(0,0,0,0.5);
    ">
        <div style="color:#ef233c;font-size:0.75rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px;">☢ Baseline Reference</div>
        <div style="color:#edf2f4;font-size:1rem;font-weight:800;margin-bottom:8px;">Little Boy — 15 kt</div>
        <div style="color:#94a3b8;font-size:0.78rem;line-height:1.5;">
            <span style="color:#cbd5e1;font-weight:600;">Country:</span> United States<br>
            <span style="color:#cbd5e1;font-weight:600;">Dropped:</span> Hiroshima, 6 Aug 1945<br>
            <span style="color:#cbd5e1;font-weight:600;">Yield:</span> ~15 kilotons TNT<br>
            <span style="color:#cbd5e1;font-weight:600;">Killed:</span> ~70,000–80,000 instantly<br>
            <span style="color:#cbd5e1;font-weight:600;">Total deaths:</span> ~140,000 by end of 1945
        </div>
        <div style="color:#64748b;font-size:0.72rem;margin-top:8px;font-style:italic;">Each icon in this grid = 1 Little Boy</div>
    </div>

    <div id="gridWrap" style="background:linear-gradient(180deg, rgba(255,255,255,0.025) 0%, rgba(255,255,255,0.01) 100%);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:20px;cursor:crosshair;">
        <canvas id="bombGrid" style="display:block;margin:0 auto;width:100%;"></canvas>
    </div>

    <script>
    (function() {{
        const canvas  = document.getElementById('bombGrid');
        const ctx     = canvas.getContext('2d');
        const tooltip = document.getElementById('tooltip');
        const wrap    = document.getElementById('gridWrap');

        const containerWidth = wrap.clientWidth - 40;
        const targetHeight   = 380;
        const totalBombs     = {hiroshima_ratio};
        const maxBombs       = Math.max(totalBombs, 3333);

        let bombW, bombH, gap, stepX, stepY, cols, rows;
        for (let size = 10; size >= 2; size--) {{
            bombH  = size;
            bombW  = Math.max(Math.round(size * 0.6), 2);
            gap    = Math.max(Math.round(size * 0.2), 1);
            stepX  = bombW + gap;
            stepY  = bombH + gap;
            cols   = Math.floor(containerWidth / stepX);
            rows   = Math.ceil(maxBombs / cols);
            if (rows * stepY <= targetHeight) break;
        }}

        canvas.width        = cols * stepX;
        canvas.height       = rows * stepY;
        canvas.style.width  = '100%';
        canvas.style.height = canvas.height + 'px';

        function drawBomb(idx, filled, highlight) {{
            const r  = Math.floor(idx / cols);
            const c  = idx % cols;
            const x  = c * stepX;
            const y  = r * stepY;

            const noseH  = bombH * 0.25;
            const bodyH  = bombH * 0.55;
            const finH   = bombH * 0.2;
            const bodyBW = bombW * 0.6;
            const cx     = x + bombW / 2;

            if (highlight) {{
                ctx.fillStyle  = '#ffffff';
                ctx.globalAlpha = 1;
            }} else if (filled) {{
                ctx.fillStyle  = '#ef233c';
                ctx.globalAlpha = 0.9;
            }} else {{
                ctx.fillStyle  = 'rgba(148,163,184,0.1)';
                ctx.globalAlpha = 1;
            }}

            ctx.beginPath();
            ctx.moveTo(cx, y);
            ctx.lineTo(cx - bodyBW/2, y + noseH);
            ctx.lineTo(cx + bodyBW/2, y + noseH);
            ctx.closePath();
            ctx.fill();

            ctx.fillRect(cx - bodyBW/2, y + noseH, bodyBW, bodyH);

            ctx.beginPath();
            ctx.moveTo(cx - bombW/2, y + noseH + bodyH + finH);
            ctx.lineTo(cx - bodyBW/2, y + noseH + bodyH);
            ctx.lineTo(cx + bodyBW/2, y + noseH + bodyH);
            ctx.lineTo(cx + bombW/2, y + noseH + bodyH + finH);
            ctx.closePath();
            ctx.fill();
        }}

        // Draw all dim first
        for (let i = 0; i < maxBombs; i++) drawBomb(i, false, false);
        ctx.globalAlpha = 1;

        // Animate fill in batches
        const BATCH = Math.max(1, Math.ceil(totalBombs / 60));
        let filled = 0;
        function animate() {{
            const end = Math.min(filled + BATCH, totalBombs);
            for (let i = filled; i < end; i++) drawBomb(i, true, false);
            filled = end;
            ctx.globalAlpha = 1;
            if (filled < totalBombs) requestAnimationFrame(animate);
        }}
        requestAnimationFrame(animate);

        // ── Hover tooltip ──
        canvas.addEventListener('mousemove', function(e) {{
            const rect = canvas.getBoundingClientRect();
            tooltip.style.display = 'block';
            tooltip.style.left    = (e.clientX + 16) + 'px';
            tooltip.style.top     = (e.clientY - 10) + 'px';

            // Flip if too close to right edge
            if (e.clientX + 16 + 230 > window.innerWidth) {{
                tooltip.style.left = (e.clientX - 230) + 'px';
            }}
        }});
        canvas.addEventListener('mouseleave', function() {{
            tooltip.style.display = 'none';
        }});
    }})();
    </script>
    </body>
    </html>
    """
    components.html(grid_html, height=560, scrolling=False)

    st.markdown('</div>', unsafe_allow_html=True)

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