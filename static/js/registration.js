// registration.js - Frontend validation and secure form submission

function escapeHTML(str) {
    return str.replace(/[&<>'"`=\/]/g, function (s) {
        return ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;',
            '`': '&#96;', '=': '&#61;', '/': '&#47;'
        })[s];
    });
}

function validateEmail(email) {
    return /^[\w-.]+@[\w-]+\.[a-zA-Z]{2,}$/.test(email);
}

function validatePhone(phone) {
    return /^\+?\d{10,15}$/.test(phone);
}

function validatePassword(pw) {
    // At least 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
    return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]).{8,}$/.test(pw);
}

document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const errorDiv = document.getElementById('reg-error');
    errorDiv.textContent = '';

    const name = escapeHTML(document.getElementById('reg-name').value.trim());
    const email = escapeHTML(document.getElementById('reg-email').value.trim());
    const phone = escapeHTML(document.getElementById('reg-phone').value.trim());
    const age = escapeHTML(document.getElementById('reg-age').value.trim());
    const gender = escapeHTML(document.getElementById('reg-gender').value);
    const address = escapeHTML(document.getElementById('reg-address').value.trim());
    const qualification = escapeHTML(document.getElementById('reg-qualification').value.trim());
    const password = document.getElementById('reg-password').value;
    const confirm = document.getElementById('reg-confirm').value;

    if (!name || !email || !phone || !age || !gender || !address || !qualification || !password || !confirm) {
        errorDiv.textContent = 'All fields are required.';
        return;
    }
    if (!validateEmail(email)) {
        errorDiv.textContent = 'Invalid email format.';
        return;
    }
    if (!validatePhone(phone)) {
        errorDiv.textContent = 'Invalid phone number.';
        return;
    }
    if (parseInt(age) < 10 || parseInt(age) > 120) {
        errorDiv.textContent = 'Age must be between 10 and 120.';
        return;
    }
    if (!validatePassword(password)) {
        errorDiv.textContent = 'Password must be at least 8 characters, include uppercase, lowercase, number, and special character.';
        return;
    }
    if (password !== confirm) {
        errorDiv.textContent = 'Passwords do not match.';
        return;
    }

    // Prepare data
    const data = {
        name, email, phone, age, gender, address, qualification,
        password: escapeHTML(password) // escape for extra safety
    };

    // Send data securely via fetch
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(resp => {
        if (resp.success) {
            window.location.href = '/login';
        } else {
            errorDiv.textContent = resp.error || 'Registration failed.';
        }
    })
    .catch(() => {
        errorDiv.textContent = 'Network error.';
    });
});
