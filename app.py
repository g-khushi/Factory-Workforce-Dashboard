import streamlit as st
from queries import get_overworked_workers, get_project_capacity
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Factory Workforce Dashboard",
    page_icon="🏭",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #f4f7fc;
}

.main {
    background-color: #f4f7fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

.title {
    font-size: 52px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 20px;
    color: #64748b;
    margin-bottom: 30px;
}

.metric-card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 20px;
}

.metric-number {
    font-size: 42px;
    font-weight: bold;
}

.metric-title {
    font-size: 18px;
    color: gray;
}

.section-card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.08);
}

.worker-item {
    background: #fff1f2;
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 12px;
    font-size: 20px;
    border-left: 6px solid #ef4444;
}

.project-item {
    background: #eff6ff;
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 12px;
    font-size: 20px;
    border-left: 6px solid #3b82f6;
}

.footer {
    margin-top: 40px;
    text-align: center;
    color: gray;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DATA
# ---------------------------------------------------
workers = get_overworked_workers()
projects = get_project_capacity()

worker_count = len(workers)
project_count = len(projects)

current_time = datetime.now().strftime("%I:%M %p")

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.markdown(
    '<div class="title">🏭 Factory Workforce Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Real-time insights from your factory operations</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# TOP METRICS
# ---------------------------------------------------
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number" style="color:#ef4444;">{worker_count}</div>
        <div class="metric-title">Overworked Workers</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number" style="color:#2563eb;">{project_count}</div>
        <div class="metric-title">Total Projects</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number" style="color:#16a34a;">Connected</div>
        <div class="metric-title">Neo4j Database</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number" style="color:#7c3aed;">{current_time}</div>
        <div class="metric-title">Last Updated</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# MAIN DASHBOARD
# ---------------------------------------------------
left, right = st.columns(2)

# ---------------------------------------------------
# OVERWORKED WORKERS
# ---------------------------------------------------
with left:

    st.markdown("""
    <div class="section-card">
    <h2>🔥 Overworked Workers</h2>
    """, unsafe_allow_html=True)

    if workers:
        for w in workers:
            st.markdown(
                f'''
                <div class="worker-item">
                👷 {w["name"]}
                </div>
                ''',
                unsafe_allow_html=True
            )
    else:
        st.success("No overloaded workers found")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# PROJECT CAPACITY
# ---------------------------------------------------
with right:

    st.markdown("""
    <div class="section-card">
    <h2>📦 Project Capacity</h2>
    """, unsafe_allow_html=True)

    if projects:
        for p in projects:
            st.markdown(
                f'''
                <div class="project-item">
                📁 {p["project"]}
                </div>
                ''',
                unsafe_allow_html=True
            )
    else:
        st.warning("No project data found")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("""
<div class="footer">
Built with ❤️ using Streamlit + Neo4j
</div>
""", unsafe_allow_html=True)