#!/usr/bin/python3
"""View for Cities"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, request


@app_views.route('/amenities', methods=[
    'GET', 'POST'
    ], strict_slashes=False)
def amenities():
    if request.method == 'GET':
        amenities = storage.all(Amenity).values()
        return [amenity.to_dict() for amenity in amenities]
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        elif "name" not in data:
            return jsonify({"error": "Missing name"}), 400
        amenity = Amenity(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=[
    'GET', 'DELETE', 'PUT'
    ], strict_slashes=False)
def amenity_by_id(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity_id:
        return jsonify({"error": "Not found"}), 404
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
