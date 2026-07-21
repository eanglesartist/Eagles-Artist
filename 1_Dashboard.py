"""
Dashboard — New Video, My Projects, Credits, Templates.
"""
import streamlit as st

from components.styles import inject_css
from components.header import render_header
from state import init_state, get_active_project, create_project

st.set_page_config(page_title="Dashboard · EagleArtistAI", page_icon="🦅", layout="wide")

init_state()
inject_css()

project = get_active_project()
render_header(project_title=project.title, credits=st.session_state.credits)

st.markdown("<div style='padding: 32px 48px;'>", unsafe_allow_html=True)
st.markdown("## Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="dash-card">🎬<h3>New Video</h3><p>Start a fresh project</p></div>', unsafe_allow_html=True)
    new_title = st.text_input("Project title", value="Untitled video", key="new_project_title", label_visibility="collapsed")
    if st.button("＋ Create", use_container_width=True, key="dash_create_project"):
        create_project(new_title or "Untitled video")
        st.switch_page("pages/2_AI_Video_Studio.py")

with col2:
    st.markdown('<div class="dash-card">📁<h3>My Projects</h3><p>Resume recent work</p></div>', unsafe_allow_html=True)
    st.write(f"{len(st.session_state.projects)} project(s) in this session")
    if st.button("Manage projects", use_container_width=True, key="dash_manage_projects"):
        st.switch_page("pages/5_Project_Manager.py")

with col3:
    st.markdown(f'<div class="dash-card">⚡<h3>{st.session_state.credits} Credits</h3><p>Generation balance</p></div>', unsafe_allow_html=True)
    if st.button("Settings & billing", use_container_width=True, key="dash_settings"):
        st.switch_page("pages/6_Settings.py")

with col4:
    st.markdown('<div class="dash-card">🗂️<h3>Templates</h3><p>Story, product, character presets</p></div>', unsafe_allow_html=True)
    st.caption("Coming soon — drop preset prompts into assets/templates/")

st.markdown("</div>", unsafe_allow_html=True)
