import time
from utils.smart_chunking import smart_chunk_text
from utils.model_fallback import call_with_fallback_models


def generate_quiz_from_text(
    text,
    chunking_enabled=True,
    model_priority=None,
    min_tokens_per_chunk=1000,
    max_tokens_per_chunk=1500,
    temperature=0.7,
    max_tokens=512
):
    """
    Generates multiple choice quiz questions from a transcript using LLMs.

    Args:
        text (str): Full transcript text.
        chunking_enabled (bool): Whether to apply smart chunking.
        model_priority (List[str]): Preferred fallback model order.
        min_tokens_per_chunk (int): Minimum tokens in a smart chunk.
        max_tokens_per_chunk (int): Maximum tokens in a smart chunk.
        temperature (float): Sampling temperature.
        max_tokens (int): Max LLM response length.

    Returns:
        List[Dict]: List of quiz items with 'chunk', 'questions', and 'model'.
    """
    print(f"[START] Quiz generation started. Chunking enabled: {chunking_enabled}")
    start_time = time.time()

    if chunking_enabled:
        chunks = smart_chunk_text(
            text,
            min_tokens_per_chunk=min_tokens_per_chunk,
            max_tokens_per_chunk=max_tokens_per_chunk
        )
        print(f"[INFO] Total smart chunks generated: {len(chunks)}")
    else:
        chunks = [text]
        print("[INFO] Using full transcript without chunking.")

    quiz_questions = []
    for i, chunk in enumerate(chunks):
        print(f"[CHUNK {i+1}/{len(chunks)}] Generating questions...")
        chunk_start = time.time()

        prompt = (
            "You are a quiz generator AI. Based on the transcript below, generate 2 to 4 multiple choice questions. "
            "Each question should have 1 correct answer and 3 plausible but incorrect options. "
            "Format strictly like this:\n\n"
            "Q1: What is ...?\nA. ...\nB. ...\nC. ...\nD. ...\nAnswer: B\n\n"
            "Keep questions fact-based and relevant to the content.\n\n"
            f"Transcript:\n{chunk}"
        )

        response, model_used = call_with_fallback_models(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            model_priority=model_priority
        )

        quiz_questions.append({
            "chunk": chunk,
            "questions": response.strip(),
            "model": model_used
        })

        print(f"[CHUNK {i+1}] Done in {time.time() - chunk_start:.2f} seconds. Model used: {model_used}")

    print(f"[END] Quiz generation completed in {time.time() - start_time:.2f} seconds.")
    return quiz_questions
