"""
BioScope Green — shared design system.
Import apply_theme() and color constants in every page.
"""
import streamlit as st

# ── Palette ────────────────────────────────────────────────────────────────────
FOREST  = "#2D6A4F"   # primary brand green
MINT    = "#52B788"   # lighter green
AMBER   = "#E9770E"   # warm accent
CHARCOAL= "#1A2332"   # headings / dark text
TEAL    = "#0F766E"   # cool green
ROSE    = "#BE123C"   # bear / downside
VIOLET  = "#6D28D9"   # extra segment
SAGE    = "#D1FAE5"   # light green tint
CREAM   = "#F8F7F4"   # page background
GREY    = "#6B7280"   # muted text

# Segment chart order
SEG_COLORS = [FOREST, MINT, AMBER, TEAL, ROSE, VIOLET]

# ── CSS ────────────────────────────────────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp                      { background-color: #F8F7F4 !important; }
.block-container            { padding-top: 1.5rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #152B22 0%, #2D6A4F 100%) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] a { color: #D1FAE5 !important; }

/* ── KPI cards ── */
.metric-card {
    background: white;
    border-radius: 14px;
    padding: 22px 24px 18px;
    border-left: 5px solid #2D6A4F;
    box-shadow: 0 2px 16px rgba(45,106,79,0.10), 0 1px 4px rgba(0,0,0,0.04);
}
.metric-label {
    font-size: 10px; color: #6B7280; font-weight: 700;
    letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 4px;
}
.metric-value {
    font-size: 32px; font-weight: 800; color: #1A2332;
    margin: 4px 0; line-height: 1.15;
}
.metric-sub { font-size: 11px; color: #9CA3AF; margin-top: 2px; }

/* ── Section headers ── */
.section-header {
    font-size: 16px; font-weight: 700; color: #2D6A4F;
    margin: 28px 0 10px; padding-bottom: 8px;
    border-bottom: 2px solid #D1FAE5; letter-spacing: 0.2px;
}

/* ── Page headings ── */
h1 { color: #1A2332 !important; font-weight: 800 !important; }
h2, h3 { color: #2D6A4F !important; font-weight: 700 !important; }

/* ── Native st.metric ── */
[data-testid="metric-container"] {
    background: white !important; border-radius: 12px !important;
    padding: 16px 20px !important; border: 1px solid #D1FAE5 !important;
    box-shadow: 0 2px 10px rgba(45,106,79,0.07) !important;
}
[data-testid="stMetricValue"]  { color: #1A2332 !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"]  { color: #2D6A4F !important; font-weight: 600 !important; font-size: 13px !important; }

/* ── Dataframe: forest green header row ── */
[data-testid="stDataFrame"] th,
[data-testid="stDataFrame"] th div,
[data-testid="stDataFrame"] th span,
.dvn-scroller .col-header-cell,
.dvn-scroller .col-header-cell span {
    color: #FFFFFF !important;
    background-color: #2D6A4F !important;
    font-weight: 700 !important;
    font-size: 12px !important;
}

/* ── Tabs ── */
button[data-baseweb="tab"]                  { font-weight: 600 !important; color: #6B7280 !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #2D6A4F !important; border-bottom: 3px solid #2D6A4F !important; }

/* ── Expander ── */
[data-testid="stExpander"] > details > summary { font-weight: 600 !important; color: #2D6A4F !important; }
[data-testid="stExpander"] { border: 1px solid #D1FAE5 !important; border-radius: 10px !important; background: white !important; }

/* ── Info box ── */
[data-testid="stInfo"] { background: #F0FDF4 !important; border-left-color: #2D6A4F !important; border-radius: 8px !important; }

/* ── Slider thumb ── */
[data-testid="stSlider"] > div > div > div > div { background: #2D6A4F !important; }

/* ── Divider ── */
hr { border-color: #D1FAE5 !important; }

/* ── Caption ── */
[data-testid="stCaptionContainer"] { color: #6B7280 !important; font-size: 12px !important; }
</style>
"""


def apply_theme():
    st.markdown(_CSS, unsafe_allow_html=True)


def chart_layout(**kwargs):
    """Return a base Plotly layout dict with BioScope Green defaults."""
    base = dict(
        plot_bgcolor='white',
        paper_bgcolor=CREAM,
        font=dict(family='Inter, sans-serif', color=CHARCOAL),
        margin=dict(l=0, r=0, t=20, b=10),
        xaxis=dict(showgrid=True, gridcolor='#E8F5EE', linecolor='#E8F5EE'),
        yaxis=dict(showgrid=True, gridcolor='#E8F5EE', linecolor='#E8F5EE'),
    )
    base.update(kwargs)
    return base
