"""
Music Generator — standalone page wrapping the AI Music provider APIs.
"""
import streamlit as st

from components.styles import inject_css
from components.header import render_header
from api.providers import AI_MUSIC_PROVIDERS, provider_labels, provider_id_from_label
from api.music_api import generate_music
from state import init_state, get_active_project, get_active_scene

st.set_page_config(page_title="Music Generator · EagleArtistAI", page_icon="🎵", layout="wide")

init_state()
inject_css()

project = get_active_project()
render_header(project_title=project.title, credits=st.session_state.credits)

st.markdown("<div style='padding: 24px 48px; max-width: 640px;'>", unsafe_allow_html=True)
st.markdown("## 🎵 Music Generator")

provider_label = st.selectbox("Music provider", provider_labels(AI_MUSIC_PROVIDERS))
provider_id = provider_id_from_label(AI_MUSIC_PROVIDERS, provider_label)

mood = st.selectbox("Mood", ["Cinematic", "Upbeat", "Ambient", "Dramatic", "Tense", "Uplifting"])
prompt = st.text_area("Describe the track", placeholder="e.g. soaring orchestral theme for a mountain flight sequence")

if st.button("Generate music", type="primary"):
    if not prompt:
        st.warning("Describe the track first.")
    else:
        result = generate_music(prompt, mood=mood.lower(), provider_id=provider_id)
        active_scene = get_active_scene()
        if active_scene:
            active_scene.assets.music_url = result.get("audio_url")
        st.success(f"Sent to {result['provider']}. Status: {result['status']}")

st.markdown("</div>", unsafe_allow_html=True)
