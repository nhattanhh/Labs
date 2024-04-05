<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bountyboy's security</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-image: url('https://globalcybervision.ro/wp-content/uploads/2020/01/Red.jpg');
            background-size:cover;  
            background-repeat: no-repeat; 
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color:chocolate;
            border-radius: 20px;    
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
            text-align: center;
        }

        h1 {
            font-size: 3rem;
            color:beige;
            margin-bottom: 30px;
        }

        form {
            margin-bottom: 30px;
            text-align: left;
        }

        input[type="text"], textarea {
            width: 100%;
            padding: 12px;
            border-radius: 5px;
            border: 2px solid #ccc;
            margin-bottom: 20px;
            box-sizing: border-box;
            font-size: 1.1rem;
        }

        button {
            padding: 12px 30px;
            background-color: #4CAF50;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1.1rem;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #45a049;
        }

        .comments {
            text-align: left;
            padding: 20px;
            border: 2px solid #ccc;
            border-radius: 10px;
            background-color: #fff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .comment p {
            color: #007bff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bountyboy's security</h1>
        <form action="index.php" method="post">
            <input type="text" name="name" placeholder="Your name">
            <textarea name="comment" placeholder="Your comment"></textarea>
            <button type="submit">Send</button>
        </form>
        <div class="comments">
            <?php
            if($_SERVER['REQUEST_METHOD'] == 'POST') {
                $name = $_POST['name'];
                $comment = htmlspecialchars($_POST['comment']);
                echo "<div class='comment'><p>$name</p> $comment</div>";
            }
            ?>
        </div>
    </div>
</body>
</html>
