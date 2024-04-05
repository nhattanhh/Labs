<?php
        if (isset($_GET["file_name"])) {
            $file_name = $_GET["file_name"];
            if (!empty($file_name)) {
                $file_path = "/var/www/html/" . $file_name;
                if (is_readable($file_path)) {
                    echo "<img src='$file_name' alt='Image'>";
                    echo "<div class='content'><pre>";
                    echo htmlspecialchars(file_get_contents($file_path));
                    echo "</pre></div>";
                } else {
                    echo "<p>File not found or not readable.</p>";
                }
            } else {
                echo "<p>Please enter a file name.</p>";
            }
        }
?>