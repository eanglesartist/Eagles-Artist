import streamlit as st
from utils.session import init_session_state
from utils.config import BASE_DIR

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="AI Cinematic Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Initialize State
init_session_state()

# 3. Load Global CSS
def load_css():
    css_path = BASE_DIR / "css" / "app.css"
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# 4. App Layout (Imported from components)
# from components.top_toolbar import render_topbar
# from components.preview_canvas import render_canvas
# from components.timeline import render_timeline
# from components.ai_director import render_director_panel

st.title("🎬 AI Cinematic Studio")
st.success("Professional Architecture Initialized.")

# Example layout for when you build the components:
# render_topbar()
# col_main, col_side = st.columns([7, 3])
# with col_main:
#     render_canvas()
#     render_timeline()
# with col_side:
#     render_director_panel()
