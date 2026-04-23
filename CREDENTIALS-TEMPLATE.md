# Central Valley Locals - Credentials Template

**Instructions:** Fill in the values below after creating accounts, then share with Operator to update the site.

---

## Google Analytics 4

1. Go to https://analytics.google.com
2. Create property for `centralvalleylocals.com`
3. Copy the Measurement ID

**Measurement ID:** `G-XXXXXXXXXX`
*(Replace XXXXXXXXXX with your actual ID)*

---

## Microsoft Clarity

1. Go to https://clarity.microsoft.com
2. Create new project for `centralvalleylocals.com`
3. Copy the Project ID

**Clarity Project ID:** `XXXXXXXXXX`
*(10 character ID from your Clarity dashboard)*

---

## Formspree

1. Go to https://formspree.io
2. Create account
3. Create 4 forms:

### Forms Needed:

| Form Name | Purpose | Form ID |
|-----------|---------|---------|
| Business Submission | submit.html | `YOUR_SUBMIT_FORM_ID` |
| Event RSVP | events.html RSVP | `YOUR_EVENT_RSVP_ID` |
| Member Introduction | events.html intro | `YOUR_INTRO_FORM_ID` |
| Referral | chambers.html | `YOUR_REFERRAL_FORM_ID` |

**Form IDs to fill in:**
```
Business Submission: f/____________
Event RSVP: f/____________
Member Introduction: f/____________
Referral: f/____________
```

---

## Supabase

1. Go to https://supabase.com
2. Create new project named `centralvalleylocals`
3. Go to Settings > API

**Project URL:** `https://________________.supabase.co`
**Anon Public Key:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
*(Copy the full anon key from your dashboard)*

---

## How to Share

After filling in, send the values to Operator:
- Just the values, one per line
- Or say "Here are the credentials:" followed by the values

---

## Files That Need These

| Credential | Files |
|------------|-------|
| GA4 ID | index.html, all pages |
| Clarity ID | index.html, all pages |
| Formspree IDs | submit.html, events.html, chambers.html |
| Supabase credentials | Stored for future backend use |

---

## Quick Commands

After you provide credentials, Operator will:

1. Update all HTML files with tracking codes
2. Replace Formspree placeholder IDs
3. Test all forms
4. Commit and deploy changes

---

*Created: April 23, 2026*