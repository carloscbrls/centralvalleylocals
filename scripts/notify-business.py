#!/usr/bin/env python3
"""
Lead Notification System for Central Valley Locals
Sends SMS notifications to businesses when they receive a new lead

Setup:
1. Twilio account required
2. Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in environment
3. Set TWILIO_PHONE_NUMBER for outgoing SMS

Usage:
  python3 notify-business.py --lead-id <lead_id>
  python3 notify-business.py --test
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime

# Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://nktjzwwenmefadtavahn.supabase.co')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')

# Twilio (optional - for SMS notifications)
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '+12094236633')

# Logs directory
LOGS_DIR = Path.home() / '.openclaw' / 'workspace' / 'centralvalleylocals' / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def get_lead(lead_id):
    """Fetch lead details from Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/leads?id=eq.{lead_id}&select=*,businesses(name,phone,email)"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]
    
    return None

def get_business_phone(business_id):
    """Fetch business phone number"""
    url = f"{SUPABASE_URL}/rest/v1/businesses?id=eq.{business_id}&select=phone,name"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data and data[0].get('phone'):
            return data[0]
    
    return None

def send_sms(to_phone, message):
    """Send SMS via Twilio"""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        log_result(f"SMS skipped (Twilio not configured): {message[:50]}...")
        return False
    
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    
    auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    data = {
        "From": TWILIO_PHONE_NUMBER,
        "To": to_phone,
        "Body": message
    }
    
    response = requests.post(url, auth=auth, data=data)
    
    if response.status_code == 201:
        log_result(f"SMS sent to {to_phone}")
        return True
    else:
        log_result(f"SMS failed: {response.text}")
        return False

def send_email_notification(business_email, lead_data):
    """Send email notification (fallback if SMS not available)"""
    # This would use your existing email system
    # For now, just log it
    log_result(f"Email notification to {business_email}: New lead from {lead_data.get('customer_name')}")

def format_lead_message(lead_data, business_name):
    """Format SMS message for business"""
    customer = lead_data.get('customer_name', 'A customer')
    phone = lead_data.get('customer_phone', 'No phone')
    service = lead_data.get('message', 'General inquiry')
    score = lead_data.get('score', 50)
    
    # Determine lead quality
    if score >= 80:
        quality = "🔥 HOT LEAD"
    elif score >= 50:
        quality = "⭐ Quality Lead"
    else:
        quality = "📋 New Lead"
    
    message = f"""{quality}

{business_name}, you have a new quote request!

From: {customer}
Phone: {phone}

{service[:100]}{'...' if len(service) > 100 else ''}

Score: {score}/100

Reply to this lead in your dashboard or call directly.

- Central Valley Locals"""
    
    return message

def notify_business(lead_id):
    """Notify business of new lead"""
    lead = get_lead(lead_id)
    
    if not lead:
        log_result(f"Lead not found: {lead_id}")
        return False
    
    business = lead.get('businesses', {})
    if not business:
        # Get business separately
        business = get_business_phone(lead.get('business_id'))
    
    if not business:
        log_result(f"Business not found for lead: {lead_id}")
        return False
    
    business_name = business.get('name', 'Business')
    business_phone = business.get('phone')
    business_email = business.get('email')
    
    # Format message
    message = format_lead_message(lead, business_name)
    
    # Try SMS first
    notified = False
    if business_phone:
        # Clean phone number
        clean_phone = ''.join(c for c in business_phone if c.isdigit())
        if len(clean_phone) == 10:
            clean_phone = f"+1{clean_phone}"
        elif len(clean_phone) == 11:
            clean_phone = f"+{clean_phone}"
        
        notified = send_sms(clean_phone, message)
    
    # Fallback to email
    if not notified and business_email:
        send_email_notification(business_email, lead)
    
    # Log the notification
    log_result(f"Lead {lead_id} → {business_name}: {'SMS sent' if notified else 'Logged'}")
    
    return True

def log_result(message):
    """Log result to file"""
    log_file = LOGS_DIR / 'notifications.log'
    timestamp = datetime.now().isoformat()
    
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    
    print(message)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Notify businesses of new leads')
    parser.add_argument('--lead-id', help='Lead ID to notify about')
    parser.add_argument('--test', action='store_true', help='Send test notification')
    
    args = parser.parse_args()
    
    if not SUPABASE_SERVICE_KEY:
        # Load from credentials file
        cred_file = Path.home() / '.openclaw' / 'credentials' / 'supabase-centralvalleylocals'
        if cred_file.exists():
            with open(cred_file) as f:
                for line in f:
                    if line.startswith('SUPABASE_SERVICE_KEY='):
                        os.environ['SUPABASE_SERVICE_KEY'] = line.split('=', 1)[1].strip()
                        break
    
    # Reload
    global SUPABASE_SERVICE_KEY
    SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')
    
    if args.test:
        # Send test notification
        test_lead = {
            'customer_name': 'Test Customer',
            'customer_phone': '(209) 555-0123',
            'message': 'This is a test lead notification.',
            'score': 85
        }
        test_message = format_lead_message(test_lead, 'Test Business')
        print("Test message:")
        print(test_message)
        print("\nNote: SMS would be sent to business phone if configured")
    
    elif args.lead_id:
        notify_business(args.lead_id)
    
    else:
        print("Use --lead-id <id> or --test")

if __name__ == "__main__":
    main()