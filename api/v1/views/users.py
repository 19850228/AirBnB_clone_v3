#!/usr/bin/python3
"""User views"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
import hashlib


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """Handles HTTP requests for User objects"""
    if request.method == 'POST':
        data = request.get_json()

        # Check if request data is JSON
        if not isinstance(data, dict):
            return jsonify({"error": "Not a JSON"}), 400

        # Check for required fields
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing {field}'}), 400

        # Validate email format
        email = data['email']
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400

        # Hash the password
        hashed_password = hash_password(data['password'])

        # Create User object
        data.pop("id", None)
        data.pop("created_at", None)
        data.pop("updated_at", None)
        data['password'] = hashed_password

        obj = User(**data)
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201

    if request.method == 'GET':
        users = storage.all(User)
        # Remove password field from response
        return jsonify([remove_password(user.to_dict()) for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def user_by_id(user_id):
    """Handles HTTP requests for a specific User object"""
    user = storage.get(User, user_id)

    if not user:
        return abort(404)

    if request.method == 'GET':
        # Remove password field from response
        return jsonify(remove_password(user.to_dict()))

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()

        # Check if request data is JSON
        if not isinstance(data, dict):
            return jsonify({"error": "Not a JSON"}), 400

        # Update user attributes
        for key, value in data.items():
            if key not in ["id", "email", "password", "created_at", "updated_at"]:
                setattr(user, key, value)

        storage.save()
        return jsonify(user.to_dict())


def validate_email(email):
    """Validate email format"""
    # Implement your email validation logic here
    return True  # Placeholder for validation logic


def hash_password(password):
    """Hash the password"""
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    return hashed_password


def remove_password(user_dict):
    """Remove password field from user dictionary"""
    user_dict.pop('password', None)
    return user_dict
