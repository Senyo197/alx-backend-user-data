#!/usr/bin/env python3
"""
API Route Module
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth

# Initialize the Flask application
app = Flask(__name__)

# Register blueprints for the application
app.register_blueprint(app_views)

# Enable CORS for all origins on the /api/v1/* routes
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Determine the authentication type based on environment variable
auth_type = getenv('AUTH_TYPE', 'auth')

# Initialize the appropriate authentication class
if auth_type == 'auth':
    auth = Auth()
elif auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'session_auth':
    auth = SessionAuth()
elif auth_type == 'session_exp_auth':
    auth = SessionExpAuth()
elif auth_type == 'session_db_auth':
    auth = SessionDBAuth()
else:
    auth = None


# Define error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 Unauthorized errors."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 Forbidden errors."""
    return jsonify({"error": "Forbidden"}), 403


# Request authentication before processing any request
@app.before_request
def authenticate_user():
    """Authenticate users before processing requests."""
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]
    if auth and auth.require_auth(request.path, excluded_paths):
        if auth.authorization_header(request) is None and \
                auth.session_cookie(request) is None:
            abort(401)
        user = auth.current_user(request)
        if user is None:
            abort(403)
        request.current_user = user


# Run the application
if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
