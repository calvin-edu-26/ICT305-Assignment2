import streamlit as st

def render(recommendations):

    bullets = "".join(
        f"<li>{item}</li>"
        for item in recommendations
    )

    st.markdown(
        f"""
<div class="story-box">
<h3>💡 Recommendations</h3>

<ul>
{bullets}
</ul>
</div>
""",
        unsafe_allow_html=True
    )
