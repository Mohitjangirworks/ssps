// Global variables
let currentNotification = 0;
let notificationInterval;
const notificationItems = document.querySelectorAll('.notification-item');

// Configuration
const API_BASE_URL = 'http://localhost:5000/api'; // SQLite Backend API URL

// Language data
const translations = {
    en: {
        home: 'Home',
        about: 'About Us',
        academics: 'Academics',
        facilities: 'Facilities',
        admissions: 'Admissions',
        results: 'Results',
        events: 'Events',
        faculty: 'Faculty',
        contact: 'Contact',
        applyNow: 'Apply Now',
        learnMore: 'Learn More',
        excellenceInEducation: 'Excellence in Education',
        nurturingMinds: 'Nurturing young minds for a brighter tomorrow'
    },
    hi: {
        home: 'होम',
        about: 'हमारे बारे में',
        academics: 'शिक्षा',
        facilities: 'सुविधाएं',
        admissions: 'प्रवेश',
        results: 'परिणाम',
        events: 'कार्यक्रम',
        faculty: 'संकाय',
        contact: 'संपर्क',
        applyNow: 'अभी आवेदन करें',
        learnMore: 'और जानें',
        excellenceInEducation: 'शिक्षा में उत्कृष्टता',
        nurturingMinds: 'उज्जवल कल के लिए युवा मन का पोषण'
    }
};

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeWebsite();
});

// Initialize all website functionality
function initializeWebsite() {
    initializeNavigation();
    initializeNotifications();
    initializeScrollEffects();
    initializeForms();
    initializeTabs();
    initializeLanguageToggle();
    initializeLightbox();
    initializeLoadingSpinner();
    initializeScrollToTop();
    
    // Load dynamic content
    loadLatestNews();
    loadEventData();
    loadResultsData();
}

// Navigation functionality
function initializeNavigation() {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Mobile menu toggle
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }

    // Smooth scroll for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = 120; // Account for fixed header
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });

                // Close mobile menu if open
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');

                // Update active link
                updateActiveNavLink(this);
            }
        });
    });

    // Update active nav link on scroll
    window.addEventListener('scroll', updateActiveNavOnScroll);
}

// Update active navigation link
function updateActiveNavLink(activeLink) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    activeLink.classList.add('active');
}

// Update navigation based on scroll position
function updateActiveNavOnScroll() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let currentSection = '';
    const scrollPos = window.scrollY + 150;

    sections.forEach(section => {
        const sectionTop = section.getBoundingClientRect().top + window.pageYOffset;
        const sectionHeight = section.offsetHeight;
        
        if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
}

// Initialize notifications
function initializeNotifications() {
    if (notificationItems.length === 0) return;

    // Show first notification
    notificationItems[0].classList.add('active');

    // Auto rotate notifications
    startNotificationRotation();

    // Pause on hover
    const notificationsBar = document.querySelector('.notifications-bar');
    if (notificationsBar) {
        notificationsBar.addEventListener('mouseenter', pauseNotificationRotation);
        notificationsBar.addEventListener('mouseleave', startNotificationRotation);
    }
}

// Start notification rotation
function startNotificationRotation() {
    notificationInterval = setInterval(() => {
        nextNotification();
    }, 4000);
}

// Pause notification rotation
function pauseNotificationRotation() {
    clearInterval(notificationInterval);
}

// Next notification
function nextNotification() {
    notificationItems[currentNotification].classList.remove('active');
    currentNotification = (currentNotification + 1) % notificationItems.length;
    notificationItems[currentNotification].classList.add('active');
}

// Previous notification
function prevNotification() {
    notificationItems[currentNotification].classList.remove('active');
    currentNotification = currentNotification === 0 ? notificationItems.length - 1 : currentNotification - 1;
    notificationItems[currentNotification].classList.add('active');
}


// Scroll effects
function initializeScrollEffects() {
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll('.highlight-card, .academic-level, .facility-card, .faculty-card, .achievement-card');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Form handling
function initializeForms() {
    // Admission form
    const admissionForm = document.getElementById('admissionForm');
    if (admissionForm) {
        admissionForm.addEventListener('submit', handleAdmissionForm);
    }

    // Contact form
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactForm);
    }
}

// Handle admission form submission
async function handleAdmissionForm(e) {
    e.preventDefault();
    showLoading();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    try {
        const response = await fetch(`${API_BASE_URL}/admissions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showAlert('success', 'Application submitted successfully! We will contact you soon.');
            e.target.reset();
            hideApplicationForm();
        } else {
            throw new Error('Failed to submit application');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('error', 'Failed to submit application. Please try again later.');
    } finally {
        hideLoading();
    }
}

// Handle contact form submission
async function handleContactForm(e) {
    e.preventDefault();
    showLoading();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    try {
        const response = await fetch(`${API_BASE_URL}/contact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showAlert('success', 'Message sent successfully! We will get back to you soon.');
            e.target.reset();
        } else {
            throw new Error('Failed to send message');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('error', 'Failed to send message. Please try again later.');
    } finally {
        hideLoading();
    }
}

// Tab functionality
function initializeTabs() {
    // Results tabs
    const resultsTabBtns = document.querySelectorAll('.results-tabs .tab-btn');
    resultsTabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.textContent.toLowerCase().replace(' ', '').replace('class', 'class').replace('xii', '12').replace('x', '10');
            showResultsTab(tabName);
        });
    });

    // Events tabs
    const eventsTabBtns = document.querySelectorAll('.events-tabs .tab-btn');
    eventsTabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.textContent.toLowerCase().replace(' ', '');
            showEventsTab(tabName);
        });
    });
}

// Show results tab
function showResultsTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.results-tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.results-tabs .tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const targetTab = document.getElementById(tabName);
    if (targetTab) {
        targetTab.classList.add('active');
    }

    // Add active class to clicked button
    event.target.classList.add('active');
}

// Show events tab
function showEventsTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.events-tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.events-tabs .tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const targetTab = document.getElementById(tabName);
    if (targetTab) {
        targetTab.classList.add('active');
    }

    // Add active class to clicked button
    event.target.classList.add('active');
}

// Application form toggle
function showApplicationForm() {
    const form = document.getElementById('application-form');
    if (form) {
        form.style.display = 'block';
        form.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function hideApplicationForm() {
    const form = document.getElementById('application-form');
    if (form) {
        form.style.display = 'none';
    }
}

// Language toggle functionality
function initializeLanguageToggle() {
    const langButtons = document.querySelectorAll('.lang-btn');
    let currentLanguage = 'en';

    langButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons
            langButtons.forEach(b => b.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Get language code
            const lang = this.id === 'lang-en' ? 'en' : 'hi';
            
            if (lang !== currentLanguage) {
                currentLanguage = lang;
                translatePage(lang);
            }
        });
    });
}

// Translate page content
function translatePage(lang) {
    const elements = document.querySelectorAll('[data-translate]');
    
    elements.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[lang] && translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });
}

// Lightbox functionality
function initializeLightbox() {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const closeBtn = document.querySelector('.lightbox-close');

    if (closeBtn) {
        closeBtn.addEventListener('click', closeLightbox);
    }

    if (lightbox) {
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });
    }

    // ESC key to close lightbox
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeLightbox();
        }
    });
}

// Open lightbox
function openLightbox(imageSrc) {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    
    if (lightbox && lightboxImg) {
        lightboxImg.src = imageSrc;
        lightbox.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

// Close lightbox
function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    
    if (lightbox) {
        lightbox.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Loading spinner
function initializeLoadingSpinner() {
    // Loading spinner is controlled by showLoading() and hideLoading() functions
}

function showLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = 'flex';
    }
}

function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = 'none';
    }
}

// Scroll to top functionality
function initializeScrollToTop() {
    // Create scroll to top button
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #FF6B35, #F7931E);
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(255, 107, 53, 0.3);
    `;

    document.body.appendChild(scrollBtn);

    // Show/hide scroll button
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 500) {
            scrollBtn.style.display = 'flex';
        } else {
            scrollBtn.style.display = 'none';
        }
    });

    // Scroll to top on click
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Alert system
function showAlert(type, message) {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.custom-alert');
    existingAlerts.forEach(alert => alert.remove());

    // Create alert element
    const alert = document.createElement('div');
    alert.className = `custom-alert alert-${type}`;
    alert.style.cssText = `
        position: fixed;
        top: 100px;
        right: 30px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        z-index: 10000;
        max-width: 400px;
        display: flex;
        align-items: center;
        gap: 10px;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    `;

    // Set background color based on type
    if (type === 'success') {
        alert.style.background = 'linear-gradient(135deg, #4CAF50, #45a049)';
        alert.innerHTML = '<i class="fas fa-check-circle"></i>' + message;
    } else if (type === 'error') {
        alert.style.background = 'linear-gradient(135deg, #f44336, #d32f2f)';
        alert.innerHTML = '<i class="fas fa-exclamation-circle"></i>' + message;
    }

    document.body.appendChild(alert);

    // Show alert
    setTimeout(() => {
        alert.style.transform = 'translateX(0)';
    }, 100);

    // Hide alert after 5 seconds
    setTimeout(() => {
        alert.style.transform = 'translateX(100%)';
        setTimeout(() => {
            alert.remove();
        }, 300);
    }, 5000);
}

// Load latest news from API
async function loadLatestNews() {
    try {
        const response = await fetch(`${API_BASE_URL}/news`);
        if (response.ok) {
            const news = await response.json();
            updateNewsTicker(news);
        }
    } catch (error) {
        console.error('Error loading news:', error);
    }
}

// Update news ticker
function updateNewsTicker(newsItems) {
    const tickerContent = document.getElementById('ticker-content');
    if (tickerContent && newsItems.length > 0) {
        tickerContent.innerHTML = newsItems.map(item => 
            `<div class="ticker-item">${item.emoji} ${item.text}</div>`
        ).join('');
    }
}

// Load event data
async function loadEventData() {
    try {
        const response = await fetch(`${API_BASE_URL}/events`);
        if (response.ok) {
            const events = await response.json();
            updateEventsSection(events);
        }
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

// Update events section
function updateEventsSection(events) {
    const upcomingEvents = events.filter(event => new Date(event.date) > new Date());
    const pastEvents = events.filter(event => new Date(event.date) <= new Date());

    updateEventsList('upcoming', upcomingEvents);
    updateEventsList('past', pastEvents);
}

// Update events list
function updateEventsList(type, events) {
    const container = document.querySelector(`#${type} .events-list`);
    if (container && events.length > 0) {
        container.innerHTML = events.map(event => {
            const date = new Date(event.date);
            const day = date.getDate();
            const month = date.toLocaleLString('en', { month: 'short' });
            
            return `
                <div class="event-card">
                    <div class="event-date">
                        <span class="date">${day}</span>
                        <span class="month">${month}</span>
                    </div>
                    <div class="event-content">
                        <h4>${event.title}</h4>
                        <p>${event.description}</p>
                        <div class="event-meta">
                            <span><i class="fas fa-clock"></i> ${event.time || 'TBD'}</span>
                            <span><i class="fas fa-map-marker-alt"></i> ${event.location}</span>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }
}

// Load results data
async function loadResultsData() {
    try {
        const response = await fetch(`${API_BASE_URL}/results`);
        if (response.ok) {
            const results = await response.json();
            updateResultsSection(results);
        }
    } catch (error) {
        console.error('Error loading results:', error);
    }
}

// Update results section
function updateResultsSection(results) {
    // Update Class XII results
    updateResultsTable('class12', results.class12);
    
    // Update Class X results
    updateResultsTable('class10', results.class10);
    
    // Update toppers
    if (results.toppers) {
        updateToppersSection(results.toppers);
    }
}

// Update results table
function updateResultsTable(className, data) {
    const tableBody = document.querySelector(`#${className} .results-table tbody`);
    if (tableBody && data && data.length > 0) {
        tableBody.innerHTML = data.map(year => `
            <tr>
                <td>${year.year}</td>
                <td>${year.passRate}</td>
                <td>${year.above90}</td>
                <td>${year.above95}</td>
                <td>${year.districtRank}</td>
                <td>${year.stateRank}</td>
            </tr>
        `).join('');
    }
}

// Update toppers section
function updateToppersSection(toppers) {
    const toppersGrid = document.querySelector('.toppers-grid');
    if (toppersGrid && toppers.length > 0) {
        toppersGrid.innerHTML = toppers.map(topper => `
            <div class="topper-card">
                <img src="${topper.photo || 'images/default-student.jpg'}" alt="${topper.name}">
                <h5>${topper.name}</h5>
                <p>${topper.percentage}% - ${topper.stream}</p>
                <p>${topper.achievement}</p>
            </div>
        `).join('');
    }
}

// Utility function to format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Utility function to validate email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Utility function to validate phone number
function isValidPhone(phone) {
    const phoneRegex = /^[+]?[\d\s\-\(\)]{10,}$/;
    return phoneRegex.test(phone);
}

// Form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    let firstInvalidField = null;

    requiredFields.forEach(field => {
        const value = field.value.trim();
        
        // Remove previous error styling
        field.classList.remove('error');
        
        if (!value) {
            field.classList.add('error');
            isValid = false;
            if (!firstInvalidField) {
                firstInvalidField = field;
            }
        } else if (field.type === 'email' && !isValidEmail(value)) {
            field.classList.add('error');
            isValid = false;
            if (!firstInvalidField) {
                firstInvalidField = field;
            }
        } else if (field.type === 'tel' && !isValidPhone(value)) {
            field.classList.add('error');
            isValid = false;
            if (!firstInvalidField) {
                firstInvalidField = field;
            }
        }
    });

    // Focus on first invalid field
    if (firstInvalidField) {
        firstInvalidField.focus();
        firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    return isValid;
}

// Add error styling for form validation
const style = document.createElement('style');
style.textContent = `
    .form-group input.error,
    .form-group select.error,
    .form-group textarea.error {
        border-color: #f44336 !important;
        box-shadow: 0 0 0 2px rgba(244, 67, 54, 0.2) !important;
    }
`;
document.head.appendChild(style);

// Performance optimization: Lazy load images
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Call lazy loading after DOM is loaded
document.addEventListener('DOMContentLoaded', initializeLazyLoading);

// Export functions for global use
window.nextSlide = nextSlide;
window.previousSlide = previousSlide;
window.currentSlide = currentSlide;
window.showResultsTab = showResultsTab;
window.showEventsTab = showEventsTab;
window.showApplicationForm = showApplicationForm;
window.hideApplicationForm = hideApplicationForm;
window.openLightbox = openLightbox;
window.closeLightbox = closeLightbox;
