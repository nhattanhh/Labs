<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
session_start();
$db = new SQLite3('database.db');
$error = '';
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Prepare a statement to retrieve the user's details by username
    $stmt = $db->prepare("SELECT * FROM users WHERE username=:username");
    $stmt->bindValue(':username', $username, SQLITE3_TEXT);
    $result = $stmt->execute()->fetchArray(SQLITE3_ASSOC);

    if ($result) {
        // Verify the password
        if (password_verify($password, $result['password'])) {
            $_SESSION['user_id'] = $result['id'];
            $_SESSION['username'] = $result['username'];
            header("Location: home.php?id=" . $result['id']); ;
            exit();
        } else {
            $error = "Invalid password";
        }
    } else {
        $error =  "User not found";
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
        background-image: url('https://t4.ftcdn.net/jpg/05/96/62/65/360_F_596626503_jrzjZNYStDexiWxQFqO7oCh6M8PdMlJs.jpg');
        background-size: 100% 100%;
        background-position: center;
        background-repeat: no-repeat;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
      }
      .container {
        background-color: rgba(250, 250, 250, 0.7);
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
      input[type="password"] {
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
      <h1>Login</h1>
      <form action="index.php" method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required />

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required />

        <input type="submit" value="Login" />
      </form>
      <?php if ($error): ?>
        <p style="color: red; text-align: center;"><?php echo htmlspecialchars($error); ?></p>
      <?php endif; ?>
      <p>Don't have an account? <a href="login.php">Sign up now</a></p>
    </div>
  </body>
</html>

