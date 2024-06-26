#!/usr/bin/python3
"""Index Module"""
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON with status: OK"""
    return jsonify({"status": "OK"}), 200

@app_views.route('/stats', strict_slashes=False)
def stats():
    """Retrieves the number of each object type"""
    models_json = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(models_json)
