"""
style_engine.py
------------------
Used by "Edit Video -> Change Style" to re-style an existing clip
(e.g. anime, claymation, film noir) without changing its content.
"""

STYLE_PRESETS = {
    "cinematic": "cinematic color grade, shallow depth of field, 35mm film look",
    "anime": "anime style, cel-shaded, vibrant colors, dynamic linework",
    "claymation": "stop-motion claymation texture, tactile lighting",
    "film_noir": "black and white, high contrast, dramatic shadows, film noir style",
    "documentary": "natural lighting, handheld realism, documentary style",
    "cyberpunk": "neon-lit, futuristic cyberpunk aesthetic, rain-soaked streets",
}


def list_styles() -> list[str]:
    return list(STYLE_PRESETS.keys())


def apply_style(scene_prompt: str, style_id: str) -> str:
    style_desc = STYLE_PRESETS.get(style_id, STYLE_PRESETS["cinematic"])
    return f"{scene_prompt}, {style_desc}"
