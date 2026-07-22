"""
AI Cinematic Studio
====================
A professional Streamlit workspace for AI-assisted video generation:
prompt-to-video creation, scene extension, camera controls, and a
credit-based billing system.

Structure:
    - Configuration & constants
    - Session state helpers
    - Billing / credits logic
    - UI components (toolbar, sidebars, canvas)
    - Dialogs
    - Page assembly
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Optional

import streamlit as st

from utils.session import init_session_state
from utils.config import BASE_DIR

# ==========================================
# 1. LOGGING
# ==========================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cinematic_studio")

# ==========================================
# 2. APP CONFIGURATION & CONSTANTS
# ==========================================
APP_NAME = "AI Cinematic Studio"
APP_ICON = "🎬"

GENERATION_COST = 50
EXTENSION_COST = 25

AI_MODELS = ["Veo 3.1 Pro", "Runway Gen-3", "Sora", "Kling"]
LENS_OPTIONS = ["24mm Wide", "35mm Standard", "50mm Portrait", "85mm Telephoto"]
MOTION_OPTIONS = ["Static", "Pan Right", "Push In", "FPV Drone"]

PLACEHOLDER_VIDEO_URL = "https://www.w3schools.com/html/mov_bbb.mp4"


@dataclass(frozen=True)
class CreditPlan:
    name: str
    credits: int
    price_usd: float
    tagline: str
    key: str


CREDIT_PLANS: list[CreditPlan] = [
    CreditPlan("Starter Pack", 50, 1.00, "Ideal for quick tests.", "plan_starter"),
    CreditPlan("Creator Pro", 300, 5.00, "Best for regular editing.", "plan_creator"),
    CreditPlan("Studio Unlimited", 700, 10.00, "Maximum power & priority.", "plan_studio"),
]

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_session_state()


# ==========================================
# 3. SESSION STATE HELPERS
# ==========================================
def ensure_default_state() -> None:
    """Guarantee every key the app relies on exists before first render."""
    defaults = {
        "user_credits": 1250,
        "current_video": None,
        "project_name": "Untitled Project",
        "scenes": [],
        "last_error": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def get_credits() -> int:
    return st.session_state["user_credits"]


def has_sufficient_credits(cost: int) -> bool:
    return get_credits() >= cost


def spend_credits(cost: int) -> None:
    st.session_state["user_credits"] -= cost
    logger.info("Spent %s credits, balance now %s", cost, get_credits())


def add_credits(amount: int) -> None:
    st.session_state["user_credits"] += amount
    logger.info("Added %s credits, balance now %s", amount, get_credits())


# ==========================================
# 4. CUSTOM STYLING
# ==========================================
def inject_custom_css() -> None:
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
                max-width: 98%;
            }
            header { visibility: hidden; }

            /* Brand accent for primary buttons */
            button[kind="primary"] {
                border-radius: 8px;
            }

            /* Subtle card styling used inside dialogs */
            .plan-card {
                border: 1px solid rgba(250, 250, 250, 0.15);
                border-radius: 10px;
                padding: 1rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# 5. DIALOGS
# ==========================================
@st.dialog("🚀 Upgrade Your Plan")
def show_upgrade_plan_dialog() -> None:
    st.write("Choose a plan or top-up package to upgrade your studio capabilities:")

    columns = st.columns(len(CREDIT_PLANS))
    for column, plan in zip(columns, CREDIT_PLANS):
        with column:
            st.markdown(f"### {plan.name}")
            st.write(f"⚡ **{plan.credits} Credits**")
            st.write(f"**${plan.price_usd:.2f} / one-time**")
            st.caption(plan.tagline)
            if st.button(f"Select ${plan.price_usd:.0f}", key=plan.key, use_container_width=True):
                add_credits(plan.credits)
                st.success(f"Upgraded with {plan.credits} credits!")
                time.sleep(1)
                st.rerun()


# ==========================================
# 6. VIDEO GENERATION SERVICE (stub)
# ==========================================
def generate_video(prompt: str, reference_image=None) -> Optional[str]:
    """
    Calls the AI video generation backend.

    NOTE: This is a placeholder implementation using a sample video so the
    UI is fully demonstrable. Replace the body of this function with a
    real call to your chosen provider's API (e.g. Veo, Runway, Sora, Kling)
    before shipping to production, and surface provider errors to the user
    via `st.error` rather than letting exceptions propagate.
    """
    try:
        time.sleep(3)  # simulated latency
        return PLACEHOLDER_VIDEO_URL
    except Exception as exc:  # pragma: no cover - defensive placeholder
        logger.exception("Video generation failed")
        st.session_state["last_error"] = str(exc)
        return None


# ==========================================
# 7. UI COMPONENTS
# ==========================================
def render_top_toolbar() -> None:
    with st.container():
        cols = st.columns([2, 1, 1, 1, 2, 1.6, 1], vertical_alignment="center")

        cols[0].markdown(f"### {APP_ICON} {APP_NAME}")
        cols[1].button("📁 Project", use_container_width=True)
        cols[2].button("💾 Save", use_container_width=True)
        cols[3].button("↩️ Undo", use_container_width=True)
        cols[4].selectbox("🧠 AI Model", AI_MODELS, label_visibility="collapsed")

        if cols[5].button(
            f"🚀 Upgrade (Bal: {get_credits()})",
            use_container_width=True,
            type="primary",
        ):
            show_upgrade_plan_dialog()

        with cols[6]:
            with st.popover("👤 Profile", use_container_width=True):
                st.write(f"**{st.session_state['project_name']}**")
                st.caption(f"Credit balance: {get_credits()}")
                st.button("Sign out", use_container_width=True)

        st.divider()


def render_left_sidebar() -> None:
    st.subheader("Library")
    tabs = st.tabs(["Storyboard", "Assets", "Uploads"])

    with tabs[0]:
        if st.session_state["scenes"]:
            for idx, scene in enumerate(st.session_state["scenes"], start=1):
                st.markdown(f"**Scene {idx}** — {scene[:60]}{'…' if len(scene) > 60 else ''}")
        else:
            st.info("Visual storyboard blocks will appear here.")

    with tabs[1]:
        st.caption("Reusable assets (characters, props, locations) will appear here.")

    with tabs[2]:
        st.caption("Files you upload for reference will appear here.")

    st.divider()
    st.subheader("🎞️ Timeline")
    if st.button("+ Add Scene", use_container_width=True):
        st.session_state["scenes"].append(st.session_state.get("_last_prompt", "New scene"))
    st.button("View Render Queue", use_container_width=True)


def render_preview_canvas() -> None:
    st.subheader("Preview Canvas")

    if st.session_state.get("current_video"):
        st.video(st.session_state["current_video"])
    else:
        st.info("🎥 Enter a prompt and click Generate to see your video here.")

    cols = st.columns([1, 4, 1])
    cols[0].button("⏮", use_container_width=True)
    cols[1].slider("Playhead", 0, 100, 50, label_visibility="collapsed")
    cols[2].button("⏭", use_container_width=True)


def render_right_sidebar() -> None:
    st.subheader("AI Director")
    tabs = st.tabs(["Prompt", "Camera", "Extend"])

    with tabs[0]:
        prompt = st.text_area(
            "Scene Description",
            height=150,
            placeholder="A cinematic wide shot of...",
            key="scene_prompt",
        )
        reference_image = st.file_uploader("Reference Image")

        if st.button(f"✨ Generate (Cost: {GENERATION_COST} Credits)", type="primary", use_container_width=True):
            if not prompt or not prompt.strip():
                st.warning("Please enter a Scene Description first.")
            elif not has_sufficient_credits(GENERATION_COST):
                st.error("❌ Not enough credits! Click 'Upgrade' above to top up.")
            else:
                with st.spinner("🎬 AI Director is generating your scene..."):
                    video_url = generate_video(prompt, reference_image)

                if video_url:
                    spend_credits(GENERATION_COST)
                    st.session_state["current_video"] = video_url
                    st.session_state["_last_prompt"] = prompt
                    st.success(f"Generation complete! (-{GENERATION_COST} Credits)")
                    st.rerun()
                else:
                    st.error(
                        "Generation failed: "
                        f"{st.session_state.get('last_error', 'Unknown error.')} "
                        "Your credits were not charged."
                    )

    with tabs[1]:
        st.selectbox("Lens", LENS_OPTIONS)
        st.selectbox("Motion", MOTION_OPTIONS)

    with tabs[2]:
        st.checkbox("Maintain Character Continuity", value=True)
        st.checkbox("Maintain Environment", value=True)

        if st.button(f"🚀 Extend (+4s, Cost: {EXTENSION_COST} Credits)", type="primary", use_container_width=True):
            if not st.session_state.get("current_video"):
                st.warning("Generate a scene first before extending it.")
            elif not has_sufficient_credits(EXTENSION_COST):
                st.error("❌ Not enough credits! Click 'Upgrade' above to top up.")
            else:
                with st.spinner("Extending scene..."):
                    time.sleep(2)
                spend_credits(EXTENSION_COST)
                st.success(f"Scene extended! (-{EXTENSION_COST} Credits)")
                st.rerun()


# ==========================================
# 8. PAGE ASSEMBLY
# ==========================================
def main() -> None:
    ensure_default_state()
    inject_custom_css()
    render_top_toolbar()

    left_col, center_col, right_col = st.columns([2.5, 5, 3.5], gap="large")

    with left_col:
        render_left_sidebar()
    with center_col:
        render_preview_canvas()
    with right_col:
        render_right_sidebar()


if __name__ == "__main__":
    main()
