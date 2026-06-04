"""Tool 2: CRM Query Engine (structured).

Predefined, parameterized functions over Supabase (Postgres). We favour explicit
functions over Text-to-SQL for the MVP: deterministic, safe (no write access via the
LLM), and reliable in a demo. Fuzzy matching via ILIKE handles partial company names.
"""
from supabase import Client, create_client

from config.settings import settings
from langchain_core.tools import tool

_client: Client | None = None


def _get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(settings.supabase_url, settings.supabase_key)
    return _client


@tool
def get_lead_status(company_name: str) -> str:
    """Look up the status and owning sales rep of a lead by company name.
    Use for questions like "Who owns the Acme Corp lead?" or
    "What's the status of the Acme lead?".
    """
    res = (
        _get_client()
        .table("leads")
        .select("full_name,company_name,status,owner_rep,email")
        .ilike("company_name", f"%{company_name}%")
        .execute()
    )
    rows = res.data
    if not rows:
        return f"No lead found matching company '{company_name}'."
    lines = [
        f"- {r['full_name']} at {r['company_name']}: status='{r['status']}', "
        f"owner={r['owner_rep']}, email={r.get('email')}"
        for r in rows
    ]
    return "Matching leads:\n" + "\n".join(lines)


@tool
def get_deal_size(account_name: str) -> str:
    """Look up opportunity/deal size(s), stage, and close date for an account by name.
    Use for questions like "What is the deal size for Acme Corp?".
    """
    client = _get_client()
    accounts = (
        client.table("accounts")
        .select("id,name")
        .ilike("name", f"%{account_name}%")
        .execute()
    )
    if not accounts.data:
        return f"No account found matching '{account_name}'."

    out = []
    for acc in accounts.data:
        opps = (
            client.table("opportunities")
            .select("name,deal_size,stage,close_date,owner_rep")
            .eq("account_id", acc["id"])
            .execute()
        )
        if not opps.data:
            out.append(f"{acc['name']}: no opportunities on record.")
            continue
        for o in opps.data:
            out.append(
                f"{acc['name']} — {o['name']}: ${float(o['deal_size']):,.0f}, "
                f"stage={o['stage']}, close={o['close_date']}, owner={o['owner_rep']}"
            )
    return "\n".join(out)


@tool
def get_leads_by_rep(rep_name: str) -> str:
    """List all leads owned by a given sales rep.
    Use for questions like "What leads does Jane Smith own?".
    """
    res = (
        _get_client()
        .table("leads")
        .select("full_name,company_name,status")
        .ilike("owner_rep", f"%{rep_name}%")
        .execute()
    )
    if not res.data:
        return f"No leads found for rep '{rep_name}'."
    lines = [f"- {r['full_name']} ({r['company_name']}): {r['status']}" for r in res.data]
    return f"Leads owned by '{rep_name}':\n" + "\n".join(lines)


CRM_TOOLS = [get_lead_status, get_deal_size, get_leads_by_rep]
