"""
providers.py
------------------
Central registry of pluggable AI providers per category, shown in the
UI's provider dropdowns (components/ai_panel.py, voice_panel.py, etc).

Add a real API key in .env and flip `enabled` once a provider is wired
up in its corresponding api/*.py module.
"""

AI_VIDEO_PROVIDERS = {
    "google_veo": {"label": "Google Veo", "env_key": "VIDEO_AI_GOOGLE_VEO_KEY", "enabled": False},
    "openai_video": {"label": "OpenAI Video", "env_key": "VIDEO_AI_OPENAI_KEY", "enabled": False},
    "runway": {"label": "Runway", "env_key": "VIDEO_AI_RUNWAY_KEY", "enabled": False},
    "kling": {"label": "Kling AI", "env_key": "VIDEO_AI_KLING_KEY", "enabled": False},
    "pika": {"label": "Pika", "env_key": "VIDEO_AI_PIKA_KEY", "enabled": False},
}

AI_IMAGE_PROVIDERS = {
    "openai_image": {"label": "OpenAI Image", "env_key": "IMAGE_AI_OPENAI_KEY", "enabled": False},
    "midjourney": {"label": "Midjourney", "env_key": "IMAGE_AI_MIDJOURNEY_KEY", "enabled": False},
    "flux": {"label": "Flux", "env_key": "IMAGE_AI_FLUX_KEY", "enabled": False},
}

AI_VOICE_PROVIDERS = {
    "openai_voice": {"label": "OpenAI Voice", "env_key": "VOICE_AI_OPENAI_KEY", "enabled": False},
    "elevenlabs": {"label": "ElevenLabs", "env_key": "VOICE_AI_ELEVENLABS_KEY", "enabled": False},
    "google_voice": {"label": "Google Voice", "env_key": "VOICE_AI_GOOGLE_KEY", "enabled": False},
}

AI_MUSIC_PROVIDERS = {
    "suno": {"label": "Suno", "env_key": "MUSIC_AI_SUNO_KEY", "enabled": False},
    "udio": {"label": "Udio", "env_key": "MUSIC_AI_UDIO_KEY", "enabled": False},
    "ai_music_api": {"label": "AI Music API", "env_key": "MUSIC_AI_GENERIC_KEY", "enabled": False},
}


def provider_labels(category: dict) -> list[str]:
    return [v["label"] for v in category.values()]


def provider_id_from_label(category: dict, label: str) -> str | None:
    for key, v in category.items():
        if v["label"] == label:
            return key
    return None
