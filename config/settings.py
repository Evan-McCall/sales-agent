"""Central configuration, loaded from environment / .env via pydantic-settings."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ---- LLM ----
    llm_provider: str = "anthropic"  # "anthropic" | "openai"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-6"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"

    # Embeddings always run through OpenAI (Anthropic has no embeddings endpoint).
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536

    # ---- Pinecone ----
    pinecone_api_key: str = ""
    pinecone_index: str = "sales-agent"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"

    # ---- Supabase ----
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_db_url: str = ""  # direct Postgres URI, used only for migrations/seeding

    # ---- Retrieval ----
    top_k: int = 5


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
