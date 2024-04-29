#!/usr/bin/python3
"""Amenities views"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

# Retrieve the list of all Amenity objects or create a new one
@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    if request.method == 'GET':
        amenities = storage.all(Amenity)
        return jsonify([obj.to_dict() for obj in amenities.values()])
    elif request.method == 'POST':
        new_amenity = request.get_json()
        if not new_amenity:
            abort(400, "Not a JSON")
        if "name" not in new_amenity:
            abort(400, "Missing name")
        amenity = Amenity(**new_amenity)
        storage.new(amenity)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)

# Retrieve, delete, or update a specific Amenity object
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        update_data = request.get_json()
        if not update_data:
            abort(400, "Not a JSON")
        for key, value in update_data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict())
