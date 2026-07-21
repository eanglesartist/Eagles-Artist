"""
header.py
------------------
Top bar: EagleArtistAI branding, menu, credits, project actions.
"""
import streamlit as st


def render_header(project_title: str = "Untitled video", credits: int = 1000):
    st.markdown(
        f"""
    <div class="topbar">
        <div class="logo-area">
            <div class="logo-badge">🦅</div>
            <div class="title-block">
                EagleArtistAI Studio
                <span style="color:#94A3B8; font-weight:500; font-size:13px;">/ {project_title}</span>
            </div>
            <div class="menu">
                <span>File</span><span>Edit</span><span>View</span><span>Insert</span>
                <span>Format</span><span>Scene</span><span>Arrange</span><span>Tools</span><span>Help</span>
            </div>
        </div>
        <div class="top-actions">
            <span class="credits-pill">⚡ Credits: {credits}</span>
            <span class="top-link">Projects</span>
            <span class="top-link">Templates</span>
            <button class="btn-play-outline">▶ Play</button>
            <button class="btn-share-solid">🔒 Share ▾</button>
            <div class="avatar-circle">🦊</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
