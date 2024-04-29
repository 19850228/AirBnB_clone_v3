#!/usr/bin/python3
"""places_review Module"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves all reviews associated with a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a review by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a review by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a new review for a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    
    data = request.get_json()
    if not data or not isinstance(data, dict):
        abort(400, 'Invalid JSON')
    
    required_fields = ['user_id', 'text']
    for field in required_fields:
        if field not in data:
            abort(400, f'Missing {field}')
    
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404, 'User not found')

    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a review by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    
    data = request.get_json()
    if not data or not isinstance(data, dict):
        abort(400, 'Invalid JSON')
    
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    
    review.save()
    return jsonify(review.to_dict())
