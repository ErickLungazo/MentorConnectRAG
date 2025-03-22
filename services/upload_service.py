import os
from flask import request, url_for

UPLOAD_FOLDER = "data"  # Directory to save uploaded files
ALLOWED_EXTENSIONS = {"txt", "pdf", "md", "csv", "docx"}  # Allowed file types

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file has a valid extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    """Handles file uploads and returns the file URL."""
    try:
        if "file" not in request.files:
            return {"error": "No file provided"}, 400

        file = request.files["file"]

        if file.filename == "":
            return {"error": "No selected file"}, 400

        if file and allowed_file(file.filename):
            # Save the file
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Generate file URL (assuming a `/download/<filename>` endpoint exists)
            file_url = url_for("upload.download_file", filename=file.filename, _external=True)

            return {
                "message": f"File '{file.filename}' uploaded successfully!",
                "file_url": file_url
            }, 200

        return {"error": "Invalid file type. Allowed types: txt, pdf, md, csv, docx"}, 400

    except Exception as e:
        return {"error": str(e)}, 500
