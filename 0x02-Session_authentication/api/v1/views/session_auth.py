#!/usr/bin/env python3
"""
Flask view module for handling all routes related to session authentication.
"""
import os
from typing import Tuple
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    POST /api/v1/auth_session/login
    Authenticates a user and creates a session.

    Returns:
        Tuple[str, int]: JSON representation of the authenticated User
        object and status code.
    """
    error_not_found = {"error": "no user found for this email"}
    email = request.form.get('email')
    if not email or not email.strip():
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password or not password.strip():
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(error_not_found), 404

    if len(users) == 0:
        return jsonify(error_not_found), 404

    user = users[0]
    if user.is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        response.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return response

    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> Tuple[str, int]:
    """
    DELETE /api/v1/auth_session/logout
    Logs out a user by destroying the session.

    Returns:
        Tuple[str, int]: An empty JSON object and status code.
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
