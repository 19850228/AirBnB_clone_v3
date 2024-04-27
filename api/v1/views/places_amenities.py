#!/usr/bin/python3
"""places_amenities Module"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from uuid import UUID


def is_valid_uuid(uuid_str):
    """Check if a string is a valid UUID"""
    try:
        UUID(uuid_str, version=4)
        return True
    except ValueError:
        return False


def is_amenity_in_place(place, amenity):
    """Check if an amenity is associated with a place"""
    if storage.__class__.__name__ == 'DBStorage':
        return amenity in place.amenities
    else:
        return amenity.id in place.amenity_ids


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities_in_places(place_id):
    """Retrieves the list of all amenities in a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_in_place(place_id, amenity_id):
    """Deletes an amenity from a place object"""
    if not is_valid_uuid(place_id) or not is_valid_uuid(amenity_id):
        abort(404)

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if not is_amenity_in_place(place, amenity):
        abort(404)

    if storage.__class__.__name__ == 'DBStorage':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity.id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Links an amenity to a place"""
    if not is_valid_uuid(place_id) or not is_valid_uuid(amenity_id):
        abort(404)

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if is_amenity_in_place(place, amenity):
        return jsonify(amenity.to_dict()), 200

    if storage.__class__.__name__ == 'DBStorage':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
