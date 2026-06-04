"""Smoke tests for the knowledge-base tool.

Pure tests run offline. The integration test requires a populated Pinecone index plus
an OpenAI embeddings key, and is skipped unless RUN_INTEGRATION=1 is set.
"""
import os

import pytest

from agent.tools.knowledge_base import search_knowledge_base

INTEGRATION = os.getenv("RUN_INTEGRATION") == "1"


def test_tool_metadata():
    assert search_knowledge_base.name == "search_knowledge_base"
    assert "polic" in search_knowledge_base.description.lower()


@pytest.mark.skipif(not INTEGRATION, reason="set RUN_INTEGRATION=1 with a populated Pinecone index")
def test_refund_policy_retrieval():
    out = search_knowledge_base.invoke({"query": "What is the refund window?"})
    assert "30 days" in out or "refund" in out.lower()
