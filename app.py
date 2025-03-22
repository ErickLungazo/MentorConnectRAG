from flask import Flask
from flask_cors import CORS  # ✅ Import Flask-CORS
from routes.train import train_bp
from routes.query import query_bp
from routes.upload import upload_bp  # ✅ Import the upload route

app = Flask(__name__)

# ✅ Enable CORS for all API routes
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # ✅ Allow all necessary methods
    supports_credentials=True  # ✅ Needed if you ever use authentication
)

# Register Blueprints
app.register_blueprint(train_bp, url_prefix='/api')
app.register_blueprint(query_bp, url_prefix='/api')
app.register_blueprint(upload_bp, url_prefix='/api')  # ✅ Register upload route

@app.route('/', methods=['GET'])
def home():
    return {"message": "Welcome to the MentorConnect RAG API!"}

if __name__ == '__main__':
    app.run(debug=True)
