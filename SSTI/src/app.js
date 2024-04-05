document.addEventListener('DOMContentLoaded', function() {
    const formInput = document.getElementById('content');
    const renderedContent = document.querySelector('.rendered-content');

    formInput.addEventListener('input', function() {
        renderedContent.style.display = 'none';
    });
});
