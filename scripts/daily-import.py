#!/usr/bin/env python3
"""
Central Valley Locals - Daily Business Importer
Runs daily via cron to add new businesses from leads database

Cron: 0 8 * * * /Users/cc3po/.openclaw/workspace/centralvalleylocals/scripts/run-daily-import.sh
"""

import json
import requests
import os
import re
from pathlib import Path
from datetime import datetime

# Supabase Configuration (from environment)
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nktjzwwenmefadtavahn.supabase.co')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY not set")
    exit(1)

# Paths
WORKSPACE = Path.home() / '.openclaw' / 'workspace'
LEADS_FILE = WORKSPACE / 'leads' / 'dental-vet-prospects-2026-04-23.json'
LOGS_DIR = WORKSPACE / 'centralvalleylocals' / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def get_categories():
    """Get all categories from Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/categories?select=id,name,slug"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return {cat['slug']: cat['id'] for cat in response.json()}
    
    return {}

def get_existing_businesses():
    """Get existing business slugs from Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/businesses?select=slug"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return {b['slug'] for b in response.json()}
    
    return set()

def category_from_keywords(keywords):
    """Determine category from business keywords"""
    keyword_map = {
        'technology': ['it', 'tech', 'computer', 'software', 'web', 'digital', 'automation'],
        'health-wellness': ['dental', 'dentist', 'doctor', 'medical', 'health', 'wellness', 'vet', 'veterinary'],
        'home-services': ['hvac', 'plumbing', 'plumber', 'electrician', 'roofing', 'landscaping', 'handyman'],
        'automotive': ['auto', 'car', 'mechanic', 'tire', 'oil', 'transmission'],
        'professional-services': ['lawyer', 'attorney', 'accountant', 'financial', 'insurance', 'real estate'],
        'restaurants': ['restaurant', 'food', 'cafe', 'bakery', 'pizza', 'mexican', 'chinese'],
        'retail': ['store', 'shop', 'retail', 'boutique'],
        'nonprofits': ['nonprofit', 'charity', 'foundation', 'chamber', 'community'],
    }
    
    keywords_lower = ' '.join(keywords).lower()
    
    for category, words in keyword_map.items():
        for word in words:
            if word in keywords_lower:
                return category
    
    return 'professional-services'  # Default

def add_business(business, categories, existing_slugs):
    """Add a single business to Supabase"""
    # Generate slug
    name = business.get('name', business.get('business_name', 'Unknown'))
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    
    # Check if exists
    if slug in existing_slugs:
        return None
    
    # Determine category
    keywords = [name, business.get('category', ''), business.get('description', '')]
    category_slug = category_from_keywords(keywords)
    category_id = categories.get(category_slug)
    
    if not category_id:
        category_id = categories.get('professional-services')
    
    # Prepare data
    data = {
        "name": name,
        "slug": slug,
        "category_id": category_id,
        "description": business.get('description', f"Local business serving {business.get('city', 'Central Valley')}"),
        "phone": business.get('phone', business.get('phone_number', '')),
        "email": business.get('email', ''),
        "website": business.get('website', ''),
        "address": business.get('address', ''),
        "city": business.get('city', ''),
        "state": "CA",
        "zip_code": business.get('zip_code', business.get('zip', '')),
        "is_featured": False,
        "is_active": True
    }
    
    # Insert
    url = f"{SUPABASE_URL}/rest/v1/businesses"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return slug
    elif response.status_code == 409:
        return None  # Already exists
    
    return None

def log_result(message):
    """Log result to file"""
    log_file = LOGS_DIR / 'import.log'
    timestamp = datetime.now().isoformat()
    
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    
    print(message)

def main():
    print("=== Central Valley Locals - Daily Import ===")
    
    # Get categories
    categories = get_categories()
    log_result(f"Loaded {len(categories)} categories")
    
    # Get existing businesses
    existing = get_existing_businesses()
    log_result(f"Found {len(existing)} existing businesses")
    
    # Load leads file
    if not LEADS_FILE.exists():
        log_result(f"ERROR: Leads file not found: {LEADS_FILE}")
        return
    
    with open(LEADS_FILE, 'r') as f:
        leads = json.load(f)
    
    log_result(f"Loaded {len(leads)} leads from file")
    
    # Add businesses
    added = 0
    for lead in leads:
        slug = add_business(lead, categories, existing)
        if slug:
            added += 1
            log_result(f"✅ Added: {lead.get('name', lead.get('business_name', 'Unknown'))}")
            existing.add(slug)
    
    log_result(f"✅ Total added: {added} businesses")
    log_result(f"📊 Total in database: {len(existing)} businesses")

if __name__ == "__main__":
    main()