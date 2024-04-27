#!/usr/bin/python3
"""Cities views"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def cities_by_state(state_id):
    """Retrieves the list of cities by state or creates a new city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400

        if 'name' not in data:
            return jsonify({'error': 'Missing name'}), 400

        data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)
        data['state_id'] = state_id

        city = City(**data)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def city_by_id(city_id):
    """Retrieves, deletes, or updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400

        for key in ('id', 'state_id', 'created_at', 'updated_at'):
            data.pop(key, None)

        for key, value in data.items():
            setattr(city, key, value)

        storage.save()
        return jsonify(city.to_dict())
