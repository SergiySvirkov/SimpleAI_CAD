from flask import Flask, request, jsonify
import os
import boto3
import requests
from modules.ai_processor import AIProcessor
from modules.cad_converter import CADConverter
from modules.file_handler import FileHandler

app = Flask(__name__)
ai_processor = AIProcessor()
cad_converter = CADConverter()
file_handler = FileHandler()

# AWS S3 setup
S3_BUCKET = "your-s3-bucket-name"
s3_client = boto3.client("s3")

# Autodesk Forge API setup (if required)
AUTODESK_CLIENT_ID = "your-client-id"
AUTODESK_CLIENT_SECRET = "your-client-secret"
AUTODESK_BASE_URL = "https://developer.api.autodesk.com"

def autodesk_authenticate():
    auth_url = f"{AUTODESK_BASE_URL}/authentication/v1/authenticate"
    data = {
        "client_id": AUTODESK_CLIENT_ID,
        "client_secret": AUTODESK_CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "data:read data:write data:create"
    }
    response = requests.post(auth_url, data=data)
    return response.json().get("access_token")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    file_path = file_handler.save_file_locally(file, os.path.join("uploads", file.filename))
    s3_url = file_handler.upload_to_s3(file_path)
    
    return jsonify({"message": "File uploaded successfully", "s3_url": s3_url})

@app.route("/process", methods=["POST"])
def process_file():
    data = request.json
    file_url = data.get("file_url")
    if not file_url:
        return jsonify({"error": "File URL is required"}), 400
    
    file_path = "downloads/temp.rcp"
    os.system(f"wget {file_url} -O {file_path}")
    
    prediction = ai_processor.infer(file_path)
    output_cad = cad_converter.convert_to_cad(file_path, "output_model.stl")
    
    return jsonify({"prediction": int(prediction[0]), "cad_file": output_cad})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
