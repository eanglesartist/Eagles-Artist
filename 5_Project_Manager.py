"""
Project Manager — list/select/create projects, each with its own Scene timeline.
"""
import streamlit as st

from components.styles import inject_css
from components.header import render_header
from state import init_state, get_active_project, create_project

st.set_page_config(page_title="Projects · EagleArtistAI", page_icon="📁", layout="wide")

init_state()
inject_css()

project = get_active_project()
render_header(project_title=project.title, credits=st.session_state.credits)

st.markdown("<div style='padding: 24px 48px;'>", unsafe_allow_html=True)
st.markdown("## 📁 Project Manager")

new_title = st.text_input("New project title", placeholder="e.g. Eagle Documentary Teaser")
if st.button("＋ New project"):
    create_project(new_title or "Untitled video")
    st.rerun()

st.markdown("### Your projects")
for pid, proj in st.session_state.projects.items():
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 2, 1])
        with c1:
            st.markdown(f"**{proj.title}**")
            st.caption(f"{len(proj.scenes)} scene(s) · {proj.total_duration()}s total")
        with c2:
            st.caption(f"Created {proj.created_at[:19].replace('T', ' ')}")
        with c3:
            if st.button("Open", key=f"open_{pid}"):
                st.session_state.active_project_id = pid
                st.session_state.active_scene_id = proj.scenes[0].id if proj.scenes else None
                st.switch_page("pages/2_AI_Video_Studio.py")

st.markdown("</div>", unsafe_allow_html=True)
