import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from models.market_model import calc_topdown, calc_som, calc_sam
from utils.theme import apply_theme, FOREST, MINT, AMBER, CHARCOAL, CREAM, SEG_COLORS, chart_layout

st.set_page_config(
    page_title="BioScope — Market Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()

# ── Header ────────────────────────────────────────────────────────────────────
_, col_title = st.columns([1, 8])
with col_title:
    st.markdown("# 🔬 BioScope Innovations")
    st.markdown("#### Clean Protein Certification™ — Investor Market Intelligence Dashboard")
st.divider()

# ── Data ──────────────────────────────────────────────────────────────────────
td        = calc_topdown()
sam       = calc_sam()
som       = calc_som()

tam_glob  = td['global_tam']
tam_na    = td['na_tam']
tam_us    = td['us_tam']
total_sam = sam['combined_sam']
som_y1    = som['total']['y1']
som_y2    = som['total']['y2']
som_y3    = som['total']['y3']

# ── KPI strip ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)

def kpi(col, label, value, sub, border=FOREST):
    col.markdown(
        f'<div class="metric-card" style="border-left-color:{border}">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-sub">{sub}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

kpi(c1, "Global TAM",  f"${tam_glob:.2f}B",       "Rapid food safety testing",    FOREST)
kpi(c2, "US TAM",      f"${tam_us:.2f}B",          "Top-down primary market",      MINT)
kpi(c3, "N.Am SAM",    f"${total_sam/1e9:.1f}B",   "Physically serviceable",       AMBER)
kpi(c4, "Y3 SOM",      f"${som_y3/1e6:.0f}M",      "Obtainable by Year 3",         "#7C3AED")
kpi(c5, "Gross Margin","80–86%",                    "By tier (T1 → T3)",            "#0F766E")

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.markdown('<div class="section-header">TAM Funnel — Top-Down</div>', unsafe_allow_html=True)
    labels = [s['label'] for s in td['waterfall']]
    values = [s['value'] for s in td['waterfall']]
    colors = [AMBER if i == len(labels) - 1 else FOREST for i in range(len(labels))]

    fig_funnel = go.Figure(go.Bar(
        x=values, y=labels, orientation='h',
        marker_color=colors,
        marker_line=dict(width=0),
        text=[f"${v:.2f}B" for v in values],
        textposition='outside',
        textfont=dict(size=12, color=CHARCOAL),
    ))
    fig_funnel.update_layout(**chart_layout(
        height=280,
        margin=dict(l=0, r=70, t=10, b=10),
        xaxis=dict(title='$B', showgrid=True, gridcolor='#E8F5EE'),
        yaxis=dict(autorange='reversed', showgrid=False),
    ))
    st.plotly_chart(fig_funnel, use_container_width=True)

with right:
    st.markdown('<div class="section-header">Revenue Projections — Y1 to Y3 (Base Case)</div>', unsafe_allow_html=True)

    seg_names  = [s['name'] for s in som['segments']] + ['BM2 Licensed Labs']
    y1_vals    = [s['som_y1'] for s in som['segments']] + [som['bm2']['y1']]
    y2_vals    = [s['som_y2'] for s in som['segments']] + [som['bm2']['y2']]
    y3_vals    = [s['som_y3'] for s in som['segments']] + [som['bm2']['y3']]

    fig_rev = go.Figure()
    for i, name in enumerate(seg_names):
        fig_rev.add_trace(go.Bar(
            name=name,
            x=['Year 1', 'Year 2', 'Year 3'],
            y=[y1_vals[i]/1e6, y2_vals[i]/1e6, y3_vals[i]/1e6],
            marker_color=SEG_COLORS[i % len(SEG_COLORS)],
            marker_line=dict(width=0),
        ))
    fig_rev.update_layout(**chart_layout(
        barmode='stack', height=280,
        margin=dict(l=0, r=0, t=10, b=10),
        yaxis=dict(title='Revenue ($M)', showgrid=True, gridcolor='#E8F5EE'),
        legend=dict(orientation='h', y=-0.28, font=dict(size=10)),
    ))
    fig_rev.add_annotation(
        x='Year 3', y=som_y3/1e6,
        text=f"<b>${som_y3/1e6:.0f}M</b>",
        showarrow=True, arrowhead=2, ax=44, ay=-30,
        font=dict(size=13, color=FOREST),
    )
    st.plotly_chart(fig_rev, use_container_width=True)

# ── Summary table ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Market Sizing Summary</div>', unsafe_allow_html=True)

summary_data = {
    'Level': [
        'TAM — Global (Rapid Food Safety)',
        'TAM — North America',
        'TAM — US (Primary)',
        'SAM — North America',
        'SOM — Year 1', 'SOM — Year 2', 'SOM — Year 3',
    ],
    'Value': [
        f"${tam_glob:.2f}B", f"${tam_na:.2f}B", f"${tam_us:.2f}B",
        f"${total_sam/1e9:.1f}B",
        f"${som_y1/1e6:.1f}M", f"${som_y2/1e6:.1f}M", f"${som_y3/1e6:.0f}M",
    ],
    'Methodology': [
        'Global × rapid testing share (65%)',
        'Global TAM × N.Am share (38%)',
        'N.Am TAM × US share (87%)',
        'Bottom-up, N.Am buyers × 8 core analytes × BioScope pricing',
        'BM1 direct + BM2 licensing',
        'BM1 direct + BM2 licensing',
        'BM1 direct + BM2 licensing (7 labs)',
    ],
}
st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

# ── Navigation cards ───────────────────────────────────────────────────────────
st.divider()
st.markdown("### Navigate the Analysis")
nav1, nav2, nav3, nav4, nav5 = st.columns(5)
with nav1:
    st.markdown("**📊 Market Sizing**\n\nTop-down & bottom-up TAM with adjustable assumptions")
with nav2:
    st.markdown("**💰 Revenue Model**\n\nY1–Y3 SOM by segment, customer count, BM1 vs BM2")
with nav3:
    st.markdown("**🔀 Scenario Analysis**\n\nBear / Base / Bull comparison with custom levers")
with nav4:
    st.markdown("**🎯 Sensitivity**\n\nTornado chart — what moves the needle most")
with nav5:
    st.markdown("**⚔️ Competitive Landscape**\n\nPositioning map and competitor differentiation table")
