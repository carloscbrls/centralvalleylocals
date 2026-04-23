-- Central Valley Locals Database Schema
-- Generated: 2026-04-23
-- Database: PostgreSQL (Supabase)

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- BUSINESSES TABLE
-- ============================================
CREATE TABLE businesses (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  category VARCHAR(100),
  category_id UUID REFERENCES categories(id),
  city VARCHAR(100),
  address TEXT,
  phone VARCHAR(50),
  email VARCHAR(255),
  website VARCHAR(500),
  description TEXT,
  hours JSONB,
  services TEXT[],
  tags TEXT[],
  
  -- Verification
  verified BOOLEAN DEFAULT FALSE,
  verified_at TIMESTAMP,
  verified_by VARCHAR(100),
  
  -- Listing tier
  tier VARCHAR(50) DEFAULT 'free', -- free, verified, featured, premium, elite
  
  -- Chamber member
  chamber_member BOOLEAN DEFAULT FALSE,
  chamber_name VARCHAR(255),
  
  -- Media
  logo_url VARCHAR(500),
  photos TEXT[],
  
  -- Social
  facebook VARCHAR(255),
  instagram VARCHAR(255),
  linkedin VARCHAR(255),
  twitter VARCHAR(255),
  
  -- Stats
  views INTEGER DEFAULT 0,
  clicks INTEGER DEFAULT 0,
  leads_sent INTEGER DEFAULT 0,
  rating DECIMAL(3, 2) DEFAULT 0,
  review_count INTEGER DEFAULT 0,
  
  -- Metadata
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  created_by VARCHAR(100),
  
  -- Full-text search
  search_vector TSVECTOR
);

-- Create index for search
CREATE INDEX idx_businesses_search ON businesses USING GIN(search_vector);
CREATE INDEX idx_businesses_category ON businesses(category);
CREATE INDEX idx_businesses_city ON businesses(city);
CREATE INDEX idx_businesses_tier ON businesses(tier);
CREATE INDEX idx_businesses_verified ON businesses(verified);

-- ============================================
-- CATEGORIES TABLE
-- ============================================
CREATE TABLE categories (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(100) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  icon VARCHAR(50),
  description TEXT,
  parent_id UUID REFERENCES categories(id),
  order_index INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Insert default categories
INSERT INTO categories (name, slug, icon, order_index) VALUES
('Automotive', 'automotive', '🔧', 1),
('Dental', 'dental', '🦷', 2),
('HVAC', 'hvac', '❄️', 3),
('Plumbing', 'plumbing', '🚿', 4),
('Professional Services', 'professional', '💼', 5),
('Tools & Equipment', 'tools', '🛠️', 6),
('Health & Wellness', 'health', '💪', 7),
('Financial', 'financial', '💰', 8),
('Home Services', 'home-services', '🏠', 9),
('Food & Dining', 'food', '🍽️', 10);

-- ============================================
-- USERS TABLE (Business Owners)
-- ============================================
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  full_name VARCHAR(255),
  phone VARCHAR(50),
  business_id UUID REFERENCES businesses(id),
  role VARCHAR(50) DEFAULT 'owner', -- owner, admin, viewer
  email_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  last_login TIMESTAMP
);

-- ============================================
-- LEADS TABLE
-- ============================================
CREATE TABLE leads (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  -- Lead info
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  phone VARCHAR(50),
  message TEXT,
  
  -- Source tracking
  source VARCHAR(100), -- website, form, phone, referral
  campaign VARCHAR(100),
  utm_source VARCHAR(100),
  utm_medium VARCHAR(100),
  utm_campaign VARCHAR(100),
  
  -- Assignment
  business_id UUID REFERENCES businesses(id),
  assigned_to UUID REFERENCES users(id),
  
  -- Status
  status VARCHAR(50) DEFAULT 'new', -- new, contacted, qualified, converted, lost
  
  -- Scoring
  score INTEGER DEFAULT 0,
  
  -- Metadata
  ip_address VARCHAR(50),
  user_agent TEXT,
  referrer TEXT,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  converted_at TIMESTAMP
);

CREATE INDEX idx_leads_business ON leads(business_id);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_created ON leads(created_at);

-- ============================================
-- REVIEWS TABLE
-- ============================================
CREATE TABLE reviews (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  business_id UUID REFERENCES businesses(id) NOT NULL,
  user_id UUID REFERENCES users(id),
  
  -- Review content
  rating INTEGER CHECK (rating >= 1 AND rating <= 5),
  title VARCHAR(255),
  content TEXT,
  
  -- Verification
  verified BOOLEAN DEFAULT FALSE, -- verified purchase/service
  source VARCHAR(50), -- google, yelp, direct
  
  -- Moderation
  approved BOOLEAN DEFAULT FALSE,
  flagged BOOLEAN DEFAULT FALSE,
  flag_reason TEXT,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_reviews_business ON reviews(business_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_reviews_approved ON reviews(approved);

-- ============================================
-- PARTNERSHIPS TABLE (B2B Networking)
-- ============================================
CREATE TABLE partnerships (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  business_a_id UUID REFERENCES businesses(id) NOT NULL,
  business_b_id UUID REFERENCES businesses(id) NOT NULL,
  
  -- Partnership type
  type VARCHAR(50), -- referral, cross-promotion, co-marketing
  
  -- Tracking
  referrals_sent INTEGER DEFAULT 0,
  referrals_received INTEGER DEFAULT 0,
  
  -- Status
  status VARCHAR(50) DEFAULT 'pending', -- pending, active, inactive
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Prevent duplicate partnerships
  UNIQUE(business_a_id, business_b_id)
);

-- ============================================
-- SUBSCRIPTIONS TABLE
-- ============================================
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  business_id UUID REFERENCES businesses(id) NOT NULL,
  user_id UUID REFERENCES users(id),
  
  -- Stripe
  stripe_customer_id VARCHAR(255),
  stripe_subscription_id VARCHAR(255),
  
  -- Plan
  tier VARCHAR(50) NOT NULL,
  price DECIMAL(10, 2),
  interval VARCHAR(20), -- month, year
  
  -- Status
  status VARCHAR(50) DEFAULT 'active', -- active, past_due, canceled, expired
  
  -- Billing
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  cancel_at_period_end BOOLEAN DEFAULT FALSE,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_business ON subscriptions(business_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);

-- ============================================
-- ANALYTICS TABLE
-- ============================================
CREATE TABLE analytics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  business_id UUID REFERENCES businesses(id),
  
  -- Metrics
  metric VARCHAR(100) NOT NULL, -- page_view, click, lead, call
  value DECIMAL(10, 2) DEFAULT 1,
  
  -- Context
  source VARCHAR(100),
  medium VARCHAR(100),
  campaign VARCHAR(100),
  
  -- User
  ip_address VARCHAR(50),
  user_agent TEXT,
  
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_analytics_business ON analytics(business_id);
CREATE INDEX idx_analytics_metric ON analytics(metric);
CREATE INDEX idx_analytics_created ON analytics(created_at);

-- ============================================
-- EVENTS TABLE (Chamber Events)
-- ============================================
CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  
  -- Date/time
  event_date DATE,
  start_time TIME,
  end_time TIME,
  
  -- Location
  location VARCHAR(255),
  address TEXT,
  city VARCHAR(100),
  
  -- Organizer
  chamber_id VARCHAR(255),
  chamber_name VARCHAR(255),
  
  -- Registration
  registration_url VARCHAR(500),
  cost VARCHAR(100),
  
  -- Metadata
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_events_city ON events(city);

-- ============================================
-- FUNCTIONS
-- ============================================

-- Update timestamp on modification
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to tables
CREATE TRIGGER update_businesses_updated_at
  BEFORE UPDATE ON businesses
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_leads_updated_at
  BEFORE UPDATE ON leads
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_reviews_updated_at
  BEFORE UPDATE ON reviews
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_subscriptions_updated_at
  BEFORE UPDATE ON subscriptions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

-- ============================================
-- VIEWS
-- ============================================

-- Featured businesses view
CREATE VIEW featured_businesses AS
SELECT * FROM businesses
WHERE verified = TRUE
  AND tier IN ('featured', 'premium', 'elite')
ORDER BY rating DESC, review_count DESC;

-- Recent leads view
CREATE VIEW recent_leads AS
SELECT 
  l.*,
  b.name as business_name,
  b.city as business_city
FROM leads l
LEFT JOIN businesses b ON l.business_id = b.id
ORDER BY l.created_at DESC
LIMIT 100;

-- Business stats view
CREATE VIEW business_stats AS
SELECT 
  b.id,
  b.name,
  COUNT(DISTINCT l.id) as lead_count,
  COUNT(DISTINCT r.id) as review_count,
  AVG(r.rating) as avg_rating,
  SUM(a.value) as total_views
FROM businesses b
LEFT JOIN leads l ON b.id = l.business_id
LEFT JOIN reviews r ON b.id = r.business_id AND r.approved = TRUE
LEFT JOIN analytics a ON b.id = a.business_id
GROUP BY b.id, b.name;

-- ============================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================

-- Enable RLS
ALTER TABLE businesses ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- Public can read verified businesses
CREATE POLICY "Public can view verified businesses"
  ON businesses FOR SELECT
  USING (verified = TRUE);

-- Business owners can update their own business
CREATE POLICY "Business owners can update own business"
  ON businesses FOR UPDATE
  USING (created_by = auth.uid()::text);

-- Leads are private (admin only)
CREATE POLICY "Only admins can view all leads"
  ON leads FOR SELECT
  USING (auth.jwt() ->> 'role' = 'admin');

-- ============================================
-- SEED DATA
-- ============================================

-- Insert existing businesses from current directory
INSERT INTO businesses (name, slug, category, city, phone, description, verified, tier) VALUES
('Faith RLR LLC', 'faith-rlr-llc', 'Tools & Equipment', 'Manteca', '(209) 767-3328', 'Mobile tool distributor serving automotive technicians. Owner-operated with personalized service, after-hours support, and competitive pricing.', TRUE, 'featured'),
('Dr. Alan S. Lee DDS', 'dr-alan-lee', 'Dental', 'Manteca', '(209) 239-2990', '30+ years serving Manteca with comprehensive dental care including implants, whitening, crowns, and preventive care. Family-owned practice.', TRUE, 'featured'),
('Matt Safdari', 'matt-safdari', 'Financial', 'Central Valley', '(209) 640-5103', 'Financial planning, life insurance, retirement strategies, wealth management. Helping families achieve financial independence.', TRUE, 'verified');

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON TABLE businesses IS 'Directory of local businesses';
COMMENT ON TABLE users IS 'Business owner accounts';
COMMENT ON TABLE leads IS 'Customer inquiries and quote requests';
COMMENT ON TABLE reviews IS 'Customer reviews for businesses';
COMMENT ON TABLE partnerships IS 'B2B networking relationships';
COMMENT ON TABLE subscriptions IS 'Premium listing subscriptions';
COMMENT ON TABLE analytics IS 'Page views, clicks, and conversions';
COMMENT ON TABLE events IS 'Chamber and community events';