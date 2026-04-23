// Central Valley Locals - Business Submission Form
// Uses Netlify Forms for free submission handling

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('business-submit-form');
    const submitButton = form.querySelector('button[type="submit"]');
    const successMessage = document.createElement('div');
    successMessage.className = 'success-message';
    successMessage.innerHTML = `
        <div class="success-icon">✅</div>
        <h2>Submission Received!</h2>
        <p>Thank you for adding your business to Central Valley Locals.</p>
        <p>We'll review your submission and contact you within 24-48 hours for verification.</p>
        <a href="index.html" class="btn btn-primary">Return to Directory</a>
    `;
    
    // Set submission date
    document.getElementById('submission_date').value = new Date().toISOString();

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validate required fields
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        // Show loading state
        submitButton.disabled = true;
        submitButton.textContent = 'Submitting...';
        
        // Collect form data
        const formData = new FormData(form);
        
        // Add Netlify form name (required for Netlify Forms)
        formData.append('form-name', 'business-submission');
        
        try {
            // Submit to Netlify Forms
            const response = await fetch('/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                },
                body: new URLSearchParams(formData).toString()
            });

            if (response.ok) {
                // Show success message
                form.style.display = 'none';
                document.querySelector('.form-sidebar').style.display = 'none';
                form.parentElement.appendChild(successMessage);
                successMessage.classList.add('show');
                
                // Scroll to top
                window.scrollTo({ top: 0, behavior: 'smooth' });
                
                // Store submission locally as backup
                storeSubmissionLocally(formData);
            } else {
                throw new Error('Submission failed');
            }
        } catch (error) {
            console.error('Submission error:', error);
            
            // Show error message
            const errorMessage = document.createElement('div');
            errorMessage.className = 'error-message show';
            errorMessage.innerHTML = `
                <p>⚠️ There was an error submitting your form. Please try again or contact us directly.</p>
                <p>Email: info@centralvalleylocals.com</p>
            `;
            form.insertBefore(errorMessage, form.firstChild);
            
            // Reset button
            submitButton.disabled = false;
            submitButton.textContent = 'Submit for Review';
            
            // Store locally as backup
            storeSubmissionLocally(formData);
        }
    });
});

// Store submission locally as backup
function storeSubmissionLocally(formData) {
    const submission = {};
    formData.forEach((value, key) => {
        submission[key] = value;
    });
    submission.stored_at = new Date().toISOString();
    
    // Get existing submissions from localStorage
    const existing = JSON.parse(localStorage.getItem('cvl_submissions') || '[]');
    existing.push(submission);
    
    // Store updated submissions
    localStorage.setItem('cvl_submissions', JSON.stringify(existing));
}

// Auto-save form data (prevents data loss)
const autoSaveFields = [
    'business_name', 'owner_name', 'phone', 'email', 
    'address', 'city', 'description', 'website'
];

autoSaveFields.forEach(fieldId => {
    const field = document.getElementById(fieldId);
    if (field) {
        // Load saved value
        const saved = localStorage.getItem(`cvl_draft_${fieldId}`);
        if (saved) {
            field.value = saved;
        }
        
        // Save on change
        field.addEventListener('input', () => {
            localStorage.setItem(`cvl_draft_${fieldId}`, field.value);
        });
    }
});

// Clear draft after successful submission
function clearDraft() {
    autoSaveFields.forEach(fieldId => {
        localStorage.removeItem(`cvl_draft_${fieldId}`);
    });
}