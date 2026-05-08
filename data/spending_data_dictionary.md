# Spending & Re-Allocation Datasets — Data Dictionary

**Topic: Global Military Spending vs. Re-Allocation Impact Costs**

These two tables power the infographic comparing the world's annual military budgets against the one-time cost of major humanitarian, scientific, and infrastructure initiatives.

---

## Files

### `military_spending.csv` — Military spending by country / region
One row per country or aggregate region. Use this for bar charts, treemaps, or any ranked comparison of defence budgets.

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

**Source:** [Visual Capitalist](https://www.visualcapitalist.com/) citing [SIPRI Military Expenditure Database](https://www.sipri.org/databases/milex) (2023 figures).

---

### `reallocation_costs.csv` — Re-allocation impact costs by initiative
One row per initiative. Use this for side-by-side comparisons against `military_spending.csv` totals.

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

## ⚠️ Methodology caveats

1. **"Rest of World" is an aggregate.** The `military_spending.csv` row labelled `Rest of World` ($306B) represents the combined spending of all countries not individually itemised. It cannot be attributed to any single country on a map.

2. **SIPRI figures are in constant 2023 USD.** Dollar amounts are inflation-adjusted to a common year, so they are directly comparable across the dataset.

3. **Re-allocation costs are estimates, not budgets.** The figures in `reallocation_costs.csv` are published cost projections or programme estimates — not approved or spent amounts. Treat them as order-of-magnitude comparisons only.

4. **AI investment figure is private + public combined.** The Stanford HAI $252B figure (Chapter 4: Economy) aggregates reported private-sector AI investment globally for a single year. It is not a government budget line.

5. **WASH cost is infrastructure gap, not annual spend.** The UNICEF / World Bank $114B figure represents the estimated total capital investment needed to achieve universal safe water and sanitation access, not an annual expenditure.

6. **Türkiye spelling.** The country is stored as `Türkiye` (the official UN name as of 2022). Ensure any join with external country-name tables handles this alongside the older `Turkey` spelling.
