"""Smoke tests for the CRM tools.

The pure tests run offline (no API keys). The integration tests hit a live, seeded
Supabase and are skipped unless RUN_INTEGRATION=1 is set.
"""
import os

import pytest

from agent.tools.crm import CRM_TOOLS, get_deal_size, get_lead_status, get_leads_by_rep

INTEGRATION = os.getenv("RUN_INTEGRATION") == "1"


def test_tools_are_registered():
    names = {t.name for t in CRM_TOOLS}
    assert names == {"get_lead_status", "get_deal_size", "get_leads_by_rep"}


def test_tools_have_descriptions():
    for tool in CRM_TOOLS:
        assert tool.description and len(tool.description) > 20


@pytest.mark.skipif(not INTEGRATION, reason="set RUN_INTEGRATION=1 with a seeded Supabase")
def test_get_lead_status_acme():
    out = get_lead_status.invoke({"company_name": "Acme"})
    assert "Acme Corp" in out


@pytest.mark.skipif(not INTEGRATION, reason="set RUN_INTEGRATION=1 with a seeded Supabase")
def test_get_deal_size_acme():
    out = get_deal_size.invoke({"account_name": "Acme"})
    assert "$" in out


@pytest.mark.skipif(not INTEGRATION, reason="set RUN_INTEGRATION=1 with a seeded Supabase")
def test_get_leads_by_rep():
    out = get_leads_by_rep.invoke({"rep_name": "Jane Smith"})
    assert "Jane Smith" in out or "Acme Corp" in out
