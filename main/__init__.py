import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token
from flask_migrate import Migrate
from flask_restx import Api
from datetime import timedelta
from flask_cors import CORS  # Add this import

# Create the Flask app and configure the database and JWT manager
app = Flask(__name__)
# Configure CORS
CORS(app, resources={r"/api/*": {
    "origins": ["https://izog.me", " http://127.0.0.1:5000"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
}})
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE')
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Set token expiry time
app.config['PROPAGATE_EXCEPTIONS'] = True
# Initialize the database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app, doc='/docs')  # Swagger UI at /docs

# Set up error handlers for JWTManager

migrate = Migrate(app, db)

from main import route