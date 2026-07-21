"""
prompt_builder.py
------------------
Turns a short, casual user prompt ("attack goat") into a detailed,
production-ready prompt for the video generation provider.

This is a rule-based stand-in for an LLM call. Swap `expand_prompt`
to call api/openai_api.py's chat completion once a real key is set,
using this template as the system prompt.
"""
import random

SUBJECT_HINTS = {
    "goat": "a realistic mountain goat",
    "eagle": "a golden eagle",
    "wolf": "a lone wolf",
    "car": "a sports car",
    "dragon": "a mythical dragon",
    "robot": "a futuristic robot",
}

ACTION_HINTS = {
    "attack": "running aggressively",
    "fly": "soaring gracefully",
    "run": "sprinting",
    "walk": "walking calmly",
    "fight": "clashing fiercely",
    "dance": "dancing rhythmically",
}

SETTINGS = [
    "through snowy mountains",
    "across a golden desert at sunset",
    "through a dense misty forest",
    "over a futuristic city skyline",
    "along a rocky coastline",
]

CAMERA_STYLES = [
    "drone camera",
    "handheld tracking shot",
    "slow dolly-in",
    "wide cinematic pan",
    "orbiting crane shot",
]

QUALITY_TAGS = ["cinematic wildlife documentary", "hyper-realistic", "epic film still", "studio quality"]
MOTION_TAGS = ["slow motion", "smooth motion", "dynamic motion"]

DEFAULT_DURATION = "8 seconds"
DEFAULT_RESOLUTION = "4K"
DEFAULT_LIGHTING = "natural lighting"


def _find_hint(word_map, prompt_lower):
    for key, value in word_map.items():
        if key in prompt_lower:
            return value
    return None


def expand_prompt(user_prompt: str, seed: int | None = None) -> str:
    """
    Expand a short prompt into a detailed, structured cinematic prompt.

    Example:
        expand_prompt("attack goat") ->
        "A realistic mountain goat running aggressively through snowy
         mountains, cinematic wildlife documentary, drone camera,
         slow motion, 8 seconds, 4K, natural lighting"
    """
    if seed is not None:
        random.seed(seed)

    prompt_lower = (user_prompt or "").lower().strip()
    if not prompt_lower:
        return ""

    subject = _find_hint(SUBJECT_HINTS, prompt_lower)
    action = _find_hint(ACTION_HINTS, prompt_lower)

    if not subject:
        # fall back to using the raw noun phrase as the subject
        subject = user_prompt.strip().capitalize()
    else:
        subject = subject[0].upper() + subject[1:]

    setting = random.choice(SETTINGS)
    camera = random.choice(CAMERA_STYLES)
    quality = random.choice(QUALITY_TAGS)
    motion = random.choice(MOTION_TAGS)

    pieces = [subject]
    if action:
        pieces.append(action)
    pieces.append(setting)

    scene = " ".join(pieces)

    detailed_prompt = (
        f"{scene}, {quality}, {camera}, {motion}, "
        f"{DEFAULT_DURATION}, {DEFAULT_RESOLUTION}, {DEFAULT_LIGHTING}"
    )
    return detailed_prompt


def build_negative_prompt() -> str:
    """Default set of things to avoid in generated clips."""
    return "blurry, low quality, distorted anatomy, watermark, text overlay"
