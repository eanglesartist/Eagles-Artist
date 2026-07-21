"""
timeline.py
------------------
Renders the Scene clip timeline for the active project and returns
the id of the scene the user clicked on (via Streamlit buttons laid
under the styled strip, since raw HTML can't carry click events back).
"""
import streamlit as st


def render_timeline(project, active_scene_id: str | None, on_add_scene=None):
    st.markdown('<div class="timeline-box">', unsafe_allow_html=True)

    total = project.total_duration()
    st.markdown(
        f"""
        <div class="timeline-controls">
            <span>☰ Show timing ▾</span>
            <span style="font-family:monospace;font-weight:600;">00:{total:02d}.0 total</span>
            <span>Zoom 100% ▾</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(len(project.scenes) + 1) if project.scenes else st.columns(1)

    selected = active_scene_id
    for i, scene in enumerate(project.scenes):
        with cols[i]:
            active_class = "active" if scene.id == active_scene_id else ""
            st.markdown(
                f"""<div class="clip-thumbnail {active_class}">🎬 Scene {i+1} · {scene.duration_seconds}s</div>""",
                unsafe_allow_html=True,
            )
            if st.button("Select", key=f"select_{scene.id}", use_container_width=True):
                selected = scene.id

    with cols[-1]:
        if st.button("➕ Add Scene", key="add_scene_btn", use_container_width=True):
            if on_add_scene:
                on_add_scene()

    st.markdown("</div>", unsafe_allow_html=True)
    return selected
