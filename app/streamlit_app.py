"""Streamlit chat UI for the Sales Knowledge & CRM Agent.

Run from the project root:  streamlit run app/streamlit_app.py
"""
import os
import sys

# Make the project root importable when launched via `streamlit run app/...`.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from agent.core import build_agent, run_agent

st.set_page_config(page_title="Sales Assistant", page_icon="💼", layout="centered")
st.title("💼 Sales Knowledge & CRM Assistant")
st.caption("Ask about company policies, sales scripts, or live CRM data — one assistant, two engines.")


@st.cache_resource
def get_agent():
    return build_agent()


with st.sidebar:
    st.header("Try asking")
    st.markdown(
        """
- What is our refund policy?
- Who owns the Acme Corp lead?
- What's the deal size for Acme Corp?
- What leads does Jane Smith own?
- How should I open a cold call?
- What discount can I give without approval?
"""
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about policies, scripts, or live CRM data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, steps = run_agent(get_agent(), prompt)
        st.markdown(answer)

        if steps:
            with st.expander("🔍 Agent reasoning (tools used)"):
                for step in steps:
                    st.markdown(f"**Tool:** `{step['tool']}`")
                    st.markdown(f"**Input:** `{step['input']}`")
                    st.markdown(f"**Result:**\n\n{step['output']}")

    st.session_state.messages.append({"role": "assistant", "content": answer})
