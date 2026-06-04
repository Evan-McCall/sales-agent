"""Seed Supabase with stubbed CRM data.

Run from the project root:  python -m db.seed
(Re-running wipes and re-inserts for a clean slate.)
"""
from supabase import create_client

from config.settings import settings

client = create_client(settings.supabase_url, settings.supabase_key)

ACCOUNTS = [
    {"name": "Acme Corp", "industry": "Manufacturing", "region": "West"},
    {"name": "Globex", "industry": "Energy", "region": "East"},
    {"name": "Initech", "industry": "Software", "region": "West"},
    {"name": "Umbrella Health", "industry": "Healthcare", "region": "Central"},
    {"name": "Stark Industries", "industry": "Aerospace", "region": "East"},
    {"name": "Wayne Enterprises", "industry": "Logistics", "region": "Central"},
    {"name": "Soylent Foods", "industry": "Food & Bev", "region": "West"},
    {"name": "Hooli", "industry": "Software", "region": "West"},
    {"name": "Wonka Industries", "industry": "Food & Bev", "region": "East"},
    {"name": "Cyberdyne", "industry": "Robotics", "region": "Central"},
]

LEADS = [
    {"full_name": "John Doe", "email": "john@acme.com", "company_name": "Acme Corp", "status": "qualified", "owner_rep": "Jane Smith"},
    {"full_name": "Maria Lopez", "email": "maria@acme.com", "company_name": "Acme Corp", "status": "contacted", "owner_rep": "Jane Smith"},
    {"full_name": "Bill Lumbergh", "email": "bill@initech.com", "company_name": "Initech", "status": "new", "owner_rep": "Tom Nguyen"},
    {"full_name": "Peter Gibbons", "email": "peter@initech.com", "company_name": "Initech", "status": "unqualified", "owner_rep": "Tom Nguyen"},
    {"full_name": "Sarah Connor", "email": "sarah@cyberdyne.com", "company_name": "Cyberdyne", "status": "qualified", "owner_rep": "Jane Smith"},
    {"full_name": "Tony Stark", "email": "tony@stark.com", "company_name": "Stark Industries", "status": "converted", "owner_rep": "Raj Patel"},
    {"full_name": "Bruce Wayne", "email": "bruce@wayne.com", "company_name": "Wayne Enterprises", "status": "contacted", "owner_rep": "Raj Patel"},
    {"full_name": "Willy Wonka", "email": "willy@wonka.com", "company_name": "Wonka Industries", "status": "new", "owner_rep": "Tom Nguyen"},
    {"full_name": "Gavin Belson", "email": "gavin@hooli.com", "company_name": "Hooli", "status": "qualified", "owner_rep": "Jane Smith"},
    {"full_name": "Alice Chen", "email": "alice@globex.com", "company_name": "Globex", "status": "contacted", "owner_rep": "Raj Patel"},
]

# account_name is resolved to account_id at seed time.
OPPORTUNITIES = [
    {"name": "Acme Annual Contract", "account_name": "Acme Corp", "deal_size": 120000, "stage": "negotiation", "close_date": "2026-08-15", "owner_rep": "Jane Smith"},
    {"name": "Acme Expansion", "account_name": "Acme Corp", "deal_size": 45000, "stage": "prospecting", "close_date": "2026-10-01", "owner_rep": "Jane Smith"},
    {"name": "Initech Platform License", "account_name": "Initech", "deal_size": 80000, "stage": "prospecting", "close_date": "2026-09-20", "owner_rep": "Tom Nguyen"},
    {"name": "Stark Defense Suite", "account_name": "Stark Industries", "deal_size": 500000, "stage": "closed_won", "close_date": "2026-03-30", "owner_rep": "Raj Patel"},
    {"name": "Wayne Fleet Upgrade", "account_name": "Wayne Enterprises", "deal_size": 210000, "stage": "negotiation", "close_date": "2026-07-10", "owner_rep": "Raj Patel"},
    {"name": "Hooli Enterprise Deal", "account_name": "Hooli", "deal_size": 300000, "stage": "negotiation", "close_date": "2026-08-01", "owner_rep": "Jane Smith"},
    {"name": "Globex Pilot", "account_name": "Globex", "deal_size": 25000, "stage": "prospecting", "close_date": "2026-11-15", "owner_rep": "Raj Patel"},
    {"name": "Cyberdyne R&D", "account_name": "Cyberdyne", "deal_size": 150000, "stage": "closed_lost", "close_date": "2026-02-28", "owner_rep": "Jane Smith"},
]


def wipe() -> None:
    # Delete children first to respect foreign keys.
    client.table("opportunities").delete().neq("id", 0).execute()
    client.table("leads").delete().neq("id", 0).execute()
    client.table("accounts").delete().neq("id", 0).execute()


def seed() -> None:
    wipe()

    client.table("accounts").insert(ACCOUNTS).execute()
    accounts = client.table("accounts").select("id,name").execute().data
    name_to_id = {a["name"]: a["id"] for a in accounts}

    leads = [{**lead, "account_id": name_to_id.get(lead["company_name"])} for lead in LEADS]
    client.table("leads").insert(leads).execute()

    opps = []
    for o in OPPORTUNITIES:
        row = {k: v for k, v in o.items() if k != "account_name"}
        row["account_id"] = name_to_id.get(o["account_name"])
        opps.append(row)
    client.table("opportunities").insert(opps).execute()

    print(
        f"Seeded {len(ACCOUNTS)} accounts, {len(leads)} leads, "
        f"{len(opps)} opportunities."
    )


if __name__ == "__main__":
    seed()
