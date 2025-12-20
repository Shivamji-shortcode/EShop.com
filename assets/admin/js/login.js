/* Login Validation Logic */
/* Security Redirect: If user is already logged in, don't let them see this page */
if (document.cookie.includes("sessionid") || localStorage.getItem("isLoggedIn") === "true") {
    // If we detect a session, redirect to home immediately
    window.location.href = "/"; 
}

document.addEventListener("DOMContentLoaded", function () {
    // ... (rest of your existing login logic) ...
});

document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById("email");
    const emailError = document.getElementById("emailError");
    const passwordInput = document.getElementById("password");
    const passwordError = document.getElementById("passwordError");
    const form = document.getElementById("loginForm");

    if (form) {
        form.addEventListener("submit", function (e) {
            let valid = true;
            emailError.textContent = "";
            passwordError.textContent = "";

            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(emailInput.value)) {
                emailError.textContent = "Please enter a valid email address.";
                valid = false;
            }

            if (passwordInput.value.trim().length === 0) {
                passwordError.textContent = "Please enter your password.";
                valid = false;
            }

            if (!valid) e.preventDefault();
        });
    }
});