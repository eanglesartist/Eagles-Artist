"""
voice_panel.py
------------------
AI voiceover generation panel (used on the Studio page and could be
reused standalone).
"""
import streamlit as st

from api.providers import AI_VOICE_PROVIDERS, provider_labels, provider_id_from_label
from api.voice_api import generate_voice


def render_voice_panel(active_scene):
    st.markdown('<div class="ai-panel-header">🎙️ AI Voiceover</div>', unsafe_allow_html=True)

    provider_label = st.selectbox("Voice provider", provider_labels(AI_VOICE_PROVIDERS), key="voice_provider")
    provider_id = provider_id_from_label(AI_VOICE_PROVIDERS, provider_label)

    voice = st.selectbox("Voice", ["Narrator", "Warm", "Energetic", "Documentary"], key="voice_style")
    script = st.text_area("Script", placeholder="Enter the narration script…", key="voice_script", height=100)

    if st.button("Generate voiceover", type="primary", key="generate_voice_btn"):
        if not script:
            st.warning("Enter a script first.")
        else:
            result = generate_voice(script, voice=voice, provider_id=provider_id)
            active_scene.assets.voice_url = result.get("audio_url")
            st.success(f"Sent to {result['provider']}. Status: {result['status']}")
