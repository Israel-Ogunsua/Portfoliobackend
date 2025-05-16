import os
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token
from flask_migrate import Migrate
from flask_restx import Api
from datetime import timedelta
from flask_cors import CORS
import cloudinary
import cloudinary.uploader
import base64
from io import BytesIO

from dotenv import load_dotenv
load_dotenv()

print("Cloudinary config:", os.getenv("CLOUDINARY_API_KEY"))


# Create the Flask app and configure the database and JWT manager
app = Flask(__name__, static_folder="static", static_url_path="/static")

# Configure CORS

CORS(app, resources={r"/api/*": {"origins": ["https://izog.me"], "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

# Static file routes (still valid for non-Cloudinary fallback)
@app.route('/static/uploads/projects/<path:filename>')
def serve_project_image(filename):
    return send_from_directory('static/uploads/projects', filename)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# === DATABASE CONFIG ===
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://portfolio_hzed_user:GLUbqnpBcTkJVw9euLmtIcch22gnEdRA@dpg-cvdjrllds78s73b6tvbg-a.oregon-postgres.render.com/portfolio_hzed'
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['PROPAGATE_EXCEPTIONS'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app, doc='/docs')
migrate = Migrate(app, db)

# === CLOUDINARY CONFIG ===
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# === CLOUDINARY UPLOAD ROUTES ===

# Upload image via file (form-data)
@app.route('/api/upload-image', methods=['POST'])
@jwt_required()
def upload_image_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        result = cloudinary.uploader.upload(file, folder="project_images")
        return jsonify({'url': result['secure_url']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Upload image via base64
@app.route('/api/upload-base64', methods=['POST'])
@jwt_required()
def upload_base64_image():
    data = request.get_json()
    base64_str = data.get("image")

    if not base64_str:
        return jsonify({"error": "No image data"}), 400

    try:
        header, encoded = base64_str.split(",", 1)
        image_data = base64.b64decode(encoded)
        result = cloudinary.uploader.upload(BytesIO(image_data), folder="project_images")
        return jsonify({"url": result["secure_url"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Your app routes
from main import route
