document.addEventListener('DOMContentLoaded', function() {
    // --- Flash Message Popup Closing ---
    const closeButtons = document.getElementsByClassName('popup-close');
    Array.from(closeButtons).forEach(button => {
        button.addEventListener('click', function() {
            const notification = this.closest('.popup-notification');
            if (notification) {
                notification.style.opacity = '0';
                setTimeout(() => notification.style.display = 'none', 300); // Fade-out effect
            }
        });
    });

    // --- Helper to get CSRF token from form ---
    function getCsrfToken() {
      const csrfInput = document.querySelector('#loginform input[name="csrf_token"]');
      return csrfInput ? csrfInput.value : '';
    }

    // --- Show popup utility ---
    function showPopup(message, category = 'danger') { // Added category for styling
      // Create a new popup element dynamically
      const popup = document.createElement('div');
      popup.classList.add('popup-notification', category);
      popup.style.display = 'block';
      popup.innerHTML = `
        <strong>Notice:</strong> ${message}
        <span class="popup-close" style="float:right; padding: 0 10px 0 10px; cursor:pointer;">&times;</span>
      `;

      // Append to body or a specific container
      document.body.appendChild(popup);

      // Add event listener to the new close button
      popup.querySelector('.popup-close').addEventListener('click', function() {
          popup.style.opacity = '0';
          setTimeout(() => popup.remove(), 300); // Fade-out and remove
      });

      // Auto-hide after 5 seconds
      setTimeout(function() {
        popup.style.opacity = '0';
        setTimeout(() => popup.remove(), 300);
      }, 5000);
    }


    // --- Password Eye Toggle ---
    const loginPass = document.getElementById('login-pass'),
          loginEye = document.getElementById('login-eye');

    if (loginEye) { // Check if the eye icon exists
        loginEye.addEventListener('click', () => {
            // Toggle type attribute
            const type = loginPass.getAttribute('type') === 'password' ? 'text' : 'password';
            loginPass.setAttribute('type', type);

            // Toggle icon
            loginEye.classList.toggle('ri-eye-line');
            loginEye.classList.toggle('ri-eye-off-line');
        });
    }


    // --- Login form submissions and AJAX handling ---
    const loginForm = document.getElementById('loginform');
    if (loginForm) { // Check if the form exists
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const form = this;
            const formData = new FormData(form);

            // Get email and password from specific input IDs
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-pass').value;

            // Append email and password to formData
            formData.set('email', email);
            formData.set('password', password);

            // Add CSRF token if present
            const csrfToken = getCsrfToken();
            if (csrfToken) {
                formData.set('csrf_token', csrfToken);
            } else {
                 console.warn("CSRF token not found."); // Log a warning if token is missing
            }


            try {
                const response = await fetch('/login', {    //change this!!!!
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (result.status === 'success') {
                    // Redirect on success
                    window.location.href = result.redirect_url;
                } else {
                    // Show error message from server
                    showPopup(result.message || "Login failed. Please try again.", 'danger');
                }
            } catch (error) {
                console.error('Error during login fetch:', error);
                showPopup("An error occurred during login. Please try again.", 'danger');
            }
        });
    }
    
});