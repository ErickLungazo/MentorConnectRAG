from flask import Blueprint, request, jsonify
from services.train_service import train_vectors

# Define the Blueprint
train_bp = Blueprint('train', __name__)

@train_bp.route('/train', methods=['POST'])
def train():
    """
    API Endpoint to trigger the training process.
    Expects a JSON payload with 'type', 'source_url', and optionally 'query'.
    """
    data = request.get_json()
    source_type = data.get("type")  # "website", "file", or "youtube"
    source_url = data.get("source_url")
    test_query = data.get("query", "What is MentorConnect?")  # Default test query

    if not source_type or not source_url:
        return jsonify({"error": "Both 'type' and 'source_url' are required."}), 400

    response = train_vectors(source_type, source_url, test_query)
    return jsonify(response)