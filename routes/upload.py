from flask import Blueprint, request, jsonify, send_from_directory
from services.upload_service import upload_file
import os

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload():
    response, status_code = upload_file()
    return jsonify(response), status_code

@upload_bp.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    """Serve the uploaded file from the 'data/' directory."""
    upload_folder = "data"
    return send_from_directory(upload_folder, filename, as_attachment=True)
