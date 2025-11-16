from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def embed_texts(texts: list[str]):
    """Embed only valid, non-empty strings."""
    cleaned = [t.strip() for t in texts if t and t.strip()]

    if not cleaned:
        raise ValueError("No valid text to embed (all chunks empty).")

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=cleaned
    )
    return response.data