import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from models.market_model import calc_topdown, calc_bottomup, segment_totals, calc_sam
from data.assumptions import TAM_TOPDOWN, SEGMENTS, PRICING, ANALYTES

st.set_page_config(page_title="Market Sizing — BioScope", layout="wide")

st.markdown("""
<style>
[data-testid="stDataFrame"] th,
[data-testid="stDataFrame"] th div,
[data-testid="stDataFrame"] th span,
.dvn-scroller .col-header-cell,
.dvn-scroller .col-header-cell span { color: #000000 !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)


GREEN = "#2ECC71"; BLUE = "#1B4F72"; ORANGE = "#E67E22"

st.title("📊 Market Sizing")
st.markdown("Explore TAM through two independent methodologies. Adjust assumptions to stress-test the numbers.")

tab1, tab2 = st.tabs(["Top-Down TAM", "Bottom-Up TAM"])

# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Top-Down: Global → North America → US")
    st.markdown("Starting from the global food safety testing market, applying successive filters to reach BioScope's addressable niche.")

    with st.expander("Adjust Assumptions", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            global_mkt = st.slider("Global Food Safety Testing Market ($B, 2024)",
                                   min_value=15.0, max_value=40.0, value=TAM_TOPDOWN['global_market_2024_B'], step=0.5,
                                   help="IMARC Group / Straits Research 2024 baseline")
            rapid_share = st.slider("Rapid Testing Share (%)",
                                    0.40, 0.85, TAM_TOPDOWN['rapid_testing_share'], 0.01,
                                    format="%.0f%%",
                                    help="MarketsandMarkets: ~65% of food testing is rapid methods")
            outsourced = st.slider("Outsourced / Contract Lab Share (%)",
                                   0.25, 0.70, TAM_TOPDOWN['outsourced_share'], 0.01,
                                   format="%.0f%%",
                                   help="Eurofins FY2024: ~45% of total is outsourced")
        with c2:
            niche_share = st.slider("BioScope Niche Share — residue + auth + welfare (%)",
                                    0.30, 0.80, TAM_TOPDOWN['bioscope_niche_share'], 0.01,
                                    format="%.0f%%",
                                    help="Excludes pathogen/microbiology (Neogen/bioMérieux territory)")
            na_share = st.slider("North America Share of Global (%)",
                                 0.25, 0.55, TAM_TOPDOWN['na_share_of_global'], 0.01,
                                 format="%.0f%%",
                                 help="US $6.3B / $24.2B global ≈ 26%; Canada adds 12%")
            us_share = st.slider("US Share of North America (%)",
                                 0.70, 0.95, TAM_TOPDOWN['us_share_of_na'], 0.01,
                                 format="%.0f%%",
                                 help="Canada ≈ 13% of N.Am food testing spend")

    params = {
        'global_market_2024_B': global_mkt,
        'rapid_testing_share': rapid_share,
        'outsourced_share': outsourced,
        'bioscope_niche_share': niche_share,
        'na_share_of_global': na_share,
        'us_share_of_na': us_share,
    }
    td = calc_topdown(params)

    # KPIs
    k1, k2, k3 = st.columns(3)
    k1.metric("Global TAM (BioScope Niche)", f"${td['global_tam']:.2f}B")
    k2.metric("North America TAM", f"${td['na_tam']:.2f}B")
    k3.metric("US TAM ★ Primary Market", f"${td['us_tam']:.2f}B")

    # Waterfall
    labels = [s['label'] for s in td['waterfall']]
    values = [s['value'] for s in td['waterfall']]
    pcts = [1.0] + [values[i]/values[0] for i in range(1, len(values))]
    colors = [GREEN if i >= len(labels)-2 else BLUE for i in range(len(labels))]

    fig = go.Figure(go.Bar(
        y=labels, x=values, orientation='h',
        marker_color=colors,
        text=[f"${v:.2f}B  ({p*100:.1f}% of total)" for v, p in zip(values, pcts)],
        textposition='outside',
    ))
    fig.update_layout(
        title="TAM Funnel — Each Step Applies a Market Filter",
        height=350, margin=dict(l=0, r=200, t=40, b=10),
        xaxis=dict(title="$B", showgrid=True),
        yaxis=dict(autorange='reversed'),
        plot_bgcolor='white', paper_bgcolor='white',
    )
    st.plotly_chart(fig, use_container_width=True)

    # Market leader cross-validation table
    st.markdown("#### Market Leader Cross-Validation")
    cv_data = {
        'Company': ['Eurofins', 'SGS', 'Neogen', 'Mérieux NutriSciences', 'FSNS/Certified Group', 'Regional independents (500+)'],
        'Food Testing Revenue': ['€4.0B ($4.4B USD)', '$970M (H&N div)', '$655M (food safety)', '$1.0B (combined)', '$300–$400M', '~$500M'],
        'Note': [
            'Own stated addressable outsourced TAM — most reliable anchor',
            'H&N division; food is subset',
            'SEC 10-K FY2024 food safety segment',
            'Post Bureau Veritas acquisition (EV €360M)',
            'Private roll-up; industry estimate',
            'Residual; AOAC directory + IBISWorld',
        ],
    }
    st.dataframe(pd.DataFrame(cv_data), use_container_width=True, hide_index=True)
    st.caption("Cross-validation anchors our $1.3B US TAM — consistent with named competitor aggregate of ~$6.6B total (outsourced + in-house).")

# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Bottom-Up: Segment × Analyte Revenue Model")
    st.markdown("For each customer segment and analyte category: (# buyers × samples/yr × usage %) × BioScope price = addressable revenue.")

    with st.expander("Adjust Pricing", expanded=False):
        cp1, cp2, cp3 = st.columns(3)
        t1_price  = cp1.number_input("Tier 1 Price ($/sample)", 200, 1500, PRICING['tier1']['price'],   step=25, help="Residue compliance panel only")
        t12_price = cp2.number_input("Tier 1+2 Price ($/sample)", 400, 2000, PRICING['tier12']['price'],  step=25, help="Residue + welfare biomarkers")
        t123_price= cp3.number_input("Tier 1+2+3 Price ($/sample)", 600, 3000, PRICING['tier123']['price'], step=25, help="Full certification report")

    custom_pricing = {
        'tier1':   {**PRICING['tier1'],   'price': t1_price},
        'tier12':  {**PRICING['tier12'],  'price': t12_price},
        'tier123': {**PRICING['tier123'], 'price': t123_price},
    }

    bu_rows = calc_bottomup(SEGMENTS, custom_pricing, ANALYTES)
    seg_tots = segment_totals(bu_rows)

    # Segment summary
    seg_df = pd.DataFrame([
        {
            'Segment': v['segment'],
            'Market Spend (Commercial Labs)': v['comm_rev'],
            'BioScope Rev @ 100% Share': v['bio_rev_100pct'],
            'Y3 SOM': v['som_y3'],
        }
        for v in seg_tots.values()
    ])
    seg_df_fmt = seg_df.copy()
    for col in ['Market Spend (Commercial Labs)', 'BioScope Rev @ 100% Share', 'Y3 SOM']:
        seg_df_fmt[col] = seg_df_fmt[col].apply(lambda x: f"${x/1e6:.1f}M")

    totals_row = pd.DataFrame([{
        'Segment': 'TOTAL',
        'Market Spend (Commercial Labs)': f"${sum(v['comm_rev'] for v in seg_tots.values())/1e6:.0f}M",
        'BioScope Rev @ 100% Share': f"${sum(v['bio_rev_100pct'] for v in seg_tots.values())/1e6:.0f}M",
        'Y3 SOM': f"${sum(v['som_y3'] for v in seg_tots.values())/1e6:.0f}M",
    }])
    st.dataframe(pd.concat([seg_df_fmt, totals_row], ignore_index=True), use_container_width=True, hide_index=True)

    # Stacked bar: BioScope rev @ 100% share by segment
    seg_names = list(seg_tots.keys())
    seg_labels = [seg_tots[k]['segment'] for k in seg_names]
    bio_vals = [seg_tots[k]['bio_rev_100pct']/1e6 for k in seg_names]

    fig2 = go.Figure(go.Bar(
        x=seg_labels, y=bio_vals,
        marker_color=[GREEN, BLUE, ORANGE, '#9B59B6', '#E74C3C'],
        text=[f"${v:.0f}M" for v in bio_vals],
        textposition='outside',
    ))
    fig2.update_layout(
        title="BioScope Addressable Revenue @ 100% Penetration (by Segment)",
        height=360, margin=dict(l=0, r=0, t=50, b=10),
        yaxis=dict(title="$M", showgrid=True),
        plot_bgcolor='white', paper_bgcolor='white',
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Heatmap: analyte × segment revenue
    st.markdown("#### Analyte × Segment Heatmap — BioScope Revenue @ 100% Share ($M)")
    seg_keys = [s['key'] for s in SEGMENTS]
    seg_labels_h = [s['name'] for s in SEGMENTS]
    analyte_labels = [a['name'] for a in ANALYTES]

    heat_data = np.zeros((len(ANALYTES), len(seg_keys)))
    for r in bu_rows:
        ai = next(i for i, a in enumerate(ANALYTES) if a['name'] == r['analyte'])
        si = seg_keys.index(r['segment_key'])
        heat_data[ai][si] = r['bio_rev_100pct'] / 1e6

    fig_heat = go.Figure(go.Heatmap(
        z=heat_data,
        x=seg_labels_h,
        y=analyte_labels,
        colorscale='Blues',
        text=[[f"${v:.0f}M" for v in row] for row in heat_data],
        texttemplate="%{text}",
        textfont=dict(size=10),
        colorbar=dict(title="$M"),
    ))
    fig_heat.update_layout(
        height=460, margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(tickangle=-20),
        plot_bgcolor='white', paper_bgcolor='white',
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # Bottom-up vs top-down reconciliation
    bu_us_total = sum(v['bio_rev_100pct'] for v in seg_tots.values())
    td_base = calc_topdown()
    st.markdown("#### Bottom-Up vs. Top-Down Reconciliation")
    rc1, rc2, rc3 = st.columns(3)
    rc1.metric("Bottom-Up US TAM (BioScope 100%)", f"${bu_us_total/1e9:.2f}B")
    rc2.metric("Top-Down US TAM", f"${td_base['us_tam']/1e9:.2f}B")
    rc3.metric("Ratio (Bottom-Up / Top-Down)", f"{bu_us_total/td_base['us_tam']:.1f}×")
    st.caption(
        "Bottom-up ($4.8B) exceeds top-down ($1.3B) — typical for a novel multi-analyte service "
        "capturing spend currently fragmented across multiple labs. The top-down is a conservatism anchor."
    )
