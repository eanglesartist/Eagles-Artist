"""
caption_panel.py
------------------
Auto-caption generation + manual editing.
"""
import streamlit as st


def render_caption_panel(active_scene):
    st.markdown('<div class="ai-panel-header">💬 Captions</div>', unsafe_allow_html=True)

    language = st.selectbox("Language", ["English", "Spanish", "French", "Hindi"], key="caption_lang")

    if st.button("Auto-generate captions", key="auto_caption_btn"):
        # TODO: replace with a real speech-to-text / captioning service call
        active_scene.assets.caption_text = active_scene.prompt or "…"
        st.success(f"Captions generated in {language} (stub).")

    caption_text = st.text_area(
        "Caption text",
        value=active_scene.assets.caption_text or "",
        key="caption_text_edit",
        height=80,
    )
    active_scene.assets.caption_text = caption_text
