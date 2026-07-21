"""
Image Generator — standalone page wrapping the AI Image provider APIs.
Used for reference frames / thumbnails that feed Image → Video generation.
"""
import streamlit as st

from components.styles import inject_css
from components.header import render_header
from api.providers import AI_IMAGE_PROVIDERS, provider_labels, provider_id_from_label
from api.image_api import generate_image
from state import init_state, get_active_project

st.set_page_config(page_title="Image Generator · EagleArtistAI", page_icon="🖼️", layout="wide")

init_state()
inject_css()

project = get_active_project()
render_header(project_title=project.title, credits=st.session_state.credits)

st.markdown("<div style='padding: 24px 48px; max-width: 640px;'>", unsafe_allow_html=True)
st.markdown("## 🖼️ Image Generator")

provider_label = st.selectbox("Image provider", provider_labels(AI_IMAGE_PROVIDERS))
provider_id = provider_id_from_label(AI_IMAGE_PROVIDERS, provider_label)

prompt = st.text_area("Describe the image", placeholder="e.g. a golden eagle perched on a snowy ridge, dawn light")

if st.button("Generate image", type="primary"):
    if not prompt:
        st.warning("Describe the image first.")
    else:
        result = generate_image(prompt, provider_id=provider_id)
        st.success(f"Sent to {result['provider']}. Status: {result['status']}")
        st.caption("This reference image can be used as the source for an 'Image → Video' clip in the Studio.")

st.markdown("</div>", unsafe_allow_html=True)
