"""
music_api.py
------------------
Dispatches to the selected AI music provider (Suno, Udio, AI Music API).
"""
from api.providers import AI_MUSIC_PROVIDERS


def generate_music(prompt: str, mood: str = "cinematic", provider_id: str = "suno") -> dict:
    provider = AI_MUSIC_PROVIDERS.get(provider_id, AI_MUSIC_PROVIDERS["suno"])

    if not provider["enabled"]:
        return {"status": "stub", "provider": provider["label"], "audio_url": None, "prompt": prompt, "mood": mood}

    # TODO: call the real provider SDK/REST API here.
    raise NotImplementedError(f"{provider['label']} integration not implemented yet")
