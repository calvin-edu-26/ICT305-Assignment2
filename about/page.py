import streamlit as st

# ═════════════════════════════════════════════════════════════════════════════
# ABOUT THE TEAM PAGE
# Displays group member information as required by the project brief.
# Photos stored in about/assets/ — each member to replace placeholder.
# Emails to be updated by each member before submission.
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(layout="wide")

st.title("About the Team")
st.markdown(
    "This dashboard was developed as part of the **ICT305 Data Visualisation "
    "and Simulation** group project at Murdoch University."
)

st.divider()

# ── TEAM MEMBERS ──────────────────────────────────────────────────────────────
# Each member to replace:
#   - about/assets/<name>.jpg with their actual photo
#   - email placeholder with their actual university email

MEMBERS = [
    {
        "name": "Tong Yong Siang (Calvin)",
        "student_id": "32809789",
        "email": "32809789@student.murdoch.edu.au",
        "sub_heuristic": "Carbon Emissions by Nation",
        "photo": "about/assets/calvin.jpg",
    },
    {
        "name": "Ruben Raj",
        "student_id": "35773698",
        "email": "35773698@student.murdoch.edu.au",
        "sub_heuristic": "Climate Vulnerability & Exposure",
        "photo": "about/assets/ruben.jpg",
    },
    {
        "name": "Lam Thanh Chieu",
        "student_id": "35614306",
        "email": "35614306@student.murdoch.edu.au",
        "sub_heuristic": "Extreme Weather & Economic Damage",
        "photo": "about/assets/lam.jpg",
    },
    {
        "name": "Lucas Lord Eivan De Leon",
        "student_id": "35585816",
        "email": "35585816@student.murdoch.edu.au",
        "sub_heuristic": "Sea Level Rise & Displacement",
        "photo": "about/assets/lucas.jpg",
    },
    {
        "name": "Huang Nengjie",
        "student_id": "35021998",
        "email": "35021998@student.murdoch.edu.au",
        "sub_heuristic": "Climate Finance Gap",
        "photo": "about/assets/nengjie.jpg",
    },
]

cols = st.columns(5)

for col, member in zip(cols, MEMBERS):
    with col:
        with st.container(border=True):
            try:
                st.image(member["photo"], use_container_width=True)
            except Exception:
                st.image(
                    "https://via.placeholder.com/150x150.png?text=Photo",
                    use_container_width=True
                )
            st.markdown(f"**{member['name']}**")
            st.markdown(f"_{member['sub_heuristic']}_")
            st.caption(f"Student ID: {member['student_id']}")
            st.caption(f"✉️ {member['email']}")

st.divider()
st.caption("ICT305 — Data Visualisation and Simulation | Murdoch University")