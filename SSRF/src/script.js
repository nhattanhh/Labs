document.addEventListener('DOMContentLoaded', function() {
    const exploreBtn = document.getElementById('exploreBtn');
    exploreBtn.addEventListener('click', function() {
        fetchContent('fetch.php?url=https://viewspace.org/');
    });
});

function fetchContent(url) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.querySelector('.content').innerHTML = data;
        })
        .catch(error => {
            console.error('Failed to fetch URL content:', error);
            document.querySelector('.content').innerText = 'Failed to fetch URL content.';
        });
}
