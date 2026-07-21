"""
openai_api.py
------------------
Thin OpenAI client wrapper, used for prompt expansion (LLM) and as one
of the pluggable Voice/Image providers.
"""
import os

try:
    from openai import OpenAI
except ImportError:  # openai package not installed yet
    OpenAI = None

_client = None


def get_client():
    global _client
    if _client is None and OpenAI is not None:
        api_key = os.getenv("OPENAI_API_KEY", "")
        _client = OpenAI(api_key=api_key) if api_key else None
    return _client


def expand_prompt_with_llm(user_prompt: str) -> str:
    """
    Optional LLM-backed version of ai_engine.prompt_builder.expand_prompt.
    Falls back to the rule-based expander if no key is configured.
    """
    client = get_client()
    if client is None:
        from ai_engine.prompt_builder import expand_prompt
        return expand_prompt(user_prompt)

    # TODO: call client.chat.completions.create(...) with a system prompt
    # instructing the model to expand `user_prompt` into a detailed,
    # production-ready video generation prompt.
    from ai_engine.prompt_builder import expand_prompt
    return expand_prompt(user_prompt)
