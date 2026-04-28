# Bullets Over Hugs

**UTS Data Visualization — Assignment 3 | Semester 2, 2026**

An interactive Streamlit dashboard exploring the relationship between gun violence and social/economic indicators across countries and time.

---

## Project Structure

```
Bullets-Over-Hugs/
├── app.py                  # Landing page
├── pages/
│   ├── 1_Overview.py       # Time-series & scatter overview
│   └── 2_Deep_Dive.py      # Per-country deep dive & correlation matrix
├── data/                   # (add your datasets here)
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
| **Home** (`app.py`) | Welcome screen with top-level metrics |
| **Overview** | Multi-country time-series and scatter plots with sidebar filters |
| **Deep Dive** | Single-country bar chart, scatter with trendline, and correlation matrix |

---

## Tech Stack

| Library | Purpose |
|---------|---------|
| [Streamlit](https://streamlit.io) | App framework |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [NumPy](https://numpy.org) | Numerical operations |
| [Plotly](https://plotly.com/python/) | Interactive charts |
| [Altair](https://altair-viz.github.io) | Declarative visualizations |

---

## Data

Place your source datasets in the `data/` directory. Current pages use randomly generated placeholder data — replace the `df` construction blocks in each page with real data loading (e.g. `pd.read_csv("data/your_file.csv")`).

---

## License

For academic use only — UTS Assignment 3.
