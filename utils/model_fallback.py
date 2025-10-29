import os
import google.generativeai as genai
import functools
import hashlib

# Import the new key and model from config
from config import GOOGLE_API_KEY, GEMINI_MODEL

# Configure the Gemini client
if not GOOGLE_API_KEY:
    print("[ERROR] GOOGLE_API_KEY not found. Please set it in your .env file.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# Simple in-memory cache dictionary
_cache = {}

def cache_result(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Note: Caching is kept simple. Be aware of memory usage.
        key = hashlib.sha256(str(args).encode() + str(kwargs).encode()).hexdigest()
        if key in _cache:
            print("[CACHE HIT]")
            return _cache[key]
        result = func(*args, **kwargs)
        _cache[key] = result
        return result
    return wrapper

@cache_result
def call_with_fallback_models(prompt: str, max_tokens: int = 800, temperature: float = 0.7, model_priority=None):
    """
    Calls the Google Gemini API.

    Args:
        prompt (str): The user input prompt.
        max_tokens (int): Maximum number of tokens to generate.
        temperature (float): Sampling temperature.
        model_priority (list): This argument is no longer used by this function
                               but kept for compatibility with the rest of the app.

    Returns:
        Tuple[str, str]: (response_text, model_used)
    """
    
    model_name = GEMINI_MODEL # Use the model from config
    print(f"[INFO] Trying model: {model_name}")

    try:
        # Set up the generation config
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        # Initialize the model
        model = genai.GenerativeModel(model_name=model_name,
                                      generation_config=generation_config)

        # Generate content
        response = model.generate_content(prompt)

        if response.text:
            print(f"[SUCCESS] Model {model_name} responded.")
            return response.text.strip(), model_name
        else:
            print(f"[FAILURE] Model {model_name} returned an empty response.")
            return "Model returned an empty response.", model_name

    except Exception as e:
        print(f"[EXCEPTION] Model {model_name} request failed:", str(e))
        return f"An error occurred with the Gemini API: {str(e)}", None
