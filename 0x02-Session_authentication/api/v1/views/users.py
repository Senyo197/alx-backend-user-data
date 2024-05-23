#!/usr/bin/env python3
"""Module for User views."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """
    GET /api/v1/users
    Returns:
        JSON list of all User objects.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    GET /api/v1/users/<user_id>
    Path parameter:
        user_id: The ID of the user to retrieve.
    Returns:
        JSON representation of the User object.
        404 error if the User ID does not exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    DELETE /api/v1/users/<user_id>
    Path parameter:
        user_id: The ID of the user to delete.
    Returns:
        Empty JSON if the User has been successfully deleted.
        404 error if the User ID does not exist.
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
    JSON body:
        email: The email of the new user.
        password: The password of the new user.
        first_name: Optional first name of the new user.
        last_name: Optional last name of the new user.
    Returns:
        JSON representation of the newly created User object.
        400 error if the User cannot be created.
    """
    try:
        rj = request.get_json()
    except Exception:
        rj = None
    if rj is None:
        return jsonify({'error': 'Wrong format'}), 400
    if 'email' not in rj or rj['email'] == '':
        return jsonify({'error': 'email missing'}), 400
    if 'password' not in rj or rj['password'] == '':
        return jsonify({'error': 'password missing'}), 400
    try:
        user = User()
        user.email = rj['email']
        user.password = rj['password']
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
    Path parameter:
        user_id: The ID of the user to update.
    JSON body:
        first_name: Optional new first name.
        last_name: Optional new last name.
    Returns:
        JSON representation of the updated User object.
        404 error if the User ID does not exist.
        400 error if the User cannot be updated.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    try:
        rj = request.get_json()
    except Exception:
        return jsonify({'error': 'Wrong format'}), 400
    if rj is None:
        return jsonify({'error': 'Wrong format'}), 400
    if 'first_name' in rj:
        user.first_name = rj['first_name']
    if 'last_name' in rj:
        user.last_name = rj['last_name']
    user.save()
    return jsonify(user.to_json()), 200
