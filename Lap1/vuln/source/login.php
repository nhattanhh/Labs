<?php
//error_reporting(E_ALL);
//ini_set('display_errors', 1);

session_start();
$db = new SQLite3('database.db');

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    function sanitize_input($data) {
        $data = trim($data);
        $data = stripslashes($data);
        $data = htmlspecialchars($data);
        return $data;
    }

    $username = sanitize_input($_POST['username']);
    $email = filter_var($_POST['email'], FILTER_SANITIZE_EMAIL);
    $password = sanitize_input($_POST['password']);

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $invalid_email = true;
    }

    $password_hash = password_hash($password, PASSWORD_DEFAULT);

    do {
        $user_id = uniqid();
        
        $stmt_check = $db->prepare("SELECT COUNT(*) as count FROM users WHERE id = ?");
        $stmt_check->bindValue(1, $user_id, SQLITE3_TEXT);
        $result_check = $stmt_check->execute();
        $row = $result_check->fetchArray(SQLITE3_ASSOC);
    } while ($row['count'] > 0);

    $stmt = $db->prepare("INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)");
    $stmt->bindValue(1, $user_id, SQLITE3_TEXT);
    $stmt->bindValue(2, $username, SQLITE3_TEXT);
    $stmt->bindValue(3, $email, SQLITE3_TEXT);
    $stmt->bindValue(4, $password_hash, SQLITE3_TEXT);
    $result = $stmt->execute();
    if ($result) {
        $_SESSION['user_id'] = $user_id;
        header("Location: index.php");
        exit();
    } else {
        echo "Error: " . $db->lastErrorMsg();
    }
}
?>
<!DOCTYPE html>
<html>
  <head>
    <title>Login</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background-image: url('shop-background.jpeg');
        background-size: 110% 100%;
        background-position: center center;
        background-repeat: no-repeat;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
      }
      .container {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 2rem;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
      h1 {
        text-align: center;
        margin-bottom: 1rem;
      }
      form {
        display: flex;
        flex-direction: column;
      }
      label {
        margin-bottom: 0.5rem;
      }
      input[type="text"],
      input[type="password"],
      input[type="email"] {
        padding: 0.5rem;
        border-radius: 4px;
border: 1px solid #ccc;
      }
      input[type="submit"] {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        margin-top: 1rem;
      }
      input[type="submit"]:hover {
        background-color: #45a049;
      }
      p {
        text-align: center;
        margin-top: 1rem;
      }
      p a {color: #4CAF50;
        text-decoration: none;
      }
      p a:hover {
        text-decoration: underline;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Signup</h1>
      <form action="login.php" method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required />
        
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required />

        <input type="submit" />
      </form>
      <p>Already have an account? <a href="index.php">Login now</a></p>
    </div>
  </body>
</html>

