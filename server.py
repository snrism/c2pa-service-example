import os
import subprocess
from flask import Flask, request, send_from_directory, send_file, jsonify
from flask_cors import CORS

server = Flask(__name__, static_url_path='', static_folder='client')
CORS(server)

port = int(os.environ.get("PORT", 8000))
image_folder = 'uploads'

@server.route('/version', methods=['GET'])
def get_version():
    try:
        result = subprocess.check_output('./c2patool --version', shell=True)
        return result
    except subprocess.CalledProcessError as e:
        return str(e), 500

@server.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        file.save(os.path.join(image_folder, file.filename))

        filepath = os.path.join(image_folder, file.filename)
        command = f'./c2patool "{filepath}" -m manifest.json -o "{filepath}" -f'
        result = subprocess.check_output(command, shell=True)

        report = result.decode('utf-8')  # Assuming the output is in UTF-8 format
        return jsonify({
            'name': file.filename,
            'url': f'http://localhost:{port}/uploads/{file.filename}',
            'report': report
        })
    except Exception as e:
        return str(e), 500

@server.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(image_folder, filename)

@server.route('/')
def default():
    return send_file(os.path.join(os.path.dirname(__file__), 'client/index.html'))

if __name__ == '__main__':
    server.run(debug=True, port=port)

