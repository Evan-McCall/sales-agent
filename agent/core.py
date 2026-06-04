"""Dual-engine tool-calling agent assembly (LangChain 1.x / LangGraph).

Binds the knowledge-base tool and the CRM tools to the chat model and lets the LLM
route each query to the right engine.
"""
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, ToolMessage

from agent.llm import get_llm
from agent.tools.crm import CRM_TOOLS
from agent.tools.knowledge_base import search_knowledge_base

SYSTEM_PROMPT = """You are a Sales Assistant for the sales team. You help reps get \
fast, accurate answers without breaking their workflow.

You have two kinds of tools:
1. Knowledge base search — company policies, sales scripts, procedures, product docs.
2. CRM tools — live data about leads, accounts, deal sizes, and lead owners.

Rules:
- ALWAYS use a tool to answer factual questions. Never invent CRM data or policy details.
- For policy / script / "how do I" questions, use the knowledge base tool and cite the
  source document in your answer.
- For questions about specific leads, accounts, deals, owners, or statuses, use the CRM tools.
- If a tool returns no result, say so plainly — do not guess.
- A question may need more than one tool; use as many as needed before answering.
- Keep answers concise and rep-friendly.
"""


def build_agent():
    """Build the compiled LangGraph agent with both engines bound."""
    llm = get_llm(temperature=0)
    tools = [search_knowledge_base, *CRM_TOOLS]
    return create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)


def _text(content) -> str:
    """Normalize message content (Anthropic may return a list of content blocks)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "") for block in content if isinstance(block, dict)
        )
    return str(content)


def run_agent(agent, query: str, chat_history=None):
    """Invoke the agent and return (answer, steps).

    steps is a list of {"tool", "input", "output"} dicts for UI display.
    """
    messages = list(chat_history or []) + [{"role": "user", "content": query}]
    result = agent.invoke({"messages": messages})
    msgs = result["messages"]

    # Map tool_call_id -> tool output so each call can be paired with its result.
    outputs = {m.tool_call_id: _text(m.content) for m in msgs if isinstance(m, ToolMessage)}

    steps = []
    for m in msgs:
        if isinstance(m, AIMessage):
            for call in m.tool_calls or []:
                steps.append(
                    {
                        "tool": call["name"],
                        "input": call["args"],
                        "output": outputs.get(call["id"], ""),
                    }
                )

    answer = _text(msgs[-1].content)
    return answer, steps
