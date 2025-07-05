import os
import torch
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from utils.model_fallback import call_with_fallback_models
from typing import List, Tuple, Dict

# Load model once (GPU if available)
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2", device="cuda" if torch.cuda.is_available() else "cpu")

def embed_texts(texts: List[str]) -> np.ndarray:
    try:
        embeddings = EMBED_MODEL.encode(texts, convert_to_tensor=True, show_progress_bar=True)
        return embeddings.cpu().numpy()
    except Exception as e:
        print(f"[ERROR] Embedding failed: {e}")
        return np.array([])

def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    try:
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        faiss.normalize_L2(embeddings)
        index.add(embeddings)
        return index
    except Exception as e:
        print(f"[ERROR] Failed to build FAISS index: {e}")
        raise

def get_top_k_chunks(question: str, transcript_chunks: List[Dict], index: faiss.IndexFlatIP, k: int = 4) -> List[Dict]:
    try:
        question_vec = EMBED_MODEL.encode([question], convert_to_tensor=True)
        question_vec = question_vec.cpu().numpy()
        faiss.normalize_L2(question_vec)

        scores, indices = index.search(question_vec, k)
        return [transcript_chunks[i] for i in indices[0]]
    except Exception as e:
        print(f"[ERROR] Retrieval failed: {e}")
        return []

def generate_rag_answer(question: str, transcript_chunks: List[Dict], model_priority=None, k=4) -> Tuple[str, List[Dict]]:
    if not transcript_chunks:
        return "Transcript is empty or not loaded.", []

    try:
        texts = [entry["text"] for entry in transcript_chunks]
        embeddings = embed_texts(texts)
        if embeddings.size == 0:
            return "Failed to embed transcript.", []

        index = build_faiss_index(embeddings)
        top_chunks = get_top_k_chunks(question, transcript_chunks, index, k=k)

        context = "\n\n".join(f"[{entry['start']:.2f}s → {entry['start'] + entry['duration']:.2f}s] {entry['text']}" for entry in top_chunks)

        prompt = (
            "You are a helpful assistant that answers questions based only on the provided transcript excerpts.\n"
            "Rules:\n"
            "- Use only the information given in the excerpts.\n"
            "- Cite timestamps in your response.\n"
            "- If the answer is unclear or missing, respond: 'The transcript does not contain a clear answer.'\n\n"
            f"Transcript Excerpts:\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )

        answer, model_used = call_with_fallback_models(prompt, model_priority=model_priority)
        return answer, top_chunks

    except Exception as e:
        print(f"[ERROR] RAG QA generation failed: {e}")
        return "An unexpected error occurred while generating the answer.", []
