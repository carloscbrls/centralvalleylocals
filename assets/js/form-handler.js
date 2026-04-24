// Form submission handler for Central Valley Locals
// Connects forms to Supabase

import { supabase } from './supabase-client.js';

// Business submission form
async function handleBusinessSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    // Show loading state
    submitBtn.textContent = 'Submitting...';
    submitBtn.disabled = true;
    
    // Collect form data
    const formData = {
        name: form.business_name.value,
        slug: form.business_name.value.toLowerCase().replace(/[^a-z0-9]+/g, '-').trim('-'),
        category_id: await getCategoryId(form.category.value),
        description: form.services.value || `Local business in ${form.city.value}`,
        phone: form.phone.value,
        email: form.email.value,
        website: form.website.value,
        address: form.address.value,
        city: form.city.value,
        state: 'CA',
        zip_code: form.zip.value,
        is_active: false, // Needs approval
        is_featured: false
    };
    
    try {
        const { data, error } = await supabase
            .from('businesses')
            .insert([formData]);
        
        if (error) throw error;
        
        // Show success
        showSuccess('Thank you! Your business has been submitted for review.');
        form.reset();
        
        // Track conversion
        if (typeof gtag !== 'undefined') {
            gtag('event', 'form_submit', {
                'form_name': 'business_submission',
                'form_id': 'business-submit-form'
            });
        }
        
    } catch (error) {
        console.error('Error submitting business:', error);
        showError('There was an error submitting your business. Please try again.');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// Lead/contact form
async function handleLeadSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    
    const formData = {
        business_id: form.business_id?.value || null,
        customer_name: form.name.value,
        customer_email: form.email.value,
        customer_phone: form.phone?.value || null,
        message: form.message.value
    };
    
    try {
        const { data, error } = await supabase
            .from('leads')
            .insert([formData]);
        
        if (error) throw error;
        
        showSuccess('Thank you! We\'ll be in touch soon.');
        form.reset();
        
        // Track conversion
        if (typeof gtag !== 'undefined') {
            gtag('event', 'form_submit', {
                'form_name': 'lead_submission',
                'form_id': 'lead-form'
            });
        }
        
    } catch (error) {
        console.error('Error submitting lead:', error);
        showError('There was an error. Please try again.');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// Review submission
async function handleReviewSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Submitting...';
    submitBtn.disabled = true;
    
    const formData = {
        business_id: form.business_id.value,
        reviewer_name: form.name.value,
        rating: parseInt(form.rating.value),
        review_text: form.review.value,
        is_approved: false // Needs approval
    };
    
    try {
        const { data, error } = await supabase
            .from('reviews')
            .insert([formData]);
        
        if (error) throw error;
        
        showSuccess('Thank you for your review! It will be visible once approved.');
        form.reset();
        
    } catch (error) {
        console.error('Error submitting review:', error);
        showError('There was an error. Please try again.');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// Helper: Get category ID from slug
async function getCategoryId(slug) {
    const { data } = await supabase
        .from('categories')
        .select('id')
        .eq('slug', slug)
        .single();
    
    return data?.id || null;
}

// Helper: Show success message
function showSuccess(message) {
    const container = document.createElement('div');
    container.className = 'form-success';
    container.innerHTML = `
        <div class="success-message">
            <span class="success-icon">✓</span>
            <p>${message}</p>
        </div>
    `;
    
    const form = document.querySelector('form');
    form.parentNode.insertBefore(container, form.nextSibling);
    
    // Remove after 5 seconds
    setTimeout(() => container.remove(), 5000);
}

// Helper: Show error message
function showError(message) {
    const container = document.createElement('div');
    container.className = 'form-error';
    container.innerHTML = `
        <div class="error-message">
            <span class="error-icon">⚠️</span>
            <p>${message}</p>
        </div>
    `;
    
    const form = document.querySelector('form');
    form.parentNode.insertBefore(container, form.nextSibling);
    
    // Remove after 5 seconds
    setTimeout(() => container.remove(), 5000);
}

// Initialize forms
function initForms() {
    const businessForm = document.getElementById('business-submit-form');
    if (businessForm) {
        businessForm.addEventListener('submit', handleBusinessSubmit);
    }
    
    const leadForm = document.getElementById('lead-form');
    if (leadForm) {
        leadForm.addEventListener('submit', handleLeadSubmit);
    }
    
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', handleReviewSubmit);
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initForms);

export { handleBusinessSubmit, handleLeadSubmit, handleReviewSubmit };