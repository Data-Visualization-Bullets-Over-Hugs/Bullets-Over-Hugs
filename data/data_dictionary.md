# Conflict Casualties Dataset — Data Dictionary

**Topic 1: Modern Conflicts and Casualties (2015–2024)**

## Source
All data is from [Our World in Data](https://ourworldindata.org/war-and-peace), based on the [UCDP/PRIO Armed Conflict Dataset](https://ucdp.uu.se/) — the standard academic source for armed-conflict statistics.

## Files

### `conflict_deaths_country_year.csv` — main map/timeline table
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

### `conflict_deaths_by_type.csv` — conflict-type breakdown (long format)
One row per country-year-conflict_type. Use this for stacked bars / treemaps showing what *kind* of conflict drives deaths in each country. Long format means it works directly with Plotly's `color="conflict_type"`.

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

### `conflict_deaths_summary.csv` — country totals (one row per country)
Use this for top-N rankings, summary cards, and tooltips.

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

## ⚠️ Methodology caveats (important for narrative integrity)

1. **UCDP only counts directly battle-related deaths.** Excludes indirect deaths from famine, disease, displacement, etc. So Yemen's UCDP total (~58k) is much lower than civil-society estimates of 150k+ that include indirect causes. The dashboard should note this if displaying Yemen.

2. **Mexico and Brazil**: most deaths are classified as **unclear** rather than civilian or combatant. Don't use civilian-share metrics for these countries without a caveat — the low civilian share (Mexico: 0.7%) is a data artefact, not a finding.

3. **Cumulative civilian share for high-target conflicts**: Palestine (57.8%), Myanmar (58.3%), DRC (56.9%), Syria (27.4%). These are conflicts where civilian targeting is/was a defining feature.

4. **Years with zero deaths** are still included as rows. Most countries are peaceful in most years — that's the point. The data is rectangular: 197 countries × 10 years = 1,970 rows in the country-year table.

5. **Kosovo** uses `KOS` instead of an official ISO-3 code (none has been assigned by ISO). Make sure any country-name lookups in the dashboard handle this.

## Re-running the data preparation

The notebook `notebooks/01_topic1_conflict_casualties.ipynb` produces these files. To re-run:

```bash
pip install requests pycountry  # in addition to the project's requirements.txt
```

Then open the notebook and run all cells. The OWID downloads are cached in `data/raw/` (gitignored) so re-runs are fast.
