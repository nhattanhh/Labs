<!DOCTYPE html>
<html>
<head>
    <title>SSTI Lab</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>Server-Side Template Injection (SSTI) Lab</h1>
        <form method="post" class="form">
            <label for="content" class="form-label">Content:</label>
            <textarea name="content" id="content" rows="5" class="form-input" required></textarea>
            <button type="submit" class="form-button">Submit</button>
        </form>
        <hr>
        <?php if ($_SERVER['REQUEST_METHOD'] === 'POST'): ?>
            <div class="rendered-content">
                <h3>Rendered Content:</h3>
                <p id="rendered_content"><?php echo $_POST['content']; ?></p>
                <script src="render.js"></script>
                <script>
                    const content = document.getElementById('rendered_content').textContent;
                    const rendered = render(content, {});
                    document.getElementById('rendered_content').innerHTML = rendered;
                </script>
            </div>
        <?php endif; ?>
    </div>
    <script src="app.js"></script>
</body>
</html>
