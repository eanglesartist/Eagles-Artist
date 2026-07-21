"""
export_panel.py
------------------
Resolution / format selection + render & download/share.
"""
import streamlit as st


def render_export_panel(project):
    st.markdown('<div class="ai-panel-header">⬇️ Export</div>', unsafe_allow_html=True)

    resolution = st.radio("Resolution", ["1080p", "4K"], horizontal=True, key="export_resolution")
    fmt = st.selectbox("Format", ["MP4", "MOV"], key="export_format")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬇️ Download", type="primary", use_container_width=True, key="export_download_btn"):
            project.export.resolution = resolution
            project.export.format = fmt
            st.success(f"Rendering {project.title} at {resolution} ({fmt})… (stub)")
    with col2:
        if st.button("🔗 Share", use_container_width=True, key="export_share_btn"):
            st.info("Share link copied (stub).")
