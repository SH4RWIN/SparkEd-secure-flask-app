// ===========Password strength and confirmation logic for registration form===========
// This script runs after the DOM is fully loaded
// contains password stregth
// password confirmation
// password show toggle
document.addEventListener('DOMContentLoaded', function() {
  // Get references to all relevant DOM elements
  const passwordInput = document.getElementById('reg-password'); // Password input field
  const confirmInput = document.getElementById('reg-confirm');   // Confirm password input field
  const registerBtn = document.querySelector('.login__button');  // Register button
  // password strength fields
  const strengthText = document.getElementById('password-strength-text'); // Text label for password strength
  const strengthBar = document.getElementById('password-strength-bar');   // Visual bar for password strength
  const reqLowerUpper = document.getElementById('pw-lower-upper'); // Checklist: lower & upper
  const reqNumber = document.getElementById('pw-number');           // Checklist: number
  const reqSpecial = document.getElementById('pw-special');         // Checklist: special char
  const reqLength = document.getElementById('pw-length');           // Checklist: length

  // ===========Function to check password strength and update UI===========
  function checkStrength(val) {
    let strength = 0; // Strength score (0-4)

    // Check for each requirement using regex
    const hasLower = /[a-z]/.test(val);         // At least one lowercase
    const hasUpper = /[A-Z]/.test(val);         // At least one uppercase
    const hasNumber = /\d/.test(val);           // At least one number
    const hasSpecial = /[!@#$%^&*]/.test(val);  // At least one special char
    const hasLength = val.length >= 8;          // At least 8 characters

    // Update checklist colors: green if valid, pink if not
    reqLowerUpper.style.color = (hasLower && hasUpper) ? '#28a745' : '#F7567C';
    reqNumber.style.color = hasNumber ? '#28a745' : '#F7567C';
    reqSpecial.style.color = hasSpecial ? '#28a745' : '#F7567C';
    reqLength.style.color = hasLength ? '#28a745' : '#F7567C';

    // Increase strength for each requirement met
    if (hasLower && hasUpper) strength++;
    if (hasNumber) strength++;
    if (hasSpecial) strength++;
    if (hasLength) strength++;

    // Arrays for bar width, color, and text based on strength
    const barWidth = ['10%', '40%', '70%', '100%'][strength];
    const barColor = ['#F7567C', '#FFA500', '#FFD700', '#28a745'][strength];
    const text = ['Very Weak', 'Weak', 'Medium', 'Strong'][strength];

    // Update the strength bar and text in the UI
    strengthBar.style.width = barWidth;
    strengthBar.style.background = barColor;
    strengthText.textContent = text;
    strengthText.style.color = barColor;

    // Return true if all requirements are met (strong password)
    return strength === 4;
  }

  // ===========Function to update the register button and show password match error===========
  function updateRegisterButton() {
    // Get current values from all required fields
    const nameVal = document.getElementById('reg-name').value.trim();
    const emailVal = document.getElementById('reg-email').value.trim();
    const phoneVal = document.getElementById('reg-phone').value.trim();
    const pwVal = passwordInput.value;
    const confirmVal = confirmInput.value;

    // Check if password is strong
    const strong = checkStrength(pwVal);
    // Check if both password fields are non-empty and match
    const match = pwVal && confirmVal && pwVal === confirmVal;
    // Check if all required fields are filled
    const allFilled = nameVal && emailVal && phoneVal && pwVal && confirmVal;

    // Enable the register button only if all conditions are true
    registerBtn.disabled = !(allFilled && strong && match);

    // Show/hide password match error message
    const matchError = document.getElementById('pw-match-error');
    if (confirmVal && !match) {
      // If user typed something in confirm and it doesn't match, show warning
      matchError.textContent = '⚠️';
    } else if (confirmVal && match) {
        // if both paswords matches show ✅
        matchError.textContent = '✅'
    } else {
      // Otherwise, clear the warning
      matchError.textContent = '';
    }
  }


  // Listen for input events & all required fields for content
  passwordInput.addEventListener('input', updateRegisterButton);
  confirmInput.addEventListener('input', updateRegisterButton);
  document.getElementById('reg-name').addEventListener('input', updateRegisterButton);
  document.getElementById('reg-email').addEventListener('input', updateRegisterButton);
  document.getElementById('reg-phone').addEventListener('input', updateRegisterButton);

  // Run once on page load to set initial state
  updateRegisterButton();

  // Show password toggle logic
  const showPwCheckbox = document.getElementById('show-password');
  if (showPwCheckbox) {
    showPwCheckbox.addEventListener('change', function() {
      passwordInput.type = this.checked ? 'text' : 'password';
    });
  }
});

