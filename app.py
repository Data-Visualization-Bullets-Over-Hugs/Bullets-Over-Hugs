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
        font-size: 0.875rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.02em !important;
        color: #94a3b8 !important;
        padding: 0.45rem 1rem !important;
    }
    [data-testid="stSidebarNavLink"]:hover {
        color: #edf2f4 !important;
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
    
    st.divider()

    # Motivations Section
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### **The Fiscal Tipping Point**")
        st.write(
            """
            Military expenditure has reached record highs, often at the direct expense of 
            social and humanitarian goals. 
            This project explores the **"existential trade-off"** between defense budgets 
            and human development, aiming to shift perceptions from viewing defense as 
            an unavoidable necessity to seeing it as a choice with tangible opportunity costs.
            """
        )
    with col_right:
        st.markdown("### **Existential Vulnerability**")
        st.write(
            """
            Beyond the financial cost, we address the inherent risk of the weapons being developed.
            The threats to humanity posed by modern arsenals, including catastrophic accidents 
            or strategic miscalculations, represent a vulnerability that is often ignored 
            in traditional defense narratives. We aim to quantify these risks to ground 
            the abstract threat of modern warfare.
            """
        )

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
    p1, p2, p3 = st.columns(3)
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
        **Casualties & Impact Simulation**
        * [UNICEF - WASH Infrastructure Costs](https://www.unicef.org/media/85111/file/Wash-Reports-CostOfSanitation.pdf)
        * [ITU - Global Internet Connectivity](https://www.itu.int/dms_pub/itu-d/opb/gen/D-GEN-INVEST.CON-2020-PDF-E.pdf)
        * [Our World in Data - Casualties per War](https://ourworldindata.org/war-and-peace)
        * [NUKEMAP - Physics & Blast Formulas Engine](https://nuclearsecrecy.com/nukemap/)
        """)

    st.caption("UTS — Master of Data Science and Innovation | 2026")

# --- NAVIGATION SETUP ---
pg = st.navigation([
    st.Page(home,                                              title="Home"),
    st.Page("pages/1_Opportunity_Cost.py",                    title="Opportunity Cost"),
    st.Page("pages/2_Modern_Conflicts_and_Casualties.py",     title="Modern Conflicts & Casualties"),
    st.Page("pages/3_The_Destructive_Scale.py",               title="The Destructive Scale"),
    st.Page("pages/4_Localized_Impact_Simulator.py",          title="Impact Simulator"),
])

pg.run()