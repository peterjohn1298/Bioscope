import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import copy

from models.market_model import calc_som, sensitivity_tornado
from data.assumptions import SEGMENTS, PRICING, BM2

st.set_page_config(page_title="Sensitivity Analysis — BioScope", layout="wide")

st.markdown("""
<style>
[data-testid="stDataFrame"] th,
[data-testid="stDataFrame"] th div,
[data-testid="stDataFrame"] th span,
.dvn-scroller .col-header-cell,
.dvn-scroller .col-header-cell span { color: #000000 !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)


BLUE = "#1B4F72"; GREEN = "#2ECC71"; RED = "#E74C3C"; ORANGE = "#E67E22"

st.title("🎯 Sensitivity Analysis")
st.markdown(
    "Tornado chart showing the impact of each assumption on Y3 SOM. "
    "Each bar shows the effect of moving the assumption ±20% from its base value."
)

# ── Compute base Y3 SOM ────────────────────────────────────────────────────────
base_som = calc_som()
base_y3 = base_som['total']['y3']

# ── Compute tornado ────────────────────────────────────────────────────────────
with st.spinner("Computing sensitivity..."):
    tornado = sensitivity_tornado(base_y3, n=12)

# ── KPIs ───────────────────────────────────────────────────────────────────────
k1, k2, k3 = st.columns(3)
k1.metric("Base Case Y3 SOM", f"${base_y3/1e6:.0f}M")
k2.metric("Max Upside (top driver)", f"+${max(t['upside'] for t in tornado)/1e6:.0f}M",
          delta=f"+{max(t['upside'] for t in tornado)/base_y3*100:.1f}%")
k3.metric("Max Downside (top driver)", f"-${abs(min(t['downside'] for t in tornado))/1e6:.0f}M",
          delta=f"{min(t['downside'] for t in tornado)/base_y3*100:.1f}%")

st.divider()

# ── Tornado chart ──────────────────────────────────────────────────────────────
st.subheader("Tornado Chart — Y3 SOM Impact (±20% on each assumption)")

labels = [t['label'] for t in tornado]
upsides = [t['upside'] / 1e6 for t in tornado]
downsides = [t['downside'] / 1e6 for t in tornado]

fig = go.Figure()
fig.add_trace(go.Bar(
    name='Upside (+20%)',
    y=labels,
    x=upsides,
    orientation='h',
    marker_color=GREEN,
    text=[f"+${v:.1f}M" for v in upsides],
    textposition='outside',
))
fig.add_trace(go.Bar(
    name='Downside (−20%)',
    y=labels,
    x=downsides,
    orientation='h',
    marker_color=RED,
    text=[f"−${abs(v):.1f}M" for v in downsides],
    textposition='outside',
))
fig.add_vline(x=0, line_width=2, line_color=BLUE)
fig.update_layout(
    barmode='overlay',
    height=520,
    margin=dict(l=0, r=120, t=20, b=10),
    xaxis=dict(title='Change in Y3 SOM ($M)', showgrid=True, gridcolor='#ECF0F1', zeroline=True),
    yaxis=dict(autorange='reversed'),
    legend=dict(orientation='h', y=-0.08),
    plot_bgcolor='white', paper_bgcolor='white',
)
st.plotly_chart(fig, use_container_width=True)

# ── Tornado data table ─────────────────────────────────────────────────────────
st.subheader("Sensitivity Table")
rows = []
for t in tornado:
    swing = t['upside'] - t['downside']
    rows.append({
        'Assumption': t['label'],
        'Category': t['category'],
        'Upside (+20%)': f"+${t['upside']/1e6:.1f}M ({t['upside']/base_y3*100:+.1f}%)",
        'Downside (−20%)': f"${t['downside']/1e6:.1f}M ({t['downside']/base_y3*100:+.1f}%)",
        'Total Swing': f"${swing/1e6:.1f}M",
    })
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ── Interactive single-variable explorer ───────────────────────────────────────
st.divider()
st.subheader("Single-Variable Explorer")
st.markdown("Pick any single assumption and sweep it across a range to see the impact curve.")

sweep_options = {
    'Brands penetration (Y3)':     ('seg_pen', 'brands', 0.001, 0.15),
    'Processors penetration (Y3)': ('seg_pen', 'processors', 0.001, 0.15),
    'Retailers penetration (Y3)':  ('seg_pen', 'retailers', 0.001, 0.10),
    'Exporters penetration (Y3)':  ('seg_pen', 'exporters', 0.001, 0.15),
    'Tier 1 price ($/sample)':     ('price', 'tier1', 200, 1500),
    'Tier 1+2 price ($/sample)':   ('price', 'tier12', 400, 2000),
    'Tier 1+2+3 price ($/sample)': ('price', 'tier123', 600, 3000),
    'BM2 labs (Y3)':               ('bm2', 'labs_y3', 0, 50),
}

selected = st.selectbox("Select assumption to sweep", list(sweep_options.keys()))
sweep_type, sweep_key, sweep_min, sweep_max = sweep_options[selected]

import numpy as np
sweep_values = np.linspace(sweep_min, sweep_max, 40)
som_values = []

for v in sweep_values:
    segs = copy.deepcopy(SEGMENTS)
    prc  = copy.deepcopy(PRICING)
    bm2  = copy.deepcopy(BM2)

    if sweep_type == 'seg_pen':
        for s in segs:
            if s['key'] == sweep_key:
                if s['pen_y3'] > 0:
                    ratio = v / s['pen_y3']
                else:
                    ratio = 1.0
                s['pen_y1'] = min(1.0, s['pen_y1'] * ratio)
                s['pen_y2'] = min(1.0, s['pen_y2'] * ratio)
                s['pen_y3'] = v
    elif sweep_type == 'price':
        prc[sweep_key]['price'] = v
    elif sweep_type == 'bm2':
        bm2[sweep_key] = int(v)

    result = calc_som(segs, prc, None, bm2)
    som_values.append(result['total']['y3'] / 1e6)

# Get base value
if sweep_type == 'seg_pen':
    base_val = next(s['pen_y3'] for s in SEGMENTS if s['key'] == sweep_key)
elif sweep_type == 'price':
    base_val = PRICING[sweep_key]['price']
elif sweep_type == 'bm2':
    base_val = BM2['labs_y3']

fig_sweep = go.Figure()
fig_sweep.add_trace(go.Scatter(
    x=list(sweep_values), y=som_values,
    mode='lines', line=dict(color=BLUE, width=3),
    fill='tozeroy', fillcolor='rgba(27,79,114,0.1)',
    name='Y3 SOM',
))
fig_sweep.add_vline(x=base_val, line_dash='dash', line_color=ORANGE, line_width=2,
                    annotation_text=f"Base: {base_val}", annotation_position="top right")
fig_sweep.add_hline(y=base_y3/1e6, line_dash='dot', line_color='#95A5A6', line_width=1)
fig_sweep.update_layout(
    height=320, margin=dict(l=0, r=0, t=20, b=10),
    xaxis=dict(title=selected, showgrid=True),
    yaxis=dict(title='Y3 SOM ($M)', showgrid=True),
    plot_bgcolor='white', paper_bgcolor='white',
)
st.plotly_chart(fig_sweep, use_container_width=True)
