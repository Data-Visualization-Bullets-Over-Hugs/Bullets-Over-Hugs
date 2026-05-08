# Opportunity Cost & Hiroshima Baseline Datasets — Data Dictionary

**Pages: Page 1 (Opportunity Cost Calculator) & Page 3 (Destructive Scale — Hiroshima Baseline)**

These datasets power the interactive comparison between global military spending and the cost of major humanitarian initiatives (Page 1), and the scale visualisation of modern nuclear arsenals against the Hiroshima baseline (Page 3).

---

## Files

### `military_spending.csv` — Military spending by country / region
One row per country or aggregate region. Use this for the donut chart and ranked comparisons of defence budgets on Page 1.

| Column | Type | Description |
|---|---|---|
| `country` | str | Country or aggregate region name (e.g. `"Rest of World"` groups all countries not listed individually) |
| `total` | int | Spending in USD (full integer, e.g. `997000000000` = $997 billion) |
| `label` | str | Human-readable display string (e.g. `"$997B"`) |
| `currency` | str | Currency code — all values are `USD` (constant 2023 prices) |
| `source` | str | Attribution string for the original data source |
| `source_link` | str | URL of the primary source document or database |
| `location` | str | Where this data point appears in the original infographic layout |

**Row count:** 23 rows (22 named countries + 1 aggregate "Rest of World").

**Source:** [Visual Capitalist](https://www.visualcapitalist.com/) citing [SIPRI Military Expenditure Database](https://www.sipri.org/databases/milex) (2023 figures, constant 2023 USD).

**Quick reference — top spenders:**

| Country | Total | Label |
|---|---|---|
| United States | $997,000,000,000 | $997B |
| China | $314,000,000,000 | $314B |
| Rest of World | $306,000,000,000 | $306B |
| Russia | $149,000,000,000 | $149B |
| Germany | $88,000,000,000 | $88B |

---

### `reallocation_costs.csv` — Re-allocation impact costs by initiative
One row per initiative. Use this for the dynamic metric cards on Page 1 that update as the user moves the What-If slider.

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

---

### `nuke_blast_effects.csv` — Nuclear weapon yield and Hiroshima ratio (Page 3)
One row per bomb. 7 rows. Used on Page 3 to power the scale visualisation comparing modern weapons against the Hiroshima baseline.

For full column documentation of `nuke_blast_effects.csv` see `nuke_blast_effects_data_dictionary.md`. The columns specifically used on Page 3 are documented below.

| Column | Type | Description |
|---|---|---|
| `bomb_name` | str | Display name (e.g. `"Tsar Bomba"`) |
| `dropdown_label` | str | Pre-built dropdown option text (e.g. `"Tsar Bomba (50 Mt)"`) |
| `yield_kt` | int | Yield in kilotons |
| `yield_mt` | float | Yield in megatons (`yield_kt / 1000`) |
| `yield_display` | str | Human-readable yield string (e.g. `"50 Mt"`) |
| `hiroshima_ratio` | float | `yield_kt / 15` — how many Little Boy (Hiroshima) bombs this weapon equals in raw explosive yield |
| `country` | str | Country of origin |
| `year` | int | Year first tested or deployed |
| `description` | str | One-sentence historical context |

**Hiroshima ratio quick reference (Page 3 core data):**

| Bomb | yield_kt | hiroshima_ratio |
|---|---|---|
| Little Boy (baseline) | 15 | 1 |
| Fat Man | 20 | 1 |
| R-12 / SS-4 | 2,300 | 153 |
| Dong Feng-4 | 3,300 | 220 |
| Ivy Mike | 10,400 | 693 |
| Castle Bravo | 15,000 | 1,000 |
| Tsar Bomba | 50,000 | 3,333 |

⚠ `hiroshima_ratio` is a **yield ratio only** — it does not scale linearly to casualties or blast radius (which follow a cube-root scaling law). A bomb 3,333× the yield does not cause 3,333× the deaths. Display this caveat on Page 3.

---

## ⚠️ Methodology caveats

1. **"Rest of World" is an aggregate.** The `military_spending.csv` row labelled `Rest of World` ($306B) represents combined spending of all countries not individually itemised. It cannot be mapped to a single country.

2. **SIPRI figures are in constant 2023 USD.** Dollar amounts are inflation-adjusted to a common year and are directly comparable across the dataset.

3. **Re-allocation costs are estimates, not budgets.** Figures in `reallocation_costs.csv` are published cost projections — not approved or spent amounts. Treat them as order-of-magnitude comparisons only.

4. **AI investment figure is private + public combined.** The Stanford HAI $252B figure aggregates reported global private-sector AI investment for a single year. It is not a government budget line.

5. **WASH cost is infrastructure gap, not annual spend.** The UNICEF / World Bank $114B figure represents the estimated total capital investment needed to achieve universal safe water and sanitation access, not an annual expenditure.

6. **Hiroshima ratio is yield-only.** The `hiroshima_ratio` column measures explosive yield equivalence, not destructive equivalence. Blast radius scales as the cube root of yield, so 3,333× the yield produces approximately 15× the blast radius — not 3,333×.

7. **Türkiye spelling.** The country is stored as `Türkiye` (the official UN name as of 2022). Ensure any join with external country-name tables handles this alongside the older `Turkey` spelling.

---

## Source attribution for academic purposes

When citing military spending data:
> SIPRI Military Expenditure Database. Stockholm International Peace Research Institute. sipri.org/databases/milex. Figures in constant 2023 USD. Accessed via Visual Capitalist (2024).

When citing re-allocation cost data:
> International Telecommunication Union (ITU), Stanford HAI AI Index (2024), UNICEF / World Bank WASH Programme, NASA Office of Inspector General (IG-22-003). Full source links in `reallocation_costs.csv`.
