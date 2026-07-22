import streamlit as st
import time
import uuid
import stripe
from utils.session import init_session_state
from utils.config import BASE_DIR
from utils.db import init_db, get_or_create_user, get_user_credits, deduct_credits, add_credits

# ==========================================
# 1. PAGE CONFIGURATION & STATE
# ==========================================
st.set_page_config(
    page_title="AI Cinematic Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database tables
init_db()

# Initialize session state
init_session_state()

# Ensure a unique user ID for this browser session (acts as a "guest" login)
if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())

# Load credits from DB into session state (sync)
if "user_credits" not in st.session_state or st.session_state.get("_db_synced") is None:
    st.session_state["user_credits"] = get_or_create_user(st.session_state["user_id"])
    st.session_state["_db_synced"] = True

# ==========================================
# 2. STRIPE RETURN URL HANDLER (Instant Credits)
# ==========================================
# Retrieve session_id from URL parameters
session_id = st.query_params.get("session_id")

if session_id and not st.session_state.get(f"processed_{session_id}"):
    try:
        # Load Stripe secret key from secrets
        stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
        
        # Verify payment status with Stripe
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        
        if checkout_session.payment_status == "paid":
            user_id = st.session_state["user_id"]
            
            # Determine credits based on amount paid (in dollars)
            amount_total = checkout_session.amount_total / 100
            credits_map = {1.0: 50, 5.0: 300, 10.0: 700}
            credits_to_add = credits_map.get(amount_total, 0)
            
            if credits_to_add > 0:
                # Update DB and session state
                new_balance = add_credits(user_id, credits_to_add, session_id)
                st.session_state["user_credits"] = new_balance
                st.session_state[f"processed_{session_id}"] = True
                
                # Remove query param to avoid reprocessing on next rerun
                st.query_params.clear()
                
                st.success(f"✅ Payment successful! Added {credits_to_add} credits. New balance: {new_balance}")
                st.rerun()  # Force refresh to update UI
    except Exception as e:
        st.error(f"Payment verification failed: {e}")
        st.query_params.clear()

# ==========================================
# 3. CUSTOM CSS INJECTION
# ==========================================
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 98%; }
        header { visibility: hidden; } 
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. DIALOG: STRIPE PAYMENT LINKS POPUP
# ==========================================
@st.dialog("💳 Secure Checkout ($1 - $10)")
def show_upgrade_plan_dialog():
    st.write("Select your plan. You will be redirected to secure checkout:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Starter Pack")
        st.write("⚡ **50 Credits**")
        st.write("**$1.00**")
        # st.link_button opens the URL in a new tab, preserving your Streamlit app
        st.link_button("🔗 Pay $1.00", "https://buy.stripe.com/your_actual_link_1", type="primary")
            
    with col2:
        st.markdown("### Creator Pro")
        st.write("⚡ **300 Credits**")
        st.write("**$5.00**")
        st.link_button("🔗 Pay $5.00", "https://buy.stripe.com/your_actual_link_5", type="primary")
            
    with col3:
        st.markdown("### Studio Unlimited")
        st.write("⚡ **700 Credits**")
        st.write("**$10.00**")
        st.link_button("🔗 Pay $10.00", "https://buy.stripe.com/your_actual_link_10", type="primary")
        
    st.divider()
    st.info("💡 Make sure your Stripe Payment Links have the 'Return URL' set to your app's URL (e.g., https://yourapp.com) so users are redirected back.")

# ==========================================
# 5. UI COMPONENTS
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
    
    # Use a local sample video or the hardcoded one as fallback
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
            # Deduct from database
            user_id = st.session_state["user_id"]
            success, new_balance = deduct_credits(user_id, 50)
            
            if not success:
                st.error("❌ Not enough credits! Please click 'Upgrade' above to top up.")
            elif not prompt.strip():
                st.warning("Please enter a Scene Description first.")
                # Refund the credits since we deducted but didn't generate
                # (In real app, you might check prompt before deduction)
                add_credits(user_id, 50) 
                st.session_state["user_credits"] = get_user_credits(user_id)
            else:
                with st.spinner("🎬 AI Director is generating your scene..."):
                    time.sleep(3)  # Simulate generation
                    # Update session state with new balance
                    st.session_state["user_credits"] = new_balance
                    # Set a video (you can replace this with your local video file)
                    st.session_state["current_video"] = "https://www.w3schools.com/html/mov_bbb.mp4"
                    st.success(f"✅ Generation complete! (-50 Credits) Remaining: {new_balance}")
                    # No st.rerun() needed – the UI will update on next interaction
                    # But we force a rerun to update the balance in the top bar immediately
                    st.rerun()
        
    with tabs[1]:
        st.selectbox("Lens", ["24mm Wide", "35mm Standard", "50mm Portrait", "85mm Telephoto"])
        st.selectbox("Motion", ["Static", "Pan Right", "Push In", "FPV Drone"])
        
    with tabs[2]:
        st.checkbox("Maintain Character Continuity", value=True)
        st.checkbox("Maintain Environment", value=True)
        st.button("🚀 Extend (+4s)", type="primary", use_container_width=True)

# ==========================================
# 6. MAIN WORKSPACE LAYOUT
# ==========================================
render_top_toolbar()

left_col, center_col, right_col = st.columns([2.5, 5, 3.5], gap="large")

with left_col:
    render_left_sidebar()

with center_col:
    render_preview_canvas()

with right_col:
    render_right_sidebar()
