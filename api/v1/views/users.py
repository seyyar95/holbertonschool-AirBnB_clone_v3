#!/usr/bin/python3
"""View for Cities"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, request


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    if request.method == 'GET':
        users = storage.all(User).values()
        return jsonify([user.to_dict() for user in users])
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        elif "email" not in data.keys():
            return jsonify({"error": "Missing email"}), 400
        elif "password" not in data.keys():
            return jsonify({"error": "Missing password"}), 400
        user = User(**data)
        storage.save()
        return jsonify(user.to_dict()), 201


@app_views.route('users/<user_id>', methods=[
    'GET', 'DELETE', 'PUT'
    ], strict_slashes=False)
def user_by_id(user_id):
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
