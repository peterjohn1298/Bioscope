import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import copy

from models.market_model import calc_som
from data.assumptions import SEGMENTS, PRICING, BM2
from utils.theme import apply_theme, FOREST, MINT, AMBER, CHARCOAL, SEG_COLORS, chart_layout

st.set_page_config(page_title="Revenue Model — BioScope", layout="wide")
apply_theme()

st.title("💰 Revenue Model")
st.markdown("Adjust assumptions in the sidebar — charts and numbers update live.")

# ── Sidebar controls ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Assumptions")

    st.subheader("Year 3 Penetration")
    pen_pct = {}
    for seg in SEGMENTS:
        label = f"{seg['name']} {'★' if seg.get('beachhead') else ''}"
        pen_pct[seg['key']] = st.slider(
            label,
            min_value=0.1, max_value=15.0,
            value=round(seg['pen_y3'] * 100, 1),
            step=0.1,
            format="%.1f%%",
            key=f"pen_{seg['key']}",
        )

    st.divider()
    st.subheader("Pricing ($/sample)")
    t1_p   = st.number_input("Tier 1 — Residue only",  200,  1500, PRICING['tier1']['price'],   step=25)
    t12_p  = st.number_input("Tier 1+2 — + Welfare",   400,  2000, PRICING['tier12']['price'],  step=25)
    t123_p = st.number_input("Tier 1+2+3 — Full Cert", 600,  3000, PRICING['tier123']['price'], step=25)

    st.divider()
    st.subheader("BM2 Lab Licensing")
    bm2_y1      = st.number_input("Labs signed by Y1",       0,       10,      BM2['labs_y1'],            step=1)
    bm2_y2      = st.number_input("Labs signed by Y2",       0,       20,      BM2['labs_y2'],            step=1)
    bm2_y3      = st.number_input("Labs signed by Y3",       0,       50,      BM2['labs_y3'],            step=1)
    license_fee = st.number_input("Annual license fee ($)",  50_000,  500_000, BM2['annual_license_fee'], step=10_000)
    sample_fee  = st.number_input("Per-sample fee ($)",      5,       100,     BM2['per_sample_fee'],     step=5)
    avg_samples = st.number_input("Avg samples/lab/year",    1_000,   100_000, BM2['avg_samples_per_lab'],step=1_000)

    rev_per_lab = license_fee + sample_fee * avg_samples
    st.caption(f"Revenue per lab: **${rev_per_lab:,.0f}/yr**")

# ── Build model ────────────────────────────────────────────────────────────────
custom_segs = []
for seg in SEGMENTS:
    s = copy.deepcopy(seg)
    base_pen = pen_pct[seg['key']] / 100.0
    ratio = (base_pen / seg['pen_y3']) if seg['pen_y3'] > 0 else 1.0
    s['pen_y1'] = min(1.0, seg['pen_y1'] * ratio)
    s['pen_y2'] = min(1.0, seg['pen_y2'] * ratio)
    s['pen_y3'] = base_pen
    custom_segs.append(s)

custom_pricing = {
    'tier1':   {**PRICING['tier1'],   'price': t1_p},
    'tier12':  {**PRICING['tier12'],  'price': t12_p},
    'tier123': {**PRICING['tier123'], 'price': t123_p},
}
custom_bm2 = {
    **BM2,
    'labs_y1': bm2_y1, 'labs_y2': bm2_y2, 'labs_y3': bm2_y3,
    'annual_license_fee': license_fee,
    'per_sample_fee': sample_fee,
    'avg_samples_per_lab': avg_samples,
}

som = calc_som(custom_segs, custom_pricing, None, custom_bm2)

# ── KPIs ───────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Year 1 Revenue",      f"${som['total']['y1']/1e6:.1f}M")
k2.metric("Year 2 Revenue",      f"${som['total']['y2']/1e6:.1f}M")
k3.metric("Year 3 Revenue",      f"${som['total']['y3']/1e6:.0f}M")
k4.metric("BM2 Y3 Contribution", f"${som['bm2']['y3']/1e6:.1f}M",
          delta=f"{som['bm2']['y3']/som['total']['y3']*100:.1f}% of Y3" if som['total']['y3'] > 0 else "—")

st.divider()

# ── Charts ─────────────────────────────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.subheader("Revenue by Segment")
    seg_names = [s['name'] for s in som['segments']] + ['BM2 Licensed Labs']
    y1_v = [s['som_y1'] for s in som['segments']] + [som['bm2']['y1']]
    y2_v = [s['som_y2'] for s in som['segments']] + [som['bm2']['y2']]
    y3_v = [s['som_y3'] for s in som['segments']] + [som['bm2']['y3']]

    fig_stack = go.Figure()
    for i, name in enumerate(seg_names):
        fig_stack.add_trace(go.Bar(
            name=name,
            x=['Year 1', 'Year 2', 'Year 3'],
            y=[y1_v[i]/1e6, y2_v[i]/1e6, y3_v[i]/1e6],
            marker_color=SEG_COLORS[i % len(SEG_COLORS)],
            marker_line=dict(width=0),
        ))
    fig_stack.update_layout(**chart_layout(
        barmode='stack', height=360,
        yaxis=dict(title='$M', showgrid=True, gridcolor='#E8F5EE'),
        legend=dict(orientation='h', y=-0.3, font=dict(size=10)),
        margin=dict(l=0, r=0, t=10, b=80),
    ))
    st.plotly_chart(fig_stack, use_container_width=True, key="revenue_by_segment")

with right:
    st.subheader("BM1 Direct vs BM2 Licensing")
    fig_split = go.Figure()
    years = ['Year 1', 'Year 2', 'Year 3']
    fig_split.add_trace(go.Bar(
        name='BM1 — Reference Lab (Direct)',
        x=years, y=[som['bm1']['y1']/1e6, som['bm1']['y2']/1e6, som['bm1']['y3']/1e6],
        marker_color=FOREST, marker_line=dict(width=0),
    ))
    fig_split.add_trace(go.Bar(
        name='BM2 — Lab Licensing',
        x=years, y=[som['bm2']['y1']/1e6, som['bm2']['y2']/1e6, som['bm2']['y3']/1e6],
        marker_color=AMBER, marker_line=dict(width=0),
    ))
    fig_split.update_layout(**chart_layout(
        barmode='group', height=360,
        yaxis=dict(title='$M', showgrid=True, gridcolor='#E8F5EE'),
        legend=dict(orientation='h', y=-0.15),
        margin=dict(l=0, r=0, t=10, b=60),
    ))
    st.plotly_chart(fig_split, use_container_width=True, key="bm1_vs_bm2")

# ── Customer table ─────────────────────────────────────────────────────────────
st.subheader("Customer Count & Revenue per Customer")
rows = []
for s in som['segments']:
    rows.append({
        'Segment': s['name'] + (' ★ Beachhead' if s['beachhead'] else ''),
        'Total Buyers (US)': f"{s['buyers']:,}",
        'Y1 Customers': s['y1_customers'],
        'Y2 Customers': s['y2_customers'],
        'Y3 Customers': s['y3_customers'],
        'Avg Rev / Customer': f"${s['avg_rev_per_customer']:,.0f}",
        'Y3 Revenue': f"${s['som_y3']/1e6:.1f}M",
    })
rows.append({
    'Segment': 'BM2 Licensed Labs',
    'Total Buyers (US)': f"{BM2['total_addressable_labs_na']} (N.Am)",
    'Y1 Customers': int(bm2_y1),
    'Y2 Customers': int(bm2_y2),
    'Y3 Customers': int(bm2_y3),
    'Avg Rev / Customer': f"${rev_per_lab:,.0f}",
    'Y3 Revenue': f"${som['bm2']['y3']/1e6:.1f}M",
})
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
