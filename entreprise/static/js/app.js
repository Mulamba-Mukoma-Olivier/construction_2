document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        }
    });
});