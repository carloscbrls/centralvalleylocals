#!/bin/bash
# Deploy Central Valley Locals to Netlify
# Run this after netlify login is complete

echo "Deploying Central Valley Locals..."

# Check if logged in
if netlify status 2>&1 | grep -q "Not logged in"; then
    echo "Not logged in. Running netlify login..."
    netlify login
fi

# Deploy to production
netlify deploy --prod --dir=.

echo ""
echo "Deployment complete!"
echo "Site: https://centralvalleylocals.com (after domain linked)"
