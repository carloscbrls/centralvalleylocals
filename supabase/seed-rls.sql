-- Central Valley Locals - Seed Data + RLS Policies
-- Run AFTER the schema

-- Seed sample businesses
insert into businesses (category_id, name, slug, description, city, state, zip_code, website, is_featured)
select id, 'CC3PO Technology Services', 'cc3po-technology-services',
'Local IT support, websites, automation, and digital solutions.',
'Lathrop', 'CA', '95330', 'https://cc3po.com', true
from categories where slug = 'technology'
on conflict (slug) do nothing;

insert into businesses (category_id, name, slug, description, city, state, zip_code, is_featured)
select id, 'Central Valley Community Partner', 'central-valley-community-partner',
'Community-focused local organization serving Central Valley residents.',
'Manteca', 'CA', '95336', false
from categories where slug = 'nonprofits'
on conflict (slug) do nothing;

insert into businesses (category_id, name, slug, description, city, state, zip_code, is_featured)
select id, 'Local Chamber Business', 'local-chamber-business',
'Sample chamber-connected local business listing.',
'Lathrop', 'CA', '95330', false
from categories where slug = 'professional-services'
on conflict (slug) do nothing;

-- Enable Row Level Security
alter table categories enable row level security;
alter table businesses enable row level security;
alter table leads enable row level security;
alter table reviews enable row level security;
alter table partnerships enable row level security;
alter table subscriptions enable row level security;
alter table analytics enable row level security;
alter table events enable row level security;

-- Public read policies
create policy "Public can read categories"
on categories for select
using (true);

create policy "Public can read active businesses"
on businesses for select
using (is_active = true);

create policy "Public can read approved reviews"
on reviews for select
using (is_approved = true);

create policy "Public can read events"
on events for select
using (true);

-- Public insert policies for forms
create policy "Anyone can submit leads"
on leads for insert
with check (true);

create policy "Anyone can submit reviews"
on reviews for insert
with check (true);

create policy "Anyone can submit partnerships"
on partnerships for insert
with check (true);