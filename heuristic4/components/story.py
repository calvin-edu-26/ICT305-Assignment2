import streamlit as st

def story_header(number, title, subtitle):

    st.markdown(f"""
<div class="section-card">
<h3>{number} {title}</h3>
<p>{subtitle}</p>
</div>
""", unsafe_allow_html=True)

def insight_box(insights, analysis, conclusion=None):

    bullets = "".join(
        f"<li>{item}</li>"
        for item in insights
    )

    conclusion_html = ""

    if conclusion:
        conclusion_html = f"""
<h3 style="margin-top:22px;">Key Takeaway</h3>
<p style="font-size:20px;font-weight:700;color:var(--text-color);line-height:1.5;">
{conclusion}
</p>
"""

    st.markdown(
        f"""
<div class="story-box">
<h3>🔍 Insights</h3>

<ul>
{bullets}
</ul>

<h3>📊 Analysis</h3>

<p>{analysis}</p>

{conclusion_html}
</div>
""",
        unsafe_allow_html=True
    )

def risk_zone_legend():

    st.markdown("""
<div class="story-box">
<h3>Understanding the Risk Zones</h3>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:20px;">

<div style="display:flex;align-items:flex-start;gap:12px;">
<div style="width:18px;height:18px;background:#DC2626;border-radius:4px;margin-top:3px;flex-shrink:0;"></div>
<div>
<b style="color:var(--text-color);">Critical Risk</b>
<p style="margin:6px 0 0 0;color:var(--text-color);opacity:0.85;">
High displacement pressure combined with lower economic capacity.
These countries need urgent adaptation support.
</p>
</div>
</div>

<div style="display:flex;align-items:flex-start;gap:12px;">
<div style="width:18px;height:18px;background:#F97316;border-radius:4px;margin-top:3px;flex-shrink:0;"></div>
<div>
<b style="color:var(--text-color);">High Exposure, Higher Capacity</b>
<p style="margin:6px 0 0 0;color:var(--text-color);opacity:0.85;">
High exposure but stronger economic ability to invest in adaptation and resilience.
</p>
</div>
</div>

</div>
</div>
""", unsafe_allow_html=True)

def decision_support_box():

    st.markdown("""
<div class="story-box">
<h3>Decision Support</h3>
<p>
This dashboard helps decision-makers identify where climate adaptation support should be prioritised.
</p>

<ul>
<li><b>Governments:</b> plan relocation, coastal protection, and adaptation funding.</li>
<li><b>NGOs:</b> identify countries needing urgent humanitarian or resilience support.</li>
<li><b>International climate agencies:</b> compare exposure, responsibility, and adaptive capacity.</li>
<li><b>Policymakers:</b> prioritise countries where high displacement pressure overlaps with lower economic readiness.</li>
</ul>
</div>
""", unsafe_allow_html=True)
