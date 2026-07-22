import streamlit as st
from utils.session import init_session_state
from utils.config import BASE_DIR

# ==========================================
# 1. PAGE CONFIGURATION & STATE
# ==========================================
st.set_page_config(
    page_title="AI Cinematic Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed" 
)
init_session_state()

# ==========================================
# 2. CUSTOM CSS INJECTION
# ==========================================
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 98%; }
        header { visibility: hidden; } 
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. UI COMPONENTS (Mocks)
# ==========================================
def render_top_toolbar():
    with st.container():
        cols = st.columns([2, 1, 1, 1, 2, 1, 1], vertical_alignment="center")
        cols[0].markdown("### 🎬 Cinematic Studio")
        cols[1].button("📁 Project", use_container_width=True)
        cols[2].button("💾 Save", use_container_width=True)
        cols[3].button("↩️ Undo", use_container_width=True)
        cols[4].selectbox("🧠 AI Model", ["Veo 3.1 Pro", "Runway Gen-3", "Sora", "Kling"], label_visibility="collapsed")
        cols[5].markdown("**Credits: 1,250**")
        cols[6].button("👤 Profile", use_container_width=True)
        st.divider()

def render_left_sidebar():
    st.subheader("Library")
    tabs = st.tabs(["Storyboard", "Assets", "Uploads"])
    with tabs[0]: 
        st.info("Visual storyboard blocks will appear here.")
    
    st.divider()
    st.subheader("🎞️ Timeline")
    st.button("+ Add Scene", use_container_width=True)
    st.button("View Render Queue", use_container_width=True)

def render_preview_canvas():
    st.subheader("Preview Canvas")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4") 
    
    cols = st.columns([1, 4, 1])
    cols[0].button("⏮", use_container_width=True)
    cols[1].slider("Playhead", 0, 100, 50, label_visibility="collapsed")
    cols[2].button("⏭", use_container_width=True)

def render_right_sidebar():
    st.subheader("AI Director")
    tabs = st.tabs(["Prompt", "Camera", "Extend"])
    
    with tabs[0]:
        st.text_area("Scene Description", height=150, placeholder="A cinematic wide shot of...")
        st.file_uploader("Reference Image")
        st.button("✨ Generate", type="primary", use_container_width=True)
        
    with tabs[1]:
        st.selectbox("Lens", ["24mm Wide", "35mm Standard", "50mm Portrait", "85mm Telephoto"])
        st.selectbox("Motion", ["Static", "Pan Right", "Push In", "FPV Drone"])
        
    with tabs[2]:
        st.checkbox("Maintain Character Continuity", value=True)
        st.checkbox("Maintain Environment", value=True)
        st.button("🚀 Extend (+4s)", type="primary", use_container_width=True)

# ==========================================
# 4. MAIN WORKSPACE LAYOUT
# ==========================================
render_top_toolbar()

# 3-column grid (Left Menu | Main Canvas | AI Director)
left_col, center_col, right_col = st.columns([2.5, 5, 3.5], gap="large")

with left_col:
    render_left_sidebar()

with center_col:
    render_preview_canvas()

with right_col:
    render_right_sidebar()
