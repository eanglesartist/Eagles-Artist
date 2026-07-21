import streamlit as st
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Grok",
    page_icon="∅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PROFESSIONAL GROK-STYLE STYLING & ANIMATIONS ---
st.markdown("""
<style>
    /* Global Palette & Fonts */
    :root {
        --bg-main: #FFFFFF;
        --bg-sidebar: #FAFAFA;
        --border-color: #E5E7EB;
        --text-main: #0F1419;
        --text-muted: #6B7280;
        --hover-bg: #F5F5F5;
        --radius: 24px;
    }

    .stApp {
        background-color: var(--bg-main);
        color: var(--text-main);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide standard UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar Layout */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar);
        border-right: 1px solid var(--border-color);
        padding: 16px 12px;
    }

    /* Cards with Smooth Hover Animations */
    .card {
        background: #FFFFFF;
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 24px;
        transition: all 0.25s ease;
    }
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.08);
    }

    /* Floating Chat Input Bar Customization */
    .stChatInput {
        position: fixed;
        bottom: 30px;
        left: 55%;
        transform: translateX(-50%);
        width: 60% !important;
        z-index: 999;
    }
    .stChatInput textarea {
        border-radius: 999px !important;
        background: #FFFFFF !important;
        border: 1px solid #EAEAEA !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.06) !important;
        padding-left: 20px !important;
    }

    /* Navigation Links Styling */
    .nav-link {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 12px;
        border-radius: 12px;
        font-weight: 500;
        font-size: 14px;
        color: var(--text-main);
        text-decoration: none;
        transition: background 0.2s;
        margin-bottom: 4px;
    }
    .nav-link:hover {
        background-color: var(--hover-bg);
    }
</style>
""", unsafe_allow_html=True)

# --- LEFT SIDEBAR NAVIGATION ---
with st.sidebar:
    # Top Logo Header
    col_logo, col_col = st.columns([4, 1])
    with col_logo:
        st.markdown("### ∅ **Grok**")
    with col_col:
        st.markdown("«")

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation Items with Material-style representation
    st.markdown('<a class="nav-link" href="#">🔍 Search</a>', unsafe_allow_html=True)
    st.markdown('<a class="nav-link" href="#" style="background-color: #F5F5F5; font-weight: 600;">✨ New Chat</a>', unsafe_allow_html=True)
    st.markdown('<a class="nav-link" href="#">🎨 Imagine</a>', unsafe_allow_html=True)
    st.markdown('<a class="nav-link" href="#">⚡ Automations</a>', unsafe_allow_html=True)
    st.markdown('<a class="nav-link" href="#">🔌 Skills &amp; Connectors</a>', unsafe_allow_html=True)

    st.markdown("<hr style='border:0; border-top:1px solid #E5E7EB; margin:20px 0;'>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:13px; font-weight:600; color:#6B7280; padding:0 12px;'>Projects ˃</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px; font-weight:600; color:#6B7280; padding:0 12px; margin-top:10px;'>History ˃</p>", unsafe_allow_html=True)

    # User Profile at Bottom of Sidebar
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<hr style='border:0; border-top:1px solid #E5E7EB; margin:10px 0;'>", unsafe_allow_html=True)

    col_prof_img, col_prof_txt = st.columns([1, 3])
    with col_prof_img:
        st.markdown("🟠")
    with col_prof_txt:
        st.markdown("<span style='font-size:14px; font-weight:600;'>Pomodoro Lofi</span><br><span style='font-size:11px; color:#6B7280;'>ccpanel.ag@gmail.com</span>", unsafe_allow_html=True)

# --- MAIN WORKSPACE AREA ---
st.markdown("<div style='text-align: right; font-size: 14px; font-weight: 600; color: #6B7280; padding: 10px 20px;'>🔒 Private</div>", unsafe_allow_html=True)

# Center Stage Title / Logo
st.markdown("<br>", unsafe_allow_html=True)
col_lg1, col_lg2, col_lg3 = st.columns([1, 2, 1])
with col_lg2:
    st.markdown("<h1 style='text-align: center; font-size: 48px; font-weight: 700; letter-spacing: -1px;'>∅ Grok</h1>", unsafe_allow_html=True)

# --- CHAT & CONVERSATION HISTORY LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- API KEYS SETUP ACCORDION (Optional workspace control) ---
with st.expander("🔑 Configure API Keys (OpenAI & Replicate)", expanded=False):
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        openai_key = st.text_input("OpenAI API Key", type="password")
    with col_k2:
        replicate_key = st.text_input("Replicate API Token", type="password")

    if openai_key and replicate_key:
        os.environ["OPENAI_API_KEY"] = openai_key
        os.environ["REPLICATE_API_TOKEN"] = replicate_key
        st.success("API credentials loaded securely for session.")

# --- CONNECT X ACCOUNT PROMPT CARD ---
st.markdown("<br>", unsafe_allow_html=True)
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    st.markdown("""
        <div class="card" style="display: flex; align-items: center; justify-content: space-between; padding: 16px 20px;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="background: #F4F4F5; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">𝕏</div>
                <div>
                    <div style="font-weight: 600; font-size: 14px;">Connect your X account</div>
                    <div style="font-size: 13px; color: #6B7280;">Unlock early features and personalized content.</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <span style="font-size: 13px; color: #6B7280; cursor: pointer;">Dismiss</span>
                <button style="background: #000000; color: #FFFFFF; border: none; padding: 8px 18px; border-radius: 999px; font-weight: 600; cursor: pointer;">Connect</button>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- FLOATING CHAT INPUT BAR ---
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Unified generation response simulation or hookup to tools
            response_text = f"Processing your creative workspace instruction: '{prompt}'. Configure your API keys above to execute live generation models."
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# --- SUPERGROK UPGRADE WIDGET (BOTTOM RIGHT FIXED) ---
st.markdown("""
    <div style="position: fixed; bottom: 24px; right: 24px; background: #09090B; color: #FFFFFF; padding: 14px 20px; border-radius: 20px; display: flex; align-items: center; gap: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); z-index: 999;">
        <div>
            <div style="font-size: 15px; font-weight: 700;">SuperGrok</div>
            <div style="font-size: 12px; color: #A1A1AA;">Unlock extended capabilities</div>
        </div>
        <button style="background: #FFFFFF; color: #000000; border: none; padding: 8px 18px; border-radius: 999px; font-weight: 700; font-size: 13px; cursor: pointer;">Upgrade</button>
    </div>
""", unsafe_allow_html=True)
