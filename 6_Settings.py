"""
Settings — API provider configuration status + credits.
"""
import os
import streamlit as st

from components.styles import inject_css
from components.header import render_header
from api.providers import AI_VIDEO_PROVIDERS, AI_IMAGE_PROVIDERS, AI_VOICE_PROVIDERS, AI_MUSIC_PROVIDERS
from state import init_state, get_active_project

st.set_page_config(page_title="Settings · EagleArtistAI", page_icon="⚙️", layout="wide")

init_state()
inject_css()

project = get_active_project()
render_header(project_title=project.title, credits=st.session_state.credits)

st.markdown("<div style='padding: 24px 48px; max-width: 760px;'>", unsafe_allow_html=True)
st.markdown("## ⚙️ Settings")

st.markdown(f"**Account:** {st.session_state.user_email}")
st.markdown(f"**Credits remaining:** ⚡ {st.session_state.credits}")

st.markdown("### AI Provider status")
st.caption("Configure real API keys in `.env`, then set `enabled=True` in `api/providers.py`.")


def render_provider_table(title, providers):
    st.markdown(f"**{title}**")
    for pid, info in providers.items():
        key_present = bool(os.getenv(info["env_key"]))
        status = "🟢 Key found" if key_present else "⚪ Not configured"
        enabled = "✅ Enabled" if info["enabled"] else "🚧 Stub mode"
        st.write(f"- {info['label']} — {status} — {enabled}")


render_provider_table("AI Video", AI_VIDEO_PROVIDERS)
render_provider_table("AI Image", AI_IMAGE_PROVIDERS)
render_provider_table("Voice", AI_VOICE_PROVIDERS)
render_provider_table("Music", AI_MUSIC_PROVIDERS)

st.markdown("</div>", unsafe_allow_html=True)
