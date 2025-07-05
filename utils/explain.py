import os
import requests
from dotenv import load_dotenv
from utils.model_fallback import call_with_fallback_models

load_dotenv()

def explain_text_eli5(text, temperature=0.7, max_tokens=800, model_priority=None):
    """
    Generates a simplified explanation of the input text using LLMs.
    The explanation is designed for a 10-year-old while retaining key ideas.

    Args:
        text (str): Input text to explain.
        temperature (float): Sampling temperature.
        max_tokens (int): Max tokens for LLM output.
        model_priority (list): Optional list of preferred models (in order).

    Returns:
        Tuple[str, str]: Explanation string and the model used.
    """
    prompt = (
        "Explain the following text in very simple terms a curious 10-year-old can understand. "
        "Use easy language but retain all important concepts, facts, and context:\n\n"
        f"{text}"
    )

    explanation, model_used = call_with_fallback_models(
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        model_priority=model_priority
    )

    return explanation, model_used
