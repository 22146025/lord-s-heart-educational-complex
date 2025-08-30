// API Configuration
const API_BASE_URL = 'https://syllas20.pythonanywhere.com/api';

// Utility functions
function showMessage(message, type = 'success') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    if (type === 'success') {
        messageDiv.style.backgroundColor = '#28a745';
    } else if (type === 'error') {
        messageDiv.style.backgroundColor = '#dc3545';
    } else {
        messageDiv.style.backgroundColor = '#ffc107';
        messageDiv.style.color = '#000';
    }
    
    document.body.appendChild(messageDiv);
    
    // Remove message after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// API Functions
async function submitAdmissionApplication(formData) {
    try {
        const response = await fetch(`${API_BASE_URL}/admissions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to submit application');
        }
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error submitting admission application:', error);
        throw error;
    }
}

async function submitContactMessage(formData) {
    try {
        const response = await fetch(`${API_BASE_URL}/contact/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to send message');
        }
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error submitting contact message:', error);
        throw error;
    }
}

// Form handling functions
function handleAdmissionFormSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Convert FormData to object
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    // Map form field names to API field names
    const apiData = {
        surname: data.surname,
        first_name: data.firstname,
        other_names: data.othernames,
        date_of_birth: data.dob,
        age: parseInt(data.age) || null,
        gender: data.gender?.toLowerCase(),
        place_of_birth: data.placeofbirth,
        region_of_birth: data.regionofbirth,
        home_town: data.hometown,
        region_of_home_town: data.regionhometown,
        last_school_attended: data.lastschool,
        location_of_last_school: data.schoollocation,
        class_before_admission: data.previousclass,
        religious_denomination: data.religion,
        hobbies: data.hobbies,
        disability_or_allergy: data.disability,
        father_name: data.fathername,
        mother_name: data.mothername,
        father_occupation: data.fatheroccupation,
        mother_occupation: data.motheroccupation,
        father_contact: data.fathercontact,
        mother_contact: data.mothercontact,
        father_email: data.fatheremail,
        mother_email: data.motheremail,
        postal_address: data.postal,
        place_of_residence: data.residence,
        house_number: data.housenumber
    };
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Submitting...';
    submitBtn.disabled = true;
    
    submitAdmissionApplication(apiData)
        .then(result => {
            showMessage('Application submitted successfully! We will contact you soon.', 'success');
            form.reset();
        })
        .catch(error => {
            showMessage(`Error: ${error.message}`, 'error');
        })
        .finally(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
}

function handleContactFormSubmit(event) {
    event.preventDefault();
    
    console.log('Contact form submitted!');
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Get form inputs
    const nameInput = form.querySelector('input[name="name"]');
    const emailInput = form.querySelector('input[name="email"]');
    const messageInput = form.querySelector('textarea[name="message"]');
    
    console.log('Form inputs found:', { nameInput, emailInput, messageInput });
    
    const data = {
        name: nameInput.value,
        email: emailInput.value,
        message: messageInput.value
    };
    
    console.log('Sending data:', data);
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    
    submitContactMessage(data)
        .then(result => {
            showMessage('Message sent successfully! We will get back to you soon.', 'success');
            form.reset();
        })
        .catch(error => {
            showMessage(`Error: ${error.message}`, 'error');
        })
        .finally(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
}

// Initialize form handlers when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing form handlers...');
    console.log('Current pathname:', window.location.pathname);
    
    // Handle admission form
    const admissionForm = document.querySelector('form');
    if (admissionForm && window.location.pathname.includes('admissions.html')) {
        console.log('Admission form found and handler attached');
        admissionForm.addEventListener('submit', handleAdmissionFormSubmit);
    }
    
    // Handle contact form
    const contactForm = document.querySelector('.contact-form');
    console.log('Contact form found:', contactForm);
    if (contactForm && window.location.pathname.includes('contact.html')) {
        console.log('Contact form handler attached');
        contactForm.addEventListener('submit', handleContactFormSubmit);
    } else {
        console.log('Contact form not found or not on contact page');
    }
});

// Add CSS for message animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .message {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
`;
document.head.appendChild(style);
