"""
AI Multi-Creative Studio — Pro
--------------------------------
Generate AI images (OpenAI DALL-E or Replicate), design posters with
custom text overlays, and export finished artwork — all in one Streamlit app.

Requirements (requirements.txt):
    streamlit>=1.32
    openai>=1.14
    replicate>=0.25
    pillow>=10.0
    requests>=2.31

Run:
    streamlit run app.py
"""

import io
import time

import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Optional SDKs — imported lazily so the app still loads if a package is missing.
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import replicate
except ImportError:
    replicate = None


# ----------------------------------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Multi-Creative Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# STYLE
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main .block-container { padding-top: 2rem; max-width: 1100px; }
    h1, h2, h3 { font-weight: 700; }
    .stButton>button {
        border-radius: 999px;
        padding: 0.6rem 1.6rem;
        font-weight: 600;
        border: none;
    }
    .studio-card {
        background: rgba(127,127,127,0.06);
        border: 1px solid rgba(127,127,127,0.15);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
    }
    .studio-caption { color: rgba(127,127,127,0.9); font-size: 0.85rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------
defaults = {
    "generated_image": None,   # PIL.Image of the latest AI-generated art
    "poster_image": None,      # PIL.Image after text overlay
    "generated_video": None,   # bytes of the latest generated video clip
    "history": [],             # list of (label, PIL.Image) for this session
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ----------------------------------------------------------------------------
# SIDEBAR — API KEYS & SETTINGS
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    st.markdown("**OpenAI API Key**")
    openai_key = st.text_input(
        "OpenAI API Key", type="password", label_visibility="collapsed",
        placeholder="sk-...",
    )

    st.markdown("**Replicate API Token**")
    replicate_key = st.text_input(
        "Replicate API Token", type="password", label_visibility="collapsed",
        placeholder="r8_...",
    )

    st.divider()

    engine = st.radio(
        "Image generation engine",
        options=["OpenAI (DALL-E 3)", "Replicate (SDXL)"],
        index=0,
    )

    image_size = st.selectbox(
        "Image size",
        options=["1024x1024", "1024x1792", "1792x1024"],
        index=0,
        help="Only applies to OpenAI DALL-E 3.",
    )

    st.divider()
    st.caption(
        "API keys are used only for this session and are never stored or logged."
    )


def keys_ready(require_openai=False, require_replicate=False) -> bool:
    """Validate that the necessary API credentials are present."""
    if require_openai and not openai_key:
        st.error("💡 Please enter your OpenAI API key in the sidebar to continue.")
        return False
    if require_replicate and not replicate_key:
        st.error("💡 Please enter your Replicate API token in the sidebar to continue.")
        return False
    return True


# ----------------------------------------------------------------------------
# GENERATION HELPERS
# ----------------------------------------------------------------------------
def generate_with_openai(prompt: str, size: str) -> Image.Image:
    if OpenAI is None:
        raise RuntimeError("The 'openai' package is not installed.")
    client = OpenAI(api_key=openai_key)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    img_bytes = requests.get(image_url, timeout=60).content
    return Image.open(io.BytesIO(img_bytes)).convert("RGBA")


def generate_with_replicate(prompt: str) -> Image.Image:
    if replicate is None:
        raise RuntimeError("The 'replicate' package is not installed.")
    client = replicate.Client(api_token=replicate_key)
    output = client.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08",
        input={"prompt": prompt},
    )
    image_url = output[0] if isinstance(output, list) else output
    img_bytes = requests.get(image_url, timeout=60).content
    return Image.open(io.BytesIO(img_bytes)).convert("RGBA")


def add_text_to_image(
    base_image: Image.Image,
    text: str,
    color: str,
    font_size: int,
    position: str,
    stroke: bool,
) -> Image.Image:
    img = base_image.copy().convert("RGBA")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    if not text:
        return img

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    margin = int(img.width * 0.05)

    positions = {
        "Top": ((img.width - text_w) / 2, margin),
        "Center": ((img.width - text_w) / 2, (img.height - text_h) / 2),
        "Bottom": ((img.width - text_w) / 2, img.height - text_h - margin),
    }
    xy = positions.get(position, positions["Bottom"])

    draw.text(
        xy,
        text,
        font=font,
        fill=color,
        stroke_width=max(2, font_size // 25) if stroke else 0,
        stroke_fill="#000000",
    )
    return img


def to_png_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="PNG")
    return buf.getvalue()


def _resolve_replicate_url(output) -> str:
    """Normalize a Replicate prediction output into a single media URL."""
    if isinstance(output, list):
        output = output[0]
    # Newer replicate SDKs return a FileOutput object with a .url attribute.
    return getattr(output, "url", output)


def animate_image_to_video(image: Image.Image, motion_strength: int) -> bytes:
    """Turn a still image into a short video clip using Stable Video Diffusion."""
    if replicate is None:
        raise RuntimeError("The 'replicate' package is not installed.")
    client = replicate.Client(api_token=replicate_key)

    buf = io.BytesIO()
    image.convert("RGB").save(buf, format="PNG")
    buf.seek(0)

    output = client.run(
        "stability-ai/stable-video-diffusion:"
        "3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172dc",
        input={
            "input_image": buf,
            "motion_bucket_id": motion_strength,
            "frames_per_second": 6,
            "cond_aug": 0.02,
        },
    )
    video_url = _resolve_replicate_url(output)
    return requests.get(video_url, timeout=120).content


def generate_video_from_text(prompt: str) -> bytes:
    """Generate a short video clip directly from a text prompt."""
    if replicate is None:
        raise RuntimeError("The 'replicate' package is not installed.")
    client = replicate.Client(api_token=replicate_key)

    output = client.run(
        "minimax/video-01",
        input={"prompt": prompt},
    )
    video_url = _resolve_replicate_url(output)
    return requests.get(video_url, timeout=120).content


# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.title("🎬 AI Multi-Creative Studio")
st.markdown(
    "Create images, design posters, and export finished artwork — all in one place."
)

tab_generate, tab_poster, tab_video, tab_history = st.tabs(
    ["🎨 Generate Image", "✍️ Poster Editor", "🎥 Video Creator", "🕘 History"]
)

# ----------------------------------------------------------------------------
# TAB 1 — IMAGE GENERATION
# ----------------------------------------------------------------------------
with tab_generate:
    st.markdown('<div class="studio-card">', unsafe_allow_html=True)
    st.subheader("1. Describe your image")
    prompt = st.text_area(
        "Prompt",
        value="A majestic eagle soaring over snow-capped mountains at sunrise, cinematic lighting",
        height=110,
        label_visibility="collapsed",
    )
    st.markdown(
        f'<span class="studio-caption">Engine: {engine}</span>',
        unsafe_allow_html=True,
    )

    generate_clicked = st.button("🚀 Generate Image", use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)

    if generate_clicked:
        needs_openai = engine.startswith("OpenAI")
        needs_replicate = engine.startswith("Replicate")

        if not prompt.strip():
            st.error("Please enter a description for your image.")
        elif keys_ready(require_openai=needs_openai, require_replicate=needs_replicate):
            with st.spinner("Generating your art... this can take up to a minute."):
                try:
                    if needs_openai:
                        image = generate_with_openai(prompt, image_size)
                    else:
                        image = generate_with_replicate(prompt)

                    st.session_state.generated_image = image
                    st.session_state.history.insert(0, (prompt[:60], image))
                    st.success("✅ Image generated! Head to the Poster Editor tab to add text.")
                except Exception as exc:
                    st.error(f"Generation failed: {exc}")

    if st.session_state.generated_image is not None:
        st.image(
            st.session_state.generated_image,
            caption="Latest generated image",
            use_container_width=True,
        )
        st.download_button(
            "⬇️ Download image",
            data=to_png_bytes(st.session_state.generated_image),
            file_name=f"ai-image-{int(time.time())}.png",
            mime="image/png",
        )

# ----------------------------------------------------------------------------
# TAB 2 — POSTER EDITOR
# ----------------------------------------------------------------------------
with tab_poster:
    if st.session_state.generated_image is None:
        st.info("Generate an image in the first tab, then come back here to add text.")
    else:
        st.markdown('<div class="studio-card">', unsafe_allow_html=True)
        st.subheader("2. Add text to your poster")

        poster_text = st.text_input("Poster text", value="")

        col1, col2, col3 = st.columns(3)
        with col1:
            text_color = st.color_picker("Text color", "#FFFFFF")
        with col2:
            text_size = st.slider("Font size", min_value=10, max_value=200, value=80)
        with col3:
            text_position = st.selectbox("Position", ["Top", "Center", "Bottom"], index=2)

        stroke = st.checkbox("Add outline for readability", value=True)

        apply_clicked = st.button("🖌 Apply Text")
        st.markdown("</div>", unsafe_allow_html=True)

        if apply_clicked:
            st.session_state.poster_image = add_text_to_image(
                st.session_state.generated_image,
                poster_text,
                text_color,
                text_size,
                text_position,
                stroke,
            )
            st.session_state.history.insert(0, (f"Poster: {poster_text[:40]}", st.session_state.poster_image))

        display_image = st.session_state.poster_image or st.session_state.generated_image
        st.image(display_image, caption="Poster preview", use_container_width=True)
        st.download_button(
            "⬇️ Download poster",
            data=to_png_bytes(display_image),
            file_name=f"ai-poster-{int(time.time())}.png",
            mime="image/png",
        )

# ----------------------------------------------------------------------------
# TAB 3 — VIDEO CREATOR
# ----------------------------------------------------------------------------
with tab_video:
    st.markdown('<div class="studio-card">', unsafe_allow_html=True)
    st.subheader("3. Turn your artwork into a video")

    video_mode = st.radio(
        "Mode",
        options=["Animate my image", "Create from text"],
        horizontal=True,
        help=(
            "Animate: brings your generated image to life with motion. "
            "Create: generates a new clip directly from a text description."
        ),
    )

    if video_mode == "Animate my image":
        if st.session_state.generated_image is None:
            st.info("Generate an image in the first tab first — this mode animates it.")
        else:
            st.image(
                st.session_state.poster_image or st.session_state.generated_image,
                caption="Source frame",
                width=320,
            )
            motion_strength = st.slider(
                "Motion strength", min_value=1, max_value=255, value=127,
                help="Higher values add more movement to the clip.",
            )
            video_clicked = st.button("🎬 Animate Image")

            if video_clicked:
                if keys_ready(require_replicate=True):
                    with st.spinner("Animating your image... this can take a few minutes."):
                        try:
                            source = st.session_state.poster_image or st.session_state.generated_image
                            video_bytes = animate_image_to_video(source, motion_strength)
                            st.session_state.generated_video = video_bytes
                            st.success("✅ Video ready below.")
                        except Exception as exc:
                            st.error(f"Video generation failed: {exc}")

    else:  # Create from text
        video_prompt = st.text_area(
            "Describe your video",
            value="A cozy coffee shop at sunrise, steam rising from a cup, warm cinematic light",
            height=100,
            help="You can describe scenes, characters, camera movement, and mood.",
        )
        video_clicked = st.button("🎬 Create Video")

        if video_clicked:
            if not video_prompt.strip():
                st.error("Please describe the video you want to create.")
            elif keys_ready(require_replicate=True):
                with st.spinner("Creating your video... this can take a few minutes."):
                    try:
                        video_bytes = generate_video_from_text(video_prompt)
                        st.session_state.generated_video = video_bytes
                        st.success("✅ Video ready below.")
                    except Exception as exc:
                        st.error(f"Video generation failed: {exc}")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.generated_video is not None:
        st.video(st.session_state.generated_video)
        st.download_button(
            "⬇️ Download video",
            data=st.session_state.generated_video,
            file_name=f"ai-video-{int(time.time())}.mp4",
            mime="video/mp4",
        )

# ----------------------------------------------------------------------------
# TAB 4 — HISTORY
# ----------------------------------------------------------------------------
with tab_history:
    st.subheader("Session history")
    if not st.session_state.history:
        st.caption("Nothing generated yet this session.")
    else:
        cols = st.columns(3)
        for i, (label, img) in enumerate(st.session_state.history):
            with cols[i % 3]:
                st.image(img, caption=label, use_container_width=True)

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.divider()
st.caption("Powered by OpenAI • Replicate • Streamlit — © 2026 AI Creative Studio")
