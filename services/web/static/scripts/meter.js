function checkPasswordStrength(password) {
    const strength = calculatePasswordStrength(password);
    const strengthBar = $('#strengthBar');
    strengthBar.removeClass('very-weak weak medium strong');

    if (strength === 0) {
        strengthBar.addClass('very-weak');
    } else if (strength === 1) {
        strengthBar.addClass('weak');
    } else if (strength === 2) {
        strengthBar.addClass('medium');
    } else {
        strengthBar.addClass('strong');
    }

    strengthBar.width((strength + 1) * 25 + '%');
}

function calculatePasswordStrength(password) {
    const length = password.length;

    // Set a minimum length for a password to be considered strong
    const minLength = 12;

    // Criteria for password strength
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasDigit = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]/.test(password);

    // Calculate strength based on criteria
    if (length < minLength) {
        return 0; // Very Weak
    } else if (hasUpperCase && hasLowerCase && hasDigit && hasSpecialChar) {
        return 3; // Strong
    } else if ((hasUpperCase && hasLowerCase) || (hasDigit && hasSpecialChar)) {
        return 2; // Medium
    } else {
        return 1; // Weak
    }
}

function togglePasswordVisibility() {
    const passwordInput = $('#password');
    const showPasswordCheckbox = $('#showPassword');

    if (showPasswordCheckbox.prop('checked')) {
        passwordInput.prop('type', 'text');
    } else {
        passwordInput.prop('type', 'password');
    }
}