# Bullets Over Hugs

**UTS Data Visualization — Assignment 3 | Master of Data Science and Innovation | Semester 2, 2026**

An interactive Streamlit dashboard quantifying the cost and risks of the global arms race — exploring patterns in military spending, the human cost of conflict, and the existential threat of nuclear weapons.

> **Content Advisory:** This project contains data and visualisations related to armed conflict, civilian casualties, and nuclear weapons. All content is presented for educational and policy analysis purposes only.

---

## Project Structure

```
Bullets-Over-Hugs/
├── app.py                                        # Home page & navigation
├── pages/
│   ├── 1_Opportunity_Cost.py                     # Military budget re-allocation
│   ├── 2_Modern_Conflicts_and_Casualties.py      # Conflict fatalities map
│   ├── 3_The_Destructive_Scale.py                # Destructive scale visualisation
│   ├── 4_Localized_Impact_Simulator.py           # Nuclear impact simulator
│   └── 5_Nuclear_Reality.py                      # Current nuclear arsenal reality
├── data/                                         # Datasets & data dictionaries
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repo-url>
cd Bullets-Over-Hugs
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at [http://localhost:8501](http://localhost:8501).

---

## Pages

| Page | Description |
|------|-------------|
| **Home** (`app.py`) | Welcome screen, project overview, team info, and data sources |
| **Opportunity Cost** | Dashboard translating military budgets into tangible outcomes (NASA missions, internet connectivity, WASH infrastructure) |
| **Modern Conflicts & Casualties** | Fatalities and conflict density over 2015–2024, mapping the human cost of conventional warfare |
| **The Destructive Scale** | Historical baselines visualising the destructive scale of modern nuclear weapons |
| **Impact Simulator** | Localized geographic impact simulation of nuclear weapons in Sydney |
| **Nuclear Reality** | A closing reflection on 12,187 warheads, 2,100 on high alert, and the true cost of the arms race |

---

## Tech Stack

| Library | Purpose |
|---------|---------|
| [Streamlit](https://streamlit.io) | App framework |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [NumPy](https://numpy.org) | Numerical operations |
| [Plotly](https://plotly.com/python/) | Interactive charts |

---

## Data Sources

| Source | Topic |
|--------|-------|
| [SIPRI](https://www.sipri.org/media/press-release/2026/global-military-spending-rise-continues) | Military spending trends |
| [Visual Capitalist](https://www.visualcapitalist.com/sp/gxeu01-defence-spending/) | Global defence spending |
| [Stanford HAI](https://hai.stanford.edu/ai-index/2026-ai-index-report) | Global AI investment |
| [NASA OIG](https://oig.nasa.gov/wp-content/uploads/2024/02/IG-22-003.pdf) | Artemis program cost |
| [UNICEF](https://www.unicef.org/media/85111/file/Wash-Reports-CostOfSanitation.pdf) | WASH infrastructure costs |
| [ITU](https://www.itu.int/dms_pub/itu-d/opb/gen/D-GEN-INVEST.CON-2020-PDF-E.pdf) | Global internet connectivity |
| [Our World in Data](https://ourworldindata.org/war-and-peace) | Casualties per war |
| [NUKEMAP](https://nuclearsecrecy.com/nukemap/) | Nuclear blast physics & formulas |
| [FAS](https://fas.org/initiative/status-world-nuclear-forces/) | Status of world nuclear forces, 2026 |

---

## Credits

**Group 21** — UTS Master of Data Science and Innovation, 2026

| Member | Role |
|--------|------|
| **Juan Vargas Torres** | Orator & Scrum Master |
| **Maria Jose Bustamante Grajales** | The Analyst |
| **Nick Rossetto** | Data Architect |
| **Aditya Ahlawat** | Artist & Dashboard Developer |
| **Ngoc Thanh Tuan Nguyen** | The Artist |
| **Kankshi Shah** | Data Architect |
| **Vinod Nair Bhaskaran** | The Analyst |

---

## License

For academic use only — UTS Assignment 3.
