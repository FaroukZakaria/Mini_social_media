document.addEventListener('DOMContentLoaded', function() {
    const commentToggleBtns = document.querySelectorAll('.comment-toggle-btn');
    commentToggleBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            const commentForm = this.nextElementSibling;
            commentForm.style.display = commentForm.style.display === 'none' ? 'block' : 'none';
        });
    });
});
