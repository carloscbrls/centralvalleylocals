# Central Valley Locals: Automation Roadmap

**Created:** April 23, 2026
**Goal:** Enable Operator (AI agent) to run the directory autonomously with minimal human intervention

---

## Executive Summary

This document defines the automation infrastructure needed to transform Central Valley Locals from a manually-managed static site to an autonomous, revenue-generating platform operated by the Village AI agent system.

**Current State:** Static HTML site, manual submissions, no automation
**Target State:** Autonomous directory with self-service onboarding, automated content, and AI-operated workflows

**Estimated Timeline:** 6-9 months to full autonomy
**Key Dependency:** Backend infrastructure + Village agent integration

---

## Current State (What's Manual Now)

### Business Onboarding
- ❌ Manual form submission (submit.html → email)
- ❌ Manual email verification (Carlos sends emails)
- ❌ Manual business verification (Carlos calls businesses)
- ❌ Manual listing creation (Carlos creates HTML files)
- ❌ Manual photo/logo uploads
- ❌ Manual category assignment

### Content Creation
- ❌ No blog content (insights.cc3po.com is separate)
- ❌ No social media presence (no accounts created)
- ❌ No email newsletters
- ❌ No business spotlights
- ❌ No SEO content generation

### Lead Management
- ❌ No lead capture system
- ❌ No auto-response to inquiries
- ❌ No lead distribution
- ❌ No follow-up sequences
- ❌ No review request automation

### Marketing
- ❌ No social posting schedule
- ❌ No email marketing system
- ❌ No referral tracking
- ❌ No cross-promotion matching

### Monitoring
- ⚠️ Basic uptime (Netlify provides)
- ❌ No listing quality checks
- ❌ No broken link detection
- ❌ No SEO rank tracking
- ❌ No performance analytics

### Revenue
- ❌ No payment processing
- ❌ No subscription billing
- ❌ No invoice generation
- ❌ No upgrade/downgrade flows

### Technical
- ⚠️ Static HTML on Netlify (simple but limited)
- ❌ No database
- ❌ No authentication system
- ❌ No admin dashboard
- ❌ No API endpoints

---

## Future State (What's Automated)

### Business Onboarding (Fully Automated)
- ✅ Self-registration form → database
- ✅ Email verification (SendGrid/Postmark webhook)
- ✅ Business verification workflow (structured process)
- ✅ Automatic listing creation (template-based)
- ✅ Photo/logo uploads (cloud storage)
- ✅ Category auto-suggestion (AI-assisted)
- ✅ Welcome email sequence (triggered on approval)

### Content Automation (Village-Operated)
- ✅ Weekly business spotlights (Taylor writes, Foreman assigns)
- ✅ SEO blog content (Taylor + Alex research)
- ✅ Social media posts (Sam schedules)
- ✅ Email newsletters (Leo automates)
- ✅ Content calendar (Foreman manages)

### Lead Automation (Fully Automated)
- ✅ Lead capture forms (category-specific)
- ✅ Auto-response to inquiries (< 5 min)
- ✅ Lead distribution to businesses (email + dashboard)
- ✅ Follow-up sequences (drip campaigns)
- ✅ Review request after service (timed triggers)

### Marketing Automation (Village-Operated)
- ✅ Social posting schedule (Sam executes)
- ✅ Email marketing sequences (Leo manages)
- ✅ Referral program automation (tracked in DB)
- ✅ Cross-promotion matching (algorithm + AI review)

### Monitoring Automation (Operator-Managed)
- ✅ Site uptime monitoring (alerts to Operator)
- ✅ Listing quality checks (weekly scan)
- ✅ Broken link detection (automated crawler)
- ✅ SEO rank tracking (monthly report via Alex)
- ✅ Performance analytics dashboard

### Revenue Automation (Fully Automated)
- ✅ Subscription billing (Stripe webhooks)
- ✅ Payment reminders (automated emails)
- ✅ Account upgrades/downgrades (self-service)
- ✅ Invoice generation (PDF + email)
- ✅ Payment failure handling (dunning)

### Village Integration (Agent-Assigned)

| Agent | Role in CVL | Automation Level |
|-------|-------------|------------------|
| **Operator** | Overall coordination, monitoring, alerts | Full autonomy |
| **Taylor** | Business spotlights, SEO content, guides | Human + AI assisted |
| **Sam** | Social media posts, engagement | Scheduled + monitored |
| **Leo** | Email newsletters, sequences | Automated triggers |
| **Alex** | Market research, SEO analysis, competitor intel | Research + reports |
| **Foreman** | Task assignment, content calendar, quality checks | Coordination only |
| **Rico** | Compliance verification, policy checks | Rule-based automation |

---

## Implementation Phases

### Phase 1: Infrastructure Foundation (Weeks 1-4)

**Goal:** Transform from static site to dynamic platform

#### Technical Requirements

| Component | Solution | Priority |
|-----------|----------|----------|
| Backend | Node.js + Express or Next.js API routes | Critical |
| Database | Supabase (PostgreSQL) or PlanetScale | Critical |
| Authentication | Supabase Auth or Clerk | Critical |
| File Storage | Cloudinary (images) + Supabase Storage | High |
| Email Service | SendGrid or Postmark | Critical |
| Payments | Stripe | High |
| Hosting | Netlify (frontend) + Vercel/Railway (backend) | Critical |

#### Deliverables

- [ ] Set up Supabase project with database schema
- [ ] Migrate existing business data to database
- [ ] Create business listing CRUD API endpoints
- [ ] Build admin dashboard for Operator access
- [ ] Implement basic authentication for business owners
- [ ] Set up Stripe account for subscriptions

#### Database Schema (Core Tables)

```sql
-- Businesses
CREATE TABLE businesses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  category_id UUID REFERENCES categories(id),
  city VARCHAR(100),
  phone VARCHAR(20),
  email VARCHAR(255),
  website VARCHAR(255),
  description TEXT,
  address TEXT,
  hours JSONB,
  verified BOOLEAN DEFAULT FALSE,
  featured BOOLEAN DEFAULT FALSE,
  tier VARCHAR(50) DEFAULT 'free',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Users (Business Owners)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  business_id UUID REFERENCES businesses(id),
  role VARCHAR(50) DEFAULT 'owner',
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

-- Subscriptions
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id UUID REFERENCES businesses(id),
  stripe_customer_id VARCHAR(255),
  stripe_subscription_id VARCHAR(255),
  tier VARCHAR(50),
  status VARCHAR(50),
  current_period_end TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Agent Assignment:**
- **Operator:** Monitors infrastructure alerts
- **Carlos:** Reviews architecture decisions (human approval)

---

### Phase 2: Business Onboarding Automation (Weeks 5-8)

**Goal:** Self-service business registration with verification workflow

#### Workflow

```
Business Submission Flow:
1. Business owner fills form → API creates record (status: pending)
2. Email verification sent → Owner clicks link → (status: email_verified)
3. Verification webhook triggers Operator task
4. Operator/Carlos verifies business (calls/emails) → (status: verified)
5. Listing auto-created → Welcome email sent → (status: active)
```

#### Automation Points

| Step | Automation | Human Required |
|------|------------|----------------|
| Form submission | ✅ Automated | No |
| Email verification | ✅ Automated | No |
| Business verification | ⚠️ Semi-automated | Yes (call/email) |
| Listing creation | ✅ Automated | No |
| Welcome email | ✅ Automated | No |

#### Deliverables

- [ ] Build submission form (React/Vue component)
- [ ] Create email verification flow (SendGrid webhook)
- [ ] Build verification dashboard for Operator
- [ ] Create verification call script template
- [ ] Auto-generate listing pages from database
- [ ] Set up welcome email sequence (3 emails)

**Agent Assignment:**
- **Operator:** Receives verification tasks, marks verified after call
- **Leo:** Sends welcome emails via SendGrid
- **Foreman:** Tracks verification queue

---

### Phase 3: Content Automation (Weeks 9-12)

**Goal:** Village agents create and publish content autonomously

#### Content Calendar (Weekly)

| Day | Content Type | Agent | Automation |
|-----|--------------|-------|------------|
| Monday | Business spotlight (featured listing) | Taylor | AI-generated, human-reviewed |
| Tuesday | SEO blog post (category guide) | Taylor | AI-generated, human-reviewed |
| Wednesday | Social posts (3x per day) | Sam | Scheduled via Buffer/Hootsuite |
| Thursday | Email newsletter (bi-weekly) | Leo | Automated template |
| Friday | Market research report | Alex | Monthly, Operator-reviewed |

#### Content Pipeline

```
Content Creation Flow:
1. Foreman assigns content task (Monday 8 AM)
2. Taylor researches + writes draft (by Wednesday)
3. Operator reviews for quality (Wednesday PM)
4. Taylor edits if needed (Thursday AM)
5. Sam schedules social posts (Thursday PM)
6. Content publishes automatically (Friday 9 AM)
```

#### Business Spotlight Template

```markdown
# {Business Name}: {Tagline}

**Category:** {Category}
**Location:** {City}, CA
**Why We Love Them:** {AI-generated highlight}

{Business description from listing}

## What Makes Them Special
{AI-generated based on reviews/services}

## Services
{List from business profile}

## Contact
- Phone: {phone}
- Website: {website}
- Address: {address}

*Featured listing in Central Valley Locals directory.*
```

#### Deliverables

- [ ] Set up content management system (Sanity/Contentful or database)
- [ ] Create content calendar in Foreman's task system
- [ ] Build spotlight generation workflow for Taylor
- [ ] Integrate Buffer API for Sam's social scheduling
- [ ] Create email templates for Leo's newsletters
- [ ] Set up content approval queue for Operator

**Agent Assignment:**
- **Taylor:** Writes spotlights + SEO content
- **Sam:** Schedules social posts
- **Leo:** Manages email sequences
- **Alex:** Monthly research reports
- **Foreman:** Assigns tasks, tracks calendar
- **Operator:** Reviews quality, approves content

---

### Phase 4: Lead Automation (Weeks 13-16)

**Goal:** Automated lead capture, distribution, and follow-up

#### Lead Flow

```
Lead Capture Flow:
1. User submits quote request (category-specific form)
2. Lead stored in database → Auto-response sent (< 5 min)
3. Lead assigned to matching businesses (based on category + location)
4. Business receives email notification + dashboard alert
5. Business responds via dashboard
6. 3-day follow-up triggered if no response
7. 7-day review request sent after marked "completed"
```

#### Lead Forms (By Category)

| Category | Fields | Priority |
|----------|--------|----------|
| HVAC | Service type, urgency, address, photos | High |
| Plumbing | Issue type, urgency, address, photos | High |
| Dental | Service type, insurance, preferred times | Medium |
| Automotive | Service type, vehicle info, location | Medium |
| General | Name, email, phone, message, category | Low |

#### Lead Distribution Logic

```javascript
// Lead Assignment Algorithm
async function assignLead(lead) {
  const businesses = await db.query(`
    SELECT * FROM businesses
    WHERE category_id = $1
    AND city = $2
    AND verified = true
    AND featured = true  // Premium first
    ORDER BY tier DESC, created_at ASC
    LIMIT 5
  `, [lead.category_id, lead.city]);

  // Notify top 3 businesses
  for (const business of businesses.slice(0, 3)) {
    await sendLeadNotification(business, lead);
  }

  return businesses;
}
```

#### Deliverables

- [ ] Build category-specific lead forms
- [ ] Create auto-response email templates
- [ ] Build lead distribution system
- [ ] Create business owner dashboard (lead inbox)
- [ ] Implement follow-up sequence triggers
- [ ] Build review request automation (7-day delay)

**Agent Assignment:**
- **Operator:** Monitors lead flow, escalates stuck leads
- **Leo:** Manages email sequences
- **Foreman:** Tracks lead metrics weekly

---

### Phase 5: Marketing Automation (Weeks 17-20)

**Goal:** Scheduled, automated marketing across channels

#### Social Media Schedule (Sam)

| Platform | Frequency | Content | Automation |
|----------|-----------|---------|------------|
| Facebook | 2x/day | Business highlights, community events | Buffer API |
| Instagram | 1x/day | Visual business features | Buffer API |
| LinkedIn | 3x/week | B2B networking, Chamber news | Buffer API |
| Twitter/X | 3x/day | Quick updates, retweets | Buffer API |

#### Email Marketing (Leo)

| Email Type | Frequency | Trigger | List |
|------------|-----------|---------|------|
| Newsletter | Bi-weekly | Friday 9 AM | All subscribers |
| Business tips | Weekly | Tuesday 2 PM | Business owners |
| Featured spotlight | Weekly | Thursday 10 AM | All businesses |
| Lead notification | Instant | On lead receipt | Business owner |
| Review request | After service | 7-day delay | Customer |

#### Referral Program

```
Referral Tracking:
1. Business A shares unique referral link
2. Business B signs up via link
3. Referral tracked in database
4. Business A receives credit (free month or discount)
5. Business B gets welcome bonus
```

#### Deliverables

- [ ] Set up Buffer/Hootsuite API integration
- [ ] Create social post templates for Sam
- [ ] Build email newsletter templates (Leo)
- [ ] Create referral tracking system
- [ ] Build cross-promotion matching algorithm
- [ ] Set up marketing analytics dashboard

**Agent Assignment:**
- **Sam:** Schedules social posts via Buffer API
- **Leo:** Manages email sequences via SendGrid
- **Taylor:** Creates social content templates
- **Foreman:** Tracks marketing KPIs

---

### Phase 6: Monitoring Automation (Weeks 21-24)

**Goal:** Proactive monitoring with Operator oversight

#### Monitoring Dashboard

| Metric | Check Frequency | Alert Threshold | Agent |
|--------|-----------------|-----------------|-------|
| Site uptime | 5 min | < 99.5% uptime | Operator |
| Page speed | Hourly | > 3s load time | Operator |
| Broken links | Daily | Any broken link | Operator |
| Listing quality | Weekly | Missing fields | Foreman |
| SEO rankings | Monthly | Position drop > 5 | Alex |
| Business verification queue | Daily | > 10 pending | Operator |
| Lead response time | Hourly | > 24h response | Foreman |

#### Automated Checks

```javascript
// Daily Health Check (runs via cron)
async function dailyHealthCheck() {
  const results = {
    uptime: await checkUptime(),
    brokenLinks: await scanBrokenLinks(),
    pendingVerifications: await countPendingVerifications(),
    staleLeads: await findStaleLeads(),
    missingPhotos: await findListingsWithoutPhotos()
  };

  if (results.uptime < 99.5) {
    await alertOperator('Uptime below threshold');
  }

  if (results.brokenLinks.length > 0) {
    await createTask('Fix broken links', results.brokenLinks);
  }

  return results;
}
```

#### Deliverables

- [ ] Set up uptime monitoring (UptimeRobot or Pingdom)
- [ ] Create broken link scanner (cron job)
- [ ] Build listing quality checker (required fields)
- [ ] Integrate SEO rank tracking (Ahrefs/SEMrush API)
- [ ] Create Operator alert system (Telegram/Slack)
- [ ] Build monitoring dashboard

**Agent Assignment:**
- **Operator:** Receives all alerts, takes action
- **Alex:** Monthly SEO reports
- **Foreman:** Tracks quality metrics

---

### Phase 7: Revenue Automation (Weeks 25-28)

**Goal:** Self-service billing with automated workflows

#### Subscription Tiers

| Tier | Monthly | Annual | Features |
|------|---------|--------|----------|
| Free | $0 | $0 | Basic listing, contact form |
| Featured | $49 | $499 ($41/mo) | Top of category, badge, priority |
| Professional | $99 | $949 ($79/mo) | Everything + analytics, leads |
| Premium | $199 | $1,899 ($158/mo) | Everything + spotlight, priority support |
| Elite | $399 | $3,799 ($316/mo) | Everything + exclusivity, dedicated support |

#### Stripe Integration

```
Subscription Flow:
1. Business owner selects tier
2. Stripe checkout redirects to payment
3. Webhook updates database (subscription created)
4. Features enabled immediately
5. Invoice generated and emailed
6. Monthly billing automatic (Stripe handles)
7. Failed payment triggers dunning sequence
```

#### Dunning Sequence (Failed Payments)

```
Day 1: Payment failed → Retry email
Day 3: Retry attempt #2 → Email notification
Day 7: Retry attempt #3 → Warning email
Day 14: Final notice → Downgrade to free tier
Day 30: Account suspended (data retained 90 days)
```

#### Deliverables

- [ ] Set up Stripe products and pricing
- [ ] Build checkout flow (Stripe Elements)
- [ ] Create webhook handlers for subscription events
- [ ] Build upgrade/downgrade self-service
- [ ] Create invoice generation (PDF + email)
- [ ] Implement dunning email sequence
- [ ] Build revenue dashboard for Operator

**Agent Assignment:**
- **Operator:** Monitors failed payments, revenue alerts
- **Leo:** Manages dunning email sequences
- **Foreman:** Tracks MRR, churn, LTV metrics

---

### Phase 8: Village Integration (Weeks 29-32)

**Goal:** Full agent autonomy with human oversight only

#### Agent Workflows

```
Daily Operator Routine:
6:00 AM - Check monitoring dashboard
6:15 AM - Review verification queue
6:30 AM - Assign tasks to village agents
7:00 AM - Review content queue
7:30 AM - Check lead flow metrics
8:00 AM - Send daily summary to Carlos

Weekly:
Monday - Assign content tasks to Taylor
Tuesday - Review Alex's research
Wednesday - Quality check content
Thursday - Approve social schedule
Friday - Review revenue metrics
```

#### Task Assignment Matrix

| Task | Assigns To | Frequency | Approval |
|------|------------|-----------|----------|
| Business spotlight | Taylor | Weekly | Operator |
| SEO content | Taylor | Weekly | Operator |
| Social posts | Sam | Daily | Scheduled |
| Email newsletter | Leo | Bi-weekly | Operator |
| Research report | Alex | Monthly | Operator |
| Verification | Operator | Daily | Carlos (edge cases) |
| Payment issues | Operator | As needed | Carlos (> $500) |

#### Operator Permissions

| Area | Full Access | View Only | Notify Only |
|------|-------------|-----------|-------------|
| Business listings | ✅ | — | — |
| User accounts | ✅ | — | — |
| Content queue | ✅ | — | — |
| Revenue | — | ✅ | Alert on issues |
| Infrastructure | ✅ | — | — |
| Marketing | ✅ | — | — |

#### Deliverables

- [ ] Create Operator dashboard (all controls in one place)
- [ ] Build task queue for Foreman assignments
- [ ] Set up agent communication channels (Telegram/Slack)
- [ ] Create content approval workflow
- [ ] Build escalation system for Carlos intervention
- [ ] Create daily/weekly automation reports

---

## Timeline Summary

| Phase | Weeks | Focus | Human Hours | Agent Hours |
|-------|-------|-------|--------------|-------------|
| 1. Infrastructure | 1-4 | Backend, DB, Auth | 40 hrs | 20 hrs |
| 2. Onboarding | 5-8 | Verification workflow | 20 hrs | 30 hrs |
| 3. Content | 9-12 | Spotlight, SEO | 10 hrs | 40 hrs |
| 4. Leads | 13-16 | Forms, distribution | 15 hrs | 25 hrs |
| 5. Marketing | 17-20 | Social, email | 10 hrs | 30 hrs |
| 6. Monitoring | 21-24 | Health checks | 5 hrs | 20 hrs |
| 7. Revenue | 25-28 | Stripe, billing | 15 hrs | 25 hrs |
| 8. Integration | 29-32 | Agent workflows | 10 hrs | 40 hrs |
| **Total** | **32 weeks** | — | **125 hrs** | **230 hrs** |

**Human Time Investment:** ~4 hours/week during implementation
**Agent Time Investment:** ~7 hours/week (ongoing after launch)

---

## Ongoing Automation (Post-Launch)

### Daily Automation

| Time | Task | Agent |
|------|------|-------|
| 6:00 AM | Uptime check | Operator |
| 6:15 AM | Verification queue review | Operator |
| 7:00 AM | Lead queue check | Foreman |
| 8:00 AM | Daily summary to Carlos | Operator |
| 9:00 AM | Social post scheduling | Sam |
| 12:00 PM | Lead follow-up check | Foreman |
| 6:00 PM | End-of-day metrics | Operator |

### Weekly Automation

| Day | Task | Agent |
|-----|------|-------|
| Monday | Assign content tasks | Foreman → Taylor |
| Tuesday | Research assignment | Foreman → Alex |
| Wednesday | Content review | Operator |
| Thursday | Newsletter send | Leo |
| Friday | Spotlight publish | Taylor → Operator |
| Saturday | SEO rank report | Alex → Operator |
| Sunday | Planning for next week | Foreman |

### Monthly Automation

| Task | Agent | Frequency |
|------|-------|-----------|
| Revenue report | Operator | Monthly |
| Churn analysis | Alex | Monthly |
| SEO ranking check | Alex | Monthly |
| Content calendar planning | Foreman | Monthly |
| Listing quality audit | Foreman | Monthly |
| Customer feedback review | Alex | Monthly |

---

## Technical Architecture

### Frontend

```
centralvalleylocals.com (Netlify)
├── Static pages (marketing, about)
├── Dynamic pages (listings, search) → Next.js
├── Business dashboard (React)
└── Admin dashboard (React) → Operator
```

### Backend

```
API Server (Vercel/Railway)
├── /api/businesses (CRUD)
├── /api/leads (CRUD)
├── /api/auth (login/register)
├── /api/subscriptions (Stripe webhooks)
├── /api/verification (workflow)
└── /api/admin (Operator dashboard)
```

### Database (Supabase)

```
PostgreSQL
├── businesses
├── users
├── leads
├── subscriptions
├── content (spotlights, blog posts)
├── tasks (Foreman queue)
└── analytics (metrics)
```

### Integrations

| Service | Purpose | Agent |
|---------|---------|-------|
| SendGrid | Email delivery | Leo |
| Stripe | Payments | Operator |
| Buffer | Social scheduling | Sam |
| Cloudinary | Image hosting | Taylor |
| UptimeRobot | Monitoring | Operator |
| Telegram Bot | Agent notifications | All |

---

## Risk Mitigation

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Database failure | Low | Critical | Daily backups, replica |
| API downtime | Medium | High | Monitoring + alerts, fallback pages |
| Stripe issues | Low | High | Manual payment option, support |
| Email delivery issues | Medium | Medium | Backup provider (Postmark) |
| Agent failure | Low | Medium | Escalation to Carlos, retry logic |

### Business Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Low conversion | Medium | High | A/B testing, UX optimization |
| High churn | Medium | High | Dunning, exit surveys |
| Spam listings | Medium | Medium | Verification workflow, captcha |
| Negative reviews | Low | Medium | Review response templates |
| Competition | High | Medium | Quality focus, community moat |

---

## Success Metrics

### Technical Metrics

| Metric | Target | Tracking |
|--------|--------|----------|
| Uptime | 99.9% | UptimeRobot |
| Page load | < 2s | Lighthouse |
| API response | < 200ms | Custom metrics |
| Lead response | < 5 min | DB timestamp |
| Verification time | < 24 hrs | Workflow tracking |

### Business Metrics

| Metric | Month 3 | Month 6 | Month 12 |
|--------|---------|---------|----------|
| Listings | 100 | 300 | 600 |
| Paid conversions | 5% | 8% | 10% |
| MRR | $500 | $2,000 | $5,000 |
| Lead volume | 50/mo | 200/mo | 500/mo |
| Verification rate | 80% | 90% | 95% |

### Agent Efficiency Metrics

| Metric | Target |
|--------|--------|
| Content quality (approval rate) | 85% |
| Lead response time | < 5 min |
| Verification time | < 24 hrs |
| Human intervention rate | < 10% |

---

## Next Steps

### Immediate (Week 1)

1. **Set up Supabase project** - Create database schema
2. **Choose hosting** - Decide on Vercel vs Railway
3. **Create Stripe account** - Set up products/pricing
4. **Draft verification workflow** - Define call script, email templates

### Short-Term (Weeks 2-4)

1. **Build backend API** - Node.js/Express endpoints
2. **Create admin dashboard** - React app for Operator
3. **Migrate business data** - Import existing listings
4. **Set up SendGrid** - Email templates ready

### Medium-Term (Weeks 5-8)

1. **Launch onboarding** - Self-registration live
2. **Test verification workflow** - End-to-end testing
3. **Integrate Village agents** - Task assignment live
4. **Start content production** - First spotlight published

---

## Conclusion

This automation roadmap transforms Central Valley Locals from a manually-operated directory to an autonomous platform run by the Village AI agent system. The key is **infrastructure first, automation second, agent integration third**.

**The goal:** Operator runs day-to-day operations, Carlos intervenes only for edge cases and strategic decisions.

**Estimated time to full autonomy:** 6-9 months
**Estimated human time after launch:** 2-4 hours/week (down from 20+ hours/week manual)

---

*Document created: April 23, 2026*
*For: Central Valley Locals Directory Project*
*By: Operator (AI Agent)*