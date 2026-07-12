# ── SHARED CONSTANTS ──────────────────────────────────────────────────────────
# Shared across heuristic3 chart files and loaders.
# Import with: from heuristic3.constants import COLORS, ACCENT, INCOME_GROUPS, INCOME_ORDER

# Colour-blind friendly palette — one colour per World Bank income group.
COLORS = {
    "Low Income":          "#d62728",
    "Lower Middle Income": "#ff7f0e",
    "Upper Middle Income": "#2ca02c",
    "High Income":         "#1f77b4",
}
ACCENT = "#d62728"

# ── INCOME GROUP LOOKUP  (World Bank 2023) ────────────────────────────────────
INCOME_GROUPS = {
    "Australia":"High Income","Austria":"High Income","Belgium":"High Income",
    "Canada":"High Income","Denmark":"High Income","Finland":"High Income",
    "France":"High Income","Germany":"High Income","Iceland":"High Income",
    "Ireland":"High Income","Italy":"High Income","Japan":"High Income",
    "Luxembourg":"High Income","Netherlands":"High Income","New Zealand":"High Income",
    "Norway":"High Income","Portugal":"High Income","Singapore":"High Income",
    "South Korea":"High Income","Spain":"High Income","Sweden":"High Income",
    "Switzerland":"High Income","United Kingdom":"High Income","United States":"High Income",
    "Israel":"High Income","Greece":"High Income","Czech Republic":"High Income",
    "Slovakia":"High Income","Slovenia":"High Income","Estonia":"High Income",
    "Latvia":"High Income","Lithuania":"High Income","Poland":"High Income",
    "Hungary":"High Income","Croatia":"High Income","Romania":"High Income",
    "Bulgaria":"High Income","Chile":"High Income","Uruguay":"High Income",
    "Saudi Arabia":"High Income","United Arab Emirates":"High Income",
    "Kuwait":"High Income","Qatar":"High Income","Bahrain":"High Income",
    "Oman":"High Income","Malta":"High Income","Cyprus":"High Income",
    "China":"Upper Middle Income","Brazil":"Upper Middle Income",
    "Mexico":"Upper Middle Income","Russia":"Upper Middle Income",
    "Turkey":"Upper Middle Income","South Africa":"Upper Middle Income",
    "Argentina":"Upper Middle Income","Colombia":"Upper Middle Income",
    "Peru":"Upper Middle Income","Malaysia":"Upper Middle Income",
    "Thailand":"Upper Middle Income","Iran":"Upper Middle Income",
    "Iraq":"Upper Middle Income","Ecuador":"Upper Middle Income",
    "Kazakhstan":"Upper Middle Income","Algeria":"Upper Middle Income",
    "Dominican Republic":"Upper Middle Income","Belarus":"Upper Middle Income",
    "Azerbaijan":"Upper Middle Income","Albania":"Upper Middle Income",
    "Botswana":"Upper Middle Income","Gabon":"Upper Middle Income",
    "India":"Lower Middle Income","Indonesia":"Lower Middle Income",
    "Philippines":"Lower Middle Income","Vietnam":"Lower Middle Income",
    "Bangladesh":"Lower Middle Income","Pakistan":"Lower Middle Income",
    "Nigeria":"Lower Middle Income","Egypt":"Lower Middle Income",
    "Morocco":"Lower Middle Income","Ghana":"Lower Middle Income",
    "Kenya":"Lower Middle Income","Senegal":"Lower Middle Income",
    "Cambodia":"Lower Middle Income","Myanmar":"Lower Middle Income",
    "Bolivia":"Lower Middle Income","Honduras":"Lower Middle Income",
    "El Salvador":"Lower Middle Income","Nicaragua":"Lower Middle Income",
    "Sri Lanka":"Lower Middle Income","Nepal":"Lower Middle Income",
    "Zambia":"Lower Middle Income","Zimbabwe":"Lower Middle Income",
    "Ivory Coast":"Lower Middle Income",
    "Ethiopia":"Low Income","Tanzania":"Low Income","Uganda":"Low Income",
    "Mozambique":"Low Income","Madagascar":"Low Income","Malawi":"Low Income",
    "Mali":"Low Income","Burkina Faso":"Low Income","Niger":"Low Income",
    "Chad":"Low Income","Democratic Republic of Congo":"Low Income",
    "Afghanistan":"Low Income","Haiti":"Low Income","Sudan":"Low Income",
    "South Sudan":"Low Income","Guinea":"Low Income","Togo":"Low Income",
    "Sierra Leone":"Low Income","Liberia":"Low Income",
    "Central African Republic":"Low Income","Somalia":"Low Income",
    "Rwanda":"Low Income","Burundi":"Low Income",
    "Dominica":"Low Income","Samoa":"Low Income",
}
INCOME_ORDER = ["Low Income","Lower Middle Income","Upper Middle Income","High Income"]
