$(document).ready(function() {
    $('#readForm').submit(function(event) {
        event.preventDefault(); 
        var filePath = $('#filePath').val();
        $.get('display.php', {file: filePath}, function(data) {
            $('#book-content').html(data);
        }).fail(function() {
             $('#book-content').html("<p>Failed to load file.</p>");
        });
    });
});
