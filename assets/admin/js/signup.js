/* Signup Validation Logic */
/* Security Redirect: Logged in users shouldn't sign up again */
if (document.cookie.includes("sessionid")) {
    window.location.href = "/";
}

document.addEventListener("DOMContentLoaded", function () {
    // ... (rest of your existing signup logic) ...
});

document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById("email");
    const emailError = document.getElementById("emailError");
    const passwordInput = document.getElementById("password");
    const passwordError = document.getElementById("passwordError");
    const phoneInput = document.querySelector("input[name='phone']");
    const phoneError = document.getElementById("phoneError");
    const form = document.getElementById("signupForm");

    if (form) {
        form.addEventListener("submit", function (e) {
            let valid = true;
            emailError.textContent = "";
            passwordError.textContent = "";
            phoneError.textContent = "";

            // Email validation
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailInput.value.match(emailPattern)) {
                emailError.textContent = "Please enter a valid email address.";
                valid = false;
            }

            // Phone validation (10 digits)
            const phonePattern = /^[0-9]{10}$/;
            if (!phonePattern.test(phoneInput.value)) {
                phoneError.textContent = "Please enter a valid 10-digit phone number.";
                valid = false;
            }

            // Password validation
            const password = passwordInput.value;
            const passRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#\$%\^&\*])[A-Za-z\d!@#\$%\^&\*]{8,}$/;
            if (!passRegex.test(password)) {
                passwordError.textContent = "Password must be 8+ chars, with upper, lower, number & special char.";
                valid = false;
            }

            if (!valid) e.preventDefault();
        });
    }
});