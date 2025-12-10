// Global variables
let token = localStorage.getItem('token');

// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});

function checkAuth() {
    if (token) {
        showCalculator();
        document.getElementById('logout-btn').style.display = 'block';
    } else {
        showAuth();
        document.getElementById('logout-btn').style.display = 'none';
    }
}

function showAuth() {
    document.getElementById('auth-section').style.display = 'block';
    document.getElementById('calculator-section').style.display = 'none';
}

function showCalculator() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('calculator-section').style.display = 'block';
}

// Logout functionality
const logoutBtn = document.getElementById('logout-btn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('token');
        token = null;
        showAuth();
        logoutBtn.style.display = 'none';
        showMessage('Logged out successfully', 'success');
    });
}

// Toggle between login and register
const toggleAuthLink = document.getElementById('toggle-auth-link');
const authTitle = document.getElementById('auth-title');
const authSubmitBtn = document.getElementById('auth-submit-btn');
const emailField = document.getElementById('email');
const toggleText = document.getElementById('toggle-text');

let isLoginMode = true;

if (toggleAuthLink) {
    toggleAuthLink.addEventListener('click', (e) => {
        e.preventDefault();
        isLoginMode = !isLoginMode;
        
        if (isLoginMode) {
            authTitle.textContent = 'Login';
            authSubmitBtn.textContent = 'Login';
            emailField.style.display = 'none';
            emailField.removeAttribute('required');
            toggleText.textContent = "Don't have an account?";
            toggleAuthLink.textContent = 'Register';
        } else {
            authTitle.textContent = 'Register';
            authSubmitBtn.textContent = 'Register';
            emailField.style.display = 'block';
            emailField.setAttribute('required', 'required');
            toggleText.textContent = 'Already have an account?';
            toggleAuthLink.textContent = 'Login';
        }
    });
}

// Handle auth form submission
const authForm = document.getElementById('auth-form');
if (authForm) {
    authForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const email = document.getElementById('email').value;
        
        if (isLoginMode) {
            await login(username, password);
        } else {
            await register(username, email, password);
        }
    });
}

async function register(username, email, password) {
    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('Registration successful! Please login.', 'success');
            // Switch to login mode
            toggleAuthLink.click();
        } else {
            showMessage(data.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    }
}

async function login(username, password) {
    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch('/auth/login', {
            method: 'POST',
            body: formData,
        });
        
        const data = await response.json();
        
        if (response.ok) {
            token = data.access_token;
            localStorage.setItem('token', token);
            showMessage('Login successful!', 'success');
            checkAuth();
        } else {
            showMessage(data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage('Network error. Please try again.', 'error');
    }
}

function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.error, .success');
    existingMessages.forEach(msg => msg.remove());
    
    const messageDiv = document.createElement('div');
    messageDiv.className = type;
    messageDiv.textContent = message;
    
    const form = document.getElementById('auth-form') || document.getElementById('calc-form');
    if (form) {
        form.parentNode.insertBefore(messageDiv, form);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
}

// Helper function to make authenticated requests
async function fetchWithAuth(url, options = {}) {
    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
    };
    
    return fetch(url, { ...options, headers });
}
