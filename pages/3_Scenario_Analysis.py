import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import copy

from models.market_model import calc_scenario, calc_som, SCENARIOS
from data.assumptions import SEGMENTS, PRICING, BM2

st.set_page_config(page_title="Scenario Analysis — BioScope", layout="wide")

st.markdown("""
<style>
[data-testid="stDataFrame"] th,
[data-testid="stDataFrame"] th div,
[data-testid="stDataFrame"] th span,
.dvn-scroller .col-header-cell,
.dvn-scroller .col-header-cell span { color: #000000 !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)


GREEN  = "#2ECC71"; BLUE = "#1B4F72"; RED = "#E74C3C"; ORANGE = "#E67E22"

st.title("🔀 Scenario Analysis")
st.markdown("Compare Bear / Base / Bull cases side-by-side — or build a fully custom scenario.")

# ── Compute the three presets ──────────────────────────────────────────────────
bear = calc_scenario('bear')
base = calc_scenario('base')
bull = calc_scenario('bull')

# ── Custom scenario sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.header("Custom Scenario")
    st.caption("Start from a preset, then override individual levers.")
    preset_start = st.selectbox("Start from", ['Base', 'Bear', 'Bull'])
    start_sc = {'Base': 'base', 'Bear': 'bear', 'Bull': 'bull'}[preset_start]
    sc_cfg = SCENARIOS[start_sc]

    st.subheader("Penetration Multiplier")
    pen_mult = st.slider("All segments ×", 0.25, 3.0, sc_cfg['pen_multiplier'], 0.05,
                         help="Multiplied against base penetration rates for each segment")

    st.subheader("Segment-Level Overrides (Y3 %)")
    seg_pen_custom = {}
    for seg in SEGMENTS:
        base_pen = seg['pen_y3'] * pen_mult
        val = st.slider(seg['name'], 0.001, 0.20, min(0.20, base_pen), 0.001,
                        format="%.1f%%", key=f"cust_{seg['key']}")
        seg_pen_custom[seg['key']] = val

    st.subheader("Pricing Multiplier")
    price_mult = st.slider("All tiers ×", 0.70, 1.50, sc_cfg['price_multiplier'], 0.01)

    st.subheader("BM2 Licensing")
    c_bm2_y2 = st.number_input("Labs Y2", 0, 20, sc_cfg['bm2_labs']['y2'])
    c_bm2_y3 = st.number_input("Labs Y3", 0, 50, sc_cfg['bm2_labs']['y3'])

# ── Build custom scenario ──────────────────────────────────────────────────────
custom_segs = []
for seg in SEGMENTS:
    s = copy.deepcopy(seg)
    base_pen = seg_pen_custom[seg['key']]
    if seg['pen_y3'] > 0:
        ratio = base_pen / seg['pen_y3']
    else:
        ratio = 1.0
    s['pen_y1'] = min(1.0, seg['pen_y1'] * ratio)
    s['pen_y2'] = min(1.0, seg['pen_y2'] * ratio)
    s['pen_y3'] = base_pen
    custom_segs.append(s)

custom_prc = {}
for k in PRICING:
    custom_prc[k] = {**PRICING[k], 'price': round(PRICING[k]['price'] * price_mult)}

custom_bm2 = {**BM2, 'labs_y1': 0, 'labs_y2': c_bm2_y2, 'labs_y3': c_bm2_y3}
custom = calc_som(custom_segs, custom_prc, None, custom_bm2)

# ── Scenario summary cards ─────────────────────────────────────────────────────
c_bear, c_base, c_bull, c_cust = st.columns(4)

def scenario_card(col, label, color, som_result, note=""):
    y3 = som_result['total']['y3']
    y1 = som_result['total']['y1']
    y2 = som_result['total']['y2']
    col.markdown(f"""
    <div style="background:white;border-radius:10px;padding:18px;border-top:5px solid {color};
                box-shadow:0 2px 8px rgba(0,0,0,0.08);text-align:center;">
        <div style="font-size:12px;color:#7F8C8D;font-weight:700;text-transform:uppercase">{label}</div>
        <div style="font-size:30px;font-weight:800;color:{color};margin:6px 0">${y3/1e6:.0f}M</div>
        <div style="font-size:11px;color:#95A5A6">Y1: ${y1/1e6:.1f}M &nbsp;|&nbsp; Y2: ${y2/1e6:.1f}M</div>
        <div style="font-size:11px;color:#7F8C8D;margin-top:4px">{note}</div>
    </div>""", unsafe_allow_html=True)

scenario_card(c_bear, "Bear (Conservative)", RED,   bear, "50% pen. / base pricing")
scenario_card(c_base, "Base Case",           BLUE,  base, "Excel model assumptions")
scenario_card(c_bull, "Bull (Optimistic)",   GREEN, bull, "1.75× pen. / +10% pricing")
scenario_card(c_cust, "Custom Scenario",     ORANGE, custom, f"Pen mult {pen_mult:.2f}× / Price {price_mult:.2f}×")

st.divider()

# ── Side-by-side grouped bar ───────────────────────────────────────────────────
st.subheader("Revenue Comparison — Year 1 / 2 / 3")
years = ['Year 1', 'Year 2', 'Year 3']
scenarios_data = [
    ('Bear',   RED,    bear),
    ('Base',   BLUE,   base),
    ('Bull',   GREEN,  bull),
    ('Custom', ORANGE, custom),
]

fig_compare = go.Figure()
for label, color, sc in scenarios_data:
    fig_compare.add_trace(go.Bar(
        name=label,
        x=years,
        y=[sc['total']['y1']/1e6, sc['total']['y2']/1e6, sc['total']['y3']/1e6],
        marker_color=color,
        text=[f"${v:.0f}M" for v in [sc['total']['y1']/1e6, sc['total']['y2']/1e6, sc['total']['y3']/1e6]],
        textposition='outside',
    ))
fig_compare.update_layout(
    barmode='group', height=420,
    yaxis=dict(title='Revenue ($M)', showgrid=True, gridcolor='#ECF0F1'),
    legend=dict(orientation='h', y=-0.12),
    margin=dict(l=0, r=0, t=10, b=60),
    plot_bgcolor='white', paper_bgcolor='white',
    transition={'duration': 400, 'easing': 'cubic-in-out'},
)
st.plotly_chart(fig_compare, use_container_width=True, key="scenario_compare")

# ── Segment breakdown comparison ───────────────────────────────────────────────
st.subheader("Y3 Revenue by Segment — All Scenarios")

seg_names_all = [s['name'] for s in base['segments']] + ['BM2 Licensed Labs']
sc_list = [('Bear', RED, bear), ('Base', BLUE, base), ('Bull', GREEN, bull), ('Custom', ORANGE, custom)]

fig_seg = go.Figure()
for sc_label, sc_color, sc_result in sc_list:
    y3_by_seg = [s['som_y3']/1e6 for s in sc_result['segments']] + [sc_result['bm2']['y3']/1e6]
    fig_seg.add_trace(go.Bar(
        name=sc_label,
        x=seg_names_all,
        y=y3_by_seg,
        marker_color=sc_color,
    ))
fig_seg.update_layout(
    barmode='group', height=400,
    yaxis=dict(title='Y3 Revenue ($M)', showgrid=True, gridcolor='#ECF0F1'),
    xaxis=dict(tickangle=-15),
    legend=dict(orientation='h', y=-0.2),
    margin=dict(l=0, r=0, t=10, b=80),
    plot_bgcolor='white', paper_bgcolor='white',
    transition={'duration': 400, 'easing': 'cubic-in-out'},
)
st.plotly_chart(fig_seg, use_container_width=True, key="scenario_by_segment")

# ── Scenario assumptions table ─────────────────────────────────────────────────
st.subheader("Scenario Assumption Summary")
rows = []
for sc_key in ('bear', 'base', 'bull'):
    sc = SCENARIOS[sc_key]
    rows.append({
        'Scenario': sc['label'],
        'Description': sc['description'],
        'Pen. Multiplier': f"{sc['pen_multiplier']:.2f}×",
        'Price Multiplier': f"{sc['price_multiplier']:.2f}×",
        'BM2 Labs (Y1/Y2/Y3)': f"0 / {sc['bm2_labs']['y2']} / {sc['bm2_labs']['y3']}",
        'Y3 Revenue': f"${calc_scenario(sc_key)['total']['y3']/1e6:.0f}M",
    })
rows.append({
    'Scenario': 'Custom',
    'Description': 'User-configured via sidebar',
    'Pen. Multiplier': f"{pen_mult:.2f}×",
    'Price Multiplier': f"{price_mult:.2f}×",
    'BM2 Labs (Y1/Y2/Y3)': f"0 / {c_bm2_y2} / {c_bm2_y3}",
    'Y3 Revenue': f"${custom['total']['y3']/1e6:.0f}M",
})
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ── Rob's cross-check ──────────────────────────────────────────────────────────
rob_y5 = 62_000_000
st.info(
    f"**Cross-check vs. BioScope internal model:** Rob's stated Y5 ARR target is "
    f"${rob_y5/1e6:.0f}M. "
    f"Bear Y3: ${bear['total']['y3']/1e6:.0f}M ({bear['total']['y3']/rob_y5:.1f}×) | "
    f"Base Y3: ${base['total']['y3']/1e6:.0f}M ({base['total']['y3']/rob_y5:.1f}×) | "
    f"Bull Y3: ${bull['total']['y3']/1e6:.0f}M ({bull['total']['y3']/rob_y5:.1f}×)"
)
