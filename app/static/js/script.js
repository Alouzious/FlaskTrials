// Simple navbar behavior (optional, for dropdowns or future work)
console.log("Website loaded successfully!");

document.addEventListener('DOMContentLoaded', function() {
    // Future dynamic JS for navbar can come here
});

// Example: show a small toast message after form submission (optional)
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast-message';
    toast.innerText = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Flash message auto-hide and fade-out effect
setTimeout(function() {
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        flashMessages.style.transition = 'opacity 0.5s ease-out';
        flashMessages.style.opacity = '0';
        setTimeout(() => flashMessages.remove(), 500); // remove from DOM
    }
}, 3000);
