def build_context(chunks: list[str]) -> str:
    """
    Build a formatted block of context to pass into the LLM prompt.
    """
    if not chunks:
        return "No relevant context found."

    body = "\n\n----\n\n".join(chunks)

    return (
        "You are an assistant that answers strictly using the provided context.\n"
        "If the answer is not found in the context, say 'I don't know.'\n\n"
        f"Context:\n{body}\n\n"
    )
