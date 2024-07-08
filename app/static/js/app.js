document.addEventListener('DOMContentLoaded', function() {
    // This code will run once the DOM is fully loaded.
    alert("Welcome to Home Income Manager!");
});

document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navList = document.querySelector('.nav-list');

    navToggle.addEventListener('click', function() {
        navList.classList.toggle('active');
    });
});
