/* Modern Profile Logic */
document.addEventListener("DOMContentLoaded", function () {
    const profileForm = document.querySelector("form");
    const updateBtn = document.querySelector(".btn-modern-update");

    if (profileForm && updateBtn) {
        profileForm.addEventListener("submit", function () {
            updateBtn.disabled = true;
            updateBtn.style.opacity = "0.7";
            updateBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Updating...';
        });
    }
});