# Nuclear Blast Effects Dataset — Data Dictionary

**Topic 2: Localised Impact Simulator (Sydney CBD)**

## Source

Data collected from [NUKEMAP](https://nuclearsecrecy.com/nukemap/) (Wellerstein, 2012–2026), running each of 7 historical nuclear weapons over Sydney CBD. NUKEMAP's blast and thermal radii come from public-domain physics in:
- Glasstone & Dolan, *The Effects of Nuclear Weapons*, 1977
- Fletcher et al., *Nuclear Bomb Effects Computer*, US Atomic Energy Commission, 1953

Casualty estimates use NUKEMAP's server-side model based on LandScan population data (24-hour ambient population).

**Bomb specifications** (yields, burst altitudes, fission fractions) sourced from NUKEMAP's `presets.js`, traceable to historical record.

## File: `nuke_blast_effects.csv`

One row per bomb. 7 rows × 25 columns.

### Identifiers and display

| Column | Type | Description |
|---|---|---|
| `display_order` | int | 1–7. Recommended dropdown order (chronological by historical first-use). |
| `bomb_id` | str | Machine-friendly key. Use this for joins/lookups. |
| `bomb_name` | str | Display name (e.g. "Little Boy"). |
| `dropdown_label` | str | Pre-built dropdown option text (e.g. "Tsar Bomba (50 Mt)"). |

### Bomb specifications

| Column | Type | Description |
|---|---|---|
| `country` | str | Country of origin/test. |
| `year` | int | Year first tested or deployed. |
| `yield_kt` | int | Yield in kilotons. |
| `yield_mt` | float | Yield in megatons (yield_kt / 1000). |
| `yield_display` | str | Human-readable yield ("15 kt" or "50 Mt"). |
| `burst_type` | str | "Airburst" or "Surface". |

### Geography (Sydney CBD ground zero)

| Column | Type | Description |
|---|---|---|
| `centroid_lat` | float | -33.8688 (Sydney CBD latitude). Same for all rows. |
| `centroid_lon` | float | 151.2093 (Sydney CBD longitude). Same for all rows. |

### Effect radii (km)

These are the four ring radii to draw on the map. **All in kilometres.**

| Column | Type | Description |
|---|---|---|
| `fireball_km` | float | Maximum fireball radius. Inside: vaporisation. |
| `heavy_5psi_km` | float | 5 psi airblast radius. Inside: most residential buildings collapse, fatalities widespread. NUKEMAP labels this "Moderate blast damage"; the brief calls it "Heavy damage". |
| `moderate_1psi_km` | float | 1 psi airblast radius. Inside: glass shatters, light injuries widespread. NUKEMAP labels this "Light blast damage"; the brief calls it "Moderate damage". |
| `thermal_3rd_km` | float | Thermal radiation radius for 3rd-degree burns. Inside: severe burns requiring medical attention. |

⚠ **Ring order is not fixed.** For small bombs (< 10 Mt), thermal sits between the two blast rings. For very large bombs, thermal becomes the outermost ring. Sort rings by radius before drawing — see VISUALISER_GUIDE.md.

### Casualties

| Column | Type | Description |
|---|---|---|
| `fatalities` | int | NUKEMAP estimated fatalities for this bomb over Sydney CBD. |
| `injuries` | int | NUKEMAP estimated injuries. |
| `total_casualties` | int | fatalities + injuries. |
| `psi_1_population` | int | Average people in the 1 psi blast range over a 24-hour period. |

### Derived metrics

| Column | Type | Description |
|---|---|---|
| `fatalities_per_kt` | float | fatalities / yield_kt. Drops sharply with yield (saturation effect). |
| `fatality_to_injury_ratio` | float | fatalities / injuries. Rises with yield — bigger bombs kill rather than injure. |
| `hiroshima_ratio` | float | yield_kt / 15. How many Hiroshima bombs (Little Boy, 15 kt) this weapon equals in raw explosive yield. Little Boy itself = 1.0 by definition. |

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

⚠ `hiroshima_ratio` is a **yield ratio only** — it does not scale linearly to casualties or blast radius (which follow a cube-root scaling law). A bomb 3,333× the yield does not cause 3,333× the deaths.

### Context

| Column | Type | Description |
|---|---|---|
| `description` | str | One-sentence historical context for the bomb. |
| `notes` | str | Per-bomb methodology notes (detonation altitude, NUKEMAP warnings, model failures). |

## ⚠ Methodology caveats (important for narrative integrity)

1. **NUKEMAP's own framing**: *"Modeling casualties from a nuclear attack is difficult. These numbers should be seen as evocative, not definitive."* Display this disclaimer prominently in the dashboard.

2. **Fallout deliberately excluded** per the brief. UCDP/NUKEMAP fatality figures here are direct effects only (blast, thermal, prompt radiation). Real-world fatalities from a surface burst would be much higher when fallout is included — Castle Bravo, Ivy Mike, and Tsar Bomba (the surface bursts here) would produce massive radioactive contamination not reflected in these numbers.

3. **24-hour population averaging**: `psi_1_population` is the average number of people in the 1 psi range over a 24-hour cycle. Daytime CBD population would be much higher; nighttime much lower. The casualty figures use this average.

4. **Yields > 20 Mt are extrapolated**: NUKEMAP explicitly warns that for yields above 20 Mt (Tsar Bomba), the model scales from 20 Mt validation rather than direct calculation. Tsar Bomba figures should be treated as approximate.

5. **Surface vs airburst**: Castle Bravo and Ivy Mike are surface bursts (test detonations on coral atolls). All others are airbursts at altitudes optimised for blast effect. NUKEMAP's defaults for each preset are used.

6. **No 20 psi or 500 rem rings** for some bombs: NUKEMAP cannot compute 20 psi blast or 500 rem radiation effects when the optimal-airblast detonation altitude exceeds the maximum altitude at which those effects reach the ground. Affects R-12, Dong Feng-4, and Tsar Bomba. Not a problem for our dashboard since neither effect is part of the brief.

## Re-running the data preparation

The notebook `notebooks/02_topic2_nuke_simulator.ipynb` produces this file from a hand-collected raw lookup template (`notebooks/nukemap_lookups_template.xlsx`, gitignored). To re-run:

```bash
pip install openpyxl pandas  # in addition to project requirements
```

Open the notebook and run all cells. To regenerate the raw lookups (e.g., if NUKEMAP updates), follow the instructions in the Excel template's "Instructions" sheet.

## Source attribution for academic purposes

When citing the source of the casualty and radius data:

> Wellerstein, Alex. *NUKEMAP*. nuclearsecrecy.com/nukemap/. Lookups performed [INSERT DATE]. Underlying physics from Glasstone & Dolan (1977) and the US AEC Nuclear Bomb Effects Computer (1953).
