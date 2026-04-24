#!/usr/bin/env python3
"""
Add Businesses to Supabase
Central Valley Locals Directory

Usage:
  python3 add-businesses.py

This script adds businesses from the leads database to Supabase.
"""

import json
import requests
from pathlib import Path

# Supabase Configuration
SUPABASE_URL = "https://nktjzwwenmefadtavahn.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rdGp6d3dlbm1lZmFkdGF2YWhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU0NjY2NjgsImV4cCI6MjA2MTA0MjY2OH0.4hVqTgd3Vb0lOqpN0XjRlQJZGqR0Zm0W8RjZQGJZGJM"

# Business data to add
BUSINESSES = [
    {
        "name": "Faith RLR LLC",
        "slug": "faith-rlr-llc",
        "category": "technology",
        "description": "Mobile tool distributor serving automotive technicians. Owner-operated with personalized service, after-hours support, and competitive pricing.",
        "phone": "(209) 767-3328",
        "city": "Manteca",
        "state": "CA",
        "zip_code": "95336",
        "website": "https://faithrlr.com",
        "is_featured": True
    },
    {
        "name": "Dr. Alan S. Lee DDS",
        "slug": "dr-alan-lee",
        "category": "health-wellness",
        "description": "30+ years serving Manteca with comprehensive dental care including implants, whitening, crowns, and preventive care. Family-owned practice.",
        "phone": "(209) 239-2990",
        "city": "Manteca",
        "state": "CA",
        "zip_code": "95336",
        "website": "",
        "is_featured": True
    },
    {
        "name": "Matt Safdari - Financial Planning",
        "slug": "matt-safdari",
        "category": "professional-services",
        "description": "Financial planning, life insurance, retirement strategies, wealth management. Helping families achieve financial independence.",
        "phone": "(209) 640-5103",
        "city": "Central Valley",
        "state": "CA",
        "zip_code": "",
        "website": "",
        "is_featured": True
    },
    {
        "name": "CC3PO Technology Services",
        "slug": "cc3po-technology-services",
        "category": "technology",
        "description": "Local IT support, websites, automation, and digital solutions for small businesses.",
        "phone": "(209) 423-6633",
        "city": "Lathrop",
        "state": "CA",
        "zip_code": "95330",
        "website": "https://cc3po.com",
        "is_featured": True
    },
    {
        "name": "Central Valley HVAC",
        "slug": "central-valley-hvac",
        "category": "home-services",
        "description": "Heating, ventilation, and air conditioning services for residential and commercial properties.",
        "phone": "(209) 555-0123",
        "city": "Manteca",
        "state": "CA",
        "zip_code": "95336",
        "website": "",
        "is_featured": False
    },
    {
        "name": "Manteca Auto Repair",
        "slug": "manteca-auto-repair",
        "category": "automotive",
        "description": "Full-service auto repair shop specializing in brakes, oil changes, and engine diagnostics.",
        "phone": "(209) 555-0456",
        "city": "Manteca",
        "state": "CA",
        "zip_code": "95336",
        "website": "",
        "is_featured": False
    },
    {
        "name": "Stockton Plumbing Pros",
        "slug": "stockton-plumbing-pros",
        "category": "home-services",
        "description": "Licensed plumber offering residential and commercial plumbing services, emergency repairs, and installations.",
        "phone": "(209) 555-0789",
        "city": "Stockton",
        "state": "CA",
        "zip_code": "95202",
        "website": "",
        "is_featured": False
    },
    {
        "name": "Tracy Dental Group",
        "slug": "tracy-dental-group",
        "category": "health-wellness",
        "description": "Family dentistry offering cleanings, fillings, crowns, and cosmetic procedures.",
        "phone": "(209) 555-0234",
        "city": "Tracy",
        "state": "CA",
        "zip_code": "95376",
        "website": "",
        "is_featured": False
    },
    {
        "name": "Modesto Real Estate Group",
        "slug": "modesto-real-estate-group",
        "category": "real-estate",
        "description": "Helping families find their dream homes in Central Valley. First-time buyers welcome.",
        "phone": "(209) 555-0567",
        "city": "Modesto",
        "state": "CA",
        "zip_code": "95350",
        "website": "",
        "is_featured": False
    },
    {
        "name": "Greater Lathrop Chamber of Commerce",
        "slug": "greater-lathrop-chamber",
        "category": "nonprofits",
        "description": "Supporting local businesses through networking, events, and advocacy.",
        "phone": "(209) 555-0890",
        "city": "Lathrop",
        "state": "CA",
        "zip_code": "95330",
        "website": "",
        "is_featured": False
    }
]

def get_category_id(category_slug):
    """Get category ID from slug"""
    url = f"{SUPABASE_URL}/rest/v1/categories?slug=eq.{category_slug}"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['id']
    
    return None

def add_business(business):
    """Add a business to Supabase"""
    # Get category ID
    category_id = get_category_id(business['category'])
    
    if not category_id:
        print(f"⚠️  Category not found: {business['category']}")
        return False
    
    # Prepare business data
    data = {
        "category_id": category_id,
        "name": business['name'],
        "slug": business['slug'],
        "description": business.get('description', ''),
        "phone": business.get('phone', ''),
        "email": business.get('email', ''),
        "website": business.get('website', ''),
        "address": business.get('address', ''),
        "city": business.get('city', ''),
        "state": business.get('state', 'CA'),
        "zip_code": business.get('zip_code', ''),
        "is_featured": business.get('is_featured', False),
        "is_active": True
    }
    
    # Insert business
    url = f"{SUPABASE_URL}/rest/v1/businesses"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"✅ Added: {business['name']}")
        return True
    elif response.status_code == 409:
        print(f"⚠️  Already exists: {business['name']}")
        return False
    else:
        print(f"❌ Error adding {business['name']}: {response.text}")
        return False

def main():
    print("=== Adding Businesses to Supabase ===\n")
    
    success_count = 0
    
    for business in BUSINESSES:
        if add_business(business):
            success_count += 1
    
    print(f"\n✅ Added {success_count} businesses")
    print(f"📊 Total in database: Check Supabase dashboard")

if __name__ == "__main__":
    main()