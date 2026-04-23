import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from data.assumptions import COMPETITORS

st.set_page_config(page_title="Competitive Landscape — BioScope", layout="wide")

BLUE = "#1B4F72"; GREEN = "#2ECC71"; ORANGE = "#E67E22"

st.title("⚔️ Competitive Landscape")
st.markdown(
    "BioScope's competitive position across **turnaround speed** and **analyte breadth** — "
    "the two dimensions that define the Clean Protein Certification™ value proposition."
)

# ── Positioning bubble chart ───────────────────────────────────────────────────
st.subheader("Positioning Map — Speed vs. Analyte Coverage")

# Color by type
type_colors = {
    'Commercial Lab': '#E74C3C',
    'Rapid Test Kits': '#E67E22',
    'Microbiology Diagnostics': '#E67E22',
    'Life Science / Diagnostics': '#E67E22',
    'Analytical Instruments': '#9B59B6',
    'Analytical Instruments / MS': '#9B59B6',
    'Life Science / Instruments': '#9B59B6',
    'Certification Body': '#95A5A6',
    'NGS / DNA Startup': '#3498DB',
    'Origin Verification': '#3498DB',
    'Integrated Certification Platform': '#2ECC71',
}

fig_pos = go.Figure()

for c in COMPETITORS:
    is_bio = c['name'].startswith('BioScope')
    color = type_colors.get(c['type'], '#7F8C8D')
    size = max(8, min(60, c['revenue_B'] * 2 + (12 if is_bio else 4)))

    fig_pos.add_trace(go.Scatter(
        x=[c['speed']],
        y=[c['breadth']],
        mode='markers+text',
        marker=dict(
            size=size,
            color=color,
            line=dict(width=3 if is_bio else 1, color='black' if is_bio else color),
            opacity=1.0 if is_bio else 0.75,
            symbol='star' if is_bio else 'circle',
        ),
        text=[c['name'].replace('BioScope (Clean Protein Cert™)', '★ BioScope')],
        textposition='top center' if not is_bio else 'middle right',
        textfont=dict(size=11 if is_bio else 9, color='black' if is_bio else '#2C3E50'),
        name=c['type'],
        hovertemplate=(
            f"<b>{c['name']}</b><br>"
            f"Type: {c['type']}<br>"
            f"Revenue: {c['revenue']}<br>"
            f"Speed Score: {c['speed']}/10<br>"
            f"Breadth Score: {c['breadth']}/10<br>"
            f"<extra></extra>"
        ),
        showlegend=False,
    ))

fig_pos.add_annotation(x=2, y=5, text="<b>Slow &amp; Narrow</b><br>(commodity labs)", showarrow=False,
                        font=dict(size=10, color='#BDC3C7'))
fig_pos.add_annotation(x=8, y=2, text="<b>Fast &amp; Narrow</b><br>(single-analyte kits)", showarrow=False,
                        font=dict(size=10, color='#BDC3C7'))
fig_pos.add_annotation(x=8.5, y=9.5, text="<b>★ BioScope Target Zone</b>", showarrow=False,
                        font=dict(size=11, color=GREEN, family='Arial Black'))

# Quadrant lines
fig_pos.add_hline(y=5, line_dash='dot', line_color='#D5D8DC')
fig_pos.add_vline(x=5, line_dash='dot', line_color='#D5D8DC')

fig_pos.update_layout(
    height=520,
    xaxis=dict(title='Turnaround Speed  →  (1 = Days/Weeks, 10 = Minutes)',
               range=[0, 11], showgrid=True, gridcolor='#F2F3F4'),
    yaxis=dict(title='Analyte Coverage  →  (1 = Narrow, 10 = Comprehensive)',
               range=[0, 11], showgrid=True, gridcolor='#F2F3F4'),
    margin=dict(l=0, r=0, t=20, b=10),
    plot_bgcolor='white', paper_bgcolor='white',
    showlegend=False,
)
st.plotly_chart(fig_pos, use_container_width=True)
st.caption("Bubble size proportional to company revenue. ★ = BioScope. Scores are illustrative.")

# ── Category legend ────────────────────────────────────────────────────────────
leg1, leg2, leg3, leg4, leg5 = st.columns(5)
leg1.markdown("🔴 **Commercial Labs**")
leg2.markdown("🟠 **Rapid Test / Diagnostics**")
leg3.markdown("🟣 **Analytical Instruments**")
leg4.markdown("⚫ **Certification Bodies**")
leg5.markdown("🔵 **Startups**  🟢 **BioScope**")

st.divider()

# ── Competitor table ───────────────────────────────────────────────────────────
st.subheader("Competitor Detail Table")

filter_type = st.multiselect(
    "Filter by type",
    options=sorted(set(c['type'] for c in COMPETITORS)),
    default=sorted(set(c['type'] for c in COMPETITORS)),
)

filtered = [c for c in COMPETITORS if c['type'] in filter_type]

rows = []
for c in filtered:
    rows.append({
        'Competitor': c['name'],
        'Type': c['type'],
        'Revenue': c['revenue'],
        'Funding / Mkt Cap': c['funding'],
        'Segments Served': c['segments'],
        'BioScope Differentiation': c['differentiation'],
    })

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, hide_index=True,
             column_config={
                 'BioScope Differentiation': st.column_config.TextColumn(width='large'),
             })

# ── Key differentiation summary ────────────────────────────────────────────────
st.divider()
st.subheader("BioScope vs. Competition — 3 Core Differentiators")

d1, d2, d3 = st.columns(3)

with d1:
    st.markdown(f"""
    <div style="background:#EBF5FB;border-radius:10px;padding:16px;border-left:4px solid {BLUE}">
        <div style="font-weight:700;color:{BLUE};margin-bottom:6px">⚡ Speed</div>
        <div style="font-size:13px">
        BioScope delivers results in <b>minutes</b> via ambient DESI-MS.
        Commercial labs (Eurofins, SGS) require <b>3–21 days</b>.
        Rapid kits are fast but answer only one question at a time.
        </div>
    </div>""", unsafe_allow_html=True)

with d2:
    st.markdown(f"""
    <div style="background:#EAFAF1;border-radius:10px;padding:16px;border-left:4px solid {GREEN}">
        <div style="font-weight:700;color:#196F3D;margin-bottom:6px">🔬 Comprehensiveness</div>
        <div style="font-size:13px">
        <b>14 analyte categories</b> across residues, welfare biomarkers, and authenticity markers in a
        single scan — no sample fragmentation. Competitors either test one analyte class
        (rapid kits) or charge per analyte (commercial labs).
        </div>
    </div>""", unsafe_allow_html=True)

with d3:
    st.markdown(f"""
    <div style="background:#FEF9E7;border-radius:10px;padding:16px;border-left:4px solid {ORANGE}">
        <div style="font-weight:700;color:#784212;margin-bottom:6px">🏷️ Certification Value</div>
        <div style="font-size:13px">
        No existing competitor combines <b>testing + welfare + authenticity + origin</b> into a single
        investable certification badge. Bureau Veritas certifies process; BioScope certifies
        the product. That's a new category.
        </div>
    </div>""", unsafe_allow_html=True)

# ── White-space map ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("White Space — Capability Gaps in the Market")

gap_data = {
    'Capability': [
        'Multi-residue chemical testing',
        'Animal welfare biomarkers (cortisol, lactate)',
        'Species authentication (DNA)',
        'Geographic origin (IRMS)',
        'Nutritional fingerprint (fatty acids, vitamins)',
        'All of the above in one scan',
        'Certification badge + traceability report',
    ],
    'Commercial Labs': ['✅', '⚠️ Research only', '⚠️ Outsourced', '⚠️ Few labs', '✅ (unbundled, high cost)', '❌', '❌'],
    'Rapid Test Kits': ['⚠️ Single analyte', '❌', '❌', '❌', '❌', '❌', '❌'],
    'Instruments (Bruker etc.)': ['✅ (DIY)', '⚠️', '⚠️', '✅ (IRMS only)', '✅ (GC-FID)', '❌ (separate instruments)', '❌'],
    'BioScope': ['✅', '✅', '✅', '✅', '✅', '✅', '✅'],
}

gap_df = pd.DataFrame(gap_data)
st.dataframe(gap_df, use_container_width=True, hide_index=True)
