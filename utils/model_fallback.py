import os
import requests
from dotenv import load_dotenv
import functools
import hashlib

load_dotenv()

from config import TOGETHER_API_KEY, MODEL_PRIORITY

API_URL = "https://api.together.xyz/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

# Default model priority (edit this if you want to change defaults across app)
MODEL_PRIORITY = MODEL_PRIORITY

# Simple in-memory cache dictionary
_cache = {}

def cache_result(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = hashlib.sha256(str(args).encode() + str(kwargs).encode()).hexdigest()
        if key in _cache:
            print("[CACHE HIT]")
            return _cache[key]
        result = func(*args, **kwargs)
        _cache[key] = result
        return result
    return wrapper

@cache_result
def call_with_fallback_models(prompt: str, max_tokens: int = 300, temperature: float = 0.7, model_priority=None):
    """
    Calls Together AI models with fallback priority order.

    Args:
        prompt (str): The user input prompt.
        max_tokens (int): Maximum number of tokens to generate.
        temperature (float): Sampling temperature.
        model_priority (list): Custom model list to override default.

    Returns:
        Tuple[str, str]: (response_text, model_used)
    """
    if model_priority is None:
        model_priority = MODEL_PRIORITY

    for model in model_priority:
        print(f"[INFO] Trying model: {model}")
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=20)
            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                print(f"[SUCCESS] Model {model} responded.")
                return result["choices"][0]["message"]["content"].strip(), model
            else:
                print(f"[FAILURE] Model {model} returned unexpected result: {result}")
        except Exception as e:
            print(f"[EXCEPTION] Model {model} request failed:", str(e))

    return "All models failed to respond.", None
