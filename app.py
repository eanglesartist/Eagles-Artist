import streamlit as st
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Creative Studio Workspace",
    page_icon="∅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS TO MATCH GROK LAYOUT ---
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #ffffff;
        color: #0f1419;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements for a clean SaaS look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #fcfcfc;
        border-right: 1px solid #eff3f4;
        padding-top: 1rem;
    }

    /* Input containers */
    .stTextInput input, .stTextArea textarea {
        background-color: #f4f4f5 !important;
        border-radius: 12px !important;
        border: 1px solid #e4e4e7 !important;
        color: #0f1419 !important;
    }

    /* Primary buttons */
    .stButton button {
        background-color: #09090b !important;
        color: white !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
        transition: transform 0.2s ease;
    }
    .stButton button:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR WORKSPACE NAVIGATION ---
with st.sidebar:
    st.markdown("### ∅ **Studio**")
    st.write("---")
    
    # Navigation Links
    st.markdown("🔍 **Search**")
    st.markdown("✨ **New Studio Session** (Active)")
    st.markdown("🎨 **Imagine & Poster**")
    st.markdown("⚡ **Automations**")
    st.markdown("🔌 **Skills & Connectors**")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("#### **Projects**")
    st.markdown("#### **History**")
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # User Profile at bottom of sidebar
    st.markdown("---")
    col_avatar, col_info = st.columns([1, 3])
    with col_avatar:
        st.markdown("🟠")
    with col_info:
        st.markdown("**Pomodoro Lofi**")
        st.caption("ccpanel.ag@gmail.com")

# --- MAIN WORKSPACE AREA ---
st.markdown("<div style='text-align: right; color: #536471; font-weight: 600; font-size: 14px;'>🔒 Private Workspace</div>", unsafe_allow_html=True)

# Centered Title / Logo Area
col_spacer1, col_center, col_spacer2 = st.columns([1, 2, 1])
with col_center:
    st.markdown("<h1 style='text-align: center; font-size: 42px; letter-spacing: -1px;'>∅ Studio</h1>", unsafe_allow_html=True)

# --- TOOL INPUT WORKSPACE ---
with st.container():
    st.markdown("### 🎨 Create Image & Poster")
    
    # API Keys Configuration (Collapsible or sidebar)
    with st.expander("🔑 API Keys Setup (OpenAI & Replicate)", expanded=False):
        openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
        replicate_key = st.text_input("Replicate API Token", type="password", placeholder="r8_...")

    # Prompt text area styled like Grok input bar
    prompt = st.text_area("What do you want to create today?", value="A majestic eagle soaring over snow-capped mountains at sunset", height=90)
    
    col_style, col_btn = st.columns([2, 1])
    with col_style:
        style_choice = st.selectbox("Style", ["Photorealistic", "Anime Linework", "Oil Painting", "Vector Logo"])
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_clicked = st.button("🚀 Generate Asset", use_container_width=True)

    if generate_clicked:
        if not openai_key or not replicate_key:
            st.warning("⚠️ Please provide your API keys in the setup section above to begin generating assets.")
        else:
            os.environ["OPENAI_API_KEY"] = openai_key
            os.environ["REPLICATE_API_TOKEN"] = replicate_key
            st.info("🔄 Connecting to AI models... Processing your request.")
            # Generation logic goes here

# --- CONNECT X ACCOUNT BANNER ---
st.markdown("<br>", unsafe_allow_html=True)
col_banner_spacer1, col_banner_center, col_banner_spacer2 = st.columns([1, 2, 1])
with col_banner_center:
    st.markdown("""
        <div style="border: 1px solid #eff3f4; border-radius: 16px; padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; background: #fafafa;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="font-size: 20px; font-weight: bold; background: #f4f4f5; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">𝕏</div>
                <div>
                    <div style="font-weight: 600; font-size: 14px;">Connect your 𝕏 account</div>
                    <div style="font-size: 12px; color: #536471;">Unlock early features and personalized content.</div>
                </div>
            </div>
            <div>
                <button style="background: #000; color: #fff; border: none; padding: 6px 16px; border-radius: 50px; font-weight: 600; cursor: pointer;">Connect</button>
            </div>
        </div>
    """, unsafe_allow_html=True)
