from ingestion.pdf_extractor import extract_pdf
from ingestion.url_extractor import extract_url
from ingestion.text_chunker import chunk_text
from ingestion.embedder import embed_texts
from vectorstore.chroma_store import ChromaStore

class IngestionPipeline:
    def __init__(self):
        self.store = ChromaStore()

    def ingest_pdf(self, filepath: str):
        text = extract_pdf(filepath)
        chunks = chunk_text(text)
        embeddings = embed_texts(chunks)
        self.store.add(chunks, embeddings)
        return len(chunks)

    def ingest_url(self, url: str):
        text = extract_url(url)
    
        if not text or not text.strip():
            raise ValueError(f"Could not extract readable text from URL: {url}")
    
        chunks = chunk_text(text)
        chunks = [c for c in chunks if c.strip()]   # remove empty chunks
    
        if not chunks:
            raise ValueError("No valid chunks extracted from URL.")
    
        embeddings = embed_texts(chunks)
        self.store.add(chunks, embeddings)
    
        return len(chunks)

