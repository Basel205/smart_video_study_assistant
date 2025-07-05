import nltk
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')

# Load embedding model (GPU accelerated if CUDA available)
model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda" if torch.cuda.is_available() else "cpu")

def smart_chunk_text(text, min_tokens_per_chunk=1000, max_tokens_per_chunk=1500, similarity_threshold=0.7):
    sentences = nltk.sent_tokenize(text)
    embeddings = model.encode(sentences, convert_to_tensor=True)

    chunks = []
    current_chunk = [sentences[0]]
    current_length = len(sentences[0].split())

    for i in range(1, len(sentences)):
        sim = cosine_similarity([
            embeddings[i - 1].cpu().numpy(),
            embeddings[i].cpu().numpy()
        ])[0, 1]

        sentence = sentences[i]
        sentence_length = len(sentence.split())

        current_chunk.append(sentence)
        current_length += sentence_length

        if current_length >= min_tokens_per_chunk and (
            sim < similarity_threshold or current_length >= max_tokens_per_chunk
        ):
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
