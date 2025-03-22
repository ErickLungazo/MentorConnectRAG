from flask import Blueprint, request, jsonify
from services.query_service import query_vectors

# Define the Blueprint
query_bp = Blueprint('query', __name__)

@query_bp.route('/query', methods=['POST'])
def query():
    """
    API Endpoint to query the vector store.
    Expects a JSON payload with a 'query' field.
    """
    data = request.get_json()
    query_text = data.get("query", "What is MentorConnect?")  # Default query

    response = query_vectors(query_text)
    return jsonify(response)