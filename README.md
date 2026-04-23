# Central Valley Locals

**Live Site:** https://centralvalleylocals.com (pending domain registration)
**Repository:** https://github.com/cc3po/centralvalleylocals

## About

Central Valley Locals is a local business directory serving Manteca, Modesto, Stockton, Tracy, and throughout California's Central Valley. We connect residents with trusted local businesses, supporting community networking and local economic growth.

## Mission

**Connect neighbors with trusted local businesses.**

We believe when local businesses support each other, everyone wins. Our directory isn't just a list—it's a network of Central Valley business owners helping each other grow.

### Core Values

- **Connect** — Build relationships between local businesses and customers
- **Trust** — Verified businesses with real reviews from real customers
- **Support** — Help local businesses grow through networking and visibility

## Features

- **Verified Listings** — Every business is personally verified before listing
- **Business Networking** — Local businesses can connect and cross-promote
- **Category Organization** — Automotive, Dental, HVAC, Plumbing, Tools & Equipment
- **City Focus** — Manteca, Modesto, Stockton, Tracy, Turlock, Merced
- **Featured Listings** — Premium visibility for businesses

## Categories

| Category | Description | Businesses |
|----------|-------------|------------|
| [Automotive](categories/automotive.html) | Auto repair, tools, parts | 3+ |
| [Dental](categories/dental.html) | Dentists, orthodontists | 6+ |
| [HVAC](categories/hvac.html) | Heating & cooling | 5+ |
| [Plumbing](categories/plumbing.html) | Plumbing services | 4+ |
| [Tools & Equipment](categories/tools.html) | Mobile tool distributors | 1+ |

## Featured Businesses

### Faith RLR LLC - Matco Tools
- **Owner:** Richard Regalado
- **Phone:** (209) 767-3328
- **Location:** Manteca, CA (serves Central Valley)
- **Type:** Mobile tool distributor
- **Rating:** 4.9/5 (12 reviews)
- **Why Featured:** Owner-operated, personalized service, community involvement

### Dr. Alan S. Lee DDS
- **Owner:** Dr. Alan S. Lee
- **Phone:** (209) 239-2990
- **Location:** 715 N Main St, Manteca, CA
- **Type:** Family & cosmetic dentistry
- **Rating:** 4.8/5
- **Why Featured:** 30+ years experience, comprehensive care

## Directory Structure

```
centralvalleylocals/
├── index.html                  # Homepage
├── assets/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   └── main.js            # JavaScript
│   └── images/                # Logo, icons
├── businesses/
│   ├── faith-rlr-llc.html     # Matco Tools
│   └── dr-alan-lee.html       # Dentist (client)
├── categories/
│   ├── automotive.html
│   ├── dental.html
│   ├── hvac.html
│   ├── plumbing.html
│   └── tools.html
└── README.md
```

## Development

### Local Setup

```bash
# Clone the repository
git clone https://github.com/cc3po/centralvalleylocals.git

# Navigate to directory
cd centralvalleylocals

# Open in browser
open index.html
```

### Deployment

1. Register domain: `centralvalleylocals.com`
2. Set up hosting (SiteGround, Netlify, or GitHub Pages)
3. Point DNS to hosting
4. Deploy files

### Adding New Businesses

1. Research business (phone, address, reviews)
2. Create HTML file in `businesses/` directory
3. Add structured data (Schema.org LocalBusiness)
4. Link from category page
5. Update homepage featured section if applicable

## Data Sources

Business data sourced from:
- Google Business Profile
- Yelp
- Facebook Business Pages
- Direct phone calls
- California Secretary of State business registry

## Future Features

- [ ] Search functionality
- [ ] Filter by city
- [ ] Filter by rating
- [ ] Business claim/verification
- [ ] Review submission
- [ ] Featured business upgrade (paid)
- [ ] Business networking events
- [ ] Newsletter signup

## Contact

- **Email:** info@centralvalleylocals.com
- **Phone:** (209) 555-1234
- **Project:** [CC3PO](https://cc3po.com)

## License

© 2026 Central Valley Locals. All rights reserved.

---

**Created by Operator for CC3PO**