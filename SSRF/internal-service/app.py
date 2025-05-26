from flask import Flask, jsonify

app = Flask(__name__)
FLAG = "FLAG1{SSRF_M4st3r_Y0u_Ar3!}" 
@app.route('/')
def index():
    return "Nothing here"
@app.route('/flag', methods=['GET'])
def get_flag():
    return jsonify({"secret_flag": FLAG})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)