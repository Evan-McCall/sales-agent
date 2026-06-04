-- Sales Agent CRM schema (stubbed Salesforce-style data for the MVP).
-- Run this in the Supabase SQL editor before seeding.

drop table if exists opportunities cascade;
drop table if exists leads cascade;
drop table if exists accounts cascade;

create table accounts (
    id          bigint generated always as identity primary key,
    name        text not null unique,
    industry    text,
    region      text,
    created_at  timestamptz default now()
);

create table leads (
    id            bigint generated always as identity primary key,
    full_name     text not null,
    email         text,
    company_name  text not null,
    status        text check (status in ('new','contacted','qualified','unqualified','converted')),
    owner_rep     text,                       -- sales rep who owns the lead
    account_id    bigint references accounts(id),
    created_at    timestamptz default now()
);

create table opportunities (
    id          bigint generated always as identity primary key,
    name        text not null,
    account_id  bigint references accounts(id),
    deal_size   numeric(12,2),
    stage       text check (stage in ('prospecting','negotiation','closed_won','closed_lost')),
    close_date  date,
    owner_rep   text
);

-- Indexes for the case-insensitive lookups the agent performs most.
create index idx_leads_company on leads (lower(company_name));
create index idx_leads_owner   on leads (lower(owner_rep));
create index idx_accounts_name on accounts (lower(name));
