from flask import Flask, request, render_template
import requests
import re
app = Flask(__name__)
def is_safe_url_basic(url):
    if re.match(r"^https?://(?!localhost|127\.0\.0\.1).*", url, re.IGNORECASE):
        return True
    return False

def is_safe_url_advanced(url):
    try:
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ['http', 'https']:
            return False, "Only support http/https."
        if parsed_url.hostname == 'localhost' or parsed_url.hostname == '127.0.0.1':
            return False, "Access denied."
        if parsed_url.hostname == 'secret.internal': 
             return False, "Forbidden."
    except Exception:
        return False, "Invalid URL."
    return True, "Valid URL."


@app.route('/', methods=['GET', 'POST'])
def index():
    content = None
    error = None
    url = ""
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            is_safe, msg = is_safe_url_advanced(url)
            if is_safe:
                try:
                    response = requests.get(url, timeout=3, stream=True, allow_redirects=True) 
                    content_buffer = b""
                    for chunk in response.iter_content(chunk_size=1024):
                        content_buffer += chunk
                        if len(content_buffer) > 1024 * 1024: 
                            error = "Nội dung quá lớn."
                            content_buffer = b""
                            break
                    if not error:
                        content = content_buffer.decode('utf-8', errors='ignore')

                except requests.exceptions.RequestException as e:
                    error = f"Error while access: {e}"
            else:
                error = msg
        else:
            error = "Type URL pls."
    return render_template('index.html', content=content, error=error, submitted_url=url)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False) 