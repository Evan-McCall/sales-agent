"""Tool 1: Knowledge Base Retriever (unstructured).

Semantic search over policies, sales scripts, and product docs stored in Pinecone.
"""
from langchain_core.tools import tool
from langchain_pinecone import PineconeVectorStore

from agent.llm import get_embeddings
from config.settings import settings

_vectorstore = None


def _get_vectorstore() -> PineconeVectorStore:
    """Lazily build (and cache) the Pinecone-backed vector store."""
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = PineconeVectorStore(
            index_name=settings.pinecone_index,
            embedding=get_embeddings(),
        )
    return _vectorstore


@tool
def search_knowledge_base(query: str) -> str:
    """Search the company knowledge base for policies, sales scripts, procedures,
    product documentation, and any "how do I" / "what is our policy on" question.
    Returns the most relevant document excerpts, each labelled with its source.
    """
    docs = _get_vectorstore().similarity_search(query, k=settings.top_k)
    if not docs:
        return "No relevant documents found in the knowledge base."

    chunks = []
    for d in docs:
        source = d.metadata.get("source", "unknown")
        page = d.metadata.get("page")
        location = source if page is None else f"{source} (p.{int(page) + 1})"
        chunks.append(f"[Source: {location}]\n{d.page_content}")
    return "\n\n---\n\n".join(chunks)
