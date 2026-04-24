// Central Valley Locals - Supabase Client
// Connects the static site to the Supabase database

import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'

// Supabase Configuration
const SUPABASE_URL = 'https://nktjzwwenmefadtavahn.supabase.co'
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rdGp6d3dlbm1lZmFkdGF2YWhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU0NjY2NjgsImV4cCI6MjA2MTA0MjY2OH0.4hVqTgd3Vb0lOqpN0XjRlQJZGqR0Zm0W8RjZQGJZGJM'

// Initialize Supabase client
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// Export for use in other modules
export { supabase }

// ============================================
// API FUNCTIONS
// ============================================

/**
 * Get all categories
 */
async function getCategories() {
  const { data, error } = await supabase
    .from('categories')
    .select('*')
    .order('name')
  
  if (error) {
    console.error('Error fetching categories:', error)
    return []
  }
  
  return data
}

/**
 * Get all businesses (optionally filtered by category)
 */
async function getBusinesses(options = {}) {
  let query = supabase
    .from('businesses')
    .select(`
      *,
      categories(name, slug)
    `)
    .eq('is_active', true)
    .order('name')
  
  if (options.category) {
    query = query.eq('category_id', options.category)
  }
  
  if (options.city) {
    query = query.eq('city', options.city)
  }
  
  if (options.featured) {
    query = query.eq('is_featured', true)
  }
  
  if (options.limit) {
    query = query.limit(options.limit)
  }
  
  const { data, error } = await query
  
  if (error) {
    console.error('Error fetching businesses:', error)
    return []
  }
  
  return data
}

/**
 * Get a single business by slug
 */
async function getBusiness(slug) {
  const { data, error } = await supabase
    .from('businesses')
    .select(`
      *,
      categories(name, slug)
    `)
    .eq('slug', slug)
    .eq('is_active', true)
    .single()
  
  if (error) {
    console.error('Error fetching business:', error)
    return null
  }
  
  return data
}

/**
 * Get featured businesses for homepage
 */
async function getFeaturedBusinesses() {
  return getBusinesses({ featured: true, limit: 6 })
}

/**
 * Search businesses by query
 */
async function searchBusinesses(query) {
  const { data, error } = await supabase
    .from('businesses')
    .select(`
      *,
      categories(name, slug)
    `)
    .eq('is_active', true)
    .or(`name.ilike.%${query}%,description.ilike.%${query}%,city.ilike.%${query}%`)
    .limit(20)
  
  if (error) {
    console.error('Error searching businesses:', error)
    return []
  }
  
  return data
}

/**
 * Submit a new business (public form)
 */
async function submitBusiness(formData) {
  const { data, error } = await supabase
    .from('businesses')
    .insert([{
      name: formData.name,
      slug: formData.name.toLowerCase().replace(/\s+/g, '-'),
      category_id: formData.category_id,
      description: formData.description,
      phone: formData.phone,
      email: formData.email,
      website: formData.website,
      address: formData.address,
      city: formData.city,
      zip_code: formData.zip_code,
      is_active: false, // Needs approval
      is_featured: false
    }])
  
  if (error) {
    console.error('Error submitting business:', error)
    return { success: false, error }
  }
  
  return { success: true, data }
}

/**
 * Submit a lead/contact form
 */
async function submitLead(formData) {
  const { data, error } = await supabase
    .from('leads')
    .insert([{
      business_id: formData.business_id,
      customer_name: formData.name,
      customer_email: formData.email,
      customer_phone: formData.phone,
      message: formData.message
    }])
  
  if (error) {
    console.error('Error submitting lead:', error)
    return { success: false, error }
  }
  
  return { success: true, data }
}

/**
 * Get reviews for a business
 */
async function getBusinessReviews(businessId) {
  const { data, error } = await supabase
    .from('reviews')
    .select('*')
    .eq('business_id', businessId)
    .eq('is_approved', true)
    .order('created_at', { ascending: false })
  
  if (error) {
    console.error('Error fetching reviews:', error)
    return []
  }
  
  return data
}

/**
 * Submit a review
 */
async function submitReview(formData) {
  const { data, error } = await supabase
    .from('reviews')
    .insert([{
      business_id: formData.business_id,
      reviewer_name: formData.name,
      rating: formData.rating,
      review_text: formData.review,
      is_approved: false // Needs approval
    }])
  
  if (error) {
    console.error('Error submitting review:', error)
    return { success: false, error }
  }
  
  return { success: true, data }
}

/**
 * Get upcoming events
 */
async function getEvents(limit = 10) {
  const { data, error } = await supabase
    .from('events')
    .select('*')
    .gte('event_date', new Date().toISOString())
    .order('event_date', { ascending: true })
    .limit(limit)
  
  if (error) {
    console.error('Error fetching events:', error)
    return []
  }
  
  return data
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Format phone number
 */
function formatPhone(phone) {
  if (!phone) return ''
  return phone.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3')
}

/**
 * Generate business card HTML
 */
function businessCard(business) {
  const category = business.categories || { name: 'Uncategorized', slug: 'uncategorized' }
  
  return `
    <article class="business-card" data-business-id="${business.id}">
      <div class="business-card-header">
        ${business.logo_url ? `<img src="${business.logo_url}" alt="${business.name}" class="business-logo">` : ''}
        <span class="business-category">${category.name}</span>
      </div>
      <h3 class="business-name">
        <a href="/business/${business.slug}">${business.name}</a>
      </h3>
      <p class="business-description">${business.description || ''}</p>
      <div class="business-meta">
        ${business.city ? `<span class="business-location">📍 ${business.city}</span>` : ''}
        ${business.phone ? `<span class="business-phone">📞 ${formatPhone(business.phone)}</span>` : ''}
      </div>
      <div class="business-actions">
        ${business.website ? `<a href="${business.website}" target="_blank" rel="noopener" class="btn btn-secondary">Website</a>` : ''}
        <a href="/business/${business.slug}" class="btn btn-primary">View Details</a>
      </div>
    </article>
  `
}

/**
 * Initialize homepage
 */
async function initHomepage() {
  // Load featured businesses
  const featured = await getFeaturedBusinesses()
  const featuredContainer = document.getElementById('featured-businesses')
  
  if (featuredContainer && featured.length > 0) {
    featuredContainer.innerHTML = featured.map(businessCard).join('')
  }
  
  // Load categories
  const categories = await getCategories()
  const categoriesContainer = document.getElementById('categories-grid')
  
  if (categoriesContainer && categories.length > 0) {
    categoriesContainer.innerHTML = categories.map(cat => `
      <a href="/categories/${cat.slug}" class="category-card">
        <span class="category-icon">${getCategoryIcon(cat.slug)}</span>
        <span class="category-name">${cat.name}</span>
      </a>
    `).join('')
  }
  
  // Load upcoming events
  const events = await getEvents(3)
  const eventsContainer = document.getElementById('upcoming-events')
  
  if (eventsContainer && events.length > 0) {
    eventsContainer.innerHTML = events.map(event => `
      <div class="event-card">
        <span class="event-date">${new Date(event.event_date).toLocaleDateString()}</span>
        <h4 class="event-title">${event.title}</h4>
        ${event.location ? `<p class="event-location">📍 ${event.location}</p>` : ''}
      </div>
    `).join('')
  }
}

/**
 * Get category icon
 */
function getCategoryIcon(slug) {
  const icons = {
    'restaurants': '🍽️',
    'retail': '🛍️',
    'health-wellness': '💪',
    'professional-services': '💼',
    'home-services': '🏠',
    'nonprofits': '❤️',
    'real-estate': '🏘️',
    'automotive': '🚗',
    'events': '📅',
    'technology': '💻'
  }
  return icons[slug] || '📌'
}

// Export all functions
export {
  getCategories,
  getBusinesses,
  getBusiness,
  getFeaturedBusinesses,
  searchBusinesses,
  submitBusiness,
  submitLead,
  getBusinessReviews,
  submitReview,
  getEvents,
  formatPhone,
  businessCard,
  initHomepage,
  getCategoryIcon
}