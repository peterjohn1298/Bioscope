import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.theme import apply_theme, FOREST, MINT, AMBER, CHARCOAL, ROSE, VIOLET, TEAL, GREY, chart_layout

st.set_page_config(page_title="Competitive Landscape — BioScope", layout="wide")
apply_theme()

st.title("⚔️ Competitive Landscape")
st.markdown("No existing player combines **speed**, **breadth**, and **certification** in one service. That is BioScope's white space.")

# ═══════════════════════════════════════════════════════════════════════════════
# 1. ANIMATED POSITIONING MAP
# ═══════════════════════════════════════════════════════════════════════════════
st.subheader("Market Positioning Map")
st.caption("Click **▶ Reveal** to walk through the landscape — BioScope enters last.")

non_bio = [
    {'name': 'Eurofins / SGS', 'x': 1.8, 'y': 6.8, 'color': ROSE,   'size': 16, 'tpos': 'top center'},
    {'name': 'Neogen',         'x': 7.8, 'y': 2.0, 'color': AMBER,  'size': 14, 'tpos': 'top center'},
    {'name': 'Bruker',         'x': 3.5, 'y': 6.2, 'color': VIOLET, 'size': 13, 'tpos': 'top center'},
    {'name': 'Bureau Veritas', 'x': 1.6, 'y': 3.2, 'color': GREY,   'size': 13, 'tpos': 'bottom center'},
    {'name': 'Clear Labs',     'x': 5.2, 'y': 2.6, 'color': TEAL,   'size': 11, 'tpos': 'top center'},
]

fig = go.Figure()

# ── Quadrant backgrounds ───────────────────────────────────────────────────────
fig.add_shape(type='rect', x0=0, y0=5, x1=5, y1=10,
              fillcolor='rgba(190,18,60,0.06)', line=dict(width=0), layer='below')
fig.add_shape(type='rect', x0=5, y0=5, x1=10, y1=10,
              fillcolor='rgba(45,106,79,0.10)', line=dict(width=0), layer='below')
fig.add_shape(type='rect', x0=0, y0=0, x1=5,  y1=5,
              fillcolor='rgba(107,114,128,0.06)', line=dict(width=0), layer='below')
fig.add_shape(type='rect', x0=5, y0=0, x1=10, y1=5,
              fillcolor='rgba(233,119,14,0.06)', line=dict(width=0), layer='below')

# ── Divider lines ──────────────────────────────────────────────────────────────
fig.add_hline(y=5, line_dash='dash', line_color='#D1FAE5', line_width=1.5)
fig.add_vline(x=5, line_dash='dash', line_color='#D1FAE5', line_width=1.5)

# ── Quadrant labels ────────────────────────────────────────────────────────────
quadrant_labels = [
    dict(x=2.5,  y=9.6,  text="<b>Broad Testing,<br>Slow Delivery</b>",   color=ROSE,    bg='rgba(255,255,255,0.9)'),
    dict(x=7.5,  y=9.6,  text="<b>Full Certification<br>Platform</b>",     color=FOREST,  bg='rgba(209,250,229,0.6)'),
    dict(x=2.5,  y=0.5,  text="<b>Process Auditing<br>Only</b>",           color=GREY,    bg='rgba(255,255,255,0.9)'),
    dict(x=7.5,  y=0.5,  text="<b>Rapid, Single-<br>Purpose Kits</b>",     color=AMBER,   bg='rgba(255,255,255,0.9)'),
]
for q in quadrant_labels:
    fig.add_annotation(
        x=q['x'], y=q['y'], text=q['text'],
        showarrow=False,
        font=dict(size=13, color=q['color']),
        bgcolor=q['bg'],
        bordercolor=q['color'],
        borderwidth=1.5,
        borderpad=6,
        align='center',
    )

# ── 3 animation traces: competitors | BioScope glow ring | BioScope star ──────
fig.add_trace(go.Scatter(x=[], y=[], mode='markers+text', showlegend=False, name='competitors'))
fig.add_trace(go.Scatter(x=[], y=[], mode='markers',      showlegend=False, name='glow'))
fig.add_trace(go.Scatter(x=[], y=[], mode='markers+text', showlegend=False, name='bioscope'))

# ── Build animation frames ────────────────────────────────────────────────────
frames = []

for i in range(len(non_bio) + 1):
    shown = non_bio[:i]
    frames.append(go.Frame(
        name=str(i),
        traces=[0, 1, 2],
        data=[
            go.Scatter(
                x=[p['x'] for p in shown],
                y=[p['y'] for p in shown],
                mode='markers+text',
                marker=dict(
                    size=[p['size'] for p in shown],
                    color=[p['color'] for p in shown],
                    line=dict(width=1.5, color='white'),
                ),
                text=[p['name'] for p in shown],
                textposition=[p['tpos'] for p in shown],
                textfont=dict(size=11, color=CHARCOAL),
            ),
            go.Scatter(x=[], y=[], mode='markers'),
            go.Scatter(x=[], y=[], mode='markers+text'),
        ],
    ))

frames.append(go.Frame(
    name='bioscope',
    traces=[0, 1, 2],
    data=[
        go.Scatter(
            x=[p['x'] for p in non_bio],
            y=[p['y'] for p in non_bio],
            mode='markers+text',
            marker=dict(
                size=[p['size'] for p in non_bio],
                color=[p['color'] for p in non_bio],
                line=dict(width=1.5, color='white'),
            ),
            text=[p['name'] for p in non_bio],
            textposition=[p['tpos'] for p in non_bio],
            textfont=dict(size=11, color=CHARCOAL),
        ),
        go.Scatter(
            x=[9.5], y=[9.8], mode='markers',
            marker=dict(size=70, color='rgba(45,106,79,0.18)', symbol='circle'),
        ),
        go.Scatter(
            x=[9.5], y=[9.8], mode='markers+text',
            marker=dict(
                size=26, color=FOREST, symbol='star',
                line=dict(width=2.5, color='white'),
            ),
            text=['<b>★ BioScope</b>'],
            textposition='middle right',
            textfont=dict(size=15, color=FOREST, family='Inter, sans-serif'),
        ),
    ],
))

fig.frames = frames

fig.update_layout(
    updatemenus=[{
        'type': 'buttons',
        'showactive': False,
        'x': 0.5, 'xanchor': 'center',
        'y': -0.10, 'yanchor': 'top',
        'buttons': [{
            'label': '▶  Reveal',
            'method': 'animate',
            'args': [None, {
                'frame': {'duration': 600, 'redraw': True},
                'transition': {'duration': 400, 'easing': 'cubic-in-out'},
                'fromcurrent': True,
                'mode': 'immediate',
            }],
        }],
        'bgcolor': FOREST,
        'font': {'color': 'white', 'size': 13},
        'bordercolor': FOREST,
        'borderwidth': 0,
        'pad': {'l': 16, 'r': 16, 't': 8, 'b': 8},
    }],
    height=500,
    xaxis=dict(
        title=dict(text="← Turnaround: Weeks / Days                                                     Minutes →", font=dict(size=12, color='#555')),
        range=[0, 10], showgrid=False, zeroline=False, tickvals=[], ticktext=[],
    ),
    yaxis=dict(
        title=dict(text="← Single Test                                          Full Certification →", font=dict(size=12, color='#555')),
        range=[0, 10], showgrid=False, zeroline=False, tickvals=[], ticktext=[],
    ),
    margin=dict(l=80, r=30, t=30, b=80),
    plot_bgcolor='white',
    paper_bgcolor='#F8F7F4',
    font=dict(family='Inter, sans-serif', color=CHARCOAL),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 2. RADAR CHART + COMPETITOR SUMMARIES
# ═══════════════════════════════════════════════════════════════════════════════
st.subheader("Capability Profile")

left, right = st.columns([3, 2])

with left:
    dimensions = [
        'Turnaround Speed',
        'Analyte Breadth',
        'Welfare & Authenticity',
        'Certification Value',
        'Ease of Use',
        'Cost per Insight',
    ]
    radar_companies = {
        'BioScope':     {'scores': [10, 10, 10, 10, 10, 9], 'color': FOREST, 'dash': 'solid', 'width': 4},
        'Eurofins/SGS': {'scores': [2,  7,  2,  4,  3,  4], 'color': ROSE,   'dash': 'dot',   'width': 2},
        'Neogen':       {'scores': [8,  2,  1,  2,  8,  7], 'color': AMBER,  'dash': 'dot',   'width': 2},
        'Bruker':       {'scores': [4,  7,  3,  3,  2,  3], 'color': VIOLET, 'dash': 'dot',   'width': 2},
    }
    fig_r = go.Figure()
    for company, cfg in radar_companies.items():
        scores = cfg['scores'] + [cfg['scores'][0]]
        cats   = dimensions + [dimensions[0]]
        fig_r.add_trace(go.Scatterpolar(
            r=scores, theta=cats,
            fill='toself' if company == 'BioScope' else 'none',
            fillcolor='rgba(45,106,79,0.12)' if company == 'BioScope' else 'rgba(0,0,0,0)',
            name=company,
            line=dict(color=cfg['color'], width=cfg['width'], dash=cfg['dash']),
        ))
    fig_r.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 10]),
            angularaxis=dict(tickfont=dict(size=12)),
            bgcolor='white',
        ),
        legend=dict(orientation='h', y=-0.08, font=dict(size=11)),
        height=380,
        margin=dict(l=50, r=50, t=20, b=50),
        paper_bgcolor='#F8F7F4',
        font=dict(family='Inter, sans-serif', color=CHARCOAL),
    )
    st.plotly_chart(fig_r, use_container_width=True)

with right:
    st.markdown("<br><br>", unsafe_allow_html=True)
    insights = [
        (FOREST, "BioScope",     "The only player that scores high across every axis — fast, comprehensive, and certifiable in a single scan."),
        (ROSE,   "Eurofins/SGS", "Deep test menu but multi-week turnaround, per-test billing, and no welfare or origin capability."),
        (AMBER,  "Neogen",       "Fast kits, but each one answers a single question. Cannot bundle into a certification badge."),
        (VIOLET, "Bruker",       "Technically capable instruments — but requires a trained scientist and hours of sample prep before any result."),
    ]
    for color, name, text in insights:
        st.markdown(f"""
        <div style="margin-bottom:14px;padding:10px 14px;border-left:4px solid {color};
                    background:white;border-radius:0 8px 8px 0;
                    box-shadow:0 1px 6px rgba(45,106,79,0.07)">
            <div style="font-weight:700;color:{color};font-size:13px">{name}</div>
            <div style="font-size:12px;color:#6B7280;margin-top:3px">{text}</div>
        </div>""", unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 3. CAPABILITY GRID
# ═══════════════════════════════════════════════════════════════════════════════
st.subheader("Who Can Do What?")

grid = {
    "Capability":            ["Multi-residue chemical panel", "Animal welfare biomarkers", "Species / fraud authentication", "Geographic origin tracing", "Results in minutes", "Single scan — no fragmentation", "Investor-grade certification badge"],
    "BioScope ★":            ["✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Eurofins / SGS":        ["✅", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌"],
    "Neogen":                ["⚠️", "❌", "❌", "❌", "✅", "❌", "❌"],
    "Bruker":                ["✅", "⚠️", "✅", "⚠️", "❌", "❌", "❌"],
    "Bureau Veritas":        ["❌", "❌", "❌", "❌", "❌", "❌", "⚠️"],
    "Clear Labs":            ["❌", "❌", "✅", "❌", "⚠️", "❌", "❌"],
}

st.dataframe(
    pd.DataFrame(grid),
    use_container_width=True,
    hide_index=True,
    column_config={col: st.column_config.TextColumn(width="small") for col in grid if col != "Capability"},
)
st.caption("✅ Full capability  ·  ⚠️ Partial / requires workaround  ·  ❌ Not offered")
