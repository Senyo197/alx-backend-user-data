#!/usr/bin/env python3
"""
This module defines routes and configurations for the API.
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


# Initialize Flask app and register blueprints
app = Flask(__name__)
app.register_blueprint(app_views)


# Enable CORS for all routes under /api/v1/*
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


# Determine the type of authentication to use
auth_type = getenv('AUTH_TYPE', 'auth')
auth = Auth() if auth_type == 'auth' else BasicAuth()
if auth_type == 'basic_auth' else None


@app.errorhandler(404)
def not_found(error) -> str:
    """Handles 404 Not Found errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Handles 401 Unauthorized errors."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Handles 403 Forbidden errors."""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def authenticate_user():
    """Authenticate users before processing requests."""
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
    ]
    if auth and auth.require_auth(request.path, excluded_paths):
        if auth.authorization_header(request) is None:
            abort(401)
        if auth.current_user(request) is None:
            abort(403)


if __name__ == "__main__":
    # Run the Flask app with specified host and port
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
