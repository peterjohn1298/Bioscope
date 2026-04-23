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

# ── Radar chart ───────────────────────────────────────────────────────────────
st.divider()
st.subheader("Capability Radar — BioScope vs. Key Competitors")
st.caption("Scores across six dimensions that define value in protein quality certification.")

dimensions = [
    'Turnaround Speed',
    'Analyte Breadth',
    'Certification Value',
    'Sample Prep Simplicity',
    'Welfare / Authenticity',
    'Cost Efficiency',
]

radar_companies = {
    'BioScope':         {'scores': [10, 10, 10, 10, 10, 9],  'color': GREEN,  'dash': 'solid',  'width': 4},
    'Eurofins':         {'scores': [2,  7,  4,  3,  2,  4],  'color': '#E74C3C', 'dash': 'dot', 'width': 2},
    'Neogen':           {'scores': [8,  2,  2,  8,  1,  7],  'color': ORANGE,    'dash': 'dot', 'width': 2},
    'Bruker':           {'scores': [4,  7,  3,  2,  3,  3],  'color': '#9B59B6', 'dash': 'dot', 'width': 2},
}

fig_radar = go.Figure()

for company, cfg in radar_companies.items():
    scores = cfg['scores'] + [cfg['scores'][0]]  # close the polygon
    cats   = dimensions + [dimensions[0]]
    fig_radar.add_trace(go.Scatterpolar(
        r=scores,
        theta=cats,
        fill='toself' if company == 'BioScope' else 'none',
        fillcolor='rgba(46,204,113,0.15)' if company == 'BioScope' else 'rgba(0,0,0,0)',
        name=company,
        line=dict(color=cfg['color'], width=cfg['width'], dash=cfg['dash']),
        marker=dict(size=5 if company == 'BioScope' else 3),
    ))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 10], tickfont=dict(size=9), gridcolor='#ECF0F1'),
        angularaxis=dict(tickfont=dict(size=12)),
        bgcolor='white',
    ),
    showlegend=True,
    legend=dict(orientation='h', y=-0.12, font=dict(size=12)),
    height=460,
    margin=dict(l=60, r=60, t=20, b=60),
    paper_bgcolor='white',
)
st.plotly_chart(fig_radar, use_container_width=True)
st.caption(
    "Eurofins: broad but slow, no welfare/authenticity. "
    "Neogen: fast but single-analyte kits only. "
    "Bruker: instruments sold to labs — requires in-house expertise. "
    "BioScope: only player combining all six dimensions."
)
