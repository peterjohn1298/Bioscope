import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Competitive Landscape — BioScope", layout="wide")

GREEN  = "#2ECC71"
BLUE   = "#1B4F72"
RED    = "#E74C3C"
ORANGE = "#E67E22"
PURPLE = "#9B59B6"
GREY   = "#95A5A6"

st.title("⚔️ Competitive Landscape")
st.markdown("BioScope occupies a white space that no existing player serves — fast, comprehensive, and certifiable.")

# ═══════════════════════════════════════════════════════════════════════════════
# 1. QUADRANT MAP — clean 2×2 with only relevant players
# ═══════════════════════════════════════════════════════════════════════════════
st.subheader("Where Does Everyone Sit?")

# Only the 6 most investor-relevant competitors + BioScope
# x = turnaround speed (1=weeks, 10=minutes)
# y = scope of insight (1=one question answered, 10=full certification)
players = [
    {'name': 'BioScope',       'x': 9.5, 'y': 9.8, 'color': GREEN,  'size': 22, 'symbol': 'star',   'label_pos': 'middle right'},
    {'name': 'Eurofins / SGS', 'x': 1.8, 'y': 6.5, 'color': RED,    'size': 14, 'symbol': 'circle', 'label_pos': 'top center'},
    {'name': 'Neogen',         'x': 7.5, 'y': 2.0, 'color': ORANGE, 'size': 12, 'symbol': 'circle', 'label_pos': 'top center'},
    {'name': 'Bruker',         'x': 3.5, 'y': 6.0, 'color': PURPLE, 'size': 12, 'symbol': 'circle', 'label_pos': 'top center'},
    {'name': 'Bureau Veritas', 'x': 1.5, 'y': 3.5, 'color': GREY,   'size': 12, 'symbol': 'circle', 'label_pos': 'bottom center'},
    {'name': 'Clear Labs',     'x': 5.0, 'y': 2.5, 'color': '#3498DB', 'size': 10, 'symbol': 'circle', 'label_pos': 'top center'},
]

fig_q = go.Figure()

# Quadrant background shading
fig_q.add_shape(type='rect', x0=0, y0=5, x1=5, y1=10,
                fillcolor='rgba(231,76,60,0.05)', line=dict(width=0))
fig_q.add_shape(type='rect', x0=5, y0=5, x1=10, y1=10,
                fillcolor='rgba(46,204,113,0.08)', line=dict(width=0))
fig_q.add_shape(type='rect', x0=0, y0=0, x1=5, y1=5,
                fillcolor='rgba(149,165,166,0.05)', line=dict(width=0))
fig_q.add_shape(type='rect', x0=5, y0=0, x1=10, y1=5,
                fillcolor='rgba(230,126,34,0.05)', line=dict(width=0))

# Quadrant labels
fig_q.add_annotation(x=2.5, y=9.3, text="<b>Broad but Slow</b><br><span style='font-size:10px'>Multi-week turnaround</span>",
                     showarrow=False, font=dict(size=11, color='#AAB7B8'), align='center')
fig_q.add_annotation(x=7.5, y=9.3, text="<b>★ Integrated Platform</b><br><span style='font-size:10px'>BioScope's white space</span>",
                     showarrow=False, font=dict(size=11, color=GREEN), align='center')
fig_q.add_annotation(x=2.5, y=0.8, text="<b>Narrow & Slow</b>",
                     showarrow=False, font=dict(size=11, color='#AAB7B8'), align='center')
fig_q.add_annotation(x=7.5, y=0.8, text="<b>Fast but One Question</b>",
                     showarrow=False, font=dict(size=11, color='#AAB7B8'), align='center')

# Divider lines
fig_q.add_hline(y=5, line_dash='dash', line_color='#D5D8DC', line_width=1)
fig_q.add_vline(x=5, line_dash='dash', line_color='#D5D8DC', line_width=1)

# Plot each player
for p in players:
    is_bio = p['name'] == 'BioScope'
    fig_q.add_trace(go.Scatter(
        x=[p['x']], y=[p['y']],
        mode='markers+text',
        marker=dict(
            size=p['size'],
            color=p['color'],
            symbol=p['symbol'],
            line=dict(width=2 if is_bio else 1, color='white'),
        ),
        text=[f"<b>{p['name']}</b>" if is_bio else p['name']],
        textposition=p['label_pos'],
        textfont=dict(size=13 if is_bio else 11, color=p['color'] if is_bio else '#2C3E50'),
        showlegend=False,
        hovertemplate=f"<b>{p['name']}</b><extra></extra>",
    ))

fig_q.update_layout(
    height=430,
    xaxis=dict(title="← Days / Weeks &nbsp;&nbsp;&nbsp;&nbsp; Turnaround Speed &nbsp;&nbsp;&nbsp;&nbsp; Minutes →",
               range=[0, 10], showgrid=False, zeroline=False,
               tickvals=[], ticktext=[]),
    yaxis=dict(title="← Single Test &nbsp;&nbsp;&nbsp;&nbsp; Scope of Insight &nbsp;&nbsp;&nbsp;&nbsp; Full Certification →",
               range=[0, 10], showgrid=False, zeroline=False,
               tickvals=[], ticktext=[]),
    margin=dict(l=80, r=20, t=20, b=60),
    plot_bgcolor='white', paper_bgcolor='white',
)
st.plotly_chart(fig_q, use_container_width=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 2. RADAR CHART — capability profile side by side with clean description
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
        'BioScope':     {'scores': [10, 10, 10, 10, 10, 9], 'color': GREEN,  'dash': 'solid', 'width': 4},
        'Eurofins/SGS': {'scores': [2,  7,  2,  4,  3,  4], 'color': RED,    'dash': 'dot',   'width': 2},
        'Neogen':       {'scores': [8,  2,  1,  2,  8,  7], 'color': ORANGE, 'dash': 'dot',   'width': 2},
        'Bruker':       {'scores': [4,  7,  3,  3,  2,  3], 'color': PURPLE, 'dash': 'dot',   'width': 2},
    }

    fig_r = go.Figure()
    for company, cfg in radar_companies.items():
        scores = cfg['scores'] + [cfg['scores'][0]]
        cats   = dimensions + [dimensions[0]]
        fig_r.add_trace(go.Scatterpolar(
            r=scores, theta=cats,
            fill='toself' if company == 'BioScope' else 'none',
            fillcolor='rgba(46,204,113,0.12)' if company == 'BioScope' else 'rgba(0,0,0,0)',
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
        paper_bgcolor='white',
    )
    st.plotly_chart(fig_r, use_container_width=True)

with right:
    st.markdown("<br><br>", unsafe_allow_html=True)
    insights = [
        (GREEN,  "BioScope",     "Occupies the top-right on every axis — the only player that is simultaneously fast, broad, and certifiable."),
        (RED,    "Eurofins/SGS", "Broad test menu but slow (days–weeks), per-test billing, no welfare or origin capability."),
        (ORANGE, "Neogen",       "Fast kits but each kit answers exactly one question. Cannot bundle into a certification."),
        (PURPLE, "Bruker",       "Technically capable instruments — but sold to labs. Requires in-house scientists and separate sample prep."),
    ]
    for color, name, text in insights:
        st.markdown(f"""
        <div style="margin-bottom:14px;padding:10px 14px;border-left:4px solid {color};background:#FAFAFA;border-radius:0 6px 6px 0">
            <div style="font-weight:700;color:{color};font-size:13px">{name}</div>
            <div style="font-size:12px;color:#555;margin-top:3px">{text}</div>
        </div>""", unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 3. CAPABILITY GRID — clean ✅ / ⚠️ / ❌ matrix, no long text
# ═══════════════════════════════════════════════════════════════════════════════
st.subheader("Who Can Do What?")

capabilities = [
    "Multi-residue chemical panel",
    "Animal welfare biomarkers",
    "Species / fraud authentication",
    "Geographic origin tracing",
    "Results in minutes",
    "Single scan — no fragmentation",
    "Investor-grade certification badge",
]

grid = {
    "Capability":        capabilities,
    "BioScope ★":        ["✅", "✅", "✅", "✅", "✅", "✅", "✅"],
    "Eurofins / SGS":    ["✅", "⚠️", "⚠️", "⚠️", "❌", "❌", "❌"],
    "Neogen":            ["⚠️", "❌", "❌", "❌", "✅", "❌", "❌"],
    "Bruker":            ["✅", "⚠️", "✅", "⚠️", "❌", "❌", "❌"],
    "Bureau Veritas":    ["❌", "❌", "❌", "❌", "❌", "❌", "⚠️"],
    "Clear Labs":        ["❌", "❌", "✅", "❌", "⚠️", "❌", "❌"],
}

df_grid = pd.DataFrame(grid)

st.dataframe(
    df_grid,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Capability":     st.column_config.TextColumn(width="medium"),
        "BioScope ★":     st.column_config.TextColumn(width="small"),
        "Eurofins / SGS": st.column_config.TextColumn(width="small"),
        "Neogen":         st.column_config.TextColumn(width="small"),
        "Bruker":         st.column_config.TextColumn(width="small"),
        "Bureau Veritas": st.column_config.TextColumn(width="small"),
        "Clear Labs":     st.column_config.TextColumn(width="small"),
    }
)
st.caption("✅ Full capability  ·  ⚠️ Partial / requires workaround  ·  ❌ Not offered")
