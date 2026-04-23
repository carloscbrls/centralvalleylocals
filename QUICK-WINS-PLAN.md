# Central Valley Locals: 2-Week Quick Wins Plan

**Goal:** Start collecting leads and tracking visitors while building foundation for full platform.

**Timeline:** April 23 - May 7, 2026 (2 weeks)

---

## Week 1: Foundation

### Day 1-2: Analytics + Form Fixes
- [ ] Add Google Analytics 4 (GA4) — 2 hours
- [ ] Add Microsoft Clarity (heatmaps) — 1 hour
- [ ] Create Formspree account — 30 min
- [ ] Replace placeholder Formspree URLs — 1 hour
- [ ] Test all forms — 30 min

### Day 3-4: Supabase Setup
- [ ] Create Supabase account — 15 min
- [ ] Create database schema — 2 hours
- [ ] Set up Row Level Security — 1 hour
- [ ] Create API keys — 15 min
- [ ] Document connection details — 30 min

### Day 5-7: Lead Capture MVP
- [ ] Create lead capture form (Tally free) — 2 hours
- [ ] Connect form to email notifications — 1 hour
- [ ] Create lead storage (Google Sheets or Supabase) — 2 hours
- [ ] Test lead flow end-to-end — 1 hour
- [ ] Add form to all business pages — 2 hours

---

## Week 2: Content + Outreach

### Day 8-9: Content Foundation
- [ ] Taylor: Write 3 business spotlights — Village task
- [ ] Sam: Create social media schedule — Village task
- [ ] Sage: Set up SEO tracking — Village task
- [ ] Create "Add Your Business" landing page — 2 hours

### Day 10-11: Chamber Outreach
- [ ] Create Chamber partnership pitch — 1 hour
- [ ] Email Greater Lathrop Chamber members — Village task
- [ ] Add "Chamber Member" badges to listings — 1 hour
- [ ] Schedule follow-up sequence — Village task

### Day 12-14: Launch Prep
- [ ] Create lead intake process — 1 hour
- [ ] Set up lead notification system — 2 hours
- [ ] Write welcome email for businesses — 1 hour
- [ ] Create verification checklist — 1 hour
- [ ] Test complete flow — 2 hours

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Visitors tracked | ✅ | GA4 + Clarity installed |
| Leads captured | 5+ | Stored in database |
| Forms working | ✅ | All submissions received |
| Content published | 3 spotlights | Taylor completes |
| Chamber outreach | 20 emails | Leo sends |
| Business listings | 25+ | In database |

---

## Village Tasks (Assign Now)

| Agent | Task | Due |
|-------|------|-----|
| Taylor | Write 3 business spotlights | Day 10 |
| Sam | Create social posting schedule | Day 10 |
| Leo | Set up email sequences | Day 8 |
| Sage | SEO tracking setup | Day 9 |
| Alex | Research Chamber members | Day 10 |
| Operator | Monitor lead flow | Daily |

---

## Technical Setup Required

### Google Analytics 4
```
1. Go to analytics.google.com
2. Create property for centralvalleylocals.com
3. Get Measurement ID (G-XXXXXXXXXX)
4. Add to site header
```

### Microsoft Clarity
```
1. Go to clarity.microsoft.com
2. Create project
3. Get tracking code
4. Add to site header
```

### Formspree
```
1. Go to formspree.io
2. Create account
3. Create forms for: contact, lead capture, RSVP
4. Replace placeholder URLs in HTML
```

### Supabase
```
1. Go to supabase.com
2. Create project: centralvalleylocals
3. Create tables: businesses, leads, users
4. Get API keys
5. Store in ~/.openclaw/credentials/supabase
```

---

## Database Schema (MVP)

```sql
-- Businesses
CREATE TABLE businesses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE,
  category VARCHAR(100),
  city VARCHAR(100),
  phone VARCHAR(20),
  email VARCHAR(255),
  website VARCHAR(255),
  description TEXT,
  verified BOOLEAN DEFAULT FALSE,
  featured BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Leads
CREATE TABLE leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id UUID REFERENCES businesses(id),
  name VARCHAR(255),
  email VARCHAR(255),
  phone VARCHAR(20),
  message TEXT,
  source VARCHAR(100),
  status VARCHAR(50) DEFAULT 'new',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Users (for future)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE,
  business_id UUID REFERENCES businesses(id),
  role VARCHAR(50) DEFAULT 'owner',
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Files to Update

| File | Change |
|------|--------|
| `index.html` | Add GA4 + Clarity |
| `submit.html` | Fix Formspree form |
| `events.html` | Fix Formspree form |
| `chambers.html` | Fix Formspree form |
| All business pages | Add lead capture form |

---

## End of Week 2 Deliverables

- [ ] GA4 tracking all pages
- [ ] Clarity heatmaps running
- [ ] All forms submitting to Formspree
- [ ] Supabase database created
- [ ] Leads stored in database
- [ ] 3 business spotlights published
- [ ] Chamber outreach sent
- [ ] 25+ businesses in database

---

## Cost Breakdown

| Tool | Plan | Monthly Cost |
|------|------|--------------|
| Netlify | Free | $0 |
| Supabase | Free tier | $0 |
| Formspree | Free tier | $0 |
| Tally | Free tier | $0 |
| Google Analytics | Free | $0 |
| Microsoft Clarity | Free | $0 |
| **Total** | | **$0/month** |

---

## Notes

- This is the "foundation" phase
- Week 3+ would build full backend with auth
- Lead capture works with current static site
- Village handles content and outreach while you build foundation