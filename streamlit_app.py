import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

pg = st.navigation([
    st.Page("home.py",                          title="Overview",             icon="🔬", default=True),
    st.Page("pages/1_Market_Sizing.py",         title="Market Sizing",        icon="📊"),
    st.Page("pages/2_Revenue_Model.py",         title="Revenue Model",        icon="💰"),
    st.Page("pages/3_Scenario_Analysis.py",     title="Scenario Analysis",    icon="🔀"),
    st.Page("pages/4_Sensitivity.py",           title="Sensitivity",          icon="🎯"),
    st.Page("pages/5_Competitive_Landscape.py", title="Competitive Landscape",icon="⚔️"),
])
pg.run()
