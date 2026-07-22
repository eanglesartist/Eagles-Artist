import streamlit as st
import time
import uuid
import requests
import stripe
from utils.session import init_session_state
from utils.config import BASE_DIR

# ==========================================
# PAGE CONFIGURATION & STATE
# ==========================================
st.set_page_config(
    page_title="AI Cinematic Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)
init_session_state()

# ---------- Environment Config ----------
# Use Streamlit secrets for production, fallback to localhost for development
API_BASE = st.secrets.get("API_BASE", "http://localhost:8000")
STRIPE_SECRET_KEY = st.secrets.get("STRIPE_SECRET_KEY", "sk_test_...")

# ---------- User ID ----------
if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())

# ---------- Credits ----------
if "user_credits" not in st.session_state:
    st.session_state["user_credits"] = 1250
if "_db_synced" not in st.session_state:
    st.session_state["_db_synced"] = True

# ==========================================
# STRIPE RETURN HANDLER (Instant Credits)
# ==========================================
session_id = st.query_params.get("session_id")

if session_id and not st.session_state.get(f"processed_{session_id}"):
    try:
        stripe.api_key = STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.retrieve(session_id)

        if checkout_session.payment_status == "paid":
            user_id = st.session_state["user_id"]
            amount_total = checkout_session.amount_total / 100
            credits_map = {1.0: 50, 5.0: 300, 10.0: 700}
            credits_to_add = credits_map.get(amount_total, 0)

            if credits_to_add > 0:
                # Tell the backend to add credits (idempotent via stripe_session_id)
                add_resp = requests.post(
                    f"{API_BASE}/credits/add",
                    json={
                        "user_id": user_id,
                        "amount": credits_to_add,
                        "stripe_session_id": session_id
                    }
                )
                if add_resp.status_code == 200:
                    new_balance = add_resp.json().get("credits", 1250)
                    st.session_state["user_credits"] = new_balance
                    st.session_state[f"processed_{session_id}"] = True
                    st.query_params.clear()
                    st.success(f"✅ Payment successful! Added {credits_to_add} credits.")
                    st.rerun()
                else:
                    st.error("⚠️ Credits added but could not sync. Please refresh.")
    except Exception as e:
        st.error(f"Payment verification error: {e}")
        st.query_params.clear()

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 98%; }
        header { visibility: hidden; } 
    </style>
""", unsafe_allow_html=True)

# ==========================================
# DIALOG: STRIPE UPGRADE
# ==========================================
@st.dialog("💳 Secure Checkout ($1 - $10)")
def show_upgrade_plan_dialog():
    st.write("Select your plan. You will be redirected to secure checkout:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Starter Pack")
        st.write("⚡ **50 Credits** | **$1.00**")
        # Replace with your actual Stripe Payment Link
        st.link_button("🔗 Pay $1.00", "https://buy.stripe.com/your_link_1", type="primary")
    with col2:
        st.markdown("### Creator Pro")
        st.write("⚡ **300 Credits** | **$5.00**")
        st.link_button("🔗 Pay $5.00", "https://buy.stripe.com/your_link_5", type="primary")
    with col3:
        st.markdown("### Studio Unlimited")
        st.write("⚡ **700 Credits** | **$10.00**")
        st.link_button("🔗 Pay $10.00", "https://buy.stripe.com/your_link_10", type="primary")
    st.divider()
    st.info("💡 Replace the links with your actual Stripe Payment Links.")

# ==========================================
# UI COMPONENTS
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
            if not prompt.strip():
                st.warning("Please enter a Scene Description first.")
            else:
                with st.spinner("🎬 AI Director is generating..."):
                    try:
                        # 1. Check credits via API
                        resp = requests.get(f"{API_BASE}/credits/{st.session_state.user_id}")
                        if resp.status_code != 200:
                            st.error("Could not check credits. Try again.")
                            st.stop()
                        credits = resp.json().get("credits", 0)
                        if credits < 50:
                            st.error("❌ Not enough credits! Upgrade to continue.")
                            st.stop()
                        
                        # 2. Submit generation job
                        generate_resp = requests.post(
                            f"{API_BASE}/ai/generate",
                            json={
                                "prompt": prompt,
                                "user_id": st.session_state.user_id,
                                "model": "veo"  # or from dropdown
                            }
                        )
                        if generate_resp.status_code == 402:
                            st.error("❌ Insufficient credits (API error).")
                            st.stop()
                        if generate_resp.status_code != 200:
                            st.error(f"⚠️ Generation failed: {generate_resp.text}")
                            st.stop()
                        
                        job_data = generate_resp.json()
                        job_id = job_data["job_id"]
                        st.info(f"✅ Job queued (ID: {job_id[:8]}). Video will appear when ready.")
                        
                        # 3. Poll for completion
                        status_widget = st.empty()
                        for i in range(30):  # max 30 seconds wait
                            status_widget.info(f"⏳ Rendering... ({i+1}/30)")
                            time.sleep(1)
                            job_resp = requests.get(f"{API_BASE}/ai/job/{job_id}")
                            if job_resp.status_code == 200:
                                job = job_resp.json()
                                if job["status"] == "completed":
                                    st.session_state.current_video = job["video_url"]
                                    status_widget.success("✅ Generation complete!")
                                    break
                                elif job["status"] == "failed":
                                    status_widget.error("❌ Generation failed.")
                                    break
                            else:
                                status_widget.warning("Status check failed, but job is still running.")
                        else:
                            status_widget.warning("⏳ Still processing. Check back later.")
                        
                        # 4. Refresh credit display
                        new_cred = requests.get(f"{API_BASE}/credits/{st.session_state.user_id}")
                        if new_cred.status_code == 200:
                            st.session_state.user_credits = new_cred.json().get("credits", 0)
                        
                        st.rerun()
                        
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to backend. Is FastAPI running?")
                    except Exception as e:
                        st.error(f"❌ Unexpected error: {e}")
        
    with tabs[1]:
        st.selectbox("Lens", ["24mm Wide", "35mm Standard", "50mm Portrait", "85mm Telephoto"])
        st.selectbox("Motion", ["Static", "Pan Right", "Push In", "FPV Drone"])
        
    with tabs[2]:
        st.checkbox("Maintain Character Continuity", value=True)
        st.checkbox("Maintain Environment", value=True)
        st.button("🚀 Extend (+4s)", type="primary", use_container_width=True)

# ==========================================
# MAIN LAYOUT
# ==========================================
render_top_toolbar()
left_col, center_col, right_col = st.columns([2.5, 5, 3.5], gap="large")
with left_col:
    render_left_sidebar()
with center_col:
    render_preview_canvas()
with right_col:
    render_right_sidebar()
