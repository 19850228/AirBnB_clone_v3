#!/usr/bin/python3
"""User views"""
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """Handles HTTP requests for User objects"""
    if request.method == 'POST':
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"error": "Not a JSON"}), 400

        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing {field}'}), 400

        data.pop("id", None)
        data.pop("created_at", None)
        data.pop("updated_at", None)

        obj = User(**data)
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201

    if request.method == 'GET':
        users = storage.all(User)
        return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def user_by_id(user_id):
    """Handles HTTP requests for a specific User object"""
    user = storage.get(User, user_id)

    if not user:
        return abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in data.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, key, value)

        storage.save()
        return jsonify(user.to_dict())
