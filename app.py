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

# Ensure user credits exist in session state
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
# 3. DIALOG: BUY CREDITS POPUP
# ==========================================
@st.dialog("💳 Buy Studio Credits")
def show_buy_credits_dialog():
    st.write("Choose a credit package to power your AI video generations:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Starter")
        st.write("⚡ **500 Credits**")
        st.write("$9.99")
        if st.button("Buy 500", key="buy_500", use_container_width=True):
            st.session_state["user_credits"] += 500
            st.success("Successfully added 500 credits!")
            time.sleep(1)
            st.rerun()
            
    with col2:
        st.markdown("### Pro")
        st.write("⚡ **2,000 Credits**")
        st.write("$29.99")
        if st.button("Buy 2,000", key="buy_2000", use_container_width=True):
            st.session_state["user_credits"] += 2000
            st.success("Successfully added 2,000 credits!")
            time.sleep(1)
            st.rerun()
            
    with col3:
        st.markdown("### Studio")
        st.write("⚡ **5,000 Credits**")
        st.write("$59.99")
        if st.button("Buy 5,000", key="buy_5000", use_container_width=True):
            st.session_state["user_credits"] += 5000
            st.success("Successfully added 5,000 credits!")
            time.sleep(1)
            st.rerun()

# ==========================================
# 4. UI COMPONENTS
# ==========================================
def render_top_toolbar():
    with st.container():
        cols = st.columns([2, 1, 1, 1, 2, 1.2, 1], vertical_alignment="center")
        cols[0].markdown("### 🎬 Cinematic Studio")
        cols[1].button("📁 Project", use_container_width=True)
        cols[2].button("💾 Save", use_container_width=True)
        cols[3].button("↩️ Undo", use_container_width=True)
        cols[4].selectbox("🧠 AI Model", ["Veo 3.1 Pro", "Runway Gen-3", "Sora", "Kling"], label_visibility="collapsed")
        
        # Display live dynamic credits and a button to buy more
        current_creds = st.session_state["user_credits"]
        if cols[5].button(f"⚡ Credits: {current_creds}", use_container_width=True, type="secondary"):
            show_buy_credits_dialog()
            
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
                st.error("❌ Not enough credits! Please top up your balance.")
            elif prompt:
                with st.spinner("🎬 AI Director is generating your scene..."):
                    time.sleep(3) 
                    # Deduct 50 credits per generation
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
