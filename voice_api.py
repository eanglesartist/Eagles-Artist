"""
voice_api.py
------------------
Dispatches to the selected AI voice provider (OpenAI Voice, ElevenLabs, Google Voice).
"""
from api.providers import AI_VOICE_PROVIDERS


def generate_voice(script: str, voice: str = "narrator", provider_id: str = "openai_voice") -> dict:
    provider = AI_VOICE_PROVIDERS.get(provider_id, AI_VOICE_PROVIDERS["openai_voice"])

    if not provider["enabled"]:
        return {"status": "stub", "provider": provider["label"], "audio_url": None, "script": script, "voice": voice}

    # TODO: call the real provider SDK/REST API here.
    raise NotImplementedError(f"{provider['label']} integration not implemented yet")
