#!/usr/bin/python3
"""View for Review"""
from api.v1.views import app_views
from models import storage
from models.review import Review
from flask import jsonify, request
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=[
    'GET', 'POST'
    ], strict_slashes=False)
def reviews(place_id):
    """GETs, POSTs Review objects"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    if request.method == "GET":
        reviews = place.reviews
        return jsonify([review.to_dict() for review in reviews])
    elif request.method == "POST":
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        if 'user_id' not in data.keys():
            return jsonify({"error": "Missing user_id"}), 400
        user = storage.get(User, data['user_id'])
        if not user:
            return jsonify({"error": "Not found"}), 404
        if 'text' not in data.keys():
            return jsonify({"error": "Missing text"}), 400
        data["place_id"] = place_id
        review = Review(**data)
        storage.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=[
    'GET', 'PUT', 'DELETE'
    ], strict_slashes=False)
def review_by_id(review_id):
    """GETting, PUTting, DELETing review object by id"""
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({"error": "Not found"}), 404
    if request.method == "GET":
        return jsonify(review.to_dict())
    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        [setattr(
            review, key, value
            ) for key, value in data.items() if key not in keys]
        storage.save()
        return jsonify(review.to_dict()), 200
