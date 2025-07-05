import textwrap
from utils.model_fallback import call_with_fallback_models


def generate_timestamped_summaries(transcript, chunk_duration=90, temperature=0.7, max_tokens=400, model_priority=None):
    """
    Generate summaries for each time-based chunk of the transcript.

    Args:
        transcript (list): List of transcript entries with start, duration, and text.
        chunk_duration (int): Max duration (in seconds) per chunk.
        temperature (float): Sampling temperature.
        max_tokens (int): Max tokens to allow per summary generation.
        model_priority (list): Ordered list of preferred models.

    Returns:
        list: List of summaries with timestamps and models used.
    """
    summaries = []
    current_chunk = []
    current_start = None
    current_time = 0

    for entry in transcript:
        if current_start is None:
            current_start = entry["start"]

        current_chunk.append(entry["text"])
        current_time += entry["duration"]

        if current_time >= chunk_duration:
            chunk_text = " ".join(current_chunk)
            prompt = (
                "Summarize the following transcript segment in 2-3 short, clear sentences. "
                "Use simple language, but retain important ideas and terms:\n\n"
                f"{chunk_text}"
            )

            summary, model_used = call_with_fallback_models(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                model_priority=model_priority
            )

            summaries.append({
                "start": current_start,
                "end": entry["start"] + entry["duration"],
                "summary": summary.strip(),
                "model": model_used
            })

            current_chunk = []
            current_time = 0
            current_start = None

    # Handle the last chunk
    if current_chunk:
        chunk_text = " ".join(current_chunk)
        prompt = (
            "Summarize the following transcript segment in 2-3 short, clear sentences. "
            "Use simple language, but retain important ideas and terms:\n\n"
            f"{chunk_text}"
        )

        summary, model_used = call_with_fallback_models(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            model_priority=model_priority
        )

        summaries.append({
            "start": current_start,
            "end": transcript[-1]["start"] + transcript[-1]["duration"],
            "summary": summary.strip(),
            "model": model_used
        })

    return summaries


def generate_full_summary(transcript, temperature=0.7, max_tokens=1024, model_priority=None):
    """
    Generate a single full-context summary from the entire transcript.

    Args:
        transcript (list): List of transcript entries.
        temperature (float): Sampling temperature.
        max_tokens (int): Max tokens to generate.
        model_priority (list): Optional fallback list of LLMs.

    Returns:
        tuple: Summary string and the model used.
    """
    full_text = " ".join([entry["text"] for entry in transcript])

    prompt = (
        "Provide a detailed and clear summary of the full video transcript below. "
        "Use concise language and include all key events, explanations, and terminology:\n\n"
        f"{full_text}"
    )

    summary, model_used = call_with_fallback_models(
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        model_priority=model_priority
    )

    return summary.strip(), model_used
