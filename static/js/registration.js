
// Password strength and confirmation logic for registration form
document.addEventListener('DOMContentLoaded', function() {
  const passwordInput = document.getElementById('reg-password');
  const confirmInput = document.getElementById('reg-confirm');
  const registerBtn = document.querySelector('.login__button');
  const strengthText = document.getElementById('password-strength-text');
  const strengthBar = document.getElementById('password-strength-bar');
  const reqLowerUpper = document.getElementById('pw-lower-upper');
  const reqNumber = document.getElementById('pw-number');
  const reqSpecial = document.getElementById('pw-special');
  const reqLength = document.getElementById('pw-length');

  function checkStrength(val) {
    let strength = 0;
    const hasLower = /[a-z]/.test(val);
    const hasUpper = /[A-Z]/.test(val);
    const hasNumber = /\d/.test(val);
    const hasSpecial = /[!@#$%^&*]/.test(val);
    const hasLength = val.length >= 8;

    reqLowerUpper.style.color = (hasLower && hasUpper) ? '#28a745' : '#F7567C';
    reqNumber.style.color = hasNumber ? '#28a745' : '#F7567C';
    reqSpecial.style.color = hasSpecial ? '#28a745' : '#F7567C';
    reqLength.style.color = hasLength ? '#28a745' : '#F7567C';

    if (hasLower && hasUpper) strength++;
    if (hasNumber) strength++;
    if (hasSpecial) strength++;
    if (hasLength) strength++;

    const barWidth = ['10%', '40%', '70%', '100%'][strength];
    const barColor = ['#F7567C', '#FFA500', '#FFD700', '#28a745'][strength];
    const text = ['Very Weak', 'Weak', 'Medium', 'Strong'][strength];

    strengthBar.style.width = barWidth;
    strengthBar.style.background = barColor;
    strengthText.textContent = text;
    strengthText.style.color = barColor;

    return strength === 4;
  }

  function updateRegisterButton() {
    const pwVal = passwordInput.value;
    const confirmVal = confirmInput.value;
    const strong = checkStrength(pwVal);
    const match = pwVal && confirmVal && pwVal === confirmVal;
    registerBtn.disabled = !(strong && match);

    // Show/hide password match error
    const matchError = document.getElementById('pw-match-error');
    if (confirmVal && !match) {
      matchError.textContent = '⚠️';
    } else {
      matchError.textContent = '';
    }
  }

  passwordInput.addEventListener('input', updateRegisterButton);
  confirmInput.addEventListener('input', updateRegisterButton);
  updateRegisterButton();
});

