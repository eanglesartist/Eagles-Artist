"""
canvas.py
------------------
Main video preview screen (left/center of the Studio page).
"""
import streamlit as st


def render_canvas(duration: str = "0:08", image_url: str | None = None):
    bg_override = f"style=\"background-image:url('{image_url}')\"" if image_url else ""
    st.markdown(
        f"""
    <div class="canvas-box">
        <div class="canvas-image" {bg_override}>
            <div class="time-chip">{duration}</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
