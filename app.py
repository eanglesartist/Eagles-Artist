import streamlit as st
import time
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

if "user_credits" not in st.session_state:
    st.session_state["user_credits"] = 1250

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
# 3. DIALOG: UPGRADE PLAN POPUP ($1 - $10)
# ==========================================
@st.dialog("🚀 Upgrade Your Plan")
def show_upgrade_plan_dialog():
    st.write("Choose a plan or top-up package to upgrade your studio capabilities:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Starter Pack")
        st.write("⚡ **50 Credits**")
        st.write("**$1.00 / one-time**")
        st.write("Ideal for quick tests.")
        if st.button("Select $1", key="plan_1", use_container_width=True):
            st.session_state["user_credits"] += 50
            st.success("Upgraded with 50 credits!")
            time.sleep(1)
            st.rerun()
            
    with col2:
        st.markdown("### Creator Pro")
        st.write("⚡ **300 Credits**")
        st.write("**$5.00 / one-time**")
        st.write("Best for regular editing.")
        if st.button("Select $5", key="plan_5", use_container_width=True):
            st.session_state["user_credits"] += 300
            st.success("Upgraded with 300 credits!")
            time.sleep(1)
            st.rerun()
            
    with col3:
        st.markdown("### Studio Unlimited")
        st.write("⚡ **700 Credits**")
        st.write("**$10.00 / one-time**")
        st.write("Maximum power & priority.")
        if st.button("Select $10", key="plan_10", use_container_width=True):
            st.session_state["user_credits"] += 700
            st.success("Upgraded with 700 credits!")
            time.sleep(1)
            st.rerun()

# ==========================================
# 4. UI COMPONENTS
# ==========================================
def render_top_toolbar():
    with st.container():
        cols = st.columns([2, 1, 1, 1, 2, 1.4, 1], vertical_alignment="center")
        cols[0].markdown("### 🎬 Cinematic Studio")
        cols[1].button("📁 Project", use_container_width=True)
        cols[2].button("💾 Save", use_container_width=True)
        cols[3].button("↩️ Undo", use_container_width=True)
        cols[4].selectbox("🧠 AI Model", ["Veo 3.1 Pro", "Runway Gen-3", "Sora", "Kling"], label_visibility="collapsed")
        
        current_creds = st.session_state["user_credits"]
        if cols[5].button(f"🚀 Upgrade (Bal: {current_creds})", use_container_width=True, type="primary"):
            show_upgrade_plan_dialog()
            
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
    
    if st.session_state.get("current_video"):
        st.video(st.session_state["current_video"])
    else:
        st.info("🎥 Enter a prompt and click Generate to see your video here.") 
    
    cols = st.columns([1, 4, 1])
    cols[0].button("⏮", use_container_width=True)
    cols[1].slider("Playhead", 0, 100, 50, label_visibility="collapsed")
    cols[2].button("⏭", use_container_width=True)

def render_right_sidebar():
    st.subheader("AI Director")
    tabs = st.tabs(["Prompt", "Camera", "Extend"])
    
    with tabs[0]:
        prompt = st.text_area("Scene Description", height=150, placeholder="A cinematic wide shot of...")
        st.file_uploader("Reference Image")
        
        if st.button("✨ Generate (Cost: 50 Credits)", type="primary", use_container_width=True):
            if st.session_state["user_credits"] < 50:
                st.error("❌ Not enough credits! Please click 'Upgrade' above to top up.")
            elif prompt:
                with st.spinner("🎬 AI Director is generating your scene..."):
                    time.sleep(3) 
                    st.session_state["user_credits"] -= 50
                    st.session_state["current_video"] = "https://www.w3schools.com/html/mov_bbb.mp4"
                    st.success("Generation Complete! (-50 Credits)")
                    st.rerun()
            else:
                st.warning("Please enter a Scene Description first.")
        
    with tabs[1]:
        st.selectbox("Lens", ["24mm Wide", "35mm Standard", "50mm Portrait", "85mm Telephoto"])
        st.selectbox("Motion", ["Static", "Pan Right", "Push In", "FPV Drone"])
        
    with tabs[2]:
        st.checkbox("Maintain Character Continuity", value=True)
        st.checkbox("Maintain Environment", value=True)
        st.button("🚀 Extend (+4s)", type="primary", use_container_width=True)

# ==========================================
# 5. MAIN WORKSPACE LAYOUT
# ==========================================
render_top_toolbar()

left_col, center_col, right_col = st.columns([2.5, 5, 3.5], gap="large")

with left_col:
    render_left_sidebar()

with center_col:
    render_preview_canvas()

with right_col:
    render_right_sidebar()
