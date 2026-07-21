"""
AI Video Studio — canvas + timeline (left) and the upgraded AI panel (right),
plus the far-right tool icon rail. This is the upgraded version of the
original uploaded Streamlit UI clone.
"""
import streamlit as st

from components.styles import inject_css
from components.header import render_header
from components.canvas import render_canvas
from components.timeline import render_timeline
from components.ai_panel import render_ai_panel
from components.sidebar import render_icon_sidebar
from state import init_state, get_active_project, get_active_scene, add_scene_to_active_project

st.set_page_config(page_title="AI Video Studio · EagleArtistAI", page_icon="🦅", layout="wide")

init_state()
inject_css()

project = get_active_project()
render_header(project_title=project.title, credits=st.session_state.credits)

col_workspace, col_aipanel, col_iconbar = st.columns([6, 3, 1], gap="small")

with col_workspace:
    active_scene = get_active_scene()
    render_canvas(duration=f"0:{active_scene.duration_seconds:02d}" if active_scene else "0:00")

    selected_id = render_timeline(project, st.session_state.active_scene_id, on_add_scene=add_scene_to_active_project)
    if selected_id != st.session_state.active_scene_id:
        st.session_state.active_scene_id = selected_id
        st.rerun()

with col_aipanel:
    active_scene = get_active_scene()
    if active_scene:
        render_ai_panel(active_scene)
    else:
        st.info("Add a scene to the timeline to get started.")

with col_iconbar:
    render_icon_sidebar(active="ai_video")
