<?php
if (isset($_GET['file'])) {
    $file = $_GET['file'];
    $allowed_extensions = array('txt', 'md', 'html', 'htm');
    $file_extension = pathinfo($file, PATHINFO_EXTENSION);

    if (in_array($file_extension, $allowed_extensions)) {
        $file_path = "files/" . $file;
        if (is_file($file_path) && is_readable($file_path)) {
            echo "<pre>";
            echo file_get_contents($file_path);
            echo "</pre>";
        } else {
            echo "File not found or not readable.";
        }
    } else {
        echo "File format not supported.";
    }
} else {
    echo "No file specified.";
}
?>