-- Central Valley Locals - Simplified Schema
-- Run this in Supabase SQL Editor

-- Enable UUID support
create extension if not exists "pgcrypto";

-- Categories
create table if not exists categories (
 id uuid primary key default gen_random_uuid(),
 name text not null unique,
 slug text not null unique,
 description text,
 created_at timestamptz default now()
);

-- Businesses
create table if not exists businesses (
 id uuid primary key default gen_random_uuid(),
 category_id uuid references categories(id) on delete set null,
 name text not null,
 slug text not null unique,
 description text,
 phone text,
 email text,
 website text,
 address text,
 city text,
 state text default 'CA',
 zip_code text,
 logo_url text,
 is_featured boolean default false,
 is_active boolean default true,
 created_at timestamptz default now(),
 updated_at timestamptz default now()
);

-- Leads / inquiries
create table if not exists leads (
 id uuid primary key default gen_random_uuid(),
 business_id uuid references businesses(id) on delete cascade,
 customer_name text not null,
 customer_email text,
 customer_phone text,
 message text,
 status text default 'new',
 created_at timestamptz default now()
);

-- Reviews
create table if not exists reviews (
 id uuid primary key default gen_random_uuid(),
 business_id uuid references businesses(id) on delete cascade,
 reviewer_name text not null,
 rating int check (rating >= 1 and rating <= 5),
 review_text text,
 is_approved boolean default false,
 created_at timestamptz default now()
);

-- Partnerships
create table if not exists partnerships (
 id uuid primary key default gen_random_uuid(),
 business_id uuid references businesses(id) on delete cascade,
 partner_name text not null,
 partner_email text,
 message text,
 status text default 'pending',
 created_at timestamptz default now()
);

-- Subscriptions
create table if not exists subscriptions (
 id uuid primary key default gen_random_uuid(),
 business_id uuid references businesses(id) on delete cascade,
 plan_name text not null,
 stripe_customer_id text,
 stripe_subscription_id text,
 status text default 'active',
 starts_at timestamptz default now(),
 ends_at timestamptz
);

-- Analytics
create table if not exists analytics (
 id uuid primary key default gen_random_uuid(),
 business_id uuid references businesses(id) on delete cascade,
 event_type text not null,
 event_data jsonb,
 created_at timestamptz default now()
);

-- Events
create table if not exists events (
 id uuid primary key default gen_random_uuid(),
 title text not null,
 description text,
 event_date timestamptz not null,
 location text,
 event_url text,
 created_at timestamptz default now()
);

-- Indexes
create index if not exists idx_businesses_category_id on businesses(category_id);
create index if not exists idx_businesses_city on businesses(city);
create index if not exists idx_businesses_slug on businesses(slug);
create index if not exists idx_leads_business_id on leads(business_id);
create index if not exists idx_reviews_business_id on reviews(business_id);
create index if not exists idx_analytics_business_id on analytics(business_id);

-- Seed categories
insert into categories (name, slug, description)
values
('Restaurants', 'restaurants', 'Local food and dining'),
('Retail', 'retail', 'Shops and stores'),
('Health & Wellness', 'health-wellness', 'Health, fitness, and wellness services'),
('Professional Services', 'professional-services', 'Business and professional services'),
('Home Services', 'home-services', 'Repair, maintenance, and home support'),
('Nonprofits', 'nonprofits', 'Community organizations'),
('Real Estate', 'real-estate', 'Realtors, property, and housing'),
('Automotive', 'automotive', 'Auto repair, sales, and services'),
('Events', 'events', 'Event vendors and venues'),
('Technology', 'technology', 'IT, web, and tech services')
on conflict (slug) do nothing;