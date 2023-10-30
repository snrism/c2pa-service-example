"""
This module implements a Flask server for handling file uploads
and interacting with the c2pa_python bindings.
"""
import json
import os
import c2pa_python as c2pa
from flask import Flask, request, send_from_directory, send_file, jsonify
from flask_cors import CORS

server = Flask(__name__, static_url_path='', static_folder='client')
CORS(server)

port = int(os.environ.get("PORT", 8000))
IMAGE_FOLDER = 'uploads'
KEYS_FOLDER = 'keys'


# Create a dummy SignerInfo instance.
def generate_signer_info():
    """
    Generate a sample SignerInfo instance.

    Returns:
        c2pa.SignerInfo: A sample SignerInfo instance.
    """
    # Use OpenSSL to generate ES256 private and public keys for testing.
    pub_key_file = os.path.join(KEYS_FOLDER, "public_key.pem")
    with open(pub_key_file, "rb") as file:
        pub_key = file.read()

    # Read the private key contents.
    priv_key_file = os.path.join(KEYS_FOLDER, "private_key.pem")
    with open(priv_key_file, "rb") as file:
        priv_key = file.read()

    # Generate SignerInfo instance.
    sign_info = c2pa.SignerInfo(pub_key,
                                priv_key,
                                "es256",
                                "http://timestamp.digicert.com")
    return sign_info

# Get Manifest info.
def get_manifest():
    """
    Get a dummy sample manifest info.

    Returns:
        str: A dummy sample manifest in JSON format.
    """
    manifest_json = json.dumps(
        {
            "ta_url": "http://timestamp.digicert.com",
            "claim_generator": "CAI_Demo/0.1",
            "assertions": [
                {
                    "label": "c2pa.actions",
                    "data": {
                        "actions": [
                            {
                                "action": "c2pa.published"
                            }
                        ]
                    }
                },
                {
                    "label": "c2pa.training-mining",
                    "data": {
                        "entries": {
                            "c2pa.ai_generative_training": { "use": "notAllowed" },
                            "c2pa.ai_inference": { "use": "notAllowed" },
                            "c2pa.ai_training": { "use": "notAllowed" },
                            "c2pa.data_mining": { "use": "notAllowed" }
                        }
                    }
                }
            ]
        }
    )
    return manifest_json


@server.route('/version', methods=['GET'])
def get_version():
    """
    Get the version information from c2pa.

    Returns:
        str: Version information of c2pa.
    """
    try:
        return c2pa.version()
    except Exception as e:
        return str(e), 500

@server.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and manifest addition.

    Returns:
        str: Message indicating the status of the file upload and manifest addition.
    """
    try:
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        if not os.path.exists(IMAGE_FOLDER):
            os.makedirs(IMAGE_FOLDER)
        file.save(os.path.join(IMAGE_FOLDER, file.filename))

        filepath = os.path.join(IMAGE_FOLDER, file.filename)
        sign_info = generate_signer_info()
        result = c2pa.add_manifest_to_file_json(filepath,
                                                filepath,
                                                get_manifest(),
                                                sign_info,
                                                None)

        if (len(result) > 0):
            # Retrieve the result and display for user conusmption.
            manifest = c2pa.verify_from_file_json(filepath, IMAGE_FOLDER)
            return jsonify({
                'name': file.filename,
                'url': f'http://localhost:{port}/uploads/{file.filename}',
                'report': manifest
            })
        else:
            return "Error generating Manifest"
    except FileNotFoundError as e:
        return f"File not found: {e}", 404
    except IOError as e:
        return f"IO error: {e}", 500

@server.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@server.route('/')
def default():
    return send_file(os.path.join(os.path.dirname(__file__), 'client/index.html'))

if __name__ == '__main__':
    server.run(debug=True, port=port)
