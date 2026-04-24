import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from models.market_model import calc_topdown, calc_som, calc_sam

st.set_page_config(
    page_title="BioScope — Market Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

GREEN  = "#2ECC71"
BLUE   = "#1B4F72"
ORANGE = "#E67E22"

st.markdown("""
<style>
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 20px 24px;
        border-left: 5px solid #2ECC71;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .metric-label { font-size: 13px; color: #7F8C8D; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; }
    .metric-value { font-size: 32px; font-weight: 800; color: #1B4F72; margin: 4px 0; }
    .metric-sub   { font-size: 12px; color: #95A5A6; }
    .section-header { font-size: 20px; font-weight: 700; color: #1B4F72; margin: 24px 0 8px 0; }

    [data-testid="stDataFrame"] th,
    [data-testid="stDataFrame"] th div,
    [data-testid="stDataFrame"] th span,
    .dvn-scroller .col-header-cell,
    .dvn-scroller .col-header-cell span { color: #000000 !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 8])
with col_title:
    st.markdown("# 🔬 BioScope Innovations")
    st.markdown("#### Clean Protein Certification™ — Investor Market Intelligence Dashboard")

st.divider()

td        = calc_topdown()
sam       = calc_sam()
som       = calc_som()

tam_glob  = td['global_tam']   # already in $B
tam_na    = td['na_tam']
tam_us    = td['us_tam']
total_sam = sam['combined_sam']
som_y1    = som['total']['y1']
som_y2    = som['total']['y2']
som_y3    = som['total']['y3']

# ── KPI strip ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Global TAM</div>
        <div class="metric-value">${tam_glob:.2f}B</div>
        <div class="metric-sub">Rapid food safety testing</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="metric-card" style="border-left-color:#3498DB">
        <div class="metric-label">US TAM</div>
        <div class="metric-value">${tam_us:.2f}B</div>
        <div class="metric-sub">Top-down primary market</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""<div class="metric-card" style="border-left-color:#E67E22">
        <div class="metric-label">N.Am SAM</div>
        <div class="metric-value">${total_sam/1e9:.1f}B</div>
        <div class="metric-sub">Physically serviceable</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""<div class="metric-card" style="border-left-color:#9B59B6">
        <div class="metric-label">Y3 SOM</div>
        <div class="metric-value">${som_y3/1e6:.0f}M</div>
        <div class="metric-sub">Obtainable by Year 3</div>
    </div>""", unsafe_allow_html=True)

with c5:
    st.markdown(f"""<div class="metric-card" style="border-left-color:#E74C3C">
        <div class="metric-label">Gross Margin</div>
        <div class="metric-value">80–86%</div>
        <div class="metric-sub">By tier (T1 → T3)</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Two-column charts ──────────────────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.markdown('<div class="section-header">TAM Funnel — Top-Down</div>', unsafe_allow_html=True)
    labels = [s['label'] for s in td['waterfall']]
    values = [s['value'] for s in td['waterfall']]
    colors = [GREEN if i == len(labels)-1 else BLUE for i in range(len(labels))]

    fig_funnel = go.Figure(go.Bar(
        x=values, y=labels, orientation='h',
        marker_color=colors,
        text=[f"${v:.2f}B" for v in values],
        textposition='outside',
        textfont=dict(size=12),
    ))
    fig_funnel.update_layout(
        height=320,
        margin=dict(l=0, r=60, t=10, b=10),
        xaxis=dict(title='$B', showgrid=True, gridcolor='#ECF0F1'),
        yaxis=dict(autorange='reversed'),
        plot_bgcolor='white', paper_bgcolor='white',
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

with right:
    st.markdown('<div class="section-header">Revenue Projections — Y1 to Y3 (Base Case)</div>', unsafe_allow_html=True)

    seg_names = [s['name'] for s in som['segments']] + ['BM2 Licensed Labs']
    y1_vals   = [s['som_y1'] for s in som['segments']] + [som['bm2']['y1']]
    y2_vals   = [s['som_y2'] for s in som['segments']] + [som['bm2']['y2']]
    y3_vals   = [s['som_y3'] for s in som['segments']] + [som['bm2']['y3']]
    seg_colors = [GREEN, BLUE, ORANGE, '#9B59B6', '#E74C3C', '#1ABC9C']

    fig_rev = go.Figure()
    for i, name in enumerate(seg_names):
        fig_rev.add_trace(go.Bar(
            name=name,
            x=['Year 1', 'Year 2', 'Year 3'],
            y=[y1_vals[i]/1e6, y2_vals[i]/1e6, y3_vals[i]/1e6],
            marker_color=seg_colors[i % len(seg_colors)],
        ))
    fig_rev.update_layout(
        barmode='stack', height=320,
        margin=dict(l=0, r=0, t=10, b=10),
        yaxis=dict(title='Revenue ($M)', showgrid=True, gridcolor='#ECF0F1'),
        legend=dict(orientation='h', y=-0.25, font=dict(size=10)),
        plot_bgcolor='white', paper_bgcolor='white',
    )
    fig_rev.add_annotation(
        x='Year 3', y=som_y3/1e6,
        text=f"<b>${som_y3/1e6:.0f}M</b>",
        showarrow=True, arrowhead=2, ax=40, ay=-30,
        font=dict(size=13, color=BLUE),
    )
    st.plotly_chart(fig_rev, use_container_width=True)

# ── Market Sizing Summary table ────────────────────────────────────────────────
st.markdown('<div class="section-header">Market Sizing Summary</div>', unsafe_allow_html=True)

summary_data = {
    'Level': [
        'TAM — Global (Rapid Food Safety)',
        'TAM — North America',
        'TAM — US (Primary)',
        'SAM — North America',
        'SOM — Year 1',
        'SOM — Year 2',
        'SOM — Year 3',
    ],
    'Value': [
        f"${tam_glob:.2f}B",
        f"${tam_na:.2f}B",
        f"${tam_us:.2f}B",
        f"${total_sam/1e9:.1f}B",
        f"${som_y1/1e6:.1f}M",
        f"${som_y2/1e6:.1f}M",
        f"${som_y3/1e6:.0f}M",
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
