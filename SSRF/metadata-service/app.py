from flask import Flask, jsonify, request

app = Flask(__name__)

metadata = {
    "latest": {
        "meta-data": {
            "iam": {
                "security-credentials": {
                    "fake-role": {
                        "Code": "Success",
                        "LastUpdated": "2024-05-24T10:00:00Z",
                        "Type": "AWS-HMAC",
                        "AccessKeyId": "FLAG2{Y0uu_g0t_1h1s_AcE55_k3y}",
                        "SecretAccessKey": "sec3t_k3yT",
                        "Token": "3633366363633363",
                        "Expiration": "2024-05-25T17:00:00Z"
                    }
                }
            },
            "hostname": "internal-instance.example.com",
            "instance-id": "i-abcdef1234567890"
        }
    }
}

@app.route('/')
@app.route('/<path:path>', methods=['GET'])
def get_metadata(path='latest/meta-data/'):
    parts = path.strip('/').split('/')
    current_level = metadata
    try:
        for part in parts:
            if isinstance(current_level, dict) and part in current_level:
                current_level = current_level[part]
            elif isinstance(current_level, str): 
                return current_level
            else:
                if isinstance(current_level, dict):
                    return "\n".join(current_level.keys()) + "\n"
                return "Not Found", 404
        if isinstance(current_level, dict):
             return "\n".join(current_level.keys()) + "\n" 
        return jsonify(current_level) 
    except Exception:
        return "Error processing path", 500


if __name__ == '__main__':
  
    app.run(host='0.0.0.0', port=80, debug=False)