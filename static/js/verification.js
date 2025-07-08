document.addEventListener('DOMContentLoaded', function() {
    const codeInputs = document.querySelectorAll('.code-input');
    const verifyBtn = document.getElementById('verify-btn');
    const resendBtn = document.getElementById('resend-btn');
    const errorMessage = document.getElementById('error-message');
    const successMessage = document.getElementById('success-message');
    const timerElement = document.getElementById('timer');
    const loadingSpinner = document.querySelector('.verification-loading');

    let timeLeft = 300; // 5 minutes in seconds
    let timerInterval;

    // Auto-focus and move to next input
    codeInputs.forEach((input, index) => {
        input.addEventListener('input', function(e) {
            const value = e.target.value;
            if (value.length === 1) {
                input.classList.add('filled');
                if (index < codeInputs.length - 1) {
                    codeInputs[index + 1].focus();
                }
            } else {
                input.classList.remove('filled');
            }
        });

        input.addEventListener('keydown', function(e) {
            if (e.key === 'Backspace' && !e.target.value && index > 0) {
                codeInputs[index - 1].focus();
            }
        });
    });

    // Verify button click
    verifyBtn.addEventListener('click', function() {
        const code = Array.from(codeInputs).map(input => input.value).join('');
        
        if (code.length !== 6) {
            showError('Please enter the complete 6-digit code.');
            return;
        }

        // Show loading
        loadingSpinner.style.display = 'inline-block';
        verifyBtn.disabled = true;

        // Simulate verification (replace with actual API call)
        setTimeout(() => {
            if (code === '123456') { // Demo code
                showSuccess();
            } else {
                showError('Invalid verification code. Please try again.');
                clearInputs();
            }
            loadingSpinner.style.display = 'none';
            verifyBtn.disabled = false;
        }, 2000);
    });

    // Resend functionality
    function resendCode() {
        clearInputs();
        timeLeft = 300;
        startTimer();
        showSuccess('New verification code sent to your email!');
    }

    resendBtn.addEventListener('click', resendCode);

    // Timer functionality
    function startTimer() {
        clearInterval(timerInterval);
        timerInterval = setInterval(() => {
            timeLeft--;
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                timerElement.textContent = '00:00';
                showError('Verification code has expired. Please request a new one.');
            }
        }, 1000);
    }

    // Utility functions
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        successMessage.style.display = 'none';
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 5000);
    }

    function showSuccess(message = 'Email verified successfully! Redirecting to login...') {
        successMessage.textContent = message;
        successMessage.style.display = 'block';
        errorMessage.style.display = 'none';
        
        if (message.includes('Redirecting')) {
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
        }
    }

    function clearInputs() {
        codeInputs.forEach(input => {
            input.value = '';
            input.classList.remove('filled');
        });
        codeInputs[0].focus();
    }

    // Initialize
    startTimer();
    codeInputs[0].focus();

    // Set demo email (replace with actual user email)
    document.getElementById('user-email').textContent = 'user@example.com';
});