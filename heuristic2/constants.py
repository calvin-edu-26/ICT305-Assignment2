# ── SHARED CONSTANTS ──────────────────────────────────────────────────────────
# Shared across heuristic2 chart files and overview/chart.py.
# Import with: from heuristic2.constants import SUBREGION_COLOURS, NAME_OVERRIDES

# Fixed colour palette for UN M49 sub-regions.
# Consistent across scatter plot and bar chart.
# Designed for readability on dark backgrounds.
SUBREGION_COLOURS = {
    "Northern Africa":           "#FFD700",
    "Sub-Saharan Africa":        "#FF6B35",
    "Northern America":          "#4FC3F7",
    "Latin America & Caribbean": "#81C784",
    "Central Asia":              "#CE93D8",
    "Eastern Asia":              "#80DEEA",
    "South-eastern Asia":        "#FFB74D",
    "Southern Asia":             "#F48FB1",
    "Western Asia":              "#BCAAA4",
    "Eastern Europe":            "#90CAF9",
    "Northern Europe":           "#FFFFFF",
    "Southern Europe":           "#A5D6A7",
    "Western Europe":            "#B39DDB",
    "Oceania":                   "#80CBC4",
    "Other":                     "#757575",
}

# Country name overrides — exact strings as they appear in ND-GAIN dataset.
# Truncated or verbose names replaced with clean display labels.
# Used in bar_chart.py and overview/chart.py.
NAME_OVERRIDES = {
    "Congo, the Democratic Republic o": "DR Congo",
    "Micronesia, Federated States of": "Micronesia",
    "Sao Tome and Principe": "São Tomé & Príncipe",
    "Bolivia, Plurinational State of": "Bolivia",
    "Tanzania, United Republic of": "Tanzania",
    "Iran, Islamic Republic of": "Iran",
    "Korea, Republic of": "South Korea",
    "Korea, Democratic People's Repub": "North Korea",
    "Lao People's Democratic Republic": "Laos",
    "Moldova, Republic of": "Moldova",
    "Venezuela, Bolivarian Republic o": "Venezuela",
    "Syrian Arab Republic": "Syria",
    "Libyan Arab Jamahiriya": "Libya",
    "Saint Vincent and the Grenadines": "St. Vincent & Grenadines",
    "Saint Kitts and Nevis": "St. Kitts & Nevis",
}