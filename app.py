"""
app.py
------------------
Main entry point. Streamlit auto-discovers pages/ as the multipage nav;
this file renders the landing/dashboard content and page config used
across the whole app.
"""
import streamlit as st

from components.styles import inject_css
from components.header import render_header
from state import init_state, get_active_project

st.set_page_config(page_title="EagleArtistAI Studio", page_icon="🦅", layout="wide", initial_sidebar_state="collapsed")

init_state()
inject_css()

project = get_active_project()
render_header(project_title=project.title, credits=st.session_state.credits)

st.markdown("<div style='padding: 32px 48px;'>", unsafe_allow_html=True)
st.markdown("## 🦅 Welcome to EagleArtistAI Studio")
st.write(
    "Describe a scene in plain language and EagleArtistAI turns it into a finished video — "
    "clips, voiceover, music, and captions, all AI-generated."
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="dash-card">🎬<h3>New Video</h3><p>Start a fresh project</p></div>', unsafe_allow_html=True)
    if st.button("Open Studio", use_container_width=True, key="home_open_studio"):
        st.switch_page("pages/2_AI_Video_Studio.py")
with col2:
    st.markdown('<div class="dash-card">📁<h3>My Projects</h3><p>Resume recent work</p></div>', unsafe_allow_html=True)
    if st.button("View Projects", use_container_width=True, key="home_view_projects"):
        st.switch_page("pages/5_Project_Manager.py")
with col3:
    st.markdown(f'<div class="dash-card">⚡<h3>{st.session_state.credits} Credits</h3><p>Generation balance</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="dash-card">🗂️<h3>Templates</h3><p>Start from a preset</p></div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
