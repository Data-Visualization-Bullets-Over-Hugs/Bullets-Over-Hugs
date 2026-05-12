import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="Nuclear Reality", page_icon="☢️", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #08152f 0%, #050b18 45%, #040812 100%);
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe { border: none !important; display: block; }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ───
df = pd.read_csv("data/nuclear_warheads.csv")
total_inventory = int(df["total_inventory"].sum())
on_high_alert = 2100

components.html(f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  html, body {{
    width: 100%;
    height: 100%;
    background: transparent;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }}

  body {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: clamp(1rem, 4vw, 3rem);
  }}

  .question {{
    font-size: clamp(1.4rem, 3.5vw, 2.8rem);
    font-weight: 700;
    color: #edf2f4;
    letter-spacing: -0.02em;
    line-height: 1.35;
    text-align: center;
    margin-bottom: clamp(1.5rem, 4vw, 3rem);
  }}

  .cards-row {{
    display: flex;
    flex-wrap: wrap;
    gap: clamp(1rem, 2.5vw, 2rem);
    justify-content: center;
    width: 100%;
    max-width: 860px;
  }}

  .stat-card, .stat-card-amber {{
    flex: 1 1 260px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    padding: clamp(1.25rem, 3vw, 2.25rem) clamp(1rem, 2.5vw, 1.75rem);
    text-align: center;
  }}
  .stat-card {{
    background: rgba(239,35,60,0.06);
    border: 1px solid rgba(239,35,60,0.2);
  }}
  .stat-card-amber {{
    background: rgba(245,158,11,0.06);
    border: 1px solid rgba(245,158,11,0.25);
  }}

  .card-label {{
    font-size: clamp(0.65rem, 1.2vw, 1rem);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #94a3b8;
    margin-bottom: 0.75rem;
    line-height: 1.5;
  }}
  .card-label-amber {{
    font-size: clamp(0.65rem, 1.2vw, 1rem);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #d97706;
    margin-bottom: 0.75rem;
    line-height: 1.5;
  }}

  .big-number {{
    font-size: clamp(3.5rem, 8vw, 6.5rem);
    font-weight: 800;
    color: #ef233c;
    line-height: 1;
    letter-spacing: -0.04em;
  }}
  .alert-number {{
    font-size: clamp(3.5rem, 8vw, 6.5rem);
    font-weight: 800;
    color: #f59e0b;
    line-height: 1;
    letter-spacing: -0.04em;
  }}

  .card-sub {{
    font-size: clamp(0.75rem, 1.3vw, 1rem);
    color: #94a3b8;
    margin-top: 0.5rem;
    line-height: 1.4;
  }}
  .card-sub-amber {{
    font-size: clamp(0.75rem, 1.3vw, 1rem);
    color: #d97706;
    margin-top: 0.5rem;
    line-height: 1.4;
  }}

  .source {{
    margin-top: clamp(1.5rem, 3vw, 3rem);
    font-size: clamp(0.6rem, 1vw, 0.75rem);
    color: #2d3748;
    text-align: center;
  }}
  .source a {{ color: #2d3748; text-decoration: none; }}

  /* Stack cards on small screens */
  @media (max-width: 520px) {{
    .cards-row {{ flex-direction: column; align-items: stretch; }}
    .stat-card, .stat-card-amber {{ flex: 1 1 auto; }}
  }}
</style>
</head>
<body>
  <div class="question">
    Will we continue to do what<br>our weapons make possible?
  </div>
  <div class="cards-row">
    <div class="stat-card">
      <div class="card-label">Total nuclear warheads<br>in the world today</div>
      <div class="big-number">{total_inventory:,}</div>
      <div class="card-sub">across 9 nations</div>
    </div>
    <div class="stat-card-amber">
      <div class="card-label-amber">Warheads on high alert —<br>ready for use on short notice</div>
      <div class="alert-number">{on_high_alert:,}</div>
      <div class="card-sub-amber">US · Russia · UK · France</div>
    </div>
  </div>
  <div class="source">
    Data: Federation of American Scientists —
    <a href="https://fas.org/initiative/status-world-nuclear-forces/" target="_blank">
      Status of World Nuclear Forces, 2026
    </a>
    · UTS — Master of Data Science and Innovation | 2026
  </div>
</body>
</html>
""", height=800, scrolling=False)
