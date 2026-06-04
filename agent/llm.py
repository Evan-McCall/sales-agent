"""LLM and embedding factories. Swap the chat model via LLM_PROVIDER in .env.

Default chat model: Claude Sonnet 4.6 (claude-sonnet-4-6).
Embeddings always use OpenAI — Anthropic has no embeddings endpoint.
"""
from config.settings import settings


def get_llm(temperature: float = 0):
    """Return the chat model used by the agent."""
    if settings.llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=settings.anthropic_model,
            temperature=temperature,
            api_key=settings.anthropic_api_key,
        )

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=settings.openai_model,
        temperature=temperature,
        api_key=settings.openai_api_key,
    )


def get_embeddings():
    """Return the embedding model. Always OpenAI for now (see module docstring)."""
    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )
