#!/usr/bin/env python3
"""
Module for User Views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """
    GET /api/v1/users
    Returns:
        - JSON list of all User objects
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    GET /api/v1/users/<user_id>
    Path Parameters:
        - user_id: User ID
    Returns:
        - JSON representation of the User object
        - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)

    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        else:
            return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    DELETE /api/v1/users/<user_id>
    Path Parameters:
        - user_id: User ID
    Returns:
        - Empty JSON object if the User is successfully deleted
        - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """
    POST /api/v1/users/
    JSON Body:
        - email
        - password
        - first_name (optional)
        - last_name (optional)
    Returns:
        - JSON representation of the created User object
        - 400 if the User cannot be created
    """
    try:
        rj = request.get_json()
    except Exception:
        rj = None
    if rj is None:
        return jsonify({'error': 'Wrong format'}), 400
    if not rj.get('email'):
        return jsonify({'error': 'email missing'}), 400
    if not rj.get('password'):
        return jsonify({'error': 'password missing'}), 400

    try:
        user = User()
        user.email = rj.get('email')
        user.password = rj.get('password')
        user.first_name = rj.get('first_name')
        user.last_name = rj.get('last_name')
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    PUT /api/v1/users/<user_id>
    Path Parameters:
        - user_id: User ID
    JSON Body:
        - first_name (optional)
        - last_name (optional)
    Returns:
        - JSON representation of the updated User object
        - 404 if the User ID doesn't exist
        - 400 if the User cannot be updated
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    try:
        rj = request.get_json()
    except Exception:
        rj = None
    if rj is None:
        return jsonify({'error': 'Wrong format'}), 400

    if 'first_name' in rj:
        user.first_name = rj.get('first_name')
    if 'last_name' in rj:
        user.last_name = rj.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
