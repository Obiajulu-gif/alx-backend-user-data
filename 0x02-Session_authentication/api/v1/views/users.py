#!/usr/bin/env python3
""" Module of User views """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON representation
    """
    users = User.all()
    return jsonify([user.to_json() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id: str) -> str:
    """ GET /api/v1/users/<user_id>
    Return:
      - User object JSON representation
    """
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users
    Create a User object
    """
    user_data = request.get_json()
    if not user_data:
        abort(400, description="Not a JSON")
    if 'email' not in user_data:
        abort(400, description="Missing email")
    if 'password' not in user_data:
        abort(400, description="Missing password")

    user = User()
    user.email = user_data.get('email')
    user.password = user_data.get('password')
    user.save()

    return jsonify(user.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str) -> str:
    """ PUT /api/v1/users/<user_id>
    Update a User object
    """
    user = User.get(user_id)
    if user is None:
        abort(404)

    user_data = request.get_json()
    if not user_data:
        abort(400, description="Not a JSON")

    if 'email' in user_data:
        user.email = user_data.get('email')
    if 'password' in user_data:
        user.password = user_data.get('password')

    user.save()

    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str) -> str:
    """ DELETE /api/v1/users/<user_id>
    Delete a User object
    """
    user = User.get(user_id)
    if user is None:
        abort(404)

    user.delete()

    return jsonify({}), 200
