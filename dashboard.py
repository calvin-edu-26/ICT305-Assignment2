import streamlit as st

heuristic1 = st.Page("heuristic1/page.py", url_path="heuristics1", title="Heuristic 1")
heuristic2 = st.Page("heuristic2/page.py", url_path="heuristics2", title="Heuristic 2")
heuristic3 = st.Page("heuristic3/page.py", url_path="heuristics3", title="Heuristic 3")
heuristic4 = st.Page("heuristic4/page.py", url_path="heuristics4", title="Heuristic 4")
heuristic5 = st.Page("heuristic5/page.py", url_path="heuristics5", title="Heuristic 5")

pg = st.navigation([heuristic1, heuristic2, heuristic3, heuristic4, heuristic5])
pg.run()