def build_context(chunks: list[str], max_chars=6000) -> str:
    """Assemble best-ranked chunks into a single prompt with safety guard."""
    context = ""
    for c in chunks:
        if len(context) + len(c) < max_chars:
            context += c + "\n\n---\n\n"
        else:
            break

    return f"You are a helpful assistant. Use the following context:\n\n{context}\nAnswer clearly and accurately."
