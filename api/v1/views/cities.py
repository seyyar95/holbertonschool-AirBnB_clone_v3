#!/usr/bin/python3
"""View for Cities"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, request


@app_views.route('/states/<state_id>/cities', methods=[
    'GET', 'POST'
    ], strict_slashes=False)
def city(state_id):
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    if request.method == 'GET':
        cities = state.cities
        return jsonify([city.to_dict() for city in cities])
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        elif "name" not in data.keys():
            return jsonify({"error": "Missing name"}), 400
        data["state_id"] = state_id
        city = City(**data)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=[
    'GET', 'DELETE', 'PUT'
    ], strict_slashes=False)
def city_by_id(city_id):
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
