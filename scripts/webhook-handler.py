#!/usr/bin/env python3
"""
Supabase Webhook Handler
Central Valley Locals Directory

Receives webhooks from Supabase for form submissions and triggers actions.

Usage:
  python3 webhook-handler.py --serve

Endpoints:
  /webhook/lead          - Lead form submission
  /webhook/business      - Business submission
  /webhook/review        - Review submission
"""

import os
import json
import hashlib
import datetime
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

# Directory for logs
LOGS_DIR = Path.home() / '.openclaw' / 'workspace' / 'centralvalleylocals' / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# WEBHOOK ENDPOINTS
# ============================================

@app.route('/webhook/lead', methods=['POST'])
def handle_lead():
    """Handle lead form submission webhook"""
    try:
        data = request.json
        
        # Log the submission
        log_submission('leads', data)
        
        # Send notification (can be extended)
        send_notification(
            subject=f"New Lead: {data.get('customer_name', 'Unknown')}",
            body=f"""
New lead received:

Name: {data.get('customer_name', 'N/A')}
Email: {data.get('customer_email', 'N/A')}
Phone: {data.get('customer_phone', 'N/A')}
Message: {data.get('message', 'N/A')}
Business ID: {data.get('business_id', 'N/A')}

Time: {datetime.datetime.now().isoformat()}
"""
        )
        
        return jsonify({"success": True, "message": "Lead received"})
    
    except Exception as e:
        log_error('lead_webhook', str(e))
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/webhook/business', methods=['POST'])
def handle_business():
    """Handle business submission webhook"""
    try:
        data = request.json
        
        # Log the submission
        log_submission('businesses', data)
        
        # Send notification
        send_notification(
            subject=f"New Business Listing: {data.get('name', 'Unknown')}",
            body=f"""
New business submitted for review:

Name: {data.get('name', 'N/A')}
Category: {data.get('category_id', 'N/A')}
Description: {data.get('description', 'N/A')}
City: {data.get('city', 'N/A')}
Phone: {data.get('phone', 'N/A')}
Email: {data.get('email', 'N/A')}
Website: {data.get('website', 'N/A')}

Time: {datetime.datetime.now().isoformat()}

Action Required:
1. Review the submission
2. Verify the business information
3. Set is_active = true in Supabase to approve
"""
        )
        
        return jsonify({"success": True, "message": "Business submission received"})
    
    except Exception as e:
        log_error('business_webhook', str(e))
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/webhook/review', methods=['POST'])
def handle_review():
    """Handle review submission webhook"""
    try:
        data = request.json
        
        # Log the submission
        log_submission('reviews', data)
        
        # Send notification
        send_notification(
            subject=f"New Review: {data.get('rating', 0)} stars",
            body=f"""
New review submitted:

Business ID: {data.get('business_id', 'N/A')}
Reviewer: {data.get('reviewer_name', 'Anonymous')}
Rating: {data.get('rating', 0)}/5
Review: {data.get('review_text', 'No text')}

Time: {datetime.datetime.now().isoformat()}

Action Required:
1. Review the content
2. Set is_approved = true in Supabase to publish
"""
        )
        
        return jsonify({"success": True, "message": "Review received"})
    
    except Exception as e:
        log_error('review_webhook', str(e))
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "centralvalleylocals-webhook",
        "timestamp": datetime.datetime.now().isoformat()
    })

# ============================================
# HELPER FUNCTIONS
# ============================================

def log_submission(table, data):
    """Log a submission to file"""
    log_file = LOGS_DIR / f"{table}.json"
    
    entries = []
    if log_file.exists():
        with open(log_file, 'r') as f:
            entries = json.load(f)
    
    entries.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "data": data
    })
    
    with open(log_file, 'w') as f:
        json.dump(entries, f, indent=2)
    
    print(f"📝 Logged submission to {table}")

def log_error(webhook_type, error):
    """Log an error"""
    error_file = LOGS_DIR / "errors.json"
    
    errors = []
    if error_file.exists():
        with open(error_file, 'r') as f:
            errors = json.load(f)
    
    errors.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "webhook": webhook_type,
        "error": error
    })
    
    with open(error_file, 'w') as f:
        json.dump(errors, f, indent=2)
    
    print(f"❌ Error in {webhook_type}: {error}")

def send_notification(subject, body):
    """Send notification (can be extended to email, Slack, etc.)"""
    # For now, just log it
    notification = {
        "timestamp": datetime.datetime.now().isoformat(),
        "subject": subject,
        "body": body
    }
    
    notif_file = LOGS_DIR / "notifications.json"
    
    notifications = []
    if notif_file.exists():
        with open(notif_file, 'r') as f:
            notifications = json.load(f)
    
    notifications.append(notification)
    
    with open(notif_file, 'w') as f:
        json.dump(notifications, f, indent=2)
    
    print(f"📧 Notification: {subject}")

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Central Valley Locals Webhook Handler')
    parser.add_argument('--serve', action='store_true', help='Start the webhook server')
    parser.add_argument('--port', type=int, default=4020, help='Port to run on')
    
    args = parser.parse_args()
    
    if args.serve:
        print(f"🚀 Starting webhook server on port {args.port}")
        print(f"📡 Endpoints:")
        print(f"   - POST /webhook/lead")
        print(f"   - POST /webhook/business")
        print(f"   - POST /webhook/review")
        print(f"   - GET  /health")
        app.run(host='0.0.0.0', port=args.port)
    else:
        print("Use --serve to start the webhook server")