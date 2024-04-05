<!DOCTYPE html>
<html lang="en" style="background-color: #f5e8da;">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Gallery</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding: 0;
            font-family: 'Roboto', sans-serif;
            background-image: url('https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg');
            background-size:cover;  
            background-repeat: no-repeat;   
        }

        .container {
            background-color:aquamarine;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 100%;
            max-width: 500px;
            display: flex;
            flex-direction: column;
            opacity: 0.8;
        }

        h1 {
            font-size: 2rem;
            color: #6b4226;
            margin-top: 0;
            margin-bottom: 1rem;
        }

        form {
            margin-bottom: 1rem;
            display: flex;
            justify-content: center;
        }

        input[type="text"] {
            padding: 0.5rem;
            width: 80%;
            border-radius: 5px;
            border: 1px solid #ab7956;
            margin-right: 0.5rem;
            box-sizing: border-box;
        }

        button {
            padding: 0.5rem 1rem;
            background-color: #6b4226;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 20%;
        }

        button:hover {
            background-color: #ab7956;
        }

        .image {
            margin-top: 1rem;
        }

        .image img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
        }

        @media only screen and (max-width: 600px) {
            .container {
                padding: 1rem;
            }

            h1 {
                font-size: 1.5rem;
            }

            input[type="text"] {
                padding: 0.3rem;
                width: 80%;
            }

            button {
                padding: 0.3rem 0.5rem;
                width: 20%;
            }
        }
        #image li {
        list-style-type: none;
        font-size: 1.3rem;
        margin: 0.3rem;
        margin-right: 10%;
        background-color: #f0f0f0;
        border-radius: 3%;
        cursor: pointer;
        }

        #image li:hover {
        background-color: #e0e0e0;
        }
        </style>
</head>
<body>
    <div class="container">
        <h1>Image Gallery</h1>
        <p>Welcome to our image gallery! Here you can view images by entering their names in the search box below.</p>
        <h3>Image gallery</h3>
            <ul id="image">
                <li>pictures/1.jpg</li>
                <li>pictures/2.jpg</li>
                <li>pictures/3.jpg</li>
                <li>...</li>
            </ul>
        <form action="display.php" method="get">
            <input type="text" name="file_name" placeholder="Enter image name" required>
            <button type="submit">View</button>
        </form>
        <div class="content">
            <?php include 'display.php'; ?>
        </div>
    </div>
</body>
</html>