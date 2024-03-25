// Add your JavaScript code for profile.html here
document.addEventListener('DOMContentLoaded', function() {
    const changeNameBtn = document.getElementById('change-name-btn');
    const changeNameForm = document.getElementById('change-name-form');

    changeNameBtn.addEventListener('click', function() {
        changeNameForm.style.display = 'block';
    });
});
