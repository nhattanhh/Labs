from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form.get('user_input', 'Guest')
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>SSTI Lab</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div class="container">
                <h1>Result:</h1>
                <p>Hello, {{ user_input }}!</p>
                <a href="/">Back</a>
            </div>
        </body>
        </html>
        """
        return render_template_string(template, user_input=user_input)

    # Thêm endpoint cho LFI
    file = request.args.get('file', 'default.html')
    try:
        with open(file, 'r') as f:
            content = f.read()
    except Exception as e:
        content = f"Error: {str(e)}"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SSTI Lab</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <h1>Welcome to SSTI Lab</h1>
            <form method="POST">
                <label for="user_input">Enter something:</label>
                <input type="text" id="user_input" name="user_input" placeholder="Your input here">
                <button type="submit">Submit</button>
            </form>
            <h2>File Content:</h2>
            <pre>{content}</pre>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)