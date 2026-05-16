# Data Dictionary — Bullets Over Hugs

This file documents all datasets used in the project. Each section corresponds to a CSV file in the `data/` directory.

---

## Table of Contents

1. [Conflict Casualties](#1-conflict-casualties)
   - [`conflict_deaths_country_year.csv`](#conflict_deaths_country_yearcsv)
   - [`conflict_deaths_by_type.csv`](#conflict_deaths_by_typecsv)
   - [`conflict_deaths_summary.csv`](#conflict_deaths_summarycsv)
2. [Nuclear Blast Effects](#2-nuclear-blast-effects)
   - [`nuke_blast_effects.csv`](#nuke_blast_effectscsv)
3. [Military Spending & Re-Allocation Costs](#3-military-spending--re-allocation-costs)
   - [`military_spending.csv`](#military_spendingcsv)
   - [`reallocation_costs.csv`](#reallocation_costscsv)

---

## 1. Conflict Casualties

**Source:** [Our World in Data](https://ourworldindata.org/war-and-peace), based on the [UCDP/PRIO Armed Conflict Dataset](https://ucdp.uu.se/) — the standard academic source for armed-conflict statistics.

**Coverage:** 2015–2024, 197 countries.

---

### `conflict_deaths_country_year.csv`

One row per country-year. Use this for the world bubble map with a year slider.

| Column | Type | Description |
|---|---|---|
| `country` | str | Country name |
| `iso3` | str | ISO 3166-1 alpha-3 code (Kosovo uses `KOS` — non-standard but unambiguous) |
| `year` | int | Year (2015–2024) |
| `latitude` | float | Country centroid latitude (for map plotting) |
| `longitude` | float | Country centroid longitude |
| `total_deaths` | int | Total deaths in armed conflicts that year |
| `civilian_deaths` | int | Subset: deaths classified as civilian |
| `combatant_deaths` | int | Subset: deaths classified as combatant |
| `unclear_deaths` | int | Subset: deaths whose victim type couldn't be classified |

`civilian + combatant + unclear = total_deaths` exactly.

---

### `conflict_deaths_by_type.csv`

One row per country-year-conflict_type. Use this for stacked bars / treemaps showing what *kind* of conflict drives deaths in each country. Long format — works directly with Plotly's `color="conflict_type"`.

| Column | Type | Description |
|---|---|---|
| `country` | str | Country name |
| `iso3` | str | ISO-3 code |
| `year` | int | Year |
| `latitude` | float | Country centroid latitude |
| `longitude` | float | Country centroid longitude |
| `conflict_type` | str | Machine-friendly: `interstate`, `intrastate`, `non_state`, `one_sided_violence` |
| `deaths` | int | Deaths attributed to this conflict type that year |
| `conflict_type_label` | str | Display-friendly label (e.g. "One-sided violence") |

The four conflict types sum exactly to `total_deaths` in the country-year table.

**Conflict type definitions:**
- **Interstate**: state vs. state (e.g. Russia–Ukraine 2022)
- **Intrastate**: state vs. non-state group within its borders (civil wars, insurgencies)
- **Non-state**: between organised armed groups, no state party (e.g. cartel wars, militia clashes)
- **One-sided violence**: armed group attacking civilians (e.g. ethnic massacres, terrorism)

---

### `conflict_deaths_summary.csv`

One row per country (decade totals). Use this for top-N rankings, summary cards, and tooltips.

| Column | Type | Description |
|---|---|---|
| `country` | str | Country name |
| `iso3` | str | ISO-3 code |
| `latitude` | float | Country centroid latitude |
| `longitude` | float | Country centroid longitude |
| `total_deaths_2015_2024` | int | Sum of all conflict deaths over the decade |
| `civilian_deaths_2015_2024` | int | Sum of civilian deaths over the decade |
| `combatant_deaths_2015_2024` | int | Sum of combatant deaths over the decade |
| `civilian_share_pct` | float | Civilian deaths as % of total (NaN for countries with zero deaths) |
| `peak_year` | int | The year with the most deaths |
| `peak_year_deaths` | int | Deaths in that peak year |
| `years_with_conflict` | int | Out of 10 years, how many had any deaths |

**⚠️ Methodology caveats:**

1. **UCDP only counts directly battle-related deaths.** Excludes indirect deaths from famine, disease, displacement, etc. Yemen's UCDP total (~58k) is much lower than civil-society estimates of 150k+ that include indirect causes.
2. **Mexico and Brazil**: most deaths are classified as **unclear** rather than civilian or combatant. Don't use civilian-share metrics for these countries without a caveat — the low civilian share (Mexico: 0.7%) is a data artefact, not a finding.
3. **Cumulative civilian share for high-target conflicts**: Palestine (57.8%), Myanmar (58.3%), DRC (56.9%), Syria (27.4%).
4. **Years with zero deaths** are still included as rows. The data is rectangular: 197 countries × 10 years = 1,970 rows in the country-year table.
5. **Kosovo** uses `KOS` instead of an official ISO-3 code (none has been assigned by ISO).

**Re-running:** `notebooks/01_topic1_conflict_casualties.ipynb`

```bash
pip install requests pycountry
```

---

## 2. Nuclear Blast Effects

**Source:** [NUKEMAP](https://nuclearsecrecy.com/nukemap/) (Wellerstein, 2012–2026), running each of 7 historical nuclear weapons over Sydney CBD. Blast and thermal radii derived from:
- Glasstone & Dolan, *The Effects of Nuclear Weapons*, 1977
- Fletcher et al., *Nuclear Bomb Effects Computer*, US Atomic Energy Commission, 1953

Casualty estimates use NUKEMAP's server-side model based on LandScan population data (24-hour ambient population).

---

### `nuke_blast_effects.csv`

One row per bomb. 7 rows × 25 columns.

**Identifiers and display:**

| Column | Type | Description |
|---|---|---|
| `display_order` | int | 1–7. Recommended dropdown order (chronological by historical first-use). |
| `bomb_id` | str | Machine-friendly key. Use this for joins/lookups. |
| `bomb_name` | str | Display name (e.g. "Little Boy"). |
| `dropdown_label` | str | Pre-built dropdown option text (e.g. "Tsar Bomba (50 Mt)"). |

**Bomb specifications:**

| Column | Type | Description |
|---|---|---|
| `country` | str | Country of origin/test. |
| `year` | int | Year first tested or deployed. |
| `yield_kt` | int | Yield in kilotons. |
| `yield_mt` | float | Yield in megatons (`yield_kt / 1000`). |
| `yield_display` | str | Human-readable yield ("15 kt" or "50 Mt"). |
| `burst_type` | str | "Airburst" or "Surface". |

**Geography (Sydney CBD ground zero):**

| Column | Type | Description |
|---|---|---|
| `centroid_lat` | float | -33.8688 (Sydney CBD latitude). Same for all rows. |
| `centroid_lon` | float | 151.2093 (Sydney CBD longitude). Same for all rows. |

**Effect radii (km) — all values in kilometres:**

| Column | Type | Description |
|---|---|---|
| `fireball_km` | float | Maximum fireball radius. Inside: vaporisation. |
| `heavy_5psi_km` | float | 5 psi airblast radius. Inside: most residential buildings collapse, fatalities widespread. |
| `moderate_1psi_km` | float | 1 psi airblast radius. Inside: glass shatters, light injuries widespread. |
| `thermal_3rd_km` | float | Thermal radiation radius for 3rd-degree burns. Inside: severe burns requiring medical attention. |

⚠ **Ring order is not fixed.** For small bombs (< 10 Mt), thermal sits between the two blast rings. For very large bombs, thermal becomes the outermost ring. Sort rings by radius before drawing.

**Casualties:**

| Column | Type | Description |
|---|---|---|
| `fatalities` | int | NUKEMAP estimated fatalities for this bomb over Sydney CBD. |
| `injuries` | int | NUKEMAP estimated injuries. |
| `total_casualties` | int | `fatalities + injuries`. |
| `psi_1_population` | int | Average people in the 1 psi blast range over a 24-hour period. |

**Derived metrics:**

| Column | Type | Description |
|---|---|---|
| `fatalities_per_kt` | float | `fatalities / yield_kt`. Drops sharply with yield (saturation effect). |
| `fatality_to_injury_ratio` | float | `fatalities / injuries`. Rises with yield — bigger bombs kill rather than injure. |
| `hiroshima_ratio` | float | `yield_kt / 15`. How many Hiroshima bombs this weapon equals in raw explosive yield. Little Boy itself = 1.0. |

**Hiroshima ratio quick reference:**

| Bomb | yield_kt | hiroshima_ratio |
|---|---|---|
| Little Boy | 15 | 1 |
| Fat Man | 20 | 1 |
| R-12 (SS-4) | 2,300 | 153 |
| Dong Feng-4 | 3,300 | 220 |
| Ivy Mike | 10,400 | 693 |
| Castle Bravo | 15,000 | 1,000 |
| Tsar Bomba | 50,000 | 3,333 |

⚠ `hiroshima_ratio` is a **yield ratio only** — it does not scale linearly to casualties or blast radius (which follow a cube-root scaling law).

**Context:**

| Column | Type | Description |
|---|---|---|
| `description` | str | One-sentence historical context for the bomb. |
| `notes` | str | Per-bomb methodology notes (detonation altitude, NUKEMAP warnings, model failures). |

**⚠️ Methodology caveats:**

1. **NUKEMAP's own framing**: *"Modeling casualties from a nuclear attack is difficult. These numbers should be seen as evocative, not definitive."*
2. **Fallout deliberately excluded** per the brief. Figures here are direct effects only (blast, thermal, prompt radiation).
3. **24-hour population averaging**: `psi_1_population` is the average number of people in the 1 psi range over a 24-hour cycle. Daytime CBD population would be much higher; nighttime much lower.
4. **Yields > 20 Mt are extrapolated**: NUKEMAP explicitly warns that for yields above 20 Mt (Tsar Bomba), the model scales from 20 Mt validation. Tsar Bomba figures should be treated as approximate.
5. **Surface vs airburst**: Castle Bravo and Ivy Mike are surface bursts. All others are airbursts. NUKEMAP's defaults for each preset are used.
6. **No 20 psi or 500 rem rings** for R-12, Dong Feng-4, and Tsar Bomba — NUKEMAP cannot compute these effects at the optimal detonation altitude for those weapons.

**Re-running:** `notebooks/02_topic2_nuke_simulator.ipynb`

```bash
pip install openpyxl pandas
```

**Academic citation:**
> Wellerstein, Alex. *NUKEMAP*. nuclearsecrecy.com/nukemap/. Underlying physics from Glasstone & Dolan (1977) and the US AEC Nuclear Bomb Effects Computer (1953).

---

## 3. Military Spending & Re-Allocation Costs

**Source:** [SIPRI Military Expenditure Database](https://www.sipri.org/databases/milex) (2023 figures, constant 2023 USD), via [Visual Capitalist](https://www.visualcapitalist.com/). Re-allocation costs sourced from ITU, Stanford HAI, UNICEF/World Bank, and NASA OIG.

---

### `military_spending.csv`

One row per country or aggregate region. Use this for the donut chart and ranked comparisons of defence budgets.

| Column | Type | Description |
|---|---|---|
| `country` | str | Country or aggregate region name (`"Rest of World"` groups all countries not listed individually) |
| `total` | int | Spending in USD (full integer, e.g. `997000000000` = $997 billion) |
| `label` | str | Human-readable display string (e.g. `"$997B"`) |
| `currency` | str | Currency code — all values are `USD` (constant 2023 prices) |
| `source` | str | Attribution string for the original data source |
| `source_link` | str | URL of the primary source document or database |
| `location` | str | Where this data point appears in the original infographic layout |

**Row count:** 23 rows (22 named countries + 1 aggregate "Rest of World").

**Top spenders:**

| Country | Total | Label |
|---|---|---|
| United States | $997,000,000,000 | $997B |
| China | $314,000,000,000 | $314B |
| Rest of World | $306,000,000,000 | $306B |
| Russia | $149,000,000,000 | $149B |
| Germany | $88,000,000,000 | $88B |

---

### `reallocation_costs.csv`

One row per initiative. Use this for the dynamic metric cards that update as the user moves the What-If slider.

| Column | Type | Description |
|---|---|---|
| `initiative` | str | Name of the global initiative or programme |
| `total` | int | Estimated cost in USD (full integer) |
| `label` | str | Human-readable display string (e.g. `"$428B"`) |
| `currency` | str | Currency code — all values are `USD` |
| `source` | str | Attribution string for the cost estimate |
| `source_link` | str | URL of the primary source document or report |
| `location` | str | Section/page within the source document where the figure appears |

**Row count:** 4 rows.

| Initiative | Total | Primary Source |
|---|---|---|
| Global Internet Connection | $428B | [ITU: Connecting Humanity](https://www.itu.int/itu-d/reports/statistics/2023/10/06/ff23-global-internet-connectivity-statistics/) — Page 4 / Executive Summary |
| Global AI Investment | $252B | [Stanford HAI AI Index](https://aiindex.stanford.edu/report/) — Chapter 4: Economy |
| Global WASH Infrastructure | $114B | [UNICEF / World Bank](https://www.unicef.org/wash) — Overview / Executive Summary |
| NASA Artemis Missions | $93B | [NASA OIG (IG-22-003)](https://oig.nasa.gov/docs/IG-22-003.pdf) — Results in Brief (Page 2) |

**⚠️ Methodology caveats:**

1. **"Rest of World" is an aggregate.** Cannot be mapped to a single country.
2. **SIPRI figures are in constant 2023 USD.** Dollar amounts are inflation-adjusted and directly comparable across the dataset.
3. **Re-allocation costs are estimates, not budgets.** Figures are published cost projections — not approved or spent amounts. Treat them as order-of-magnitude comparisons only.
4. **AI investment figure is private + public combined.** The $252B aggregates reported global private-sector AI investment for a single year — it is not a government budget line.
5. **WASH cost is infrastructure gap, not annual spend.** The $114B represents the estimated total capital investment needed to achieve universal safe water and sanitation access.
6. **Hiroshima ratio is yield-only.** Blast radius scales as the cube root of yield, so 3,333× the yield produces approximately 15× the blast radius — not 3,333×.
7. **Türkiye spelling.** Stored as `Türkiye` (official UN name as of 2022). Ensure any join with external country-name tables handles this alongside the older `Turkey` spelling.

**Academic citations:**
> SIPRI Military Expenditure Database. Stockholm International Peace Research Institute. sipri.org/databases/milex. Figures in constant 2023 USD. Accessed via Visual Capitalist (2024).

> International Telecommunication Union (ITU), Stanford HAI AI Index (2024), UNICEF / World Bank WASH Programme, NASA Office of Inspector General (IG-22-003). Full source links in `reallocation_costs.csv`.
