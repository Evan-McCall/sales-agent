"""Dual-engine tool-calling agent assembly.

Binds the knowledge-base tool and the CRM tools to the chat model and lets the LLM
route each query to the right engine.
"""
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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


def build_agent() -> AgentExecutor:
    llm = get_llm(temperature=0)
    tools = [search_knowledge_base, *CRM_TOOLS]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        return_intermediate_steps=True,
        verbose=True,
    )
