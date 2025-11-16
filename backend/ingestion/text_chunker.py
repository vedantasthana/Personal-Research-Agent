def chunk_text(text, max_tokens=300, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    end = max_tokens

    while start < len(words):
        chunk = words[start:end]
        chunks.append(" ".join(chunk))

        start = end - overlap
        end = start + max_tokens

    return chunks
