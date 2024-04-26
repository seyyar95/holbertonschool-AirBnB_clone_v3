#!/usr/bin/python3
"""View for Places"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, request


@app_views.route('cities/<city_id>/places', methods=[
    'GET', 'POST'
    ], strict_slashes=False)
def places(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    if request.method == 'GET':
        places = city.places
        return jsonify([place.to_dict() for place in places])
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        elif "user_id" not in data.keys():
            return jsonify({"error": "Missing user_id"}), 400
        elif "name" not in data.keys():
            return jsonify({"error": "Missing name"}), 400
        user = storage.get(User, data["user_id"])
        if not user:
            return jsonify({"error": "Not found"}), 404
        data["city_id"] = city_id
        place = Place(**data)
        storage.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=[
    'GET', 'DELETE', 'PUT'
    ], strict_slashes=False)
def place_by_id(place_id):
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in keys:
                setattr(place, key, value)
            storage.save()
            return jsonify(place.to_dict()), 200
