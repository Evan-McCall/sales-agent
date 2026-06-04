"""Ingestion pipeline: load -> chunk -> embed -> upsert to Pinecone.

Loads every .pdf and .txt in data/documents/, chunks with overlap, embeds via OpenAI,
and upserts to Pinecone with deterministic IDs (so re-runs overwrite, not duplicate).

Run from the project root:  python -m ingestion.ingest_documents
"""
import glob
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

from agent.llm import get_embeddings
from config.settings import settings

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "documents")


def ensure_index() -> None:
    """Create the Pinecone index if it does not already exist."""
    pc = Pinecone(api_key=settings.pinecone_api_key)
    existing = [i["name"] for i in pc.list_indexes()]
    if settings.pinecone_index in existing:
        print(f"Index '{settings.pinecone_index}' already exists.")
        return
    pc.create_index(
        name=settings.pinecone_index,
        dimension=settings.embedding_dim,
        metric="cosine",
        spec=ServerlessSpec(cloud=settings.pinecone_cloud, region=settings.pinecone_region),
    )
    print(f"Created index '{settings.pinecone_index}'.")


def load_documents():
    docs = []
    for path in sorted(glob.glob(os.path.join(DOCS_DIR, "*.pdf"))):
        for d in PyPDFLoader(path).load():
            d.metadata["source"] = os.path.basename(path)
            docs.append(d)
    for path in sorted(glob.glob(os.path.join(DOCS_DIR, "*.txt"))):
        for d in TextLoader(path).load():
            d.metadata["source"] = os.path.basename(path)
            docs.append(d)
    return docs


def build_ids(chunks):
    """Deterministic chunk IDs keyed by source + page so re-ingestion overwrites."""
    ids, counters = [], {}
    for c in chunks:
        key = f"{c.metadata.get('source', 'doc')}-{c.metadata.get('page', 0)}"
        counters[key] = counters.get(key, -1) + 1
        ids.append(f"{key}-{counters[key]}")
    return ids


def main() -> None:
    ensure_index()
    docs = load_documents()
    if not docs:
        print(f"No documents found in {DOCS_DIR}. Add .pdf or .txt files and re-run.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    store = PineconeVectorStore(
        index_name=settings.pinecone_index,
        embedding=get_embeddings(),
        pinecone_api_key=settings.pinecone_api_key,
    )
    store.add_documents(chunks, ids=build_ids(chunks))
    print(f"Upserted {len(chunks)} chunks from {len(docs)} document page(s).")


if __name__ == "__main__":
    main()
