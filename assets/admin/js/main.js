// Auto-hide alert after 3 seconds
$(document).ready(function() {
    setTimeout(() => {
        $('.alert').alert('close');
    }, 3000);
});

// ULTRASONIC SCROLL LOGIC
const header = document.querySelector('.custom-header');

window.addEventListener('scroll', function() {
    // Using pageYOffset for maximum browser compatibility
    if (window.pageYOffset > 5) { 
        header.classList.add('nav-scrolled');
    } else {
        header.classList.remove('nav-scrolled');
    }
}, { passive: true });