import streamlit as st
import os
import io
import requests
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
import replicate

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Creative Studio Pro", page_icon="🎬", layout="wide")

# --- SESSION STATE (init early so the step indicator can read it) ---
for key in ["generated_image", "poster_image", "video_url"]:
    if key not in st.session_state:
        st.session_state[key] = None

# --- PROFESSIONAL STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

    :root {
        --ink: #14171c;
        --ink-soft: #5c6370;
        --border: #e6e8ec;
        --accent: #0a66ff;
        --accent-dark: #0850cc;
        --bg-alt: #f6f8fa;
        --good: #0ea15a;
    }

    .block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1040px; }

    /* Brand bar */
    .brand-bar {
        display: flex; align-items: center; justify-content: space-between;
        padding: 4px 0 20px 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 28px;
    }
    .brand-name { font-size: 1.35rem; font-weight: 800; letter-spacing: -0.4px; color: var(--ink); }
    .brand-name span { color: var(--accent); }
    .brand-tag {
        font-size: 0.78rem; font-weight: 600; color: var(--good);
        background: #e8f9f0; padding: 4px 12px; border-radius: 999px;
    }

    h1 { font-weight: 800 !important; letter-spacing: -0.6px !important; color: var(--ink); }
    h2, h3 { font-weight: 700 !important; letter-spacing: -0.3px !important; color: var(--ink); }

    .lede {
        color: var(--ink-soft); font-size: 1.02rem; max-width: 680px;
        margin-bottom: 6px;
    }

    /* Step indicator */
    .step-row { display: flex; gap: 10px; margin: 18px 0 30px 0; flex-wrap: wrap; }
    .step-chip {
        display: flex; align-items: center; gap: 8px;
        padding: 8px 16px; border-radius: 999px;
        border: 1px solid var(--border); background: #fff;
        font-size: 0.85rem; font-weight: 600; color: var(--ink-soft);
    }
    .step-chip.done { color: var(--good); border-color: #bfe8d1; background: #f1fbf5; }
    .step-chip.active { color: var(--accent); border-color: #bcd6ff; background: #eef4ff; }
    .step-num {
        width: 18px; height: 18px; border-radius: 50%;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 0.7rem; background: var(--bg-alt); color: var(--ink-soft);
    }
    .step-chip.done .step-num { background: var(--good); color: #fff; }
    .step-chip.active .step-num { background: var(--accent); color: #fff; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid var(--border); }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
        color: var(--ink-soft);
    }
    .stTabs [aria-selected="true"] { color: var(--accent) !important; }

    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        border: none;
    }
    .stButton>button[kind="primary"] {
        background: var(--ink);
    }
    .stButton>button[kind="primary"]:hover {
        background: var(--accent);
    }

    /* Info / caption box */
    .caption-box {
        background: var(--bg-alt);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 16px 20px;
        font-size: 0.9rem;
        color: var(--ink-soft);
        margin-bottom: 4px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #fbfbfc;
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] h3 {
        font-size: 0.82rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--ink-soft) !important;
    }

    footer { visibility: hidden; }
    .app-footer {
        text-align: center; color: var(--ink-soft); font-size: 0.82rem;
        padding-top: 24px; border-top: 1px solid var(--border); margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🔑 API Keys")
    openai_key = st.text_input("OpenAI API Key", type="password", help="Used for image generation (DALL·E 3).")
    replicate_key = st.text_input("Replicate API Token", type="password", help="Used for turning images into video.")

    st.divider()
    st.markdown("### ⚙️ Image Settings")
    image_size = st.selectbox("Aspect ratio", ["1024x1024", "1792x1024", "1024x1792"], help="Square, landscape, or portrait.")
    image_quality = st.selectbox("Quality", ["standard", "hd"])

    st.divider()
    st.caption("Your keys are only used for this session and are never stored or logged.")

# --- BRAND BAR ---
st.markdown(
    '<div class="brand-bar">'
    '<div class="brand-name">AI Creative Studio<span>.</span></div>'
    '<div class="brand-tag">● Powered by OpenAI &amp; Replicate</div>'
    '</div>',
    unsafe_allow_html=True,
)

# --- HEADER ---
st.title("🎬 Create images, posters &amp; video")
st.markdown(
    '<p class="lede">Generate an image, add poster text, then turn it into a short video — '
    'all in one guided workflow.</p>',
    unsafe_allow_html=True,
)

# --- STEP INDICATOR ---
step1_state = "done" if st.session_state.generated_image else "active"
step2_state = "done" if st.session_state.poster_image else ("active" if st.session_state.generated_image else "")
step3_state = "done" if st.session_state.video_url else ("active" if st.session_state.poster_image or st.session_state.generated_image else "")

st.markdown(
    f"""
    <div class="step-row">
        <div class="step-chip {step1_state}"><span class="step-num">1</span> Generate image</div>
        <div class="step-chip {step2_state}"><span class="step-num">2</span> Add poster text</div>
        <div class="step-chip {step3_state}"><span class="step-num">3</span> Create video</div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["🎨  Generate Image", "✍️  Add Poster Text", "🎬  Create Video"])

# =========================================================
# TAB 1 — IMAGE GENERATION
# =========================================================
with tab1:
    prompt = st.text_area(
        "Describe the image you want:",
        value="A majestic eagle soaring over snow-capped mountains at sunset",
        height=100,
    )
    style = st.selectbox("Style", ["Photorealistic", "Digital Art", "Anime", "Oil Painting", "Minimalist"])

    if st.button("🚀 Generate Image", type="primary", use_container_width=True):
        if not openai_key:
            st.error("💡 Please enter your OpenAI API key in the sidebar.")
        elif not prompt.strip():
            st.error("Please describe the image you want first.")
        else:
            try:
                with st.spinner("Generating your image..."):
                    client = OpenAI(api_key=openai_key)
                    full_prompt = f"{prompt}, {style.lower()} style"
                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=full_prompt,
                        size=image_size,
                        quality=image_quality,
                        n=1,
                    )
                    image_url = response.data[0].url
                    img_bytes = requests.get(image_url, timeout=30).content
                    st.session_state.generated_image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                    # reset downstream state since we have a fresh base image
                    st.session_state.poster_image = None
                    st.session_state.video_url = None
                st.success("Image generated!")
            except Exception as e:
                st.error(f"Something went wrong while generating the image: {e}")

    if st.session_state.generated_image:
        st.image(st.session_state.generated_image, use_container_width=True)
        buf = io.BytesIO()
        st.session_state.generated_image.save(buf, format="PNG")
        st.download_button(
            "⬇️ Download Image", buf.getvalue(), file_name="ai_image.png", mime="image/png"
        )

# =========================================================
# TAB 2 — POSTER TEXT
# =========================================================
with tab2:
    if not st.session_state.generated_image:
        st.info("Generate an image in the first tab before adding text.")
    else:
        poster_text = st.text_input("Text to place on the image:")

        col1, col2, col3 = st.columns(3)
        with col1:
            text_color = st.color_picker("Text color", "#FFFFFF")
        with col2:
            text_size = st.slider("Font size", min_value=10, max_value=200, value=80)
        with col3:
            position = st.selectbox("Position", ["Bottom", "Center", "Top"])

        if st.button("🖌️ Apply Text to Poster", type="primary", use_container_width=True):
            if not poster_text.strip():
                st.error("Please enter the text you want on the poster.")
            else:
                try:
                    image = st.session_state.generated_image.copy()
                    draw = ImageDraw.Draw(image)

                    # Try to load a bold system font; fall back gracefully if unavailable.
                    font = None
                    for font_path in [
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                        "DejaVuSans-Bold.ttf",
                    ]:
                        try:
                            font = ImageFont.truetype(font_path, text_size)
                            break
                        except Exception:
                            continue
                    if font is None:
                        font = ImageFont.load_default()

                    bbox = draw.textbbox((0, 0), poster_text, font=font)
                    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    W, H = image.size
                    x = (W - text_w) / 2

                    if position == "Bottom":
                        y = H - text_h - 50
                    elif position == "Top":
                        y = 30
                    else:
                        y = (H - text_h) / 2

                    # Subtle drop shadow for readability, then the main text.
                    draw.text((x + 2, y + 2), poster_text, fill="#00000080", font=font)
                    draw.text((x, y), poster_text, fill=text_color, font=font)

                    st.session_state.poster_image = image
                    st.session_state.video_url = None
                    st.success("Text applied!")
                except Exception as e:
                    st.error(f"Something went wrong while adding text: {e}")

    if st.session_state.poster_image:
        st.image(st.session_state.poster_image, use_container_width=True)
        buf = io.BytesIO()
        st.session_state.poster_image.save(buf, format="PNG")
        st.download_button(
            "⬇️ Download Poster", buf.getvalue(), file_name="ai_poster.png", mime="image/png"
        )

# =========================================================
# TAB 3 — VIDEO GENERATION
# =========================================================
with tab3:
    source_image = st.session_state.poster_image or st.session_state.generated_image

    if not source_image:
        st.info("Generate an image (and optionally a poster) before creating a video.")
    else:
        st.image(source_image, caption="Source image for video", width=320)
        motion = st.select_slider("Motion strength", options=["Subtle", "Medium", "Strong"], value="Medium")

        if st.button("🎬 Generate Video", type="primary", use_container_width=True):
            if not replicate_key:
                st.error("💡 Please enter your Replicate API token in the sidebar.")
            else:
                try:
                    os.environ["REPLICATE_API_TOKEN"] = replicate_key
                    motion_map = {"Subtle": 64, "Medium": 127, "Strong": 220}

                    with st.spinner("Rendering video — this can take a minute or two..."):
                        buf = io.BytesIO()
                        source_image.save(buf, format="PNG")
                        buf.seek(0)

                        output = replicate.run(
                            "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
                            input={
                                "input_image": buf,
                                "motion_bucket_id": motion_map[motion],
                                "cond_aug": 0.02,
                            },
                        )
                        video_url = output[0] if isinstance(output, list) else output
                        st.session_state.video_url = video_url

                    st.success("Video ready!")
                except Exception as e:
                    st.error(f"Something went wrong while generating the video: {e}")

    if st.session_state.video_url:
        st.video(st.session_state.video_url)
        st.markdown(f"[⬇️ Download video]({st.session_state.video_url})")

st.markdown(
    '<div class="app-footer">© 2026 AI Creative Studio · Powered by OpenAI &amp; Replicate · Built with Streamlit</div>',
    unsafe_allow_html=True,
)
