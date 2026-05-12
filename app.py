import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Bullets Over Hugs",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS STYLING ---
st.markdown("""
<style>
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #08152f 0%, #050b18 55%, #040812 100%) !important;
    }

    /* Nav links styling */
    [data-testid="stSidebarNavLink"] {
        font-size: 2.6rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
        color: #f1f5f9 !important;
        padding: 0.45rem 1rem !important;
    }
    [data-testid="stSidebarNavLink"]:hover {
        color: #ffffff !important;
    }
    [data-testid="stSidebarNavLink"][aria-current="page"] {
        font-weight: 600 !important;
        color: #edf2f4 !important;
        background: linear-gradient(90deg, rgba(239,35,60,0.25), rgba(239,35,60,0.08)) !important;
        border-left: 3px solid #ef233c !important;
        border-radius: 8px !important;
    }

    /* Hide icons to keep a minimalist look */
    [data-testid="stSidebarNavLink"] svg,
    [data-testid="stSidebarNavLink"] img,
    [data-testid="stSidebarNavLink"] [data-testid="stSidebarNavLinkIcon"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HOME PAGE CONTENT ---
def home():
    st.markdown("""
    <style>
        .stApp {
            background: radial-gradient(circle at top, #08152f 0%, #050b18 45%, #040812 100%);
            color: #edf2f4;
        }
        h1, h2, h3 { color: #edf2f4 !important; letter-spacing: -0.02em; }
        section[data-testid="stMain"] p,
        section[data-testid="stMain"] li,
        section[data-testid="stMain"] .stMarkdown { font-size: 1.05rem !important; line-height: 1.7 !important; }
    </style>
    """, unsafe_allow_html=True)

    # Header section
    st.title("Bullets Over Hugs")
    st.subheader("Quantifying the Cost and Risks of the Arms Race")

    st.markdown(
        """
        Welcome to **Bullets Over Hugs**, an interactive data storytelling project. 
        This platform explores patterns in global military spending, the human cost of conflict, 
        and the existential choices facing modern society.
        """
    )

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(239,35,60,0.08) 0%, rgba(217,4,41,0.04) 100%);
        border: 1px solid rgba(239,35,60,0.35);
        border-left: 4px solid #ef233c;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 0.5rem 0 1.5rem 0;
    ">
        <div style="display:flex;align-items:flex-start;gap:0.9rem;">
            <div style="font-size:1.8rem;margin-top:2px;">⚠️</div>
            <div>
                <div style="color:#edf2f4;font-weight:700;font-size:1.35rem;margin-bottom:0.5rem;letter-spacing:0.01em;">
                    Content Advisory
                </div>
                <div style="color:#cbd5e1;font-size:1.1rem;line-height:1.7;">
                    This project contains data and visualisations related to <strong style="color:#edf2f4;">armed conflict, civilian casualties, and nuclear weapons</strong>.
                    All content is presented for educational and policy analysis purposes only.
                    Figures are drawn from peer-reviewed sources and international databases — they are not intended to sensationalise violence,
                    but to make its scale legible and its consequences unavoidable.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Target Audience Section
    st.markdown("### **Target Audience**")
    st.info(
        """
        **Who is the target persona?**  
        UN Security Council Policy Advisors and Global NGO Directors (e.g., International Campaign to Abolish Nuclear Weapons - ICAN).
        """
    )

    st.divider()

    # Project Overview
    st.markdown("### **Interactive Visualisation Modules**")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown("#### **1. Opportunity Cost**")
        st.caption("What is the re-allocation impact?")
        st.write("A dashboard translating military budgets into tangible outcomes like NASA missions, internet connectivity, and WASH infrastructure.")
    with p2:
        st.markdown("#### **2. Conflict & Casualties**")
        st.caption("Mapping the human cost")
        st.write("Visualizing fatalities and conflict density over the last decade (2015–2024) to show the true cost of conventional warfare.")
    with p3:
        st.markdown("#### **3. Impact Simulator**")
        st.caption("Visualizing the destructive scale")
        st.write("Using historical baselines to simulate the localized geographic impact of modern nuclear weapons in Sydney.")
    with p4:
        st.markdown("#### **4. Nuclear Reality**")
        st.caption("A final reckoning")
        st.write("12,187 warheads. 2,100 on high alert. A closing reflection on what the arms race truly costs — and what it makes possible.")

    st.divider()

    # Team Section
    st.markdown("### **Collaborative Team (Group 21)**")
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.write("**Juan Vargas Torres**")
        st.caption("Orator & Scrum Master")
        st.write("**Maria Jose Bustamante Grajales**")
        st.caption("The Analyst")
    with t2:
        st.write("**Nick Rossetto**")
        st.caption("Data Architect")
        st.write("**Aditya Ahlawat**")
        st.caption("Artist & Dashboard Developer")
    with t3:
        st.write("**Ngoc Thanh Tuan Nguyen**")
        st.caption("The Artist")
        st.write("**Kankshi Shah**")
        st.caption("Data Architect")
    with t4:
        st.write("**Vinod Nair Bhaskaran**")
        st.caption("The Analyst")

    st.divider()

    # Resources & Data Sources
    st.markdown("### **Resources & Data Sources**")
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.markdown("""
        **Global Defense & Development**
        * [Visual Capitalist - Defense Spending](https://www.visualcapitalist.com/sp/gxeu01-defence-spending/)
        * [SIPRI - Military Spending Trends](https://www.sipri.org/media/press-release/2026/global-military-spending-rise-continues)
        * [Stanford HAI - Global AI Investment](https://hai.stanford.edu/ai-index/2026-ai-index-report)
        * [NASA OIG - Artemis Program Cost](https://oig.nasa.gov/wp-content/uploads/2024/02/IG-22-003.pdf)
        """)
    with res_col2:
        st.markdown("""
        **Casualties, Impact & Nuclear Forces**
        * [UNICEF - WASH Infrastructure Costs](https://www.unicef.org/media/85111/file/Wash-Reports-CostOfSanitation.pdf)
        * [ITU - Global Internet Connectivity](https://www.itu.int/dms_pub/itu-d/opb/gen/D-GEN-INVEST.CON-2020-PDF-E.pdf)
        * [Our World in Data - Casualties per War](https://ourworldindata.org/war-and-peace)
        * [NUKEMAP - Physics & Blast Formulas Engine](https://nuclearsecrecy.com/nukemap/)
        * [FAS - Status of World Nuclear Forces, 2026](https://fas.org/initiative/status-world-nuclear-forces/)
        """)

    st.caption("UTS — Master of Data Science and Innovation | 2026")

# --- NAVIGATION SETUP ---
pg = st.navigation([
    st.Page(home,                                              title="Home"),
    st.Page("pages/1_Opportunity_Cost.py",                    title="Opportunity Cost"),
    st.Page("pages/2_Modern_Conflicts_and_Casualties.py",     title="Modern Conflicts & Casualties"),
    st.Page("pages/3_The_Destructive_Scale.py",               title="The Destructive Scale"),
    st.Page("pages/4_Localized_Impact_Simulator.py",          title="Impact Simulator"),
    st.Page("pages/5_Nuclear_Reality.py",                     title="Nuclear Reality"),
])

pg.run()