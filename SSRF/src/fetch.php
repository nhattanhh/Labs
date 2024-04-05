<?php
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (isset($_GET['url'])) {
        $url = $_GET['url'];
        $content = @file_get_contents($url);
        if ($content === false) {
            echo "Failed to fetch URL content.";
        } else {
            echo "<pre>$content</pre>";
        }
    } else {
        echo "URL parameter is missing.";
    }
} else {
    echo "Invalid request method.";
}
