import streamlit as st
import time
import uuid
import requests
import stripe
from utils.session import init_session_state

st.set_page_config(page_title="AI Cinematic Studio", page_icon="🎬", layout="wide", initial_sidebar_state="collapsed")
init_session_state()

API_BASE = st.secrets.get("API_BASE", "http://localhost:8000")
STRIPE_SECRET_KEY = st.secrets.get("STRIPE_SECRET_KEY", "sk_test_...")

if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())
if "user_credits" not in st.session_state:
    st.session_state["user_credits"] = 1250

# ---------- Stripe Return Handler ----------
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
                add_resp = requests.post(
                    f"{API_BASE}/credits/add",
                    json={"user_id": user_id, "amount": credits_to_add, "stripe_session_id": session_id}
                )
                if add_resp.status_code == 200:
                    st.session_state["user_credits"] = add_resp.json().get("credits", 1250)
                    st.session_state[f"processed_{session_id}"] = True
                    st.query_params.clear()
                    st.success(f"✅ Added {credits_to_add} credits!")
                    st.rerun()
                else:
                    st.error("Could not sync credits. Please refresh.")
    except Exception as e:
        st.error(f"Payment verification error: {e}")
        st.query_params.clear()

st.markdown("""<style>.block-container{padding-top:1rem;max-width:98%;} header{visibility:hidden;}</style>""", unsafe_allow_html=True)

@st.dialog("💳 Secure Checkout")
def show_upgrade_dialog():
    st.write("Select your plan:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Starter Pack\n⚡ 50 Credits\n**$1.00**")
        st.link_button("Pay $1.00", "https://buy.stripe.com/your_link_1", type="primary")
    with col2:
        st.markdown("### Creator Pro\n⚡ 300 Credits\n**$5.00**")
        st.link_button("Pay $5.00", "https://buy.stripe.com/your_link_5", type="primary")
    with col3:
        st.markdown("### Studio Unlimited\n⚡ 700 Credits\n**$10.00**")
        st.link_button("Pay $10.00", "https://buy.stripe.com/your_link_10", type="primary")
    st.info("Replace links with your actual Stripe Payment Links.")

def render_top_toolbar():
    with st.container():
        cols = st.columns([2,1,1,1,2,1.4,1], vertical_alignment="center")
        cols[0].markdown("### 🎬 Cinematic Studio")
        cols[1].button("📁 Project")
        cols[2].button("💾 Save")
        cols[3].button("↩️ Undo")
        model_display = cols[4].selectbox("🧠 AI Model", ["Veo 3.1 Pro", "Runway Gen-3", "Sora", "Kling"], label_visibility="collapsed", key="model_select")
        model_map = {"Veo 3.1 Pro":"veo","Runway Gen-3":"runway","Sora":"sora","Kling":"kling"}
        st.session_state["selected_model"] = model_map.get(model_display, "veo")
        creds = st.session_state["user_credits"]
        if cols[5].button(f"🚀 Upgrade (Bal: {creds})", type="primary"):
            show_upgrade_dialog()
        cols[6].button("👤 Profile")
        st.divider()

def render_left_sidebar():
    st.subheader("Library")
    tabs = st.tabs(["Storyboard", "Assets", "Uploads"])
    with tabs[0]: st.info("Storyboard blocks appear here.")
    st.divider()
    st.subheader("🎞️ Timeline")
    st.button("+ Add Scene")
    st.button("View Render Queue")

def render_preview_canvas():
    st.subheader("Preview Canvas")
    if st.session_state.get("current_video"):
        st.video(st.session_state["current_video"])
    else:
        st.info("🎥 Enter a prompt and click Generate.")
    cols = st.columns([1,4,1])
    cols[0].button("⏮")
    cols[1].slider("Playhead",0,100,50,label_visibility="collapsed")
    cols[2].button("⏭")

def render_right_sidebar():
    st.subheader("AI Director")
    tabs = st.tabs(["Prompt", "Camera", "Extend"])
    with tabs[0]:
        prompt = st.text_area("Scene Description", height=150, placeholder="A futuristic city at sunset...")
        st.file_uploader("Reference Image")
        if st.button("✨ Generate (Cost: 50 Credits)", type="primary", use_container_width=True):
            if not prompt.strip():
                st.warning("Please enter a prompt.")
            else:
                with st.spinner("🎬 Generating..."):
                    try:
                        resp = requests.get(f"{API_BASE}/credits/{st.session_state.user_id}")
                        if resp.status_code != 200:
                            st.error("Could not check credits.")
                            st.stop()
                        if resp.json().get("credits",0) < 50:
                            st.error("❌ Not enough credits! Upgrade.")
                            st.stop()
                        gen_resp = requests.post(
                            f"{API_BASE}/ai/generate",
                            json={
                                "prompt": prompt,
                                "user_id": st.session_state.user_id,
                                "model": st.session_state.get("selected_model","veo")
                            }
                        )
                        if gen_resp.status_code == 402:
                            st.error("❌ Insufficient credits.")
                            st.stop()
                        if gen_resp.status_code != 200:
                            st.error(f"⚠️ Generation failed: {gen_resp.text}")
                            st.stop()
                        job = gen_resp.json()
                        job_id = job["job_id"]
                        st.info(f"✅ Job queued (ID: {job_id[:8]})")
                        status_widget = st.empty()
                        for i in range(60):
                            status_widget.info(f"⏳ Rendering... ({i+1}/60)")
                            time.sleep(1)
                            job_resp = requests.get(f"{API_BASE}/ai/job/{job_id}")
                            if job_resp.status_code == 200:
                                job_data = job_resp.json()
                                if job_data["status"] == "completed":
                                    st.session_state.current_video = job_data["video_url"]
                                    status_widget.success("✅ Generation complete!")
                                    break
                                elif job_data["status"] == "failed":
                                    status_widget.error("❌ Generation failed.")
                                    break
                        else:
                            status_widget.warning("⏳ Still processing. Check later.")
                        new_cred = requests.get(f"{API_BASE}/credits/{st.session_state.user_id}")
                        if new_cred.status_code == 200:
                            st.session_state.user_credits = new_cred.json().get("credits",0)
                        st.rerun()
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend not reachable. Is it running?")
                    except Exception as e:
                        st.error(f"❌ Unexpected error: {e}")
    with tabs[1]:
        st.selectbox("Lens", ["24mm","35mm","50mm","85mm"])
        st.selectbox("Motion", ["Static","Pan Right","Push In","FPV"])
    with tabs[2]:
        st.checkbox("Maintain Character Continuity", value=True)
        st.checkbox("Maintain Environment", value=True)
        st.button("🚀 Extend (+4s)", type="primary")

render_top_toolbar()
left_col, center_col, right_col = st.columns([2.5,5,3.5], gap="large")
with left_col: render_left_sidebar()
with center_col: render_preview_canvas()
with right_col: render_right_sidebar()
